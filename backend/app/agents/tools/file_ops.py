"""
File operations tool for agents.

Provides read/write access to a sandboxed workspace directory.
Agents cannot access files outside the workspace.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Agents can only access files within this directory
WORKSPACE_DIR = Path("data/agent_workspace")


def _safe_path(filename: str) -> Path | None:
    """Resolve a filename to a safe path within the workspace."""
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    resolved = (WORKSPACE_DIR / filename).resolve()
    workspace_resolved = WORKSPACE_DIR.resolve()

    # Prevent path traversal
    if not str(resolved).startswith(str(workspace_resolved)):
        return None
    return resolved


async def read_file(filename: str) -> str:
    """Read a file from the agent workspace."""
    path = _safe_path(filename)
    if path is None:
        return "Error: Invalid file path (path traversal detected)."
    if not path.exists():
        return f"Error: File '{filename}' not found in workspace."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def write_file(filename: str, content: str) -> str:
    """Write a file to the agent workspace."""
    path = _safe_path(filename)
    if path is None:
        return "Error: Invalid file path (path traversal detected)."
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} characters to '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"


async def list_files(directory: str = ".") -> str:
    """List files in the agent workspace."""
    path = _safe_path(directory)
    if path is None:
        return "Error: Invalid directory path."
    if not path.exists():
        return f"Directory '{directory}' does not exist."
    try:
        files = sorted(p.relative_to(WORKSPACE_DIR) for p in path.rglob("*") if p.is_file())
        if not files:
            return "No files in workspace."
        return "\n".join(str(f) for f in files[:50])
    except Exception as e:
        return f"Error listing files: {str(e)}"


READ_FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "filename": {
            "type": "string",
            "description": "Path to the file relative to the agent workspace",
        },
    },
    "required": ["filename"],
}

WRITE_FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "filename": {
            "type": "string",
            "description": "Path to the file relative to the agent workspace",
        },
        "content": {
            "type": "string",
            "description": "Content to write to the file",
        },
    },
    "required": ["filename", "content"],
}

LIST_FILES_SCHEMA = {
    "type": "object",
    "properties": {
        "directory": {
            "type": "string",
            "description": "Directory to list (relative to workspace, default: root)",
            "default": ".",
        },
    },
}
