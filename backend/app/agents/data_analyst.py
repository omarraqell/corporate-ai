"""Data Analyst Agent: data analysis and insights."""

from app.agents.base_agent import BaseAgent, Tool
from app.agents.tools.code_executor import EXECUTE_PYTHON_SCHEMA, execute_python
from app.agents.tools.rag_query import RAG_QUERY_SCHEMA, query_knowledge_base


class DataAnalystAgent(BaseAgent):
    name = "data_analyst"
    description = "Data Analyst — analyzes data, generates insights and visualizations"
    system_prompt = (
        "You are the Data Analyst agent in a corporate AI system.\n\n"
        "Your responsibilities:\n"
        "- Analyze data and generate actionable insights\n"
        "- Write and execute Python code for data analysis (pandas, numpy, etc.)\n"
        "- Create data summaries with key metrics and trends\n"
        "- Query the knowledge base for context on KPIs and business metrics\n\n"
        "When executing code:\n"
        "- Use pandas for data manipulation\n"
        "- Print results clearly with labels\n"
        "- If generating charts, save to file and describe the visualization\n\n"
        "Structure your output with:\n"
        "1. Summary of Findings\n"
        "2. Key Metrics\n"
        "3. Trends & Patterns\n"
        "4. Recommendations\n\n"
        "If your findings need a polished report, mention that the Writer should format it."
    )

    def __init__(self):
        tools = [
            Tool(
                name="execute_python",
                description="Execute Python code for data analysis. Code must be complete and runnable.",
                parameters=EXECUTE_PYTHON_SCHEMA,
                fn=execute_python,
            ),
            Tool(
                name="query_knowledge_base",
                description="Search the company knowledge base for context on metrics and KPIs",
                parameters=RAG_QUERY_SCHEMA,
                fn=query_knowledge_base,
            ),
        ]
        super().__init__(tools=tools)
