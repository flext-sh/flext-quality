"""Subprocess utilities for running external commands safely.

This module provides a type-safe subprocess wrapper that integrates
with FlextResult for railway-oriented error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path

from flext_core import FlextResult


@dataclass(frozen=True)
class CommandOutput:
    """Result of running an external command."""

    stdout: str
    stderr: str
    returncode: int


class SubprocessUtils:
    """Utilities for running external commands with timeout and error handling."""

    @staticmethod
    def run_external_command(
        command: list[str],
        *,
        capture_output: bool = True,
        timeout: float = 30.0,
        cwd: Path | str | None = None,
        env: dict[str, str] | None = None,
        check: bool = False,
    ) -> FlextResult[CommandOutput]:
        """Run an external command with timeout support.

        Uses threading-based timeout for reliable cancellation.

        Args:
            command: Command and arguments as list.
            capture_output: Whether to capture stdout/stderr.
            timeout: Maximum execution time in seconds.
            cwd: Working directory for command execution.
            env: Environment variables for the command.
            check: Unused, kept for API compatibility.

        Returns:
            FlextResult containing CommandOutput on success.

        """
        _ = check  # Unused - we always use check=False internally
        if not command or any(not arg or not arg.strip() for arg in command):
            return FlextResult[CommandOutput].fail(
                "Command must contain non-empty arguments",
            )

        result_holder: list[CommandOutput | None] = [None]
        error_holder: list[str | None] = [None]
        cwd_path = Path(cwd) if cwd else None
        safe_command = [str(arg) for arg in command]

        def run_command() -> None:
            try:
                # Command is a list[str] from internal code, not user input - safe to execute
                proc = subprocess.run(
                    safe_command,
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout,
                    cwd=cwd_path,
                    env=env,
                    check=False,
                    shell=False,
                )
                result_holder[0] = CommandOutput(
                    stdout=proc.stdout or "",
                    stderr=proc.stderr or "",
                    returncode=proc.returncode,
                )
            except FileNotFoundError:
                error_holder[0] = f"Command not found: {command[0]}"
            except subprocess.TimeoutExpired:
                error_holder[0] = f"Command timed out after {timeout}s"
            except Exception as e:
                error_holder[0] = f"Command execution failed: {e}"

        thread = threading.Thread(target=run_command)
        thread.start()
        thread.join(timeout=timeout + 1)

        if thread.is_alive():
            return FlextResult[CommandOutput].fail(
                f"Command timed out after {timeout}s",
            )

        if error_holder[0]:
            return FlextResult[CommandOutput].fail(error_holder[0])

        if result_holder[0] is None:
            return FlextResult[CommandOutput].fail("No result from command execution")

        return FlextResult[CommandOutput].ok(result_holder[0])


# Module-level alias for convenience
run_external_command = SubprocessUtils.run_external_command


__all__ = [
    "CommandOutput",
    "SubprocessUtils",
    "run_external_command",
]
