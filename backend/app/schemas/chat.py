from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    message: str
    session_id: str
    agent_name: str | None = None
    classification: str | None = None
