"""Code execution bridge for TypeScript and Python.

Provides safe code execution capabilities for quality analysis tools.
Uses shell wrappers for actual execution to maintain security boundaries.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Sequence
from pathlib import Path
from typing import final

from flext_quality import c, e, m, p, r, t


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
        """Initialize the code execution bridge.

        Args:
            timeout_ms: Optional execution timeout in milliseconds; defaults
                to the configured integration timeout.
            working_dir: Optional working directory for executions; defaults
                to the current directory.

        """
        self._timeout_ms = timeout_ms or c.Quality.INTEGRATION_TIMEOUT_MS
        self._working_dir = working_dir or Path.cwd()

    @staticmethod
    def build_basedpyright_command(target_path: Path) -> p.Result[Sequence[str]]:
        """Build command for basedpyright type checker.

        Args:
            target_path: Path checked by basedpyright.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        cmd = ["basedpyright", "--outputjson", str(target_path.resolve())]
        return r[Sequence[str]].ok(cmd)

    @staticmethod
    def build_python_command(
        script_path: Path,
        *,
        args: Sequence[str] | None = None,
    ) -> p.Result[Sequence[str]]:
        """Build command for Python execution.

        Args:
            script_path: Path of the Python script to execute.
            args: Optional arguments appended to the command.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        if not script_path.exists():
            return e.fail_not_found(
                "Script",
                str(script_path),
                result_type=r[Sequence[str]],
            )
        cmd = ["python", str(script_path)]
        if args:
            cmd.extend(args)
        return r[Sequence[str]].ok(cmd)

    @staticmethod
    def build_ruff_command(
        target_path: Path,
        *,
        fix: bool = False,
        output_format: str = "json",
    ) -> p.Result[Sequence[str]]:
        """Build command for ruff linter.

        Args:
            target_path: Path checked by ruff.
            fix: Whether ruff applies its fixes.
            output_format: Output format requested from ruff.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        cmd = ["ruff", "check", str(target_path), f"--output-format={output_format}"]
        if fix:
            cmd.append("--fix")
        return r[Sequence[str]].ok(cmd)

    @staticmethod
    def build_typescript_command(
        script_path: Path,
        *,
        args: Sequence[str] | None = None,
    ) -> p.Result[Sequence[str]]:
        """Build command for TypeScript execution via npx tsx.

        Args:
            script_path: Path of the TypeScript script to execute.
            args: Optional arguments appended to the command.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        if not script_path.exists():
            return e.fail_not_found(
                "Script",
                str(script_path),
                result_type=r[Sequence[str]],
            )
        cmd = ["npx", "tsx", str(script_path)]
        if args:
            cmd.extend(args)
        return r[Sequence[str]].ok(cmd)

    def create_execution_request(
        self,
        script_path: Path,
        runtime: str,
        *,
        args: Sequence[str] | None = None,
    ) -> p.Result[m.Quality.ExecutionRequest]:
        """Create an execution request for later processing.

        Args:
            script_path: Path of the script to execute.
            runtime: Runtime identifier (``python``, ``typescript``, ``ruff``,
                or ``basedpyright``).
            args: Optional arguments appended to the request.

        Returns:
            The resulting ``p.Result[m.Quality.ExecutionRequest]``.

        """
        if runtime not in {"python", "typescript", "ruff", "basedpyright"}:
            return r[m.Quality.ExecutionRequest].fail(f"Unknown runtime: {runtime}")
        return r[m.Quality.ExecutionRequest].ok(
            m.Quality.ExecutionRequest(
                script_path=script_path,
                runtime=runtime,
                args=args or [],
                timeout_ms=self._timeout_ms,
            ),
        )

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check availability of execution runtimes.

        Returns configuration status - actual runtime checks
        should be done via shell wrapper execution.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return r[t.JsonMapping].ok({
            "status": c.Quality.IntegrationStatus.CONNECTED,
            "available": True,
            "working_dir": str(self._working_dir),
            "timeout_ms": self._timeout_ms,
            "supported_runtimes": ["python", "typescript", "ruff", "basedpyright"],
        })


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityCodeExecutionBridge"]
