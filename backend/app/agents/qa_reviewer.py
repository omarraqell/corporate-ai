"""QA Reviewer Agent: quality assurance and final gate."""

import json

from app.agents.base_agent import AgentContext, AgentResult, BaseAgent


class QAReviewerAgent(BaseAgent):
    name = "qa_reviewer"
    description = "QA Reviewer — final quality gate for all agent outputs"
    system_prompt = (
        "You are the QA Reviewer agent in a corporate AI system. "
        "You are the final quality gate before responses reach the user.\n\n"
        "Your responsibilities:\n"
        "- Evaluate completeness: Does the output fully address the user's request?\n"
        "- Check accuracy: Are facts correct? Are claims supported?\n"
        "- Assess clarity: Is the output well-structured and easy to understand?\n"
        "- Verify professionalism: Is the tone appropriate for a corporate setting?\n"
        "- Identify gaps: Is anything missing that the user would expect?\n\n"
        "You MUST respond with valid JSON in this exact format:\n"
        "{\n"
        '  "approved": true or false,\n'
        '  "feedback": "Specific feedback if not approved, or brief quality note if approved",\n'
        '  "revised_content": "The final polished content to send to the user"\n'
        "}\n\n"
        "Rules:\n"
        "- If the work is good enough (>80% quality), APPROVE it and provide the polished version\n"
        "- Only REJECT if there are significant errors, missing information, or unprofessional content\n"
        "- When approving, you may make minor edits in revised_content (grammar, clarity)\n"
        "- When rejecting, be specific about what needs to change in the feedback field\n"
        "- Always include revised_content, even when rejecting (provide the best version you can)"
    )

    def __init__(self):
        # QA is pure LLM evaluation — no tools
        super().__init__(tools=None)

    async def review(self, context: AgentContext, results: list[AgentResult]) -> dict:
        """
        Review agent results and return approval/feedback.
        Convenience method that wraps execute() with review-specific formatting.
        """
        successful = [r for r in results if r.success]
        if not successful:
            return {
                "approved": True,
                "feedback": "No successful agent outputs to review.",
                "revised_content": "I wasn't able to fully process your request. Please try again.",
            }

        combined = "\n\n---\n\n".join(
            f"## Output from {r.agent_name}\n{r.content}" for r in successful
        )

        review_context = AgentContext(
            user_message=(
                f"Review the following agent outputs for the user's request: "
                f"\"{context.user_message}\"\n\n{combined}"
            ),
            classification=context.classification,
            user_context=context.user_context,
            rag_context="",
            session_id=context.session_id,
            user_id=context.user_id,
        )

        result = await self.execute(review_context)

        # Parse the QA response as JSON
        try:
            review = json.loads(result.content)
            # Ensure required fields exist
            return {
                "approved": review.get("approved", True),
                "feedback": review.get("feedback", ""),
                "revised_content": review.get("revised_content", combined),
            }
        except (json.JSONDecodeError, TypeError):
            # If QA didn't return proper JSON, treat content as approved
            return {
                "approved": True,
                "feedback": "",
                "revised_content": result.content,
            }
