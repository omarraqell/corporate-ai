# Agent Creator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an Agent Creator sub-agent that creates persistent, user-defined agents stored in the database and executed by a generic DynamicAgent class at runtime.

**Architecture:** New `dynamic_agents` DB table stores agent configs. An `AgentCreatorAgent` writes configs via tools. A `DynamicAgent` class loads configs and runs them using a pre-built tool pool. The orchestrator gains a fallback routing step that checks dynamic agents by name match or semantic similarity.

**Tech Stack:** FastAPI, SQLAlchemy (async), Alembic, OpenAI API, httpx, Tavily API, sentence-transformers (all-MiniLM-L6-v2)

---

### Task 1: Config and Environment

**Files:**
- Modify: `backend/app/config.py`
- Modify: `.env.example`
- Modify: `.env`

- [ ] **Step 1: Add tavily_api_key to Settings**

In `backend/app/config.py`, add the Tavily key under the LLM section:

```python
# In class Settings, after ollama_base_url:
    tavily_api_key: str = ""
```

- [ ] **Step 2: Update .env.example**

Add to `.env.example` after the `# OLLAMA_BASE_URL` line:

```
TAVILY_API_KEY=tvly-...
```

- [ ] **Step 3: Update .env**

Add to `.env` after the `# OLLAMA_BASE_URL` line:

```
TAVILY_API_KEY=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
```

- [ ] **Step 4: Commit**

```bash
git add backend/app/config.py .env.example
git commit -m "feat: add tavily_api_key to settings"
```

