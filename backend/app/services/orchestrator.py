"""
CEO Orchestrator: the central nervous system of the Corporate AI System.

Pipeline:
1. Classify message (Receptionist)
2. Check HR Memory (user context)
3. Query RAG (SOPs, routing rules, company docs)
4. Determine routing (which agents to invoke)
5. Dispatch sub-agents in parallel
6. Handle inter-agent handoffs (e.g., Data → Writer)
7. QA Review (sequential, always last)
8. Synthesize final response
9. Store conversation history
"""

import asyncio
import logging
import uuid

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import create_agent_registry
from app.agents.base_agent import AgentContext, AgentResult
from app.agents.qa_reviewer import QAReviewerAgent
from app.config import settings
from app.models.conversation import Conversation
from app.services.hr_memory import HRMemoryService
from app.services.rag_pipeline import RAGService
from app.services.receptionist import ReceptionistService

logger = logging.getLogger(__name__)


# Mapping from classification labels to which agents to invoke
LABEL_TO_AGENTS = {
    "task_management": ["secretary"],
    "research_query": ["research_analyst"],
    "data_analysis": ["data_analyst"],
    "writing_request": ["writer"],
    "code_request": ["code_dev"],
    "general_inquiry": [],  # CEO handles directly with RAG context
    "multi_agent": ["research_analyst", "data_analyst", "writer"],
    "escalation": ["research_analyst", "secretary"],
}


