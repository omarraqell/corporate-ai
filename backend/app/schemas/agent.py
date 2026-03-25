from pydantic import BaseModel


class ClassificationResult(BaseModel):
    label: str
    confidence: float
    all_scores: dict[str, float] = {}


class AgentResult(BaseModel):
    agent_name: str
    content: str
    needs_writing: bool = False
    metadata: dict = {}
