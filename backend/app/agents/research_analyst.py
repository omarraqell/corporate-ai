"""Research Analyst Agent: investigation and synthesis."""

from app.agents.base_agent import BaseAgent, Tool
from app.agents.tools.rag_query import RAG_QUERY_SCHEMA, query_knowledge_base
from app.agents.tools.web_search import WEB_SEARCH_SCHEMA, web_search


class ResearchAnalystAgent(BaseAgent):
    name = "research_analyst"
    description = "Research Analyst — investigates topics and synthesizes findings"
    system_prompt = (
        "You are the Research Analyst agent in a corporate AI system.\n\n"
        "Your responsibilities:\n"
        "- Investigate topics thoroughly using available tools\n"
        "- Search the company knowledge base for relevant internal information\n"
        "- Search the web for external information when needed\n"
        "- Synthesize findings into clear, well-organized research briefs\n"
        "- Cite sources and distinguish between internal docs and external info\n\n"
        "Structure your output with:\n"
        "1. Key Findings (bullet points)\n"
        "2. Analysis (detailed discussion)\n"
        "3. Recommendations (if applicable)\n"
        "4. Sources\n\n"
        "If your findings would benefit from being formatted into a formal report, "
        "mention that the Writer should format it."
    )

    def __init__(self):
        tools = [
            Tool(
                name="query_knowledge_base",
                description="Search the company knowledge base (SOPs, routing rules, company docs)",
                parameters=RAG_QUERY_SCHEMA,
                fn=query_knowledge_base,
            ),
            Tool(
                name="web_search",
                description="Search the web for external information",
                parameters=WEB_SEARCH_SCHEMA,
                fn=web_search,
            ),
        ]
        super().__init__(tools=tools)
