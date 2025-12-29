"""Ruff Plugin - Ruff linting and auto-fix integration.

Provides check, fix, and format operations using ruff.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

from ..fix_engine.constants import FlextFixEngineConstants as c


class FlextRuffPlugin(FlextService[int]):
    """Ruff linting and auto-fix integration.

    Provides unified interface for ruff check, fix, and format operations.

    Usage:
        from flext_quality.plugins import FlextRuffPlugin

        ruff = FlextRuffPlugin()
        result = ruff.check([Path("file.py")])
        if result.is_success:
            issues = result.value.error_count
    """

    __slots__ = ("_logger",)

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Result of ruff check operation."""

        error_count: int
        files_checked: int
        violations: tuple[dict[str, object], ...] = field(default_factory=tuple)

    @dataclass(frozen=True, slots=True)
    class FixResult:
        """Result of ruff fix operation."""

        files_fixed: int
        fixes_applied: int

    @dataclass(frozen=True, slots=True)
    class FormatResult:
        """Result of ruff format operation."""

        files_formatted: int
        files_unchanged: int

    def __init__(self: Self) -> None:
        """Initialize ruff plugin."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[int]:
        """Satisfy FlextService contract."""
        return FlextResult[int].fail("Use check(), fix(), or format() methods")

    def check(
        self: Self,
        files: list[Path],
    ) -> FlextResult[CheckResult]:
        """Check files with ruff.

        Args:
            files: Files to check.

        Returns:
            Check result with error count and violations.

        """
        if not files:
            return FlextResult[FlextRuffPlugin.CheckResult].ok(
                FlextRuffPlugin.CheckResult(
                    error_count=0,
                    files_checked=0,
                )
            )

        file_paths = [str(f) for f in files]

        try:
            result = subprocess.run(
                ["ruff", "check", "--output-format=json", *file_paths],
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Validation.RUFF_TIMEOUT_SECONDS,
            )

            violations: list[dict[str, object]] = []
            if result.stdout.strip():
                violations = json.loads(result.stdout)

            check_result = FlextRuffPlugin.CheckResult(
                error_count=len(violations),
                files_checked=len(files),
                violations=tuple(violations),
            )

            self._logger.debug(
                "Ruff check: %d errors in %d files",
                check_result.error_count,
                check_result.files_checked,
            )

            return FlextResult[FlextRuffPlugin.CheckResult].ok(check_result)

        except (subprocess.TimeoutExpired, FileNotFoundError) as err:
            return FlextResult[FlextRuffPlugin.CheckResult].fail(
                f"Ruff check failed: {err}"
            )

    def fix(
        self: Self,
        files: list[Path],
    ) -> FlextResult[FixResult]:
        """Apply ruff auto-fixes to files.

        Args:
            files: Files to fix.

        Returns:
            Fix result with counts.

        """
        if not files:
            return FlextResult[FlextRuffPlugin.FixResult].ok(
                FlextRuffPlugin.FixResult(files_fixed=0, fixes_applied=0)
            )

        file_paths = [str(f) for f in files]

        try:
            result = subprocess.run(
                ["ruff", "check", "--fix", "--output-format=json", *file_paths],
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Validation.RUFF_TIMEOUT_SECONDS,
            )

            # Count fixes from output
            fixes_applied = 0
            if result.stdout.strip():
                output = json.loads(result.stdout)
                fixes_applied = len([v for v in output if v.get("fix")])

            fix_result = FlextRuffPlugin.FixResult(
                files_fixed=len(files),
                fixes_applied=fixes_applied,
            )

            self._logger.info(
                "Ruff fix: %d fixes applied to %d files",
                fixes_applied,
                len(files),
            )

            return FlextResult[FlextRuffPlugin.FixResult].ok(fix_result)

        except (subprocess.TimeoutExpired, FileNotFoundError) as err:
            return FlextResult[FlextRuffPlugin.FixResult].fail(
                f"Ruff fix failed: {err}"
            )

    def format_files(
        self: Self,
        files: list[Path],
    ) -> FlextResult[FormatResult]:
        """Format files with ruff.

        Args:
            files: Files to format.

        Returns:
            Format result with counts.

        """
        if not files:
            return FlextResult[FlextRuffPlugin.FormatResult].ok(
                FlextRuffPlugin.FormatResult(files_formatted=0, files_unchanged=0)
            )

        file_paths = [str(f) for f in files]

        try:
            # Check which files would change
            check_result = subprocess.run(
                ["ruff", "format", "--check", *file_paths],
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Validation.RUFF_TIMEOUT_SECONDS,
            )

            # Count files that would change
            would_change = check_result.returncode != 0
            files_to_format = (
                len(check_result.stdout.strip().split("\n"))
                if check_result.stdout.strip() and would_change
                else 0
            )

            # Actually format
            subprocess.run(
                ["ruff", "format", *file_paths],
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Validation.RUFF_TIMEOUT_SECONDS,
            )

            format_result = FlextRuffPlugin.FormatResult(
                files_formatted=files_to_format,
                files_unchanged=len(files) - files_to_format,
            )

            self._logger.info(
                "Ruff format: %d files formatted, %d unchanged",
                format_result.files_formatted,
                format_result.files_unchanged,
            )

            return FlextResult[FlextRuffPlugin.FormatResult].ok(format_result)

        except (subprocess.TimeoutExpired, FileNotFoundError) as err:
            return FlextResult[FlextRuffPlugin.FormatResult].fail(
                f"Ruff format failed: {err}"
            )


__all__ = ["FlextRuffPlugin"]
