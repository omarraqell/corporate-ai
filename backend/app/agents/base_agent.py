"""
Base Agent: abstract class all sub-agents inherit from.

Provides LLM calling, tool execution, and a standard interface
for the orchestrator to invoke agents uniformly.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Context bundle passed to every sub-agent."""
    user_message: str
    classification: dict
    user_context: str
    rag_context: str
    session_id: str
    user_id: str
    extra: dict = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result returned by a sub-agent."""
    agent_name: str
    content: str
    needs_writing: bool = False
    success: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class Tool:
    """A tool that an agent can call."""
    name: str
    description: str
    parameters: dict  # JSON Schema
    fn: Callable[..., Coroutine[Any, Any, str]]


class BaseAgent(ABC):
    """Abstract base agent. All six sub-agents inherit from this."""

    name: str = "base_agent"
    description: str = "Base agent"
    system_prompt: str = "You are a helpful assistant."
    max_tool_rounds: int = 5

    def __init__(self, tools: list[Tool] | None = None):
        self.llm = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model_name
        self.tools = tools or []

    def _build_tool_schemas(self) -> list[dict] | None:
        """Convert tools to OpenAI function calling format."""
        if not self.tools:
            return None
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools
        ]

    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool by name with given arguments."""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    result = await tool.fn(**arguments)
                    return str(result)
                except Exception as e:
                    logger.error(f"Tool {tool_name} failed: {e}")
                    return f"Error executing {tool_name}: {str(e)}"
        return f"Unknown tool: {tool_name}"

    def _build_user_prompt(self, context: AgentContext) -> str:
        """Build the user prompt from context. Override for custom formatting."""
        parts = [f"## User Request\n{context.user_message}"]

        if context.classification:
            parts.append(
                f"## Classification\nLabel: {context.classification.get('label', 'unknown')} "
                f"(confidence: {context.classification.get('confidence', 0):.2f})"
            )

        if context.user_context:
            parts.append(f"## User Context\n{context.user_context}")

        if context.rag_context:
            parts.append(f"## Relevant Company Knowledge\n{context.rag_context}")

        if context.extra:
            for key, value in context.extra.items():
                parts.append(f"## {key}\n{value}")

        parts.append("Please handle this request according to your role.")
        return "\n\n".join(parts)

    async def execute(self, context: AgentContext) -> AgentResult:
        """
        Run the agent. Handles multi-turn tool calling automatically.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self._build_user_prompt(context)},
        ]
        tool_schemas = self._build_tool_schemas()

        for round_num in range(self.max_tool_rounds):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 2000,
                }
                if tool_schemas:
                    kwargs["tools"] = tool_schemas

                response = await self.llm.chat.completions.create(**kwargs)
                choice = response.choices[0]

                # If the model wants to call tools
                if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                    messages.append(choice.message)

                    for tool_call in choice.message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = json.loads(tool_call.function.arguments)
                        logger.info(f"[{self.name}] Calling tool: {fn_name}({fn_args})")

                        tool_result = await self._execute_tool(fn_name, fn_args)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result,
                        })
                    continue  # Next round with tool results

                # Final response (no more tool calls)
                content = choice.message.content or ""
                return self._build_result(content)

            except Exception as e:
                logger.error(f"[{self.name}] Error in round {round_num}: {e}")
                return AgentResult(
                    agent_name=self.name,
                    content=f"Agent {self.name} encountered an error: {str(e)}",
                    success=False,
                )

        # Exhausted tool rounds
        return AgentResult(
            agent_name=self.name,
            content="Agent reached maximum tool execution rounds without completing.",
            success=False,
        )

    def _build_result(self, content: str) -> AgentResult:
        """Build an AgentResult. Override to customize needs_writing detection."""
        needs_writing = any(
            phrase in content.lower()
            for phrase in [
                "needs formal report",
                "should be formatted",
                "writer should",
                "needs documentation",
                "recommend the writer",
            ]
        )
        return AgentResult(
            agent_name=self.name,
            content=content,
            needs_writing=needs_writing,
        )
