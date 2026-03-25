"""
HR Memory Service: manages user context in Postgres + pgvector.

Handles user profile lookup, context updates, and embedding-based
similarity search for finding related user contexts.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_context import UserContext
from app.utils.embeddings import EmbeddingService


class HRMemoryService:
    def __init__(self):
        self.embedder = EmbeddingService.get_instance()

    async def get_or_create(self, db: AsyncSession, user_id: str) -> UserContext:
        """Get existing user context or create a new one."""
        result = await db.execute(
            select(UserContext).where(UserContext.user_id == user_id)
        )
        user_ctx = result.scalar_one_or_none()

        if user_ctx is None:
            user_ctx = UserContext(
                id=uuid.uuid4(),
                user_id=user_id,
                display_name="",
                preferences={},
                summary="New user. No interaction history yet.",
            )
            # Embed the initial summary
            user_ctx.embedding = self.embedder.embed_single(user_ctx.summary)
            db.add(user_ctx)
            await db.commit()
            await db.refresh(user_ctx)

        return user_ctx

    async def update_context(
        self,
        db: AsyncSession,
        user_id: str,
        new_message: str,
        agent_summary: str | None = None,
    ) -> UserContext:
        """
        Update user context with new interaction data.

        Appends interaction info to the summary and re-embeds.
        """
        user_ctx = await self.get_or_create(db, user_id)

        # Build updated summary
        addition = f"\nRecent query: {new_message[:200]}"
        if agent_summary:
            addition += f"\nOutcome: {agent_summary[:200]}"

        # Keep summary under 2000 chars by trimming oldest content
        new_summary = user_ctx.summary + addition
        if len(new_summary) > 2000:
            # Keep the last 1800 chars to leave room
            new_summary = "..." + new_summary[-1800:]

        user_ctx.summary = new_summary
        user_ctx.embedding = self.embedder.embed_single(new_summary)

        await db.commit()
        await db.refresh(user_ctx)
        return user_ctx

    async def update_preferences(
        self,
        db: AsyncSession,
        user_id: str,
        preferences: dict,
    ) -> UserContext:
        """Update user preferences (merge with existing)."""
        user_ctx = await self.get_or_create(db, user_id)
        user_ctx.preferences = {**user_ctx.preferences, **preferences}
        await db.commit()
        await db.refresh(user_ctx)
        return user_ctx

    async def get_context_summary(self, db: AsyncSession, user_id: str) -> str:
        """Get a formatted summary of user context for the orchestrator."""
        user_ctx = await self.get_or_create(db, user_id)
        parts = [f"User ID: {user_ctx.user_id}"]
        if user_ctx.display_name:
            parts.append(f"Name: {user_ctx.display_name}")
        if user_ctx.preferences:
            parts.append(f"Preferences: {user_ctx.preferences}")
        parts.append(f"History: {user_ctx.summary}")
        return "\n".join(parts)
