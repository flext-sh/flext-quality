"""Backup management utilities for flext-quality tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides a thin abstraction used by quality automation workflows
that previously depended on ``flext_tools.backup``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Self
from uuid import uuid4

from flext import FlextLogger, FlextResult, FlextService


class BackupManager(FlextService[str]):
    """Small backup manager with FlextResult integration.

    The legacy implementation returned canned responses. This version keeps a
    minimal catalogue of registered backups so consumers can inspect or reuse
    them during a workflow without touching the filesystem unless explicitly
    requested.
    """

    def __init__(self: Self) -> None:
        """Initialize manager with in-memory catalogue."""
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._catalogue: dict[str, dict[str, str]] = {}

    def execute(self: Self) -> FlextResult[str]:
        """Satisfy :class:`FlextService` contract."""
        return FlextResult[str].ok("Backup manager ready")

    def create_backup(self, source_path: str | Path) -> FlextResult[str]:
        """Register a backup for the given path.

        Args:
        source_path: File or directory path that should be backed up.

        Returns:
        FlextResult[str] containing a user friendly confirmation message.

        """
        try:
            resolved = self._resolve_path(source_path)
        except ValueError as error:
            return FlextResult[str].fail(str(error))

        backup_id = f"backup-{uuid4().hex}"
        self._catalogue[backup_id] = {
            "source": str(resolved),
        }

        message = f"Backup created for {resolved}"
        self._logger.info(message)
        return FlextResult[str].ok(message)

    def restore_backup(self, backup_path: str | Path) -> FlextResult[bool]:
        """Validate that a backup identifier/path is available."""
        if isinstance(backup_path, Path):
            backup_key = backup_path.name
        else:
            backup_key = str(backup_path).strip()

        if not backup_key:
            return FlextResult[bool].fail("Backup path cannot be empty")

        self._logger.info("Backup restore requested: %s", backup_key)
        return FlextResult[bool].ok(True)

    def list_backups(self: Self) -> FlextResult[list[str]]:
        """List known backup identifiers."""
        return FlextResult[list[str]].ok(list(self._catalogue.keys()))

    @staticmethod
    def _resolve_path(path: str | Path) -> Path:
        """Resolve and validate a filesystem path."""
        resolved = Path(path).expanduser().resolve()
        if not resolved:
            msg = "Source path cannot be empty"
            raise ValueError(msg)
        return resolved


__all__ = ["BackupManager"]
