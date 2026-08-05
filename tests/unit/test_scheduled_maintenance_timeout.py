"""Timeout runner diagnostics for scheduled documentation maintenance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import m
from flext_quality.docs.scheduled_maintenance import FlextQualityScheduledMaintenance
from flext_tests import tm


class TestsFlextQualityScheduledMaintenanceTimeout:
    """Public run_single_task preserves Git failure diagnostics via timeout runner."""

    def test_git_failure_preserves_exception_detail(self) -> None:
        """Git non-zero exit text is recorded in results.errors."""
        maintenance = FlextQualityScheduledMaintenance()
        task = m.Quality.ScheduleTaskConfig(
            description="git missing ref",
            command="git rev-parse --verify refs/flext-quality-timeout-diag-missing",
            timeout=30,
        )
        ok = maintenance.run_single_task(task)
        tm.that(ok, eq=False)
        tm.that(len(maintenance.results.errors) > 0, eq=True)
        joined = " ".join(maintenance.results.errors)
        tm.that(joined, has="Task failed in git missing ref")
        tm.that(joined.lower(), has="fatal:")

    def test_git_success_leaves_errors_empty(self) -> None:
        """Successful timed git tasks do not append errors."""
        maintenance = FlextQualityScheduledMaintenance()
        task = m.Quality.ScheduleTaskConfig(
            description="git rev-parse head",
            command="git rev-parse --verify HEAD",
            timeout=30,
        )
        ok = maintenance.run_single_task(task)
        tm.that(ok, eq=True)
        tm.that(list(maintenance.results.errors), eq=[])
