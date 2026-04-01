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