Note: Do NOT commit `.env` (it's gitignored).

---

### Task 2: DynamicAgent Database Model

**Files:**
- Create: `backend/app/models/dynamic_agent.py`

- [ ] **Step 1: Create the SQLAlchemy model**

Create `backend/app/models/dynamic_agent.py`:

```python
"""DynamicAgent model: stores user-created agent configurations."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DynamicAgent(Base):
    __tablename__ = "dynamic_agents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    system_prompt: Mapped[str] = mapped_column(Text)
    tools: Mapped[dict] = mapped_column(JSONB, default=list)
    output_format: Mapped[str] = mapped_column(String(50), default="summary")
    created_by: Mapped[str] = mapped_column(String(255))
    schedule: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/models/dynamic_agent.py
git commit -m "feat: add DynamicAgent SQLAlchemy model"
```

---

### Task 3: Alembic Migration

**Files:**
- Create: `backend/alembic/versions/003_add_dynamic_agents.py`

- [ ] **Step 1: Create the migration file**

Create `backend/alembic/versions/003_add_dynamic_agents.py`:

```python
"""Add dynamic_agents table

Revision ID: 003
Revises: 002
Create Date: 2026-04-01
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dynamic_agents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("display_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("tools", sa.JSON(), server_default="[]"),
        sa.Column("output_format", sa.String(50), server_default="summary"),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("schedule", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("dynamic_agents")
```

- [ ] **Step 2: Run the migration inside the Docker container**

```bash
docker exec corporate-ai-backend-1 alembic upgrade head
```

Expected: `INFO  [alembic.runtime.migration] Running upgrade 002 -> 003, Add dynamic_agents table`

- [ ] **Step 3: Verify the table was created**

```bash
docker exec corporate-ai-db-1 psql -U corporate -d corporate_ai -c "\d dynamic_agents"
```

Expected: Table columns listed matching the schema.

- [ ] **Step 4: Commit**

```bash
git add backend/alembic/versions/003_add_dynamic_agents.py
git commit -m "feat: add dynamic_agents migration"
```

---

### Task 4: Tavily Web Search Integration

**Files:**
- Modify: `backend/app/agents/tools/web_search.py`

- [ ] **Step 1: Replace the placeholder with Tavily**

Replace the entire contents of `backend/app/agents/tools/web_search.py`:

```python
"""
Web search tool for agents.

Uses the Tavily API for AI-optimized web search.
"""

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


async def web_search(query: str, num_results: int = 5) -> str:
    """Search the web using Tavily API."""
    if not settings.tavily_api_key:
        return (
            f"[Web search for: '{query}']\n"
            f"Web search is not configured. Add TAVILY_API_KEY to .env to enable."
        )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "query": query,
                    "max_results": num_results,
                    "api_key": settings.tavily_api_key,
                },
            )
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])
        if not results:
            return f"No web results found for: '{query}'"

        lines = []
        for r in results:
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "")[:500]
            lines.append(f"### {title}\nURL: {url}\n{content}")

        return "\n\n---\n\n".join(lines)

    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return f"Web search failed: {str(e)}"


WEB_SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The search query",
        },
        "num_results": {
            "type": "integer",
            "description": "Number of results to return (default: 5)",
            "default": 5,
        },
    },
    "required": ["query"],
}
```

- [ ] **Step 2: Test inside the container**

```bash
docker exec corporate-ai-backend-1 python -c "
import asyncio
from app.agents.tools.web_search import web_search
result = asyncio.run(web_search('latest AI news', num_results=2))
print(result[:500])
"
```

Expected: Two search results with titles, URLs, and content snippets.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/tools/web_search.py
git commit -m "feat: integrate Tavily API for web search"
```

---

### Task 5: Web Fetch Tool

**Files:**
- Create: `backend/app/agents/tools/web_fetch.py`

- [ ] **Step 1: Create the web_fetch tool**

Create `backend/app/agents/tools/web_fetch.py`:

```python
"""
Web fetch tool for agents.

Fetches a URL and extracts readable text from HTML.
Interface designed for future Playwright swap.
"""

import logging
import re

import httpx

logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 5000


async def web_fetch(url: str) -> str:
    """Fetch a URL and extract readable plain text."""
    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            headers={"User-Agent": "CorporateAI-Agent/1.0"},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

        html = response.text

        # Extract title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Untitled"

        # Remove script and style tags
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)

        # Remove all HTML tags
        text = re.sub(r"<[^>]+>", " ", text)

        # Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Decode HTML entities
        import html as html_module
        text = html_module.unescape(text)

        # Truncate
        if len(text) > MAX_CONTENT_LENGTH:
            text = text[:MAX_CONTENT_LENGTH] + "\n... (content truncated)"

        return f"Title: {title}\nURL: {url}\n\n{text}"

    except Exception as e:
        logger.error(f"Web fetch failed for {url}: {e}")
        return f"Failed to fetch {url}: {str(e)}"


WEB_FETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "description": "The URL to fetch and extract text from",
        },
    },
    "required": ["url"],
}
```

- [ ] **Step 2: Test inside the container**

```bash
docker exec corporate-ai-backend-1 python -c "
import asyncio
from app.agents.tools.web_fetch import web_fetch
result = asyncio.run(web_fetch('https://httpbin.org/html'))
print(result[:300])
"
```

Expected: Output starting with `Title:` followed by extracted text content.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/tools/web_fetch.py
git commit -m "feat: add web_fetch tool for URL text extraction"
```

---

### Task 6: Summarize Text Tool

**Files:**
- Create: `backend/app/agents/tools/summarize_text.py`

- [ ] **Step 1: Create the summarize_text tool**

Create `backend/app/agents/tools/summarize_text.py`:

```python
"""
Text summarization tool for agents.

Uses the LLM to summarize long text in various styles.
"""

import logging

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

STYLE_PROMPTS = {
    "brief": "Summarize the following text in 2-3 concise sentences.",
    "detailed": "Summarize the following text in a detailed paragraph, preserving key points.",
    "bullet_points": "Summarize the following text as a bullet-point list of key points.",
}


async def summarize_text(text: str, style: str = "brief") -> str:
    """Summarize text using the LLM."""
    prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["brief"])

    try:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=settings.llm_model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text[:10000]},  # Cap input length
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return f"Summarization failed: {str(e)}"


SUMMARIZE_TEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "The text to summarize",
        },
        "style": {
            "type": "string",
            "description": "Summary style: 'brief' (2-3 sentences), 'detailed' (paragraph), or 'bullet_points'",
            "enum": ["brief", "detailed", "bullet_points"],
            "default": "brief",
        },
    },
    "required": ["text"],
}
```

