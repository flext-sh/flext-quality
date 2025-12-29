"""FLEXT Hook Validator - Service for shell hook integration.

Provides centralized validation for shell hooks using FlextQualityOperations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes as t

from flext_quality.constants import c
from flext_quality.tools.batch_validators import FlextQualityBatchValidators
from flext_quality.tools.quality_operations import FlextQualityOperations


class FlextHookValidator(FlextService[bool]):
    """Hook validation service - called by shell hooks via Python.

    Provides centralized validation for:
    - File linting (ruff)
    - FLEXT pattern checking
    - Type checking

    Usage:
        from flext_quality.hooks.validator import FlextHookValidator

        validator = FlextHookValidator()
        passed, message = validator.validate_file("/path/to/file.py")
        if not passed:
            exit(2)

    """

    def __init__(self: Self) -> None:
        """Initialize hook validator."""
        super().__init__()
        self._ops: FlextQualityOperations | None = None
        self._validators = FlextQualityBatchValidators()

    def execute(
        self: Self,
        **_kwargs: t.GeneralValueType,
    ) -> FlextResult[bool]:
        """Execute hook validator service - FlextService interface."""
        return FlextResult[bool].ok(True)

    def _get_ops(self: Self, file_path: Path) -> FlextQualityOperations:
        """Get or create operations instance for project."""
        project_path = file_path.parent
        if self._ops is None or self._ops.project_path != project_path:
            self._ops = FlextQualityOperations(project_path)
        return self._ops

    def validate_file(
        self: Self,
        file_path: str,
        content: str | None = None,
    ) -> tuple[bool, str]:
        """Validate a single file - called by hooks.

        Args:
            file_path: Path to the file to validate
            content: Optional file content (if already read)

        Returns:
            (passed, message) - passed=True means allow, False means block

        """
        path = Path(file_path)

        # Only validate Python files
        if path.suffix != ".py":
            return True, "OK"

        # Read content if not provided
        if content is None:
            if not path.exists():
                return True, "OK"
            content = path.read_text(encoding="utf-8")

        # Check FLEXT patterns
        pattern_result = self.check_patterns(file_path, content)
        if not pattern_result[0]:
            violations = pattern_result[1]
            return False, f"BLOCKED: {len(violations)} pattern violations\n" + "\n".join(
                violations
            )

        # Run lint check via operations
        ops = self._get_ops(path)
        result = ops.lint()
        if result.is_failure:
            return False, f"BLOCKED: Lint check failed: {result.error}"

        report = result.value
        if report.errors > 0:
            return False, f"BLOCKED: {report.errors} lint errors"

        return True, "OK"

    def check_patterns(
        self: Self,
        file_path: str,
        content: str,
    ) -> tuple[bool, list[str]]:
        """Check FLEXT patterns in content.

        Args:
            file_path: Path to the file (for context)
            content: File content to check

        Returns:
            (passed, violations) - list of violation messages

        """
        violations: list[str] = []
        path = Path(file_path)

        # Check forbidden patterns from constants
        violations.extend(
            f"FORBIDDEN: Pattern {pattern!r} detected"
            for pattern in c.Quality.Patterns.FORBIDDEN_PATTERNS
            if re.search(pattern, content)
        )

        # Check architecture tier violations
        module_name = path.stem
        if module_name in c.Quality.Hooks.FOUNDATION_MODULES:
            violations.extend(
                "TIER VIOLATION: Foundation module importing from services/api"
                for pattern in c.Quality.Hooks.FORBIDDEN_IN_FOUNDATION
                if re.search(pattern, content)
            )

        return len(violations) == 0, violations

    def check_lint(
        self: Self,
        file_path: str,
    ) -> tuple[bool, str]:
        """Run lint check on file.

        Args:
            file_path: Path to the file to lint

        Returns:
            (passed, message)

        """
        path = Path(file_path)

        if not path.exists():
            return True, "OK"

        if path.suffix != ".py":
            return True, "OK"

        ops = self._get_ops(path)
        result = ops.lint()

        if result.is_failure:
            return False, f"Lint failed: {result.error}"

        report = result.value
        if report.errors > 0:
            return False, f"{report.errors} lint errors"

        return True, "OK"

    def check_type(
        self: Self,
        file_path: str,
    ) -> tuple[bool, str]:
        """Run type check on file.

        Args:
            file_path: Path to the file to type check

        Returns:
            (passed, message)

        """
        path = Path(file_path)

        if not path.exists():
            return True, "OK"

        if path.suffix != ".py":
            return True, "OK"

        ops = self._get_ops(path)
        result = ops.type_check()

        if result.is_failure:
            return False, f"Type check failed: {result.error}"

        report = result.value
        if report.errors > 0:
            return False, f"{report.errors} type errors"

        return True, "OK"


__all__ = ["FlextHookValidator"]
