from app.agents.code_dev import CodeDevAgent
from app.agents.data_analyst import DataAnalystAgent
from app.agents.qa_reviewer import QAReviewerAgent
from app.agents.research_analyst import ResearchAnalystAgent
from app.agents.secretary import SecretaryAgent
from app.agents.writer import WriterAgent

AGENT_REGISTRY = {
    "secretary": SecretaryAgent,
    "research_analyst": ResearchAnalystAgent,
    "data_analyst": DataAnalystAgent,
    "writer": WriterAgent,
    "code_dev": CodeDevAgent,
    "qa_reviewer": QAReviewerAgent,
}


def create_agent_registry() -> dict:
    """Instantiate all agents. Called once at app startup."""
    return {name: cls() for name, cls in AGENT_REGISTRY.items()}


__all__ = [
    "SecretaryAgent",
    "ResearchAnalystAgent",
    "DataAnalystAgent",
    "WriterAgent",
    "CodeDevAgent",
    "QAReviewerAgent",
    "AGENT_REGISTRY",
    "create_agent_registry",
]
