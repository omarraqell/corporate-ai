from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.rag_pipeline import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])

rag_service = RAGService()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    source: str | None = None


class QueryResult(BaseModel):
    title: str
    source: str
    content: str
    chunk_index: int
    score: float


class IngestRequest(BaseModel):
    title: str
    content: str
    source: str
    metadata: dict = {}


class IngestResponse(BaseModel):
    chunks_created: int


@router.post("/query", response_model=list[QueryResult])
async def query_rag(request: QueryRequest, db: AsyncSession = Depends(get_db)):
    chunks = await rag_service.retrieve(
        db=db,
        query=request.query,
        top_k=request.top_k,
        source_filter=request.source,
    )
    return [
        QueryResult(
            title=c.title,
            source=c.source,
            content=c.content,
            chunk_index=c.chunk_index,
            score=c.score,
        )
        for c in chunks
    ]


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest, db: AsyncSession = Depends(get_db)):
    count = await rag_service.ingest(
        db=db,
        title=request.title,
        content=request.content,
        source=request.source,
        metadata=request.metadata,
    )
    return IngestResponse(chunks_created=count)
