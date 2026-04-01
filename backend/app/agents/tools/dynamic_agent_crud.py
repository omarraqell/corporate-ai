"""
CRUD tools for the Agent Creator sub-agent.

Allows creating, listing, and deleting dynamic agents in the database.
"""

import json
import uuid

from sqlalchemy import select


async def create_dynamic_agent(
    name: str,
    display_name: str,
    description: str,
    system_prompt: str,
    tools: str,
    output_format: str = "summary",
    created_by: str = "system",
) -> str:
    """Create a new dynamic agent configuration."""
    from app.database import async_session
    from app.models.dynamic_agent import DynamicAgent

    # Parse tools from JSON string (LLM sends it as string)
    if isinstance(tools, str):
        try:
            tools_list = json.loads(tools)
        except json.JSONDecodeError:
            tools_list = [t.strip() for t in tools.split(",")]
    else:
        tools_list = tools

    valid_tools = ["web_search", "web_fetch", "summarize_text", "query_knowledge_base"]
    invalid = [t for t in tools_list if t not in valid_tools]
    if invalid:
        return f"Invalid tool names: {invalid}. Valid tools: {valid_tools}"

    async with async_session() as db:
        # Check for duplicate name
        existing = await db.execute(
            select(DynamicAgent).where(DynamicAgent.name == name)
        )
        if existing.scalar_one_or_none():
            return f"Agent with name '{name}' already exists. Choose a different name."

        agent = DynamicAgent(
            id=uuid.uuid4(),
            name=name,
            display_name=display_name,
            description=description,
            system_prompt=system_prompt,
            tools=tools_list,
            output_format=output_format,
            created_by=created_by,
        )
        db.add(agent)
        await db.commit()

    return (
        f"Dynamic agent created successfully!\n"
        f"  Name: {name}\n"
        f"  Display Name: {display_name}\n"
        f"  Tools: {tools_list}\n"
        f"  Output Format: {output_format}\n"
        f"Users can now invoke this agent by mentioning '{display_name}' in their message."
    )


async def list_dynamic_agents() -> str:
    """List all active dynamic agents."""
    from app.database import async_session
    from app.models.dynamic_agent import DynamicAgent

    async with async_session() as db:
        result = await db.execute(
            select(DynamicAgent)
            .where(DynamicAgent.is_active.is_(True))
            .order_by(DynamicAgent.created_at.desc())
        )
        agents = result.scalars().all()

    if not agents:
        return "No dynamic agents have been created yet."

    lines = []
    for a in agents:
        lines.append(
            f"- **{a.display_name}** (`{a.name}`)\n"
            f"  Description: {a.description}\n"
            f"  Tools: {a.tools}\n"
            f"  Format: {a.output_format}"
        )
    return "\n\n".join(lines)


async def delete_dynamic_agent(name: str) -> str:
    """Soft-delete a dynamic agent by name."""
    from app.database import async_session
    from app.models.dynamic_agent import DynamicAgent

    async with async_session() as db:
        result = await db.execute(
            select(DynamicAgent).where(DynamicAgent.name == name)
        )
        agent = result.scalar_one_or_none()

        if not agent:
            return f"No agent found with name '{name}'."

        if not agent.is_active:
            return f"Agent '{name}' is already deleted."

        agent.is_active = False
        await db.commit()

    return f"Agent '{agent.display_name}' (`{name}`) has been deactivated."


CREATE_DYNAMIC_AGENT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Snake_case identifier for the agent (e.g., 'ai_news_monitor')",
        },
        "display_name": {
            "type": "string",
            "description": "Human-friendly name (e.g., 'AI News Monitor')",
        },
        "description": {
            "type": "string",
            "description": "What this agent does — used for routing. Be specific.",
        },
        "system_prompt": {
            "type": "string",
            "description": "Detailed system prompt for the agent's LLM behavior",
        },
        "tools": {
            "type": "string",
            "description": 'JSON array of tool names: ["web_search", "web_fetch", "summarize_text", "query_knowledge_base"]',
        },
        "output_format": {
            "type": "string",
            "description": "Output style: summary, report, or bullet_points",
            "enum": ["summary", "report", "bullet_points"],
            "default": "summary",
        },
    },
    "required": ["name", "display_name", "description", "system_prompt", "tools"],
}

LIST_DYNAMIC_AGENTS_SCHEMA = {
    "type": "object",
    "properties": {},
}

DELETE_DYNAMIC_AGENT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The snake_case name of the agent to delete",
        },
    },
    "required": ["name"],
}
