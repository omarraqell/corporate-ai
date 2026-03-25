"""Initial schema with pgvector

Revision ID: 001
Revises:
Create Date: 2026-03-23
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # user_context (HR Memory)
    op.create_table(
        "user_context",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("display_name", sa.String(255), server_default=""),
        sa.Column("preferences", sa.JSON(), server_default="{}"),
        sa.Column("summary", sa.Text(), server_default=""),
        sa.Column("embedding", Vector(384), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # conversation_history
    op.create_table(
        "conversation_history",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.String(255), index=True, nullable=False),
        sa.Column("session_id", sa.String(255), index=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("agent_name", sa.String(100), nullable=True),
        sa.Column("metadata", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # tasks
    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("session_id", sa.String(255), index=True, nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("assigned_agent", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("parent_task_id", sa.Uuid(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # rag_documents
    op.create_table(
        "rag_documents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source", sa.String(50), index=True, nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), server_default="0"),
        sa.Column("embedding", Vector(384), nullable=True),
        sa.Column("metadata", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("rag_documents")
    op.drop_table("tasks")
    op.drop_table("conversation_history")
    op.drop_table("user_context")
    op.execute("DROP EXTENSION IF EXISTS vector")