- [ ] **Step 2: Test inside the container**

```bash
docker exec corporate-ai-backend-1 python -c "
import asyncio
from app.agents.tools.summarize_text import summarize_text
text = 'Artificial intelligence has made significant progress in recent years. Large language models have transformed natural language processing. Companies are investing billions in AI research and development. The technology is being applied across healthcare, finance, education, and many other sectors.'
result = asyncio.run(summarize_text(text, style='bullet_points'))
print(result)
"
```

Expected: A bullet-point summary of the input text.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/tools/summarize_text.py
git commit -m "feat: add summarize_text tool"
```

---

### Task 7: Tool Pool Registry

**Files:**
- Create: `backend/app/agents/tools/tool_pool.py`

- [ ] **Step 1: Create the tool pool registry**

Create `backend/app/agents/tools/tool_pool.py`:

```python
"""
Tool Pool Registry: maps tool names to Tool factory functions.

DynamicAgent instances look up their tools JSON array against this
pool at runtime to attach the correct Tool instances.
"""

from app.agents.base_agent import Tool
from app.agents.tools.rag_query import RAG_QUERY_SCHEMA, query_knowledge_base
from app.agents.tools.summarize_text import SUMMARIZE_TEXT_SCHEMA, summarize_text
from app.agents.tools.web_fetch import WEB_FETCH_SCHEMA, web_fetch
from app.agents.tools.web_search import WEB_SEARCH_SCHEMA, web_search


def build_web_search_tool() -> Tool:
    return Tool(
        name="web_search",
        description="Search the web for information on any topic",
        parameters=WEB_SEARCH_SCHEMA,
        fn=web_search,
    )


def build_web_fetch_tool() -> Tool:
    return Tool(
        name="web_fetch",
        description="Fetch a URL and extract readable text from the page",
        parameters=WEB_FETCH_SCHEMA,
        fn=web_fetch,
    )


def build_summarize_tool() -> Tool:
    return Tool(
        name="summarize_text",
        description="Summarize long text into a concise output (brief, detailed, or bullet points)",
        parameters=SUMMARIZE_TEXT_SCHEMA,
        fn=summarize_text,
    )


def build_rag_query_tool() -> Tool:
    return Tool(
        name="query_knowledge_base",
        description="Search the company knowledge base (SOPs, routing rules, company docs)",
        parameters=RAG_QUERY_SCHEMA,
        fn=query_knowledge_base,
    )


TOOL_POOL: dict[str, callable] = {
    "web_search": build_web_search_tool,
    "web_fetch": build_web_fetch_tool,
    "summarize_text": build_summarize_tool,
    "query_knowledge_base": build_rag_query_tool,
}


def get_tools_from_pool(tool_names: list[str]) -> list[Tool]:
    """Look up tool names and return Tool instances."""
    tools = []
    for name in tool_names:
        factory = TOOL_POOL.get(name)
        if factory:
            tools.append(factory())
    return tools
```

- [ ] **Step 2: Test the import**

```bash
docker exec corporate-ai-backend-1 python -c "
from app.agents.tools.tool_pool import get_tools_from_pool
tools = get_tools_from_pool(['web_search', 'web_fetch', 'summarize_text', 'query_knowledge_base'])
print(f'Loaded {len(tools)} tools: {[t.name for t in tools]}')
"
```

Expected: `Loaded 4 tools: ['web_search', 'web_fetch', 'summarize_text', 'query_knowledge_base']`

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/tools/tool_pool.py
git commit -m "feat: add tool pool registry for dynamic agents"
```

