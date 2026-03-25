"""
RAG query tool for agents.

Allows agents to search the company knowledge base directly.
"""

from app.services.rag_pipeline import RAGService

_rag = RAGService()


async def query_knowledge_base(
    query: str,
    source: str | None = None,
    top_k: int = 3,
) -> str:
    """
    Search the company knowledge base.

    Note: This tool needs a DB session. It creates its own for tool calls.
    """
    from app.database import async_session

    async with async_session() as db:
        chunks = await _rag.retrieve(
            db=db,
            query=query,
            top_k=top_k,
            source_filter=source,
        )

    if not chunks:
        return f"No results found for: '{query}'"

    results = []
    for c in chunks:
        results.append(f"[{c.source}: {c.title} (relevance: {c.score:.2f})]\n{c.content}")

    return "\n\n---\n\n".join(results)


RAG_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Search query for the knowledge base",
        },
        "source": {
            "type": "string",
            "description": "Filter by source type: 'sop', 'routing_rule', or 'company_doc'. Leave empty for all.",
            "enum": ["sop", "routing_rule", "company_doc"],
        },
        "top_k": {
            "type": "integer",
            "description": "Number of results to return (default: 3)",
            "default": 3,
        },
    },
    "required": ["query"],
}
