"""
Seed the RAG vector store with synthetic documents.

Reads documents from data/synthetic_docs/, chunks them, embeds them,
and stores them in the rag_documents table.

Run: python -m scripts.seed_rag
Use --if-empty to skip if documents already exist.
"""

import asyncio
import sys
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.document import Document
from app.services.rag_pipeline import RAGService

DATA_DIR = Path("data/synthetic_docs")

# Map directory names to source types
SOURCE_MAP = {
    "sop": "sop",
    "routing_rule": "routing_rule",
    "company_doc": "company_doc",
}

# Map directory names to titles (extracted from filename)
def filename_to_title(filename: str) -> str:
    return filename.replace("_", " ").replace("-", " ").removesuffix(".md")


async def seed(if_empty: bool = False):
    engine = create_async_engine(settings.database_url)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as db:
        # Check if already seeded
        if if_empty:
            result = await db.execute(select(func.count(Document.id)))
            count = result.scalar()
            if count and count > 0:
                print(f"RAG store already has {count} chunks. Skipping seed (--if-empty).")
                await engine.dispose()
                return

        rag = RAGService()
        total_chunks = 0

        for dir_name, source_type in SOURCE_MAP.items():
            source_dir = DATA_DIR / dir_name
            if not source_dir.exists():
                print(f"Warning: {source_dir} not found. Skipping {source_type}.")
                continue

            files = sorted(source_dir.glob("*.md"))
            print(f"\nIngesting {len(files)} {source_type} documents...")

            for file_path in files:
                content = file_path.read_text(encoding="utf-8")
                title = filename_to_title(file_path.name)

                chunks_created = await rag.ingest(
                    db=db,
                    title=title,
                    content=content,
                    source=source_type,
                    metadata={"file": file_path.name},
                )
                total_chunks += chunks_created
                print(f"  {title}: {chunks_created} chunks")

        print(f"\nDone. Total chunks ingested: {total_chunks}")

    await engine.dispose()


if __name__ == "__main__":
    if_empty = "--if-empty" in sys.argv
    asyncio.run(seed(if_empty=if_empty))
