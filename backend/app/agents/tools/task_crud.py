"""
Task CRUD tool for the Secretary agent.

Allows the Secretary to create, update, and query tasks
directly from the database.
"""

import uuid

from sqlalchemy import select

from app.models.task import Task


async def create_task(
    session_id: str,
    title: str,
    description: str = "",
    assigned_agent: str = "unassigned",
) -> str:
    """Create a new task in the tracking system."""
    from app.database import async_session

    async with async_session() as db:
        task = Task(
            id=uuid.uuid4(),
            session_id=session_id,
            title=title,
            description=description,
            assigned_agent=assigned_agent,
        )
        db.add(task)
        await db.commit()
        return f"Task created: '{title}' (assigned to: {assigned_agent}, status: pending)"


async def update_task_status(task_title: str, status: str, result: str = "") -> str:
    """Update the status of a task by title."""
    from app.database import async_session

    valid_statuses = ["pending", "in_progress", "completed", "rejected"]
    if status not in valid_statuses:
        return f"Invalid status. Must be one of: {valid_statuses}"

    async with async_session() as db:
        stmt = select(Task).where(Task.title.ilike(f"%{task_title}%")).limit(1)
        res = await db.execute(stmt)
        task = res.scalar_one_or_none()

        if not task:
            return f"No task found matching: '{task_title}'"

        task.status = status
        if result:
            task.result = result
        await db.commit()
        return f"Task '{task.title}' updated to status: {status}"


async def list_tasks(
    session_id: str = "",
    status: str = "",
    assigned_agent: str = "",
) -> str:
    """List tasks with optional filters."""
    from app.database import async_session

    async with async_session() as db:
        stmt = select(Task).order_by(Task.created_at.desc()).limit(20)
        if session_id:
            stmt = stmt.where(Task.session_id == session_id)
        if status:
            stmt = stmt.where(Task.status == status)
        if assigned_agent:
            stmt = stmt.where(Task.assigned_agent == assigned_agent)

        res = await db.execute(stmt)
        tasks = res.scalars().all()

        if not tasks:
            return "No tasks found."

        lines = []
        for t in tasks:
            lines.append(
                f"- [{t.status.upper()}] {t.title} "
                f"(assigned: {t.assigned_agent}, session: {t.session_id[:8]}...)"
            )
        return "\n".join(lines)


CREATE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "session_id": {
            "type": "string",
            "description": "Session ID this task belongs to",
        },
        "title": {
            "type": "string",
            "description": "Title of the task",
        },
        "description": {
            "type": "string",
            "description": "Detailed description of the task",
            "default": "",
        },
        "assigned_agent": {
            "type": "string",
            "description": "Agent assigned to this task",
            "default": "unassigned",
        },
    },
    "required": ["session_id", "title"],
}

UPDATE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_title": {
            "type": "string",
            "description": "Title (or partial match) of the task to update",
        },
        "status": {
            "type": "string",
            "description": "New status: pending, in_progress, completed, or rejected",
            "enum": ["pending", "in_progress", "completed", "rejected"],
        },
        "result": {
            "type": "string",
            "description": "Result or notes about the task completion",
            "default": "",
        },
    },
    "required": ["task_title", "status"],
}

LIST_TASKS_SCHEMA = {
    "type": "object",
    "properties": {
        "session_id": {
            "type": "string",
            "description": "Filter by session ID",
            "default": "",
        },
        "status": {
            "type": "string",
            "description": "Filter by status",
            "default": "",
        },
        "assigned_agent": {
            "type": "string",
            "description": "Filter by assigned agent",
            "default": "",
        },
    },
}