---

### Task 8: DynamicAgent Runtime Class

**Files:**
- Create: `backend/app/agents/dynamic_agent.py`

- [ ] **Step 1: Create the DynamicAgent class**

Create `backend/app/agents/dynamic_agent.py`:

```python
"""
DynamicAgent: a generic agent class that loads behavior from a DB config.

All user-created agents run on this single class. The system_prompt,
tools, and output_format come from the dynamic_agents table.
"""

from app.agents.base_agent import BaseAgent, AgentContext, AgentResult
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
```

- [ ] **Step 2: Test instantiation**

```bash
docker exec corporate-ai-backend-1 python -c "
from app.agents.dynamic_agent import DynamicAgent
agent = DynamicAgent(
    name='test_agent',
    display_name='Test Agent',
    description='A test agent',
    system_prompt='You are a test agent.',
    tool_names=['web_search', 'summarize_text'],
    output_format='bullet_points',
)
print(f'Agent: {agent.name}, tools: {[t.name for t in agent.tools]}')
print(f'Prompt ends with: ...{agent.system_prompt[-60:]}')
"
```

Expected: Agent created with 2 tools, system prompt ending with bullet_points format instruction.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/dynamic_agent.py
git commit -m "feat: add DynamicAgent runtime class"
```

---

### Task 9: Agent Creator CRUD Tools

**Files:**
- Create: `backend/app/agents/tools/dynamic_agent_crud.py`

- [ ] **Step 1: Create the CRUD tool functions**

Create `backend/app/agents/tools/dynamic_agent_crud.py`:

```python
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
```

- [ ] **Step 2: Test create and list**

```bash
docker exec corporate-ai-backend-1 python -c "
import asyncio
from app.agents.tools.dynamic_agent_crud import create_dynamic_agent, list_dynamic_agents, delete_dynamic_agent

async def test():
    result = await create_dynamic_agent(
        name='test_crud_agent',
        display_name='Test CRUD Agent',
        description='A test agent for CRUD verification',
        system_prompt='You are a test agent.',
        tools='[\"web_search\"]',
        output_format='summary',
        created_by='test',
    )
    print('CREATE:', result)

    result = await list_dynamic_agents()
    print('LIST:', result)

    result = await delete_dynamic_agent('test_crud_agent')
    print('DELETE:', result)

asyncio.run(test())
"
```

Expected: Agent created, listed, then soft-deleted successfully.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/tools/dynamic_agent_crud.py
git commit -m "feat: add CRUD tools for dynamic agent management"
```

---

### Task 10: Agent Creator Sub-Agent

**Files:**
- Create: `backend/app/agents/agent_creator.py`

- [ ] **Step 1: Create the AgentCreatorAgent class**

Create `backend/app/agents/agent_creator.py`:

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/agents/agent_creator.py
git commit -m "feat: add AgentCreatorAgent sub-agent"
```

---

### Task 11: Register Agent Creator and Update Receptionist

**Files:**
- Modify: `backend/app/agents/__init__.py`
- Modify: `backend/app/services/receptionist.py`
- Modify: `backend/app/services/orchestrator.py` (only the LABEL_TO_AGENTS map)

- [ ] **Step 1: Add AgentCreatorAgent to the registry**

In `backend/app/agents/__init__.py`, add the import and registry entry:

Add this import at the top with the other imports:
```python
from app.agents.agent_creator import AgentCreatorAgent
```

Add to `AGENT_REGISTRY` dict:
```python
    "agent_creator": AgentCreatorAgent,
```

Add `"AgentCreatorAgent"` to the `__all__` list.

- [ ] **Step 2: Add agent_management label to Receptionist**

In `backend/app/services/receptionist.py`:

Add `"agent_management"` to the `ROUTE_LABELS` list (after `"escalation"`):
```python
    "agent_management",
