"""Centralized batch operations library facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides unified interface for batch operations with:
- Dry-run preview
- Backup creation
- Execute with validation and auto-rollback
- Rollback from backup

Usage:
    from flext_quality.tools.batch_operations import FlextQualityBatchOperations
    from flext_quality.constants import c

    runner = FlextQualityBatchOperations.Runner()

    # Run in dry-run mode first
    result = runner.run(
        mode=c.Quality.Batch.Mode.DRY_RUN,
        operation=my_operation,
        targets=[Path("file.py")],
    )

    # Then execute with validation
    result = runner.run(
        mode=c.Quality.Batch.Mode.EXECUTE,
        operation=my_operation,
        targets=[Path("file.py")],
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes as t
from pydantic import ConfigDict

from flext_quality.constants import c
from flext_quality.protocols import p
from flext_quality.tools.batch_backup import FlextQualityBatchBackup
from flext_quality.tools.batch_validators import FlextQualityBatchValidators


class FlextQualityBatchOperations(FlextService[dict[str, t.GeneralValueType]]):
    """Centralized batch operations library facade.

    Provides standardized batch operation workflow:
    1. DRY_RUN: Preview changes without modifying
    2. BACKUP: Create timestamped backup
    3. EXECUTE: Apply changes with validation and auto-rollback
    4. ROLLBACK: Restore from backup

    All operations return FlextResult for consistent error handling.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    class Runner:
        """Execute batch operations with validation and auto-rollback."""

        def __init__(self: Self) -> None:
            """Initialize runner with validators and backup manager."""
            self._validators = FlextQualityBatchValidators()
            self._backup = FlextQualityBatchBackup()
            self._logger = FlextLogger(__name__)

        def run(
            self: Self,
            mode: c.Quality.Batch.Mode,
            operation: p.Quality.BatchOperation,
            targets: list[Path],
            *,
            backup_path: Path | None = None,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Execute operation in specified mode.

            Args:
                mode: Operation mode (DRY_RUN, BACKUP, EXECUTE, ROLLBACK).
                operation: BatchOperation protocol implementation.
                targets: List of file paths to operate on.
                backup_path: Path to backup for ROLLBACK mode.

            Returns:
                FlextResult with operation results.

            """
            self._logger.info("Running batch operation in %s mode", mode.value)

            match mode:
                case c.Quality.Batch.Mode.DRY_RUN:
                    return operation.dry_run(targets)

                case c.Quality.Batch.Mode.BACKUP:
                    result = self._backup.manager.create(targets)
                    if result.is_failure:
                        return FlextResult[dict[str, t.GeneralValueType]].fail(
                            result.error or "Backup failed",
                        )
                    return FlextResult[dict[str, t.GeneralValueType]].ok({
                        "backup_path": str(result.value),
                        "files_backed_up": len(targets),
                    })

                case c.Quality.Batch.Mode.EXECUTE:
                    return self._execute_with_validation(operation, targets)

                case c.Quality.Batch.Mode.ROLLBACK:
                    if backup_path is None:
                        # Try to get latest backup
                        latest = self._backup.manager.get_latest()
                        if latest.is_failure:
                            return FlextResult[dict[str, t.GeneralValueType]].fail(
                                "backup_path required for rollback and no latest backup found",
                            )
                        backup_path = latest.value

                    restore_result = self._backup.manager.restore(backup_path)
                    if restore_result.is_failure:
                        return FlextResult[dict[str, t.GeneralValueType]].fail(
                            restore_result.error or "Rollback failed",
                        )
                    return FlextResult[dict[str, t.GeneralValueType]].ok({
                        "restored_from": str(backup_path),
                    })

                case _:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Unknown batch operation mode: {mode}"
                    )

        def _execute_with_validation(
            self: Self,
            operation: p.Quality.BatchOperation,
            targets: list[Path],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Execute with ratchet validation and auto-rollback.

            Workflow:
            1. Get baseline error counts
            2. Create backup
            3. Execute operation
            4. Validate ratchet (errors must not increase)
            5. Rollback if validation failed

            Args:
                operation: BatchOperation to execute.
                targets: Target files.

            Returns:
                FlextResult with execution results.

            """
            # 1. Get baseline error counts
            baseline = self._validators.ruff.validate_files(targets)
            if baseline.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Baseline validation failed: {baseline.error}",
                )
            baseline_counts = baseline.value

            # 2. Create backup
            backup_result = self._backup.manager.create(targets)
            if backup_result.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Backup creation failed: {backup_result.error}",
                )
            backup_path = backup_result.value

            # 3. Execute operation
            exec_result = operation.execute(targets, backup_path)
            if exec_result.is_failure:
                self._logger.warning(
                    "Operation failed, rolling back: %s",
                    exec_result.error,
                )
                self._backup.manager.restore(backup_path)
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Operation failed: {exec_result.error}",
                )

            # 4. Validate ratchet
            after = self._validators.ruff.validate_files(targets)
            if after.is_failure:
                self._logger.warning(
                    "Post-validation failed, rolling back: %s",
                    after.error,
                )
                self._backup.manager.restore(backup_path)
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Post-validation failed: {after.error}",
                )
            after_counts = after.value

            ratchet_result = self._validators.ruff.compare_ratchet(
                baseline_counts,
                after_counts,
            )

            if ratchet_result.is_failure:
                self._logger.warning(
                    "Ratchet violation, rolling back: %s",
                    ratchet_result.error,
                )
                self._backup.manager.restore(backup_path)
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Ratchet violation: {ratchet_result.error}",
                )

            # 5. Success
            before_total = sum(baseline_counts.values())
            after_total = sum(after_counts.values())

            return FlextResult[dict[str, t.GeneralValueType]].ok({
                "status": "success",
                "files_modified": len(targets),
                "backup_path": str(backup_path),
                "errors_before": before_total,
                "errors_after": after_total,
                "errors_reduced": before_total - after_total,
            })

        def validate_targets(
            self: Self,
            targets: list[Path],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate targets and return combined error counts.

            Args:
                targets: Files to validate.

            Returns:
                FlextResult with validation results.

            """
            return self._validators.validate_all(targets)

    def __init__(self: Self) -> None:
        """Initialize batch operations service."""
        super().__init__()
        self.runner = self.Runner()
        self._logger = FlextLogger(__name__)

    def execute(
        self: Self,
        **_kwargs: object,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute batch operations service - FlextService interface."""
        return FlextResult[dict[str, t.GeneralValueType]].ok({})


__all__ = ["FlextQualityBatchOperations"]
