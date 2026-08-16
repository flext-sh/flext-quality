"""Public scheduled documentation maintenance behavior."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from flext_quality import m, u
from flext_quality.docs import FlextQualityScheduledMaintenance


def test_packaged_schedule_is_complete_and_current() -> None:
    maintenance = FlextQualityScheduledMaintenance()
    packaged = u.Cli.yaml_load_mapping(
        Path(FlextQualityScheduledMaintenance.Run.DEFAULT_CONFIG)
    )

    assert maintenance.settings == maintenance.settings.model_validate(packaged)
    assert maintenance.settings.schedules["daily_audit"].tasks == [
        "audit_quick",
        "validate_links",
        "check_critical",
    ]
    assert all(
        "python -m flext_quality.docs" in task.command
        for task in maintenance.settings.tasks.values()
    )


def test_incomplete_schedule_fails_at_typed_boundary(tmp_path: Path) -> None:
    config = tmp_path / "schedule.yaml"
    config.write_text("enabled: true\n", encoding="utf-8")

    with pytest.raises(ValidationError):
        FlextQualityScheduledMaintenance(str(config))


def test_python_module_handler_forwards_explicit_arguments(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    maintenance = FlextQualityScheduledMaintenance()

    result = maintenance.run_single_task(
        m.Quality.ScheduleTaskConfig(
            description="scheduled report",
            command=(
                "python -m flext_quality.docs.scripts.report run --format markdown "
                f"--output {reports} --filename scheduled"
            ),
            timeout=30,
        )
    )

    assert result is True
    assert (reports / "scheduled.markdown").is_file()