```

Add to `LABEL_DESCRIPTIONS` dict:
```python
    "agent_management": "Creating, listing, managing, or deleting custom AI agents",
```

- [ ] **Step 3: Add agent_management to LABEL_TO_AGENTS**

In `backend/app/services/orchestrator.py`, add to the `LABEL_TO_AGENTS` dict:
```python
    "agent_management": ["agent_creator"],
```

- [ ] **Step 4: Test classification**

```bash
docker exec corporate-ai-backend-1 python -c "
import asyncio
from app.services.receptionist import ReceptionistService
r = ReceptionistService()
result = asyncio.run(r.classify('Create an agent that monitors tech news'))
print(result)
"
```

Expected: `{'label': 'agent_management', 'confidence': ...}`

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/__init__.py backend/app/services/receptionist.py backend/app/services/orchestrator.py
git commit -m "feat: register agent_creator and add agent_management routing"
```

---

### Task 12: Dynamic Agent Routing in Orchestrator

**Files:**
- Modify: `backend/app/services/orchestrator.py`

- [ ] **Step 1: Add imports**

At the top of `backend/app/services/orchestrator.py`, add these imports:

```python
from sqlalchemy import select as sa_select
from app.agents.dynamic_agent import DynamicAgent as DynamicAgentRunner
from app.models.dynamic_agent import DynamicAgent as DynamicAgentModel
from app.utils.embeddings import EmbeddingService
```

Note: `select` is already imported — the existing import `from sqlalchemy import select` is used elsewhere. Use the same `select`.

Actually, `select` is already imported. So only add:

```python
from app.agents.dynamic_agent import DynamicAgent as DynamicAgentRunner
from app.models.dynamic_agent import DynamicAgent as DynamicAgentModel
from app.utils.embeddings import EmbeddingService
```

- [ ] **Step 2: Add _check_dynamic_agents method**

Add this method to the `OrchestratorService` class, after `_ceo_direct_response`:

```python
    async def _check_dynamic_agents(
        self, db: AsyncSession, message: str
    ) -> DynamicAgentRunner | None:
        """Check if a dynamic agent matches the message by name or semantic similarity."""
        result = await db.execute(
            select(DynamicAgentModel).where(DynamicAgentModel.is_active.is_(True))
        )
        agents = result.scalars().all()

        if not agents:
            return None

        msg_lower = message.lower()

        # 1. Explicit name match
        for agent in agents:
            if agent.display_name.lower() in msg_lower or agent.name in msg_lower:
                logger.info(f"Dynamic agent matched by name: {agent.name}")
                return DynamicAgentRunner(
                    name=agent.name,
                    display_name=agent.display_name,
                    description=agent.description,
                    system_prompt=agent.system_prompt,
                    tool_names=agent.tools,
                    output_format=agent.output_format,
                )

        # 2. Semantic similarity match
        embedder = EmbeddingService.get_instance()
        msg_embedding = embedder.embed_single(message)

        best_agent = None
        best_score = 0.0

        for agent in agents:
            desc_embedding = embedder.embed_single(agent.description)
            # Cosine similarity
            dot = sum(a * b for a, b in zip(msg_embedding, desc_embedding))
            norm_a = sum(a * a for a in msg_embedding) ** 0.5
            norm_b = sum(b * b for b in desc_embedding) ** 0.5
            similarity = dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

            if similarity > best_score:
                best_score = similarity
                best_agent = agent

        if best_agent and best_score > 0.75:
            logger.info(
                f"Dynamic agent matched by similarity: {best_agent.name} "
                f"(score: {best_score:.3f})"
            )
            return DynamicAgentRunner(
                name=best_agent.name,
                display_name=best_agent.display_name,
                description=best_agent.description,
                system_prompt=best_agent.system_prompt,
                tool_names=best_agent.tools,
                output_format=best_agent.output_format,
            )

        return None
```

