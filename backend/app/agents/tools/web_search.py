"""
Web search tool for agents.

Uses a simple approach: asks the LLM to synthesize information
based on its training data. For production, swap in a real search
API (SerpAPI, Tavily, Brave Search, etc.)
"""

import httpx

from app.config import settings


async def web_search(query: str, num_results: int = 5) -> str:
    """
    Search the web for information.

    For now, returns a note that real search requires an API key.
    Replace this with a real search provider in production.
    """
    # Placeholder: in production, integrate with a search API
    # Example with Tavily:
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://api.tavily.com/search",
    #         json={"query": query, "max_results": num_results, "api_key": settings.tavily_api_key},
    #     )
    #     results = response.json()["results"]
    #     return "\n".join(f"- {r['title']}: {r['content']}" for r in results)

    return (
        f"[Web search for: '{query}']\n"
        f"Note: Web search is not yet configured. To enable, add a search API key "
        f"(Tavily, SerpAPI, or Brave Search) to the environment and update this tool.\n"
        f"For now, please answer based on your training knowledge."
    )


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
