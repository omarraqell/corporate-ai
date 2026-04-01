"""
DynamicAgent: a generic agent class that loads behavior from a DB config.

All user-created agents run on this single class. The system_prompt,
tools, and output_format come from the dynamic_agents table.
"""

from app.agents.base_agent import BaseAgent
from app.agents.tools.tool_pool import get_tools_from_pool


class DynamicAgent(BaseAgent):
    """Agent whose behavior is defined by a database configuration."""

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        system_prompt: str,
        tool_names: list[str],
        output_format: str = "summary",
    ):
        self.name = name
        self.description = description
        self.display_name = display_name
        self.output_format = output_format

        # Build system prompt with output format instruction
        format_instructions = {
            "summary": "Provide your response as a clear, concise summary.",
            "report": "Structure your response as a professional report with sections and headers.",
            "bullet_points": "Structure your response as organized bullet points.",
        }
        format_hint = format_instructions.get(output_format, format_instructions["summary"])
        self.system_prompt = f"{system_prompt}\n\nOutput format: {format_hint}"

        # Load tools from pool
        tools = get_tools_from_pool(tool_names)
        super().__init__(tools=tools)
