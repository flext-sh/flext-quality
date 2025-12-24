"""Workspace health check helpers migrated from flext_tools.monitoring."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService


class HealthCheckService(FlextService[bool]):
    """Provide a minimal health check service for maintenance scripts."""

    def __init__(self: Self, workspace_path: str | Path) -> None:
        """Initialize health check service.

        Args:
        workspace_path: Path to the workspace to check

        """
        super().__init__()
        self._workspace = Path(workspace_path)
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[bool]:
        """Return health status summary."""
        return self.run_health_checks()

    def run_health_checks(self: Self) -> FlextResult[bool]:
        """Run placeholder health checks."""
        exists = self._workspace.exists()
        if not exists:
            self._logger.warning("Workspace path does not exist: %s", self._workspace)
        return FlextResult[bool].ok(exists)
