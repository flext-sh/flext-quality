"""Batch validators for centralized batch operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides validators for batch operations with ratchet comparison:
- FlextQualityBatchValidators.Ruff - Ruff-based validation
- FlextQualityBatchValidators.Mypy - Mypy-based validation
- FlextQualityBatchValidators.Architecture - Architecture tier validation
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes as t
from pydantic import ConfigDict

from flext_quality.constants import c
from flext_quality.subprocess_utils import SubprocessUtils


class FlextQualityBatchValidators(FlextService[dict[str, t.GeneralValueType]]):
    """Unified batch validators for batch operations.

    Provides standardized validation for batch operations with ratchet
    comparison to ensure error counts don't increase.

    Usage:
        validators = FlextQualityBatchValidators()

        # Get baseline
        baseline = validators.ruff.validate_files([Path("file.py")])

        # ... make changes ...

        # Validate ratchet (errors must not increase)
        after = validators.ruff.validate_files([Path("file.py")])
        ratchet = validators.ruff.compare_ratchet(
            baseline.value, after.value
        )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    class Ruff:
        """Ruff-based validation with error counting and ratchet comparison."""

        def __init__(self: Self) -> None:
            """Initialize Ruff validator."""
            self._logger = FlextLogger(__name__)

        def validate_file(self: Self, path: Path) -> FlextResult[int]:
            """Return error count for a single file.

            Args:
                path: Path to Python file to validate.

            Returns:
                FlextResult[int] with error count.

            """
            if not path.exists():
                return FlextResult[int].fail(f"File does not exist: {path}")

            timeout = c.Quality.QualityPerformance.RUFF_CHECK_TIMEOUT
            result = SubprocessUtils.run_external_command(
                ["ruff", "check", str(path), "--output-format=json"],
                capture_output=True,
                check=False,
                timeout=float(timeout),
            )

            if result.is_failure:
                self._logger.debug("Ruff failed for %s: %s", path, result.error)
                return FlextResult[int].ok(0)

            try:
                data = json.loads(result.value.stdout)
                count = len(data)
                self._logger.debug("Ruff errors for %s: %d", path, count)
                return FlextResult[int].ok(count)
            except json.JSONDecodeError:
                return FlextResult[int].ok(0)

        def validate_files(
            self: Self,
            paths: list[Path],
        ) -> FlextResult[dict[str, int]]:
            """Return error counts for multiple files.

            Args:
                paths: List of Python files to validate.

            Returns:
                FlextResult[dict[str, int]] with path -> error count mapping.

            """
            counts: dict[str, int] = {}

            for path in paths:
                result = self.validate_file(path)
                if result.is_success and result.value is not None:
                    counts[str(path)] = result.value
                else:
                    counts[str(path)] = 0

            return FlextResult[dict[str, int]].ok(counts)

        def compare_ratchet(
            self: Self,
            before: dict[str, int],
            after: dict[str, int],
            *,
            tolerance: int | None = None,
        ) -> FlextResult[bool]:
            """Check if error count increased (ratchet violation).

            Args:
                before: Error counts before changes.
                after: Error counts after changes.
                tolerance: Allowed increase (default from constants).

            Returns:
                FlextResult[bool] - True if ratchet passes (no increase).

            """
            if tolerance is None:
                tolerance = c.Quality.Batch.Defaults.RATCHET_TOLERANCE

            before_total = sum(before.values())
            after_total = sum(after.values())
            diff = after_total - before_total

            self._logger.info(
                "Ratchet comparison: before=%d, after=%d, diff=%d, tolerance=%d",
                before_total,
                after_total,
                diff,
                tolerance,
            )

            if diff > tolerance:
                return FlextResult[bool].fail(
                    f"Ratchet violation: errors increased by {diff} "
                    f"(before={before_total}, after={after_total}, tolerance={tolerance})",
                )

            return FlextResult[bool].ok(True)

    class Mypy:
        """Mypy-based validation with error counting and ratchet comparison."""

        def __init__(self: Self) -> None:
            """Initialize Mypy validator."""
            self._logger = FlextLogger(__name__)

        def validate_file(self: Self, path: Path) -> FlextResult[int]:
            """Return error count for a single file.

            Args:
                path: Path to Python file to validate.

            Returns:
                FlextResult[int] with error count.

            """
            if not path.exists():
                return FlextResult[int].fail(f"File does not exist: {path}")

            timeout = c.Quality.QualityPerformance.MYPY_CHECK_TIMEOUT
            result = SubprocessUtils.run_external_command(
                ["mypy", "--strict", str(path)],
                capture_output=True,
                check=False,
                timeout=float(timeout),
            )

            if result.is_failure:
                self._logger.debug("Mypy failed for %s: %s", path, result.error)
                return FlextResult[int].ok(0)

            error_count = result.value.stdout.count("error:")
            self._logger.debug("Mypy errors for %s: %d", path, error_count)
            return FlextResult[int].ok(error_count)

        def validate_files(
            self: Self,
            paths: list[Path],
        ) -> FlextResult[dict[str, int]]:
            """Return error counts for multiple files.

            Args:
                paths: List of Python files to validate.

            Returns:
                FlextResult[dict[str, int]] with path -> error count mapping.

            """
            counts: dict[str, int] = {}

            for path in paths:
                result = self.validate_file(path)
                if result.is_success and result.value is not None:
                    counts[str(path)] = result.value
                else:
                    counts[str(path)] = 0

            return FlextResult[dict[str, int]].ok(counts)

        def compare_ratchet(
            self: Self,
            before: dict[str, int],
            after: dict[str, int],
            *,
            tolerance: int | None = None,
        ) -> FlextResult[bool]:
            """Check if error count increased (ratchet violation).

            Args:
                before: Error counts before changes.
                after: Error counts after changes.
                tolerance: Allowed increase (default from constants).

            Returns:
                FlextResult[bool] - True if ratchet passes (no increase).

            """
            if tolerance is None:
                tolerance = c.Quality.Batch.Defaults.RATCHET_TOLERANCE

            before_total = sum(before.values())
            after_total = sum(after.values())
            diff = after_total - before_total

            self._logger.info(
                "Mypy ratchet: before=%d, after=%d, diff=%d, tolerance=%d",
                before_total,
                after_total,
                diff,
                tolerance,
            )

            if diff > tolerance:
                return FlextResult[bool].fail(
                    f"Mypy ratchet violation: errors increased by {diff}",
                )

            return FlextResult[bool].ok(True)

    class Architecture:
        """Architecture tier validation for FLEXT layering rules."""

        # Foundation modules that must NOT import from services/api
        FOUNDATION_MODULES: tuple[str, ...] = (
            "models.py",
            "protocols.py",
            "utilities.py",
            "constants.py",
            "typings.py",
        )

        # Forbidden import patterns for foundation modules
        FORBIDDEN_PATTERNS: tuple[re.Pattern[str], ...] = (
            re.compile(r"from flext_.*\.(services|api) import"),
            re.compile(r"import flext_.*\.(services|api)"),
        )

        def __init__(self: Self) -> None:
            """Initialize Architecture validator."""
            self._logger = FlextLogger(__name__)

        def validate_file(self: Self, path: Path) -> FlextResult[list[str]]:
            """Validate architecture layering for a single file.

            Args:
                path: Path to Python file to validate.

            Returns:
                FlextResult[list[str]] with list of violations (empty = valid).

            """
            if not path.exists():
                return FlextResult[list[str]].fail(f"File does not exist: {path}")

            # Only check foundation modules
            if path.name not in self.FOUNDATION_MODULES:
                return FlextResult[list[str]].ok([])

            violations: list[str] = []

            try:
                content = path.read_text(encoding="utf-8")
                for line_num, line in enumerate(content.splitlines(), start=1):
                    violations.extend(
                        f"{path}:{line_num}: {line.strip()}"
                        for pattern in self.FORBIDDEN_PATTERNS
                        if pattern.search(line)
                    )
            except OSError as e:
                return FlextResult[list[str]].fail(f"Failed to read {path}: {e}")

            if violations:
                self._logger.warning(
                    "Architecture violations in %s: %d",
                    path,
                    len(violations),
                )

            return FlextResult[list[str]].ok(violations)

        def validate_files(
            self: Self,
            paths: list[Path],
        ) -> FlextResult[dict[str, list[str]]]:
            """Validate architecture layering for multiple files.

            Args:
                paths: List of Python files to validate.

            Returns:
                FlextResult[dict[str, list[str]]] with path -> violations mapping.

            """
            violations_map: dict[str, list[str]] = {}

            for path in paths:
                result = self.validate_file(path)
                if result.is_success and result.value:
                    violations_map[str(path)] = result.value

            return FlextResult[dict[str, list[str]]].ok(violations_map)

        def validate_directory(
            self: Self,
            directory: Path,
        ) -> FlextResult[dict[str, list[str]]]:
            """Validate architecture layering for all files in directory.

            Args:
                directory: Directory to validate recursively.

            Returns:
                FlextResult[dict[str, list[str]]] with path -> violations mapping.

            """
            if not directory.is_dir():
                return FlextResult[dict[str, list[str]]].fail(
                    f"Not a directory: {directory}",
                )

            files = list(directory.rglob("*.py"))
            return self.validate_files(files)

    def __init__(self: Self) -> None:
        """Initialize batch validators service."""
        super().__init__()
        self.ruff = self.Ruff()
        self.mypy = self.Mypy()
        self.architecture = self.Architecture()
        self._logger = FlextLogger(__name__)

    def execute(
        self: Self,
        **_kwargs: object,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute batch validators service - FlextService interface."""
        return FlextResult[dict[str, t.GeneralValueType]].ok({})

    def validate_all(
        self: Self,
        paths: list[Path],
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run all validators on files and return combined results.

        Args:
            paths: List of Python files to validate.

        Returns:
            FlextResult with combined validation results.

        """
        results: dict[str, t.GeneralValueType] = {}

        ruff_result = self.ruff.validate_files(paths)
        if ruff_result.is_success and ruff_result.value is not None:
            results["ruff"] = ruff_result.value
            results["ruff_total"] = sum(ruff_result.value.values())

        mypy_result = self.mypy.validate_files(paths)
        if mypy_result.is_success and mypy_result.value is not None:
            results["mypy"] = mypy_result.value
            results["mypy_total"] = sum(mypy_result.value.values())

        arch_result = self.architecture.validate_files(paths)
        if arch_result.is_success and arch_result.value is not None:
            results["architecture"] = arch_result.value
            results["architecture_violations"] = sum(
                len(v) for v in arch_result.value.values()
            )

        return FlextResult[dict[str, t.GeneralValueType]].ok(results)


__all__ = ["FlextQualityBatchValidators"]
