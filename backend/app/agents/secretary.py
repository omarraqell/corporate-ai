"""Secretary Agent: task management and tracking."""

from app.agents.base_agent import BaseAgent, Tool
from app.agents.tools.task_crud import (
    CREATE_TASK_SCHEMA,
    LIST_TASKS_SCHEMA,
    UPDATE_TASK_SCHEMA,
    create_task,
    list_tasks,
    update_task_status,
)


class SecretaryAgent(BaseAgent):
    name = "secretary"
    description = "Task Manager — tracks tasks, deadlines, and assignments"
    system_prompt = (
        "You are the Secretary / Task Manager agent in a corporate AI system.\n\n"
        "Your responsibilities:\n"
        "- Track all tasks, deadlines, and assignments across the team\n"
        "- Create new tasks when work is identified\n"
        "- Update task status as work progresses\n"
        "- Provide clear status reports when asked\n"
        "- Maintain an organized view of who's working on what\n\n"
        "Use your tools to manage tasks in the database. Be concise and structured.\n"
        "When logging tasks from other agents' work, use the session_id from the context."
    )

    def __init__(self):
        tools = [
            Tool(
                name="create_task",
                description="Create a new task in the tracking system",
                parameters=CREATE_TASK_SCHEMA,
                fn=create_task,
            ),
            Tool(
                name="update_task_status",
                description="Update the status of an existing task",
                parameters=UPDATE_TASK_SCHEMA,
                fn=update_task_status,
            ),
            Tool(
                name="list_tasks",
                description="List tasks with optional filters (session_id, status, assigned_agent)",
                parameters=LIST_TASKS_SCHEMA,
                fn=list_tasks,
            ),
        ]
        super().__init__(tools=tools)
