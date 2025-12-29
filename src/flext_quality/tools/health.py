"""Workspace health check helpers migrated from flext_tools.monitoring."""

from __future__ import annotations

import socket
import tempfile
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

# Daemon socket/status paths
RUFF_DAEMON_SOCKET = Path(tempfile.gettempdir()) / "ruff-daemon.sock"
DMYPY_STATUS_FILE = Path.home() / ".dmypy.json"


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

    def check_ruff_daemon(self: Self) -> FlextResult[bool]:
        """Check if ruff-daemon is running via Unix socket.

        Returns:
            FlextResult[bool] indicating if daemon is available.

        """
        if not RUFF_DAEMON_SOCKET.exists():
            self._logger.debug("Ruff daemon socket not found: %s", RUFF_DAEMON_SOCKET)
            return FlextResult[bool].ok(False)

        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(str(RUFF_DAEMON_SOCKET))
            sock.close()
            return FlextResult[bool].ok(True)
        except (OSError, TimeoutError):
            self._logger.debug("Ruff daemon socket connection failed")
            return FlextResult[bool].ok(False)

    def check_mypy_daemon(self: Self) -> FlextResult[bool]:
        """Check if dmypy is running via status file.

        Returns:
            FlextResult[bool] indicating if daemon is available.

        """
        exists = DMYPY_STATUS_FILE.exists()
        if not exists:
            self._logger.debug(
                "MyPy daemon status file not found: %s", DMYPY_STATUS_FILE
            )
        return FlextResult[bool].ok(exists)

    def check_daemons(self: Self) -> FlextResult[dict[str, bool]]:
        """Check all quality daemons and return consolidated status.

        Returns:
            FlextResult[dict[str, bool]] with daemon names as keys.

        """
        ruff_result = self.check_ruff_daemon()
        mypy_result = self.check_mypy_daemon()

        status: dict[str, bool] = {
            "ruff": ruff_result.value if ruff_result.is_success else False,
            "mypy": mypy_result.value if mypy_result.is_success else False,
        }

        self._logger.info("Daemon status: %s", status)
        return FlextResult[dict[str, bool]].ok(status)