class OrchestratorService:
    def __init__(self):
        self.receptionist = ReceptionistService()
        self.hr_memory = HRMemoryService()
        self.rag = RAGService()
        self.llm = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model_name
        self.agents = create_agent_registry()
        self.qa_reviewer: QAReviewerAgent = self.agents["qa_reviewer"]

    async def handle_message(
        self,
        db: AsyncSession,
        user_id: str,
        session_id: str,
        message: str,
    ) -> dict:
        """Full orchestration pipeline. Returns the final response dict."""

        # --- Step 1: Classify ---
        classification = await self.receptionist.classify(message)
        logger.info(f"Classification: {classification}")

        # --- Step 2: Check HR Memory ---
        user_context_summary = await self.hr_memory.get_context_summary(db, user_id)
        logger.info(f"User context loaded for {user_id}")

        # --- Step 3: Query RAG ---
        rag_chunks = []
        for source in ["routing_rule", "sop", "company_doc"]:
            chunks = await self.rag.retrieve(db, message, top_k=2, source_filter=source)
            rag_chunks.extend(chunks)

        rag_context = "\n\n".join(
            f"[{c.source}: {c.title}]\n{c.content}" for c in rag_chunks
        )
        logger.info(f"RAG retrieved {len(rag_chunks)} chunks")

        # --- Step 4: Build context bundle ---
        context = AgentContext(
            user_message=message,
            classification=classification,
            user_context=user_context_summary,
            rag_context=rag_context,
            session_id=session_id,
            user_id=user_id,
        )

        # --- Step 5: Determine routing ---
        target_agents = LABEL_TO_AGENTS.get(classification["label"], [])

        # --- Step 6: Execute ---
        if not target_agents:
            # General inquiry — CEO handles directly with RAG context
            final_response = await self._ceo_direct_response(context, db)
        else:
            # Dispatch sub-agents
            results = await self._dispatch_agents(context, target_agents)

            # --- Step 7: Handle inter-agent handoffs ---
            results = await self._handle_handoffs(context, results)

            # --- Step 8: QA Review ---
            qa_result = await self._qa_review(context, results)

            # --- Step 9: Synthesize ---
            final_response = await self._synthesize(context, qa_result, results)

        # --- Step 10: Store conversation ---
        await self._store_conversation(
            db, user_id, session_id, message, final_response, classification
        )

        # Update HR Memory with this interaction
        await self.hr_memory.update_context(db, user_id, message, final_response[:200])

        return {
            "message": final_response,
            "session_id": session_id,
            "classification": classification["label"],
            "agents_used": target_agents if target_agents else ["ceo_direct"],
        }

    async def _dispatch_agents(
        self, context: AgentContext, agent_names: list[str]
    ) -> list[AgentResult]:
        """Dispatch multiple agents in parallel using agent classes."""
        tasks = []
        for name in agent_names:
            agent = self.agents.get(name)
            if agent:
                tasks.append(agent.execute(context))
            else:
                logger.warning(f"Unknown agent: {name}")

        results = await asyncio.gather(*tasks, return_exceptions=True)

        agent_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                agent_results.append(AgentResult(
                    agent_name=agent_names[i],
                    content=f"Agent failed with error: {str(result)}",
                    success=False,
                ))
            else:
                agent_results.append(result)

        # Always notify Secretary for task logging (fire-and-forget)
        if "secretary" not in agent_names:
            asyncio.create_task(self._notify_secretary(context, agent_results))

        return agent_results

    async def _notify_secretary(
        self, context: AgentContext, results: list[AgentResult]
    ) -> None:
        """Notify Secretary to log the task (fire-and-forget)."""
        try:
            summary = "\n".join(
                f"- {r.agent_name}: {'completed' if r.success else 'failed'}"
                for r in results
            )
            secretary = self.agents.get("secretary")
            if secretary:
                log_context = AgentContext(
                    user_message=(
                        f"Log this task execution:\n"
                        f"Original request: {context.user_message}\n"
                        f"Results:\n{summary}"
                    ),
                    classification=context.classification,
                    user_context=context.user_context,
                    rag_context="",
                    session_id=context.session_id,
                    user_id=context.user_id,
                )
                await secretary.execute(log_context)
        except Exception as e:
            logger.error(f"Secretary notification failed: {e}")

    async def _handle_handoffs(
        self, context: AgentContext, results: list[AgentResult]
    ) -> list[AgentResult]:
        """If any agent flagged needs_writing, pass their output to the Writer."""
        writing_inputs = [r for r in results if r.needs_writing and r.success]

        if not writing_inputs:
            return results

        # Check if Writer already ran
        if any(r.agent_name == "writer" for r in results):
            return results

        # Build Writer input from agents that need writing
        combined_input = "\n\n---\n\n".join(
            f"## Input from {r.agent_name}\n{r.content}" for r in writing_inputs
        )

        writer = self.agents.get("writer")
        if writer:
            writer_context = AgentContext(
                user_message=(
                    f"Polish and format the following agent outputs into a cohesive response "
                    f"for the user's original request: \"{context.user_message}\"\n\n{combined_input}"
                ),
                classification=context.classification,
                user_context=context.user_context,
                rag_context=context.rag_context,
                session_id=context.session_id,
                user_id=context.user_id,
            )
            writer_result = await writer.execute(writer_context)
            results.append(writer_result)

        return results

    async def _qa_review(
        self, context: AgentContext, results: list[AgentResult], retry: int = 0
    ) -> dict:
        """QA Reviewer evaluates all results. Max 2 retries on rejection."""
        successful = [r for r in results if r.success]
        if not successful:
            return {
                "approved": True,
                "revised_content": "I wasn't able to fully process your request. Please try again.",
                "feedback": "",
            }

        # Use the QA Reviewer agent's review method
        review = await self.qa_reviewer.review(context, successful)

        if review.get("approved", True) or retry >= 2:
            return review

        # Rejection: retry the failing agents with QA feedback
        logger.info(f"QA rejected (attempt {retry + 1}). Feedback: {review.get('feedback', '')}")
        feedback = review.get("feedback", "Please improve the quality and completeness.")

        retried_results = []
        for r in successful:
            agent = self.agents.get(r.agent_name)
            if not agent:
                retried_results.append(r)
                continue

            retry_context = AgentContext(
                user_message=(
                    f"Your previous output was reviewed and needs improvement.\n"
                    f"Original request: {context.user_message}\n"
                    f"QA Feedback: {feedback}\n"
                    f"Your previous output:\n{r.content}\n\n"
                    f"Please provide an improved version."
                ),
                classification=context.classification,
                user_context=context.user_context,
                rag_context=context.rag_context,
                session_id=context.session_id,
                user_id=context.user_id,
            )
            retried = await agent.execute(retry_context)
            retried_results.append(retried)

        return await self._qa_review(context, retried_results, retry=retry + 1)

    async def _synthesize(
        self,
        context: AgentContext,
        qa_result: dict,
        agent_results: list[AgentResult],
    ) -> str:
        """Synthesize the final response from QA-approved content."""
        revised = qa_result.get("revised_content", "")
        if revised:
            return revised

        successful = [r for r in agent_results if r.success]
        if not successful:
            return "I encountered issues processing your request. Please try again."

        if len(successful) == 1:
            return successful[0].content

        # Multiple agents: ask CEO to synthesize
        combined = "\n\n---\n\n".join(
            f"## {r.agent_name}\n{r.content}" for r in successful
        )

        try:
            response = await self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the CEO agent. Synthesize the following sub-agent "
                            "outputs into a single, coherent response for the user. "
                            "Be concise, professional, and action-oriented."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"User's original request: {context.user_message}\n\n"
                            f"Agent outputs:\n{combined}\n\n"
                            "Synthesize into a single response:"
                        ),
                    },
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            return combined

    async def _load_conversation_history(
        self, db: AsyncSession, session_id: str, limit: int = 20
    ) -> list[dict]:
        """Load recent conversation history for the session."""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
        )
        rows = result.scalars().all()
        # Reverse to get chronological order
        rows = list(reversed(rows))
        return [{"role": r.role, "content": r.content} for r in rows]

    async def _ceo_direct_response(
        self, context: AgentContext, db: AsyncSession = None
    ) -> str:
        """CEO handles general inquiries directly using RAG context."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are the CEO agent of a corporate AI system. Answer the user's "
                        "question using the provided company knowledge base. Be professional, "
                        "accurate, and helpful. If the answer isn't in the knowledge base, "
                        "say so honestly.\n\n"
                        "IMPORTANT: Never guess or invent information about the user (name, "
                        "role, etc.) unless it appears in the User Context below. If you don't "
                        "know something about the user, say so.\n\n"
                        f"## User Context\n{context.user_context}\n\n"
                        f"## Company Knowledge Base\n{context.rag_context}"
                    ),
                },
            ]

            # Add conversation history if available
            if db:
                history = await self._load_conversation_history(db, context.session_id)
                for msg in history:
                    messages.append({"role": msg["role"], "content": msg["content"]})

            # Add the current message
            messages.append({"role": "user", "content": context.user_message})

            response = await self.llm.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"CEO direct response failed: {e}")
            return "I'm having trouble accessing the knowledge base. Please try again."

    async def _store_conversation(
        self,
        db: AsyncSession,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_response: str,
        classification: dict,
    ) -> None:
        """Store both user message and assistant response in conversation history."""
        db.add(Conversation(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            role="user",
            content=user_message,
            metadata_={"classification": classification},
        ))

        db.add(Conversation(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            role="assistant",
            content=assistant_response,
            agent_name="ceo",
            metadata_={"classification": classification},
        ))

        await db.commit()
