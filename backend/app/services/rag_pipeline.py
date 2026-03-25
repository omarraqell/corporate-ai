import uuid
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.utils.embeddings import EmbeddingService


@dataclass
class RetrievedChunk:
    id: uuid.UUID
    source: str
    title: str
    content: str
    chunk_index: int
    score: float


class RAGService:
    def __init__(self):
        self.embedder = EmbeddingService.get_instance()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,       # ~500 tokens
            chunk_overlap=200,     # ~50 tokens
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        top_k: int = 5,
        source_filter: str | None = None,
    ) -> list[RetrievedChunk]:
        query_embedding = self.embedder.embed_single(query)

        # pgvector cosine distance (lower = more similar)
        distance_expr = Document.embedding.cosine_distance(query_embedding)

        stmt = (
            select(Document, distance_expr.label("distance"))
            .where(Document.embedding.isnot(None))
            .order_by(distance_expr)
            .limit(top_k)
        )

        if source_filter:
            stmt = stmt.where(Document.source == source_filter)

        result = await db.execute(stmt)
        rows = result.all()

        return [
            RetrievedChunk(
                id=doc.id,
                source=doc.source,
                title=doc.title,
                content=doc.content,
                chunk_index=doc.chunk_index,
                score=1.0 - distance,  # convert distance to similarity
            )
            for doc, distance in rows
        ]

    async def ingest(
        self,
        db: AsyncSession,
        title: str,
        content: str,
        source: str,
        metadata: dict | None = None,
    ) -> int:
        """Chunk, embed, and store a document. Returns number of chunks created."""
        chunks = self.splitter.split_text(content)
        embeddings = self.embedder.embed(chunks)

        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            doc = Document(
                id=uuid.uuid4(),
                source=source,
                title=title,
                content=chunk_text,
                chunk_index=i,
                embedding=embedding,
                metadata_=metadata or {},
            )
            db.add(doc)

        await db.commit()
        return len(chunks)

    async def delete_by_source(self, db: AsyncSession, source: str) -> int:
        """Delete all documents of a given source type. Returns count deleted."""
        result = await db.execute(
            select(Document).where(Document.source == source)
        )
        docs = result.scalars().all()
        for doc in docs:
            await db.delete(doc)
        await db.commit()
        return len(docs)
