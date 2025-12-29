# VERIFIED_NEW_MODULE
"""Backwards compatibility layer for quality plugins.

Provides stable API wrappers for external plugin scripts. Ensures all external
plugin integrations continue working during internal refactoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Self

from flext_core import FlextResult, FlextService

# Import the actual implementation (may change internally)
from flext_quality.plugins.code_quality_plugin import (
    FlextCodeQualityPlugin as _FlextCodeQualityPluginImpl,
)
from flext_quality.plugins.duplication_plugin import FlextDuplicationPlugin


class FlextCodeQualityPlugin(FlextService[int]):
    """Legacy API wrapper - maintains exact signature for external plugins.

    This class wraps the internal implementation to ensure that external
    plugin scripts continue working without modification during refactoring.

    All methods maintain their original signatures and return types.

    Example:
        from flext_quality.plugins import FlextCodeQualityPlugin

        plugin = FlextCodeQualityPlugin()
        result = plugin.check([Path("src/")])
        if result.is_success:
            logger.info("Total violations: %d", result.value.total_violations)

    """

    # Expose nested dataclasses for external API
    Violation: ClassVar = _FlextCodeQualityPluginImpl.Violation
    CheckResult: ClassVar = _FlextCodeQualityPluginImpl.CheckResult
    WorkspaceCheckResult: ClassVar = _FlextCodeQualityPluginImpl.WorkspaceCheckResult

    def __init__(
        self: Self,
        semgrep_rules_path: Path | None = None,
    ) -> None:
        """Initialize code quality plugin with internal implementation.

        Args:
            semgrep_rules_path: Path to Semgrep rules directory.
                Defaults to bundled rules in package.

        """
        super().__init__()
        self._impl = _FlextCodeQualityPluginImpl(semgrep_rules_path)

    def execute(self: Self) -> FlextResult[int]:
        """Satisfy FlextService contract.

        Returns:
            FlextResult[int]: Failure indicating use check() or check_workspace().

        """
        return self._impl.execute()

    def check(
        self: Self,
        targets: list[Path],
        categories: list[str] | None = None,
    ) -> FlextResult[FlextCodeQualityPlugin.CheckResult]:
        """Check files/directories for quality violations.

        Args:
            targets: Files or directories to check.
            categories: Filter by category (SOLID, DRY, KISS, etc.).
                If None, checks all categories.

        Returns:
            Check result with violations.

        """
        return self._impl.check(targets, categories)

    def check_workspace(
        self: Self,
        workspace_root: Path,
        categories: list[str] | None = None,
    ) -> FlextResult[FlextCodeQualityPlugin.WorkspaceCheckResult]:
        """Check entire workspace for quality violations.

        Args:
            workspace_root: Root directory of workspace to check.
            categories: Filter by category (SOLID, DRY, KISS, etc.).
                If None, checks all categories.

        Returns:
            Workspace check result with aggregated violations by project.

        """
        return self._impl.check_workspace(workspace_root, categories)


__all__ = ["FlextCodeQualityPlugin", "FlextDuplicationPlugin"]
