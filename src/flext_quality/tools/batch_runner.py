"""CLI entry point for batch operations from hooks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Usage:
    python -m flext_quality.tools.batch_runner dry-run file1.py file2.py
    python -m flext_quality.tools.batch_runner backup file1.py file2.py
    python -m flext_quality.tools.batch_runner execute file1.py file2.py
    python -m flext_quality.tools.batch_runner rollback --backup-path /tmp/backup.tar.gz
    python -m flext_quality.tools.batch_runner validate file1.py file2.py
    python -m flext_quality.tools.batch_runner ruff-count file.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextTypes as t

from flext_quality.constants import c
from flext_quality.protocols import p
from flext_quality.tools.batch_backup import FlextQualityBatchBackup
from flext_quality.tools.batch_operations import FlextQualityBatchOperations
from flext_quality.tools.batch_validators import FlextQualityBatchValidators


class DefaultBatchOperation:
    """Default no-op batch operation for validation-only runs.

    Satisfies BatchOperation protocol but does nothing - useful for
    running validators without any actual changes.
    """

    def dry_run(
        self,
        targets: list[Path],
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Preview targets without changes."""
        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "mode": "dry-run",
            "targets": [str(p) for p in targets],
            "count": len(targets),
        })

    def backup(self, targets: list[Path]) -> FlextResult[Path]:
        """Create backup of targets."""
        manager = FlextQualityBatchBackup().manager
        return manager.create(targets)

    def execute(
        self,
        targets: list[Path],
        backup_path: Path | None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """No-op execute - just return success."""
        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "mode": "execute",
            "targets": [str(p) for p in targets],
            "backup_path": str(backup_path) if backup_path else None,
            "changes": 0,
        })

    def rollback(self, backup_path: Path) -> FlextResult[bool]:
        """Restore from backup."""
        manager = FlextQualityBatchBackup().manager
        return manager.restore(backup_path)


def main() -> int:
    """CLI entry point for batch operations."""
    logger = FlextLogger(__name__)

    parser = argparse.ArgumentParser(
        prog="batch_runner",
        description="Batch operations runner for FLEXT quality tools",
    )
    parser.add_argument(
        "mode",
        choices=["dry-run", "backup", "execute", "rollback", "validate", "ruff-count"],
        help="Operation mode",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Target files to operate on",
    )
    parser.add_argument(
        "--backup-path",
        type=Path,
        help="Backup path for rollback mode",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    # Handle special modes that don't use Runner
    if args.mode == "validate":
        return _handle_validate(args, logger)

    if args.mode == "ruff-count":
        return _handle_ruff_count(args, logger)

    # Map CLI mode to enum
    mode_map = {
        "dry-run": c.Quality.Batch.Mode.DRY_RUN,
        "backup": c.Quality.Batch.Mode.BACKUP,
        "execute": c.Quality.Batch.Mode.EXECUTE,
        "rollback": c.Quality.Batch.Mode.ROLLBACK,
    }
    mode = mode_map[args.mode]

    # Convert targets to Path objects
    targets = [Path(t) for t in args.targets]

    # Run operation
    runner = FlextQualityBatchOperations.Runner()
    operation: p.Quality.BatchOperation = DefaultBatchOperation()

    result = runner.run(
        mode=mode,
        operation=operation,
        targets=targets,
        backup_path=args.backup_path,
    )

    # Output results
    if result.is_failure:
        _output_error(args, result.error or "Unknown error", logger)
        return c.Quality.Batch.ExitCode.VALIDATION_FAILED

    _output_success(args, result.value or {}, logger)
    return c.Quality.Batch.ExitCode.SUCCESS


def _handle_validate(args: argparse.Namespace, logger: FlextLogger) -> int:
    """Handle validate mode - run all validators and output results."""
    targets = [Path(t) for t in args.targets]
    validators = FlextQualityBatchValidators()

    result = validators.validate_all(targets)

    if result.is_failure:
        _output_error(args, result.error or "Validation failed", logger)
        return c.Quality.Batch.ExitCode.VALIDATION_FAILED

    _output_success(args, result.value or {}, logger)
    return c.Quality.Batch.ExitCode.SUCCESS


def _handle_ruff_count(args: argparse.Namespace, logger: FlextLogger) -> int:
    """Handle ruff-count mode - output error count for single file."""
    if not args.targets:
        _output_error(args, "ruff-count requires a target file", logger)
        return c.Quality.Batch.ExitCode.VALIDATION_FAILED

    target = Path(args.targets[0])
    validators = FlextQualityBatchValidators()

    result = validators.ruff.validate_file(target)

    if result.is_failure:
        _output_error(args, result.error or "Ruff check failed", logger)
        return c.Quality.Batch.ExitCode.VALIDATION_FAILED

    count = result.value if result.value is not None else 0

    if args.json:
        print(json.dumps({"file": str(target), "count": count}))
    else:
        print(count)

    return c.Quality.Batch.ExitCode.SUCCESS


def _output_error(
    args: argparse.Namespace,
    error: str,
    logger: FlextLogger,
) -> None:
    """Output error message."""
    logger.error(error)
    if args.json:
        print(json.dumps({"error": error}), file=sys.stderr)
    else:
        print(f"ERROR: {error}", file=sys.stderr)


def _output_success(
    args: argparse.Namespace,
    data: dict[str, t.GeneralValueType],
    logger: FlextLogger,
) -> None:
    """Output success message."""
    logger.info("Operation successful")
    if args.json:
        print(json.dumps(data, default=str))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    sys.exit(main())
