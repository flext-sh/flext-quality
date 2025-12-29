# VERIFIED_NEW_MODULE
"""Backwards compatibility layer for hook validators.

Provides stable API wrappers for external hook scripts. Ensures all external
hook integrations continue working during internal CLI refactoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes as t

# Import the actual implementation (may change internally)
from flext_quality.hooks.validator import (
    FlextHookValidator as _FlextHookValidatorImpl,
)


class FlextHookValidator(FlextService[bool]):
    """Legacy API wrapper - maintains exact signature for external hooks.

    This class wraps the internal implementation to ensure that external
    hook scripts continue working without modification during CLI refactoring.

    All methods maintain their original signatures and return types.

    Example:
        from flext_quality.hooks import FlextHookValidator

        validator = FlextHookValidator()
        passed, message = validator.validate_file("/path/to/file.py")

    """

    def __init__(self: Self) -> None:
        """Initialize hook validator with internal implementation."""
        super().__init__()
        self._impl = _FlextHookValidatorImpl()

    def execute(
        self: Self,
        **kwargs: t.GeneralValueType,
    ) -> FlextResult[bool]:
        """Execute hook validator service - FlextService interface.

        Args:
            **kwargs: Service arguments (not used).

        Returns:
            FlextResult[bool]: Always returns ok(True).

        """
        return self._impl.execute(**kwargs)

    def validate_file(
        self: Self,
        file_path: str,
        content: str | None = None,
    ) -> tuple[bool, str]:
        """Validate a single file - called by hooks.

        Args:
            file_path: Path to the file to validate.
            content: Optional file content (if already read).

        Returns:
            (passed, message) - passed=True means allow, False means block.

        """
        return self._impl.validate_file(file_path, content)

    def check_patterns(
        self: Self,
        file_path: str,
        content: str,
    ) -> tuple[bool, list[str]]:
        """Check FLEXT patterns in content.

        Args:
            file_path: Path to the file (for context).
            content: File content to check.

        Returns:
            (passed, violations) - list of violation messages.

        """
        return self._impl.check_patterns(file_path, content)

    def check_lint(
        self: Self,
        file_path: str,
    ) -> tuple[bool, str]:
        """Run lint check on file.

        Args:
            file_path: Path to the file to lint.

        Returns:
            (passed, message).

        """
        return self._impl.check_lint(file_path)

    def check_type(
        self: Self,
        file_path: str,
    ) -> tuple[bool, str]:
        """Run type check on file.

        Args:
            file_path: Path to the file to type check.

        Returns:
            (passed, message).

        """
        return self._impl.check_type(file_path)


__all__ = ["FlextHookValidator"]
