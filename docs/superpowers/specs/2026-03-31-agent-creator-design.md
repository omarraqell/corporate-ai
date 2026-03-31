# Agent Creator Sub-Agent — Design Spec

**Date:** 2026-03-31
**Status:** Approved

## Overview

Add a new "Agent Creator" sub-agent to the Corporate AI system. This agent is a factory — it creates new persistent agents on-the-fly from natural language descriptions. Created agents can browse the web, research topics, and summarize findings. They are stored as DB configs and executed by a single generic `DynamicAgent` class at runtime.

---

## Section 1: Database Schema

New table: `dynamic_agents`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `name` | VARCHAR unique | Snake_case identifier (e.g., `competitor_pricing_monitor`) |
| `display_name` | VARCHAR | Human-friendly name (e.g., "Competitor Pricing Monitor") |
| `description` | TEXT | What this agent does — used for semantic routing |
| `system_prompt` | TEXT | LLM-crafted system prompt |
| `tools` | JSON array | Tool names from the pool (e.g., `["web_search", "web_fetch", "summarize_text"]`) |
| `output_format` | VARCHAR | Preferred output style: `summary`, `report`, `bullet_points` |
| `created_by` | VARCHAR | User ID who requested creation |
| `schedule` | VARCHAR nullable | Reserved for future cron expression (null for now) |
| `is_active` | BOOLEAN default true | Soft delete / disable toggle |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Last modified |

Alembic migration required.

---

## Section 2: New Tools

### 2a. `web_fetch` tool (`backend/app/agents/tools/web_fetch.py`)

- Fetches a URL and extracts readable plain text from HTML
- Uses `httpx` (existing dependency) for HTTP GET
- Strips HTML tags for basic text extraction (no JS rendering)
- Returns: page title, URL, extracted text (truncated to ~5000 chars)
- Timeout: 10 seconds
- Interface designed so Playwright can replace httpx later for full browser automation

### 2b. `summarize_text` tool (`backend/app/agents/tools/summarize_text.py`)

- Summarizes long text using the LLM (gpt-4o-mini)
- Accepts `style` parameter: `brief` (2-3 sentences), `detailed` (paragraph), `bullet_points`
- Enables dynamic agents to chain: web_fetch → summarize_text

### 2c. Tool Pool Registry (`backend/app/agents/tools/tool_pool.py`)

Maps tool names to factory functions:

```python
TOOL_POOL = {
    "web_search": build_web_search_tool,
    "web_fetch": build_web_fetch_tool,
    "summarize_text": build_summarize_tool,
    "query_knowledge_base": build_rag_query_tool,
}
```

Each factory returns a `Tool` instance. Dynamic agents look up their `tools` JSON array against this pool at runtime.

### 2d. Tavily integration for `web_search`

- Replace the existing placeholder in `backend/app/agents/tools/web_search.py` with real Tavily API integration
- New env var: `TAVILY_API_KEY`
- Add to `config.py` settings

---

## Section 3: The Agent Creator Sub-Agent

New file: `backend/app/agents/agent_creator.py`

### Role
Receives natural language requests to create, list, or delete dynamic agents.

### Tools
- `create_dynamic_agent(name, display_name, description, system_prompt, tools, output_format)` — saves to DB
- `list_dynamic_agents()` — shows all active dynamic agents
- `delete_dynamic_agent(name)` — soft-deletes (sets `is_active=false`)

### Behavior
1. User says "Create an agent that tracks AI startup funding news"
2. Agent Creator's system prompt instructs the LLM to:
   - Generate a snake_case `name` and human-friendly `display_name`
   - Write a tailored `description` (used for routing)
   - Craft a detailed `system_prompt` for the new agent
   - Select tools from the pool
   - Pick an `output_format`
3. Calls `create_dynamic_agent` tool to persist
4. Returns confirmation with the new agent's details

### Classification
- New Receptionist label: `agent_management`
- Description: "Creating, listing, or deleting custom agents"
- Added to `LABEL_TO_AGENTS`: `"agent_management": ["agent_creator"]`

---

## Section 4: The DynamicAgent Class

New file: `backend/app/agents/dynamic_agent.py`

### Purpose
A single generic agent class that any created agent runs on. No code generation — behavior is driven entirely by DB config.

### Execution flow
1. Loads agent config from `dynamic_agents` table by name
2. Sets `system_prompt` from stored config
3. Looks up tool names against the tool pool registry, attaches matching `Tool` instances
4. Runs the standard multi-turn LLM + tool execution loop (same pattern as `BaseAgent`: max 5 rounds, OpenAI function calling)
5. Returns an `AgentResult`

### Why not subclass BaseAgent per dynamic agent?
- No Python files to generate — safer, no restart needed
- New tools added to the pool are immediately available to all dynamic agents
- Config changes in DB take effect instantly

---

## Section 5: Orchestrator Integration

### Static routing (unchanged)
Existing `LABEL_TO_AGENTS` map handles the 6 original agents plus the new Agent Creator:

```python
"agent_management": ["agent_creator"]
```

### Dynamic routing (new fallback)
After static routing, the orchestrator checks for dynamic agent matches:

1. **Explicit name match:** Scans message for a dynamic agent's `display_name` or `name`. If found, routes directly to it.
2. **Semantic similarity match:** If no name match, computes message embedding (using existing `all-MiniLM-L6-v2`) and compares against each active dynamic agent's `description` embedding. If similarity > 0.75 threshold, routes to that agent.
3. **No match:** Falls back to CEO direct response (existing behavior).

### New orchestrator method
`_check_dynamic_agents(message)` — returns matched dynamic agent config or None.

### Modified `handle_message()`
After `LABEL_TO_AGENTS` lookup yields empty list (or `general_inquiry`), call `_check_dynamic_agents()` before falling back to CEO.

### Execution
Once a dynamic agent is matched:
- Orchestrator instantiates `DynamicAgent` with the matched config
- Runs through the same pipeline: execute → QA review → synthesize → store conversation
- Secretary logs the execution as usual

---

## File Changes Summary

### New files
- `backend/app/agents/agent_creator.py` — Agent Creator sub-agent
- `backend/app/agents/dynamic_agent.py` — Generic DynamicAgent class
- `backend/app/agents/tools/web_fetch.py` — URL fetch + text extraction tool
- `backend/app/agents/tools/summarize_text.py` — LLM summarization tool
- `backend/app/agents/tools/tool_pool.py` — Tool name → factory registry
- `backend/app/models/dynamic_agent.py` — SQLAlchemy model
- `alembic/versions/xxxx_add_dynamic_agents.py` — Migration

### Modified files
- `backend/app/agents/__init__.py` — Register Agent Creator in `AGENT_REGISTRY`
- `backend/app/agents/tools/web_search.py` — Replace placeholder with Tavily integration
- `backend/app/services/orchestrator.py` — Add `agent_management` label, add `_check_dynamic_agents()` fallback
- `backend/app/services/receptionist.py` — Add `agent_management` to `ROUTE_LABELS` and `LABEL_DESCRIPTIONS`
- `backend/app/config.py` — Add `tavily_api_key` setting
- `.env.example` — Add `TAVILY_API_KEY`
- `.env` — Add `TAVILY_API_KEY`

---

## Future Extensions (not in scope now)
- Scheduled execution via cron (`schedule` field is reserved)
- Full browser automation (Playwright swap for `web_fetch`)
- Dynamic agent editing/updating
- Agent sharing between users
