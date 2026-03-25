import uuid
from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    session_id: str
    title: str
    description: str = ""
    assigned_agent: str


class TaskUpdate(BaseModel):
    status: str | None = None
    result: str | None = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    session_id: str
    title: str
    description: str
    assigned_agent: str
    status: str
    parent_task_id: uuid.UUID | None
    result: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
