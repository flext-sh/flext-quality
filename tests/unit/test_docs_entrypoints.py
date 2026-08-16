"""Public documentation module entrypoint behavior."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from flext_quality import u
from flext_quality.docs import (
    FlextQualityLinkChecker,
    FlextQualityScheduledMaintenance,
    FlextQualityStyleValidator,
)
from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
from flext_quality.docs.scripts.validate import FlextQualityDocumentationValidator


@pytest.mark.parametrize(
    ("module", "entrypoint"),
    [
        ("flext_quality.docs.scripts.audit", "FlextQualityDocumentationAuditor"),
        ("flext_quality.docs.scripts.optimize", "FlextQualityDocumentationOptimizer"),
        ("flext_quality.docs.scripts.validate", "FlextQualityDocumentationValidator"),
        ("flext_quality.docs.scripts.report", "FlextQualityDocumentationReporter"),
        ("flext_quality.docs.notifications", "FlextQualityDocumentationNotifier"),
        (
            "flext_quality.docs.scheduled_maintenance",
            "FlextQualityScheduledMaintenance",
        ),
    ],
)
def test_public_module_help(
    module: str, entrypoint: str, capsys: pytest.CaptureFixture[str]
) -> None:
    command = getattr(importlib.import_module(module), entrypoint)

    exit_code = command.main(["--help"])

    assert exit_code == 0
    assert "Usage:" in capsys.readouterr().out


def test_public_style_module_and_default_link_checker(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text("# Guide\n", encoding="utf-8")

    exit_code = FlextQualityStyleValidator.main([str(document)])
    checker = FlextQualityLinkChecker()

    assert exit_code == 0
    assert checker.settings.retry_attempts > 0


def test_validation_and_maintenance_entrypoints_use_packaged_config() -> None:
    checker = FlextQualityLinkChecker()
    validation_run = FlextQualityDocumentationValidator.Run()
    maintenance_run = FlextQualityScheduledMaintenance.Run(
        settings_path=FlextQualityScheduledMaintenance.Run.DEFAULT_CONFIG
    )

    assert not hasattr(FlextQualityDocumentationValidator, "LinkValidator")
    assert validation_run.timeout == checker.settings.external_timeout
    assert validation_run.retries == checker.settings.retry_attempts
    assert Path(maintenance_run.settings_path).is_file()
    assert Path(maintenance_run.settings_path).name == "schedule_config.yaml"


def test_default_root_public_runs_discover_checkout_readme_and_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout = tmp_path / "checkout"
    docs = checkout / "docs"
    docs.mkdir(parents=True)
    readme = checkout / "README.md"
    guide = docs / "guide.md"
    readme.write_text("# Project\n", encoding="utf-8")
    guide.write_text("# Guide\n", encoding="utf-8")
    reports = checkout / "reports"
    monkeypatch.setattr(u.Quality, "project_root", lambda: checkout)

    auditor = FlextQualityDocumentationAuditor()
    optimizer_run = FlextQualityDocumentationOptimizer.Run(
        fix_formatting=True, backup=False, output=str(reports)
    )

    assert {readme, guide}.issubset(set(auditor.find_documentation_files()))
    assert {readme, guide}.issubset(set(optimizer_run.discover_files()))
    assert FlextQualityDocumentationAuditor.Run(output=str(reports)).execute().success
    assert optimizer_run.execute().success


def test_scheduler_loads_config_forwards_arguments_and_runs_real_safe_task(
    tmp_path: Path,
) -> None:
    reports = tmp_path / "reports"
    config = tmp_path / "schedule.yaml"
    config.write_text(
        "enabled: true\n"
        f"reports_dir: {reports}\n"
        f"backup_dir: {tmp_path / 'backups'}\n"
        "schedules:\n  daily_audit:\n    enabled: true\n    time: '09:00'\n"
        "    tasks: [audit_help]\n"
        "tasks:\n  audit_help:\n    description: audit help\n"
        "    command: python -m flext_quality.docs.scripts.audit --help\n"
        "    timeout: 5\n"
        "error_handling:\n  max_retries: 0\n  retry_delay: 0\n"
        "  fail_fast: true\n  notify_on_failure: false\n"
        "logging:\n  enabled: false\n  log_file: scheduler.log\n"
        "  max_log_size: 1MB\n  retention_days: 1\n",
        encoding="utf-8",
    )
    maintenance = FlextQualityScheduledMaintenance(str(config))

    assert maintenance.settings.tasks["audit_help"].command.endswith("audit --help")
    assert maintenance.run_daily_audit()
    assert maintenance.results.tasks_completed == 1
