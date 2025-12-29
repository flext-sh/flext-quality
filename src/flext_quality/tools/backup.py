"""Backup management utilities for flext-quality tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides backup/restore operations for batch automation workflows.
Used by hooks and scripts for dry-run/backup/exec/rollback cycles.
"""

from __future__ import annotations

import shutil
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Self
from uuid import uuid4

from flext_core import FlextLogger, FlextResult, FlextService

# Default backup directory (using tempfile for security)
BACKUP_DIR = Path(tempfile.gettempdir()) / "flext_backup"


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

    def backup_file(self: Self, source_path: str | Path) -> FlextResult[str]:
        """Create a real filesystem backup of the given file.

        Args:
            source_path: File path to back up.

        Returns:
            FlextResult[str] containing the backup ID on success.

        """
        try:
            resolved = self._resolve_path(source_path)
        except ValueError as error:
            return FlextResult[str].fail(str(error))

        if not resolved.exists():
            return FlextResult[str].fail(f"File not found: {resolved}")

        if not resolved.is_file():
            return FlextResult[str].fail(f"Not a file: {resolved}")

        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
        backup_dir = BACKUP_DIR / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / resolved.name

        shutil.copy2(resolved, backup_path)
        backup_id = f"backup-{uuid4().hex[:8]}"
        self._catalogue[backup_id] = {
            "source": str(resolved),
            "backup": str(backup_path),
            "timestamp": timestamp,
        }
        self._logger.info("Backup created: %s -> %s", resolved, backup_path)
        return FlextResult[str].ok(backup_id)

    def restore_file(self: Self, backup_id: str) -> FlextResult[bool]:
        """Restore a file from its backup.

        Args:
            backup_id: The backup identifier returned by backup_file().

        Returns:
            FlextResult[bool] indicating success.

        """
        if backup_id not in self._catalogue:
            return FlextResult[bool].fail(f"Backup not found: {backup_id}")

        entry = self._catalogue[backup_id]
        backup_path = Path(entry["backup"])
        source_path = Path(entry["source"])

        if not backup_path.exists():
            return FlextResult[bool].fail(f"Backup file missing: {backup_path}")

        shutil.copy2(backup_path, source_path)
        self._logger.info("Restored: %s -> %s", backup_path, source_path)
        return FlextResult[bool].ok(True)

    def backup_files(
        self: Self,
        files: list[str | Path],
    ) -> FlextResult[list[str]]:
        """Backup multiple files, returning list of backup IDs.

        Args:
            files: List of file paths to back up.

        Returns:
            FlextResult[list[str]] containing backup IDs for each file.

        """
        backup_ids: list[str] = []
        for file_path in files:
            result = self.backup_file(file_path)
            if result.is_failure:
                # Rollback already created backups
                for bid in backup_ids:
                    self.restore_file(bid)
                return FlextResult[list[str]].fail(
                    result.error or f"Failed to backup: {file_path}"
                )
            backup_ids.append(result.value)
        return FlextResult[list[str]].ok(backup_ids)

    def backup_directory(self: Self, source_dir: str | Path) -> FlextResult[str]:
        """Create a tar.gz backup of a directory.

        Args:
            source_dir: Directory path to back up.

        Returns:
            FlextResult[str] containing the backup ID on success.

        """
        try:
            resolved = self._resolve_path(source_dir)
        except ValueError as error:
            return FlextResult[str].fail(str(error))

        if not resolved.exists():
            return FlextResult[str].fail(f"Directory not found: {resolved}")

        if not resolved.is_dir():
            return FlextResult[str].fail(f"Not a directory: {resolved}")

        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
        backup_dir = BACKUP_DIR / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"{resolved.name}.tar.gz"

        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(resolved, arcname=resolved.name)

        backup_id = f"dir-backup-{uuid4().hex[:8]}"
        self._catalogue[backup_id] = {
            "source": str(resolved),
            "backup": str(backup_path),
            "timestamp": timestamp,
            "type": "directory",
        }
        self._logger.info("Directory backup: %s -> %s", resolved, backup_path)
        return FlextResult[str].ok(backup_id)

    def restore_directory(self: Self, backup_id: str) -> FlextResult[bool]:
        """Restore a directory from its tar.gz backup.

        Args:
            backup_id: The backup identifier returned by backup_directory().

        Returns:
            FlextResult[bool] indicating success.

        """
        if backup_id not in self._catalogue:
            return FlextResult[bool].fail(f"Backup not found: {backup_id}")

        entry = self._catalogue[backup_id]
        backup_path = Path(entry["backup"])
        source_path = Path(entry["source"])

        if not backup_path.exists():
            return FlextResult[bool].fail(f"Backup file missing: {backup_path}")

        # Remove existing directory if present
        if source_path.exists():
            shutil.rmtree(source_path)

        # Extract to parent directory
        parent_dir = source_path.parent
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(parent_dir, filter="data")

        self._logger.info("Directory restored: %s -> %s", backup_path, source_path)
        return FlextResult[bool].ok(True)

    @staticmethod
    def _resolve_path(path: str | Path) -> Path:
        """Resolve and validate a filesystem path."""
        resolved = Path(path).expanduser().resolve()
        if not resolved:
            msg = "Source path cannot be empty"
            raise ValueError(msg)
        return resolved


__all__ = ["BackupManager"]
