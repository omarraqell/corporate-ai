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