- [ ] **Step 3: Modify handle_message to check dynamic agents**

In `handle_message`, replace the block at Step 5 / Step 6 (lines ~97-115). Find this code:

```python
        # --- Step 5: Determine routing ---
        target_agents = LABEL_TO_AGENTS.get(classification["label"], [])

        # --- Step 6: Execute ---
        if not target_agents:
            # General inquiry — CEO handles directly with RAG context
            final_response = await self._ceo_direct_response(context, db)
        else:
```

Replace with:

```python
        # --- Step 5: Determine routing ---
        target_agents = LABEL_TO_AGENTS.get(classification["label"], [])

        # --- Step 5b: Check dynamic agents if no static match ---
        dynamic_agent = None
        if not target_agents:
            dynamic_agent = await self._check_dynamic_agents(db, message)

        # --- Step 6: Execute ---
        if dynamic_agent:
            # Dynamic agent matched — run it through the standard pipeline
            results = [await dynamic_agent.execute(context)]
            target_agents = [dynamic_agent.name]

            # QA Review
            qa_result = await self._qa_review(context, results)
            final_response = await self._synthesize(context, qa_result, results)

            # Notify secretary
            asyncio.create_task(self._notify_secretary(context, results))
        elif not target_agents:
            # General inquiry — CEO handles directly with RAG context
            final_response = await self._ceo_direct_response(context, db)
        else:
```

The rest of the `else` block (dispatching static agents) stays unchanged.

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/orchestrator.py
git commit -m "feat: add dynamic agent routing fallback in orchestrator"
```

---

### Task 13: End-to-End Test

**Files:** None (manual testing in the running system)

- [ ] **Step 1: Restart the backend to pick up all changes**

```bash
cd C:/Users/DELL/Desktop/corporate-ai && docker compose up -d backend --force-recreate
```

Wait ~30 seconds for model loading, then verify:

```bash
docker exec corporate-ai-backend-1 alembic upgrade head
curl -s http://localhost:8001/health
```

Expected: `{"status":"ok"}`

- [ ] **Step 2: Test agent creation via the API**

```bash
curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "e2e-test-session",
    "message": "Create an agent that monitors the latest AI and machine learning news, searches the web for recent developments, and summarizes findings"
  }' | python -m json.tool
```

Expected: Response with `"classification": "agent_management"` and `"agents_used": ["agent_creator"]`. The message should confirm a new dynamic agent was created.

- [ ] **Step 3: Test invoking the created agent by name**

```bash
curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "e2e-test-session-2",
    "message": "Ask my AI News Monitor for the latest updates"
  }' | python -m json.tool
```

Expected: The dynamic agent should be matched by name, search the web using Tavily, and return summarized AI news.

- [ ] **Step 4: Test semantic routing (no name mentioned)**

```bash
curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "e2e-test-session-3",
    "message": "What are the latest developments in artificial intelligence?"
  }' | python -m json.tool
```

Expected: If the semantic similarity is > 0.75, the dynamic agent should handle this. Check the backend logs to confirm:

```bash
docker compose logs backend --tail 10
```

Look for: `Dynamic agent matched by similarity: ...`

- [ ] **Step 5: Test listing agents**

```bash
curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "e2e-test-session-4",
    "message": "List all my custom agents"
  }' | python -m json.tool
```

Expected: Response listing the created agent(s).

- [ ] **Step 6: Verify via the frontend**

Open http://localhost:3001 and try:
1. "Create an agent that tracks cryptocurrency prices and market trends"
2. Wait for confirmation
3. "What's happening in the crypto market today?"
4. Verify the new agent handles the request

---

### Task 14: Final Commit and Push

- [ ] **Step 1: Review all changes**

```bash
git status
git log --oneline -10
```

- [ ] **Step 2: Push to remote**

```bash
git push origin master
```
