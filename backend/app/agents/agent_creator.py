"""Agent Creator: a factory agent that creates new dynamic agents."""

from app.agents.base_agent import BaseAgent, Tool
from app.agents.tools.dynamic_agent_crud import (
    CREATE_DYNAMIC_AGENT_SCHEMA,
    DELETE_DYNAMIC_AGENT_SCHEMA,
    LIST_DYNAMIC_AGENTS_SCHEMA,
    create_dynamic_agent,
    delete_dynamic_agent,
    list_dynamic_agents,
)


class AgentCreatorAgent(BaseAgent):
    name = "agent_creator"
    description = "Agent Creator — creates, lists, and deletes custom dynamic agents"
    system_prompt = (
        "You are the Agent Creator in a corporate AI system.\n\n"
        "Your job is to create new specialized agents based on user requests. "
        "When a user asks you to create an agent, you must:\n\n"
        "1. Choose a descriptive snake_case `name` (e.g., 'ai_news_monitor')\n"
        "2. Choose a human-friendly `display_name` (e.g., 'AI News Monitor')\n"
        "3. Write a specific `description` of what the agent does (this is used for routing)\n"
        "4. Craft a detailed `system_prompt` that defines the agent's personality, "
        "responsibilities, and output structure\n"
        "5. Select the right tools from the available pool:\n"
        "   - web_search: Search the web for information\n"
        "   - web_fetch: Fetch and read a specific URL\n"
        "   - summarize_text: Summarize long text (brief, detailed, or bullet_points)\n"
        "   - query_knowledge_base: Search internal company documents\n"
        "6. Pick an output_format: 'summary', 'report', or 'bullet_points'\n\n"
        "Then call create_dynamic_agent with all the details.\n\n"
        "You can also list existing dynamic agents or delete them when asked.\n\n"
        "Be creative with system prompts — give each agent a clear role and personality."
    )

    def __init__(self):
        tools = [
            Tool(
                name="create_dynamic_agent",
                description="Create a new dynamic agent with the given configuration",
                parameters=CREATE_DYNAMIC_AGENT_SCHEMA,
                fn=create_dynamic_agent,
            ),
            Tool(
                name="list_dynamic_agents",
                description="List all active dynamic agents",
                parameters=LIST_DYNAMIC_AGENTS_SCHEMA,
                fn=list_dynamic_agents,
            ),
            Tool(
                name="delete_dynamic_agent",
                description="Soft-delete a dynamic agent by name",
                parameters=DELETE_DYNAMIC_AGENT_SCHEMA,
                fn=delete_dynamic_agent,
            ),
        ]
        super().__init__(tools=tools)
