import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.classification_log import ClassificationLog
from app.services.receptionist import ReceptionistService

router = APIRouter(prefix="/classify", tags=["receptionist"])

receptionist = ReceptionistService()


class ClassifyRequest(BaseModel):
    message: str


class ClassifyResponse(BaseModel):
    label: str
    confidence: float


@router.post("", response_model=ClassifyResponse)
async def classify_message(request: ClassifyRequest, db: AsyncSession = Depends(get_db)):
    result = await receptionist.classify(request.message)

    # Log for future BERT training data
    log_entry = ClassificationLog(
        id=uuid.uuid4(),
        user_message=request.message,
        label=result["label"],
        confidence=result["confidence"],
    )
    db.add(log_entry)
    await db.commit()

    return ClassifyResponse(label=result["label"], confidence=result["confidence"])
