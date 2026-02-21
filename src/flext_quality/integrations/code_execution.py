"""Code execution bridge for TypeScript and Python.

Provides safe code execution capabilities for quality analysis tools.
Uses shell wrappers for actual execution to maintain security boundaries.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import final

from flext_core import r

from flext_quality.constants import FlextQualityConstants as c


@dataclass(frozen=True)
class ExecutionRequest:
    """Request for code execution."""

    script_path: Path
    runtime: str
    args: list[str]
    timeout_ms: int


@dataclass(frozen=True)
class ExecutionResult:
    """Result of code execution."""

    runtime: str
    exit_code: int
    output: str
    parsed: dict[str, object] | None


@final
class FlextQualityCodeExecutionBridge:
    """Bridge for executing code analysis in TypeScript or Python.

    This class provides a high-level interface for code execution.
    Actual subprocess execution is delegated to shell wrappers
    to maintain security boundaries.
    """

    def __init__(
        self,
        *,
        timeout_ms: int | None = None,
        working_dir: Path | None = None,
    ) -> None:
        """Initialize the code execution bridge."""
        self._timeout_ms = timeout_ms or c.Quality.Defaults.INTEGRATION_TIMEOUT_MS
        self._working_dir = working_dir or Path.cwd()

    def build_typescript_command(
        self,
        script_path: Path,
        *,
        args: list[str] | None = None,
    ) -> r[list[str]]:
        """Build command for TypeScript execution via npx tsx."""
        if not script_path.exists():
            return r[list[str]].fail(f"Script not found: {script_path}")

        cmd = ["npx", "tsx", str(script_path)]
        if args:
            cmd.extend(args)

        return r[list[str]].ok(cmd)

    def build_python_command(
        self,
        script_path: Path,
        *,
        args: list[str] | None = None,
    ) -> r[list[str]]:
        """Build command for Python execution."""
        if not script_path.exists():
            return r[list[str]].fail(f"Script not found: {script_path}")

        cmd = ["python", str(script_path)]
        if args:
            cmd.extend(args)

        return r[list[str]].ok(cmd)

    def build_ruff_command(
        self,
        target_path: Path,
        *,
        fix: bool = False,
        output_format: str = "json",
    ) -> r[list[str]]:
        """Build command for ruff linter."""
        cmd = ["ruff", "check", str(target_path), f"--output-format={output_format}"]
        if fix:
            cmd.append("--fix")

        return r[list[str]].ok(cmd)

    def build_basedpyright_command(
        self,
        target_path: Path,
    ) -> r[list[str]]:
        """Build command for basedpyright type checker."""
        cmd = ["basedpyright", "--outputjson", str(target_path.resolve())]
        return r[list[str]].ok(cmd)

    def create_execution_request(
        self,
        script_path: Path,
        runtime: str,
        *,
        args: list[str] | None = None,
    ) -> r[ExecutionRequest]:
        """Create an execution request for later processing."""
        if runtime not in {"python", "typescript", "ruff", "basedpyright"}:
            return r[ExecutionRequest].fail(f"Unknown runtime: {runtime}")

        return r[ExecutionRequest].ok(
            ExecutionRequest(
                script_path=script_path,
                runtime=runtime,
                args=args or [],
                timeout_ms=self._timeout_ms,
            )
        )

    def health_check(self) -> r[dict[str, object]]:
        """Check availability of execution runtimes.

        Returns configuration status - actual runtime checks
        should be done via shell wrapper execution.
        """
        return r[dict[str, object]].ok({
            "status": c.Quality.IntegrationStatus.CONNECTED,
            "available": True,
            "working_dir": str(self._working_dir),
            "timeout_ms": self._timeout_ms,
            "supported_runtimes": [
                "python",
                "typescript",
                "ruff",
                "basedpyright",
            ],
        })
