"""MyPy Plugin - MyPy strict mode validation integration.

Provides type checking operations using mypy.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

from ..fix_engine.constants import FlextFixEngineConstants as c


class FlextMyPyPlugin(FlextService[int]):
    """MyPy strict mode validation integration.

    Provides unified interface for mypy type checking.

    Usage:
        from flext_quality.plugins import FlextMyPyPlugin

        mypy = FlextMyPyPlugin()
        result = mypy.check([Path("file.py")])
        if result.is_success:
            error_count = result.value.error_count
    """

    __slots__ = ("_logger", "_strict")

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Result of mypy check operation."""

        error_count: int
        files_checked: int
        errors: tuple[str, ...] = field(default_factory=tuple)

    @dataclass(frozen=True, slots=True)
    class Error:
        """Single mypy error."""

        file_path: Path
        line: int
        column: int
        severity: str
        code: str
        message: str

    def __init__(
        self: Self,
        strict: bool = True,
    ) -> None:
        """Initialize mypy plugin.

        Args:
            strict: Use strict mode. Defaults to True.

        """
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._strict = strict

    def execute(self: Self) -> FlextResult[int]:
        """Satisfy FlextService contract."""
        return FlextResult[int].fail("Use check() or get_errors() methods")

    def check(
        self: Self,
        files: list[Path],
    ) -> FlextResult[CheckResult]:
        """Check files with mypy.

        Args:
            files: Files to check.

        Returns:
            Check result with error count.

        """
        if not files:
            return FlextResult[FlextMyPyPlugin.CheckResult].ok(
                FlextMyPyPlugin.CheckResult(
                    error_count=0,
                    files_checked=0,
                )
            )

        file_paths = [str(f) for f in files]

        cmd = ["mypy", "--no-error-summary"]
        if self._strict:
            cmd.append("--strict")
        cmd.extend(file_paths)

        try:
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Validation.MYPY_TIMEOUT_SECONDS,
            )

            # Parse errors from output
            error_lines = [
                ln for ln in result.stdout.split("\n") if "error:" in ln
            ]

            check_result = FlextMyPyPlugin.CheckResult(
                error_count=len(error_lines),
                files_checked=len(files),
                errors=tuple(error_lines),
            )

            self._logger.debug(
                "MyPy check: %d errors in %d files",
                check_result.error_count,
                check_result.files_checked,
            )

            return FlextResult[FlextMyPyPlugin.CheckResult].ok(check_result)

        except (subprocess.TimeoutExpired, FileNotFoundError) as err:
            return FlextResult[FlextMyPyPlugin.CheckResult].fail(
                f"MyPy check failed: {err}"
            )

    def get_errors(
        self: Self,
        files: list[Path],
    ) -> FlextResult[list[Error]]:
        """Get detailed error list for files.

        Args:
            files: Files to check.

        Returns:
            List of parsed errors.

        """
        check_result = self.check(files)
        if check_result.is_failure:
            return FlextResult[list[FlextMyPyPlugin.Error]].fail(
                check_result.error or "Check failed"
            )

        result = check_result.value
        errors: list[FlextMyPyPlugin.Error] = []

        for error_line in result.errors:
            parsed = self._parse_error_line(error_line)
            if parsed:
                errors.append(parsed)

        return FlextResult[list[FlextMyPyPlugin.Error]].ok(errors)

    def _parse_error_line(
        self: Self,
        line: str,
    ) -> Error | None:
        """Parse a mypy error line.

        Args:
            line: Error line from mypy output.

        Returns:
            Parsed error or None if parsing fails.

        """
        # Format: file.py:line:col: severity: message [code]
        parts = line.split(":", c.Parser.MYPY_SPLIT_PARTS)
        if len(parts) < c.Parser.MYPY_SPLIT_PARTS:
            return None

        try:
            file_path = Path(parts[0])
            line_num = int(parts[1])
            col_num = int(parts[2]) if len(parts) > c.Parser.MYPY_MIN_PARTS else 0
            rest = parts[c.Parser.MYPY_MIN_PARTS].strip() if len(parts) > c.Parser.MYPY_MIN_PARTS else ""

            # Parse severity and message
            if ": " in rest:
                severity, message = rest.split(": ", 1)
            else:
                severity = "error"
                message = rest

            # Extract code from message
            code = ""
            if "[" in message and "]" in message:
                code = message[message.rfind("[") + 1 : message.rfind("]")]

            return FlextMyPyPlugin.Error(
                file_path=file_path,
                line=line_num,
                column=col_num,
                severity=severity.strip(),
                code=code,
                message=message.strip(),
            )

        except (ValueError, IndexError):
            return None


__all__ = ["FlextMyPyPlugin"]
