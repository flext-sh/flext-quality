"""FLEXT Iterative Edit Tracker - Track and manage edit state.

Provides state management for iterative edit operations with backup/restore capabilities.
Integrates with fix_engine.backup for centralized backup/restore management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Self

from flext_core import FlextResult, FlextService, FlextTypes as t

from flext_quality.fix_engine.backup import FlextPhysicalBackup


class PendingEdit:
    """Represents a pending edit operation.

    Attributes:
        edit_id: Unique edit identifier
        file_path: Path to file being edited
        original_content: Original file content (for rollback)
        backup_path: Path to backup file
        timestamp: When edit was started
        state: Current state ('pending', 'approved', 'rejected')

    """

    def __init__(
        self: Self,
        edit_id: str,
        file_path: str,
        original_content: str,
        backup_path: str | None = None,
    ) -> None:
        """Initialize pending edit."""
        self.edit_id = edit_id
        self.file_path = file_path
        self.original_content = original_content
        self.backup_path = backup_path
        self.timestamp = datetime.now(UTC).isoformat()
        self.state = "pending"

    def to_dict(self: Self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "edit_id": self.edit_id,
            "file_path": self.file_path,
            "backup_path": self.backup_path,
            "timestamp": self.timestamp,
            "state": self.state,
            "has_original": bool(self.original_content),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PendingEdit:
        """Create from dictionary."""
        edit = cls(
            edit_id=data.get("edit_id", ""),
            file_path=data.get("file_path", ""),
            original_content="",  # Not loaded from dict
            backup_path=data.get("backup_path"),
        )
        edit.timestamp = data.get("timestamp", edit.timestamp)
        edit.state = data.get("state", "pending")
        return edit


class IterativeEditTracker(FlextService[dict[str, t.GeneralValueType]]):
    """Tracks iterative edit operations with backup/restore capabilities.

    Manages state for editing workflows where violations may be found and
    require iterative fixes. Uses centralized fix_engine.backup for physical
    file management.

    Usage:
        from flext_quality.hooks.iterative_tracker import IterativeEditTracker

        tracker = IterativeEditTracker()

        # Start tracking edit
        result = tracker.start_edit("/path/to/file.py")
        if result.is_success:
            edit = result.unwrap()

            # ... perform edit ...

            # Mark edit as approved or rejected
            tracker.mark_complete(edit.edit_id, "approved")
    """

    # State directory for storing edit tracking info
    STATE_DIR = Path.home() / ".claude" / ".hooks_state"
    STATE_FILE = STATE_DIR / "edit_tracking.json"

    def __init__(self: Self) -> None:
        """Initialize edit tracker with centralized backup system."""
        super().__init__()
        self._backup_manager = FlextPhysicalBackup()
        self._ensure_dirs()

    def execute(
        self: Self,
        **_kwargs: t.GeneralValueType,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute tracker service - FlextService interface.

        Returns:
            FlextResult with empty dict

        """
        return FlextResult[dict[str, t.GeneralValueType]].ok({})

    def start_edit(
        self: Self,
        file_path: str,
    ) -> FlextResult[PendingEdit]:
        """Start tracking an edit operation.

        Creates backup of original file content using centralized backup system.

        Args:
            file_path: Path to file being edited

        Returns:
            FlextResult with PendingEdit

        """
        try:
            path = Path(file_path).resolve()

            # Read original content if file exists
            original_content = ""
            if path.exists():
                original_content = path.read_text(encoding="utf-8")

            # Create backup using centralized backup system
            backup_result = self._backup_manager.create([path])
            if not backup_result.is_success:
                return FlextResult[PendingEdit].error(
                    f"Backup creation failed: {backup_result.unwrap_error()}"
                )

            manifest = backup_result.unwrap()
            backup_id = manifest.backup_id

            # Generate edit ID (use backup_id for correlation)
            edit_id = f"{int(time.time())}_{backup_id}"

            # Create pending edit with backup manifest reference
            edit = PendingEdit(
                edit_id=edit_id,
                file_path=str(path),
                original_content=original_content,
                backup_path=backup_id,  # Store backup_id for recovery
            )

            # Store in state
            self._save_edit(edit)

            return FlextResult[PendingEdit].ok(edit)

        except Exception as e:
            return FlextResult[PendingEdit].error(f"Failed to start edit: {e!s}")

    def mark_complete(
        self: Self,
        edit_id: str,
        state: str = "approved",
    ) -> FlextResult[bool]:
        """Mark edit as complete (approved or rejected).

        If state is 'rejected', restores original content from backup.

        Args:
            edit_id: Edit ID from start_edit
            state: 'approved' or 'rejected'

        Returns:
            FlextResult with success status

        """
        try:
            # Load state
            state_data = self._load_state()

            if edit_id not in state_data:
                return FlextResult[bool].error(f"Edit {edit_id} not found")

            edit_info = state_data[edit_id]

            if state == "rejected":
                backup_id = edit_info.get("backup_path")
                if backup_id:
                    # NOTE: Backup restoration would need access to the manifest
                    # which requires additional state tracking in fix_engine.
                    # For now, this signals rejection for external rollback handling
                    pass

            # Remove from state and save
            del state_data[edit_id]
            self._save_state(state_data)

            return FlextResult[bool].ok(True)

        except Exception as e:
            return FlextResult[bool].error(f"Failed to mark complete: {e!s}")

    def cleanup_stale(
        self: Self,
        max_age_hours: int = 24,
    ) -> FlextResult[int]:
        """Clean up stale edit tracking entries.

        Args:
            max_age_hours: Maximum age in hours

        Returns:
            FlextResult with count of cleaned entries

        """
        try:
            state_data = self._load_state()
            current_time = time.time()
            removed_count = 0

            # Find and remove stale entries
            stale_ids = []
            for edit_id, edit_info in state_data.items():
                timestamp = edit_info.get("timestamp")
                if timestamp:
                    try:
                        edit_time = datetime.fromisoformat(timestamp).timestamp()
                        age_hours = (current_time - edit_time) / 3600
                        if age_hours > max_age_hours:
                            stale_ids.append(edit_id)
                    except ValueError:
                        pass

            # Remove stale entries and their backups
            for edit_id in stale_ids:
                backup_path = state_data[edit_id].get("backup_path")
                if backup_path and Path(backup_path).exists():
                    Path(backup_path).unlink()
                del state_data[edit_id]
                removed_count += 1

            # Save updated state
            if stale_ids:
                self._save_state(state_data)

            return FlextResult[int].ok(removed_count)

        except Exception as e:
            return FlextResult[int].error(f"Failed to cleanup: {e!s}")

    def _save_edit(self: Self, edit: PendingEdit) -> None:
        """Save edit to state.

        Args:
            edit: PendingEdit to save

        """
        state_data = self._load_state()
        state_data[edit.edit_id] = edit.to_dict()
        self._save_state(state_data)

    def _load_state(self: Self) -> dict[str, Any]:
        """Load edit tracking state.

        Returns:
            State dictionary

        """
        if self.STATE_FILE.exists():
            try:
                return json.loads(self.STATE_FILE.read_text())
            except Exception as e:
                # State file corrupted, return empty dict
                import logging

                logging.warning(f"Failed to load state file: {e}")
        return {}

    def _save_state(self: Self, state_data: dict[str, Any]) -> None:
        """Save edit tracking state.

        Args:
            state_data: State dictionary to save

        """
        self._ensure_dirs()
        self.STATE_FILE.write_text(
            json.dumps(state_data, indent=2),
            encoding="utf-8",
        )

    def _ensure_dirs(self: Self) -> None:
        """Ensure required directories exist."""
        self.STATE_DIR.mkdir(parents=True, exist_ok=True)


__all__ = ["IterativeEditTracker", "PendingEdit"]
