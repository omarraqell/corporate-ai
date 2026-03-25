"""Code Dev Agent: software development and automation."""

from app.agents.base_agent import BaseAgent, Tool
from app.agents.tools.code_executor import EXECUTE_PYTHON_SCHEMA, execute_python
from app.agents.tools.file_ops import (
    LIST_FILES_SCHEMA,
    READ_FILE_SCHEMA,
    WRITE_FILE_SCHEMA,
    list_files,
    read_file,
    write_file,
)


class CodeDevAgent(BaseAgent):
    name = "code_dev"
    description = "Code Dev — writes, reviews, and debugs code"
    system_prompt = (
        "You are the Code Dev agent in a corporate AI system.\n\n"
        "Your responsibilities:\n"
        "- Write clean, well-documented code\n"
        "- Debug and fix issues\n"
        "- Build scripts, tools, and automations\n"
        "- Review code for quality and security\n"
        "- Execute code to verify it works\n\n"
        "Coding standards:\n"
        "- Follow language-specific best practices\n"
        "- Include error handling\n"
        "- Add comments for non-obvious logic\n"
        "- Write testable, modular code\n"
        "- Never include hardcoded secrets or credentials\n\n"
        "You can write files to the agent workspace and execute Python code. "
        "Always test your code by executing it before returning results.\n\n"
        "If the code needs documentation, mention that the Writer should handle it."
    )

    def __init__(self):
        tools = [
            Tool(
                name="execute_python",
                description="Execute Python code to test or run scripts",
                parameters=EXECUTE_PYTHON_SCHEMA,
                fn=execute_python,
            ),
            Tool(
                name="read_file",
                description="Read a file from the agent workspace",
                parameters=READ_FILE_SCHEMA,
                fn=read_file,
            ),
            Tool(
                name="write_file",
                description="Write a file to the agent workspace",
                parameters=WRITE_FILE_SCHEMA,
                fn=write_file,
            ),
            Tool(
                name="list_files",
                description="List files in the agent workspace",
                parameters=LIST_FILES_SCHEMA,
                fn=list_files,
            ),
        ]
        super().__init__(tools=tools)
