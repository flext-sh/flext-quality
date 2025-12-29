"""Baseline management for quality gate comparisons.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextLogger, FlextResult
from flext_core.typings import FlextTypes as t

from .storage import FlextQualityBaselinesStorage


class FlextQualityBaselinesManager:
    """Manage quality baselines for dead code tracking."""

    class Manager:
        """Baseline management operations."""

        def __init__(self, baseline_path: Path) -> None:
            """Initialize baseline manager.

            Args:
                baseline_path: Path to the baseline file.

            """
            self._storage = FlextQualityBaselinesStorage.Storage(baseline_path)
            self._logger = FlextLogger(__name__)

        def get_baseline(self, project: str) -> FlextResult[int]:
            """Get baseline count for a project.

            Args:
                project: Project name.

            Returns:
                FlextResult containing the baseline count.

            """
            result = self._storage.read()
            if result.is_failure:
                return FlextResult[int].fail(result.error or "Read failed")

            baselines = result.value
            return FlextResult[int].ok(baselines.get(project, 0))

        def check_violation(
            self,
            project: str,
            current_count: int,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Check if current count exceeds baseline.

            Args:
                project: Project name.
                current_count: Current dead code count.

            Returns:
                FlextResult containing violation check results.

            """
            baseline_result = self.get_baseline(project)
            if baseline_result.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    baseline_result.error or "",
                )

            baseline = baseline_result.value
            is_violation = current_count > baseline

            return FlextResult[dict[str, t.GeneralValueType]].ok({
                "project": project,
                "baseline": baseline,
                "current": current_count,
                "is_violation": is_violation,
                "increase": current_count - baseline if is_violation else 0,
            })

        def update_baseline(self, project: str, count: int) -> FlextResult[bool]:
            """Update baseline for a project.

            Args:
                project: Project name.
                count: New dead code count.

            Returns:
                FlextResult indicating success or failure.

            """
            return self._storage.update(project, count)


__all__ = ["FlextQualityBaselinesManager"]
