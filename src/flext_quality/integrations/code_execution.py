"""Code execution bridge for TypeScript and Python.

Provides safe code execution capabilities for quality analysis tools.
Uses shell wrappers for actual execution to maintain security boundaries.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

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
        """Initialize the code execution bridge."""
        self._timeout_ms = timeout_ms or c.Quality.INTEGRATION_TIMEOUT_MS
        self._working_dir = working_dir or Path.cwd()

    def build_basedpyright_command(self, target_path: Path) -> p.Result[t.StrSequence]:
        """Build command for basedpyright type checker."""
        cmd = ["basedpyright", "--outputjson", str(target_path.resolve())]
        return r[t.StrSequence].ok(cmd)

    def build_python_command(
        self,
        script_path: Path,
        *,
        args: t.StrSequence | None = None,
    ) -> p.Result[t.StrSequence]:
        """Build command for Python execution."""
        if not script_path.exists():
            return e.fail_not_found("Script", str(script_path), result_type=r[t.StrSequence])
        cmd = ["python", str(script_path)]
        if args:
            cmd.extend(args)
        return r[t.StrSequence].ok(cmd)

    def build_ruff_command(
        self,
        target_path: Path,
        *,
        fix: bool = False,
        output_format: str = "json",
    ) -> p.Result[t.StrSequence]:
        """Build command for ruff linter."""
        cmd = ["ruff", "check", str(target_path), f"--output-format={output_format}"]
        if fix:
            cmd.append("--fix")
        return r[t.StrSequence].ok(cmd)

    def build_typescript_command(
        self,
        script_path: Path,
        *,
        args: t.StrSequence | None = None,
    ) -> p.Result[t.StrSequence]:
        """Build command for TypeScript execution via npx tsx."""
        if not script_path.exists():
            return e.fail_not_found("Script", str(script_path), result_type=r[t.StrSequence])
        cmd = ["npx", "tsx", str(script_path)]
        if args:
            cmd.extend(args)
        return r[t.StrSequence].ok(cmd)

    def create_execution_request(
        self,
        script_path: Path,
        runtime: str,
        *,
        args: t.StrSequence | None = None,
    ) -> p.Result[m.Quality.ExecutionRequest]:
        """Create an execution request for later processing."""
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
        """
        return r[t.JsonMapping].ok({
            "status": c.Quality.IntegrationStatus.CONNECTED,
            "available": True,
            "working_dir": str(self._working_dir),
            "timeout_ms": self._timeout_ms,
            "supported_runtimes": ["python", "typescript", "ruff", "basedpyright"],
        })
