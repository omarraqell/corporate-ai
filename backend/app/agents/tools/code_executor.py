"""
Sandboxed code execution tool for agents.

Executes Python code in a restricted subprocess.
For production, use a proper sandbox (Docker container, E2B, etc.)
"""

import asyncio
import logging
import sys

logger = logging.getLogger(__name__)

MAX_EXECUTION_TIME = 30  # seconds
MAX_OUTPUT_LENGTH = 5000  # characters


async def execute_python(code: str) -> str:
    """
    Execute Python code in a subprocess and return the output.

    Security: This runs code with the same permissions as the backend.
    For production, use a sandboxed execution environment.
    """
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, "-c", code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=MAX_EXECUTION_TIME,
            )
        except asyncio.TimeoutError:
            process.kill()
            return f"Error: Code execution timed out after {MAX_EXECUTION_TIME} seconds."

        output = ""
        if stdout:
            output += stdout.decode("utf-8", errors="replace")
        if stderr:
            output += "\nSTDERR:\n" + stderr.decode("utf-8", errors="replace")

        if not output.strip():
            output = "(No output produced)"

        # Truncate if too long
        if len(output) > MAX_OUTPUT_LENGTH:
            output = output[:MAX_OUTPUT_LENGTH] + "\n... (output truncated)"

        return output

    except Exception as e:
        logger.error(f"Code execution failed: {e}")
        return f"Error executing code: {str(e)}"


EXECUTE_PYTHON_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "Python code to execute. Must be a complete, runnable script.",
        },
    },
    "required": ["code"],
}
