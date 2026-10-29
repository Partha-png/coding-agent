
"""Execute agent-generated shell commands inside Docker Sandbox."""

import os
import shutil
import subprocess
from pathlib import Path


# sandbox.py is inside agent/, so the project root is its parent directory.
PROJECT = Path(__file__).resolve().parent.parent

# This must match the sandbox you created from Windows PowerShell.
SANDBOX_NAME = os.environ.get(
    "CODING_AGENT_SANDBOX",
    "coding-agent-dev",
)


def _find_sbx():
    """Find the Docker Sandbox CLI accessible from this environment."""
    for executable_name in ("sbx.exe", "sbx"):
        executable_path = shutil.which(executable_name)

        if executable_path:
            return executable_path

    raise RuntimeError(
        "Docker Sandbox CLI was not found. "
        "From WSL, verify that `sbx.exe ls` works."
    )


def name():
    """Return the execution backend name."""
    return f"docker-sandbox ({SANDBOX_NAME})"


def run(command, timeout=60):
    """Run a shell command inside Docker Sandbox.

    Returns subprocess.CompletedProcess, including stdout, stderr,
    and the exit code. Never falls back to host shell execution.
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command must be a non-empty string")

    executable = _find_sbx()

    sandbox_command = [
        executable,
        "exec",
        SANDBOX_NAME,
        "bash",
        "-lc",
        command,
    ]

    return subprocess.run(
        sandbox_command,
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
