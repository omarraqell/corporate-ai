from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB pool, load BERT model, etc.
    # These will be wired in later phases
    yield
    # Shutdown: cleanup


def create_app() -> FastAPI:
    app = FastAPI(
        title="Corporate AI System",
        description="Multi-Agent Corporate AI Orchestration API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    from app.routers import chat, rag, receptionist, tasks
    app.include_router(chat.router, prefix="/api")
    app.include_router(rag.router, prefix="/api")
    app.include_router(receptionist.router, prefix="/api")
    app.include_router(tasks.router, prefix="/api")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
