#!/usr/bin/env python3
"""FLEXT Quality Scheduled Documentation Maintenance.

Automated scheduled maintenance system for regular documentation quality checks,
optimizations, and reporting. Designed to run as a cron job or scheduled task.
"""

from __future__ import annotations

import runpy
import shlex
import sys
import threading
import time
from collections.abc import (
    Callable,
)
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, ClassVar, override

import pytest
import schedule
from git import InvalidGitRepositoryError, Repo

from flext_cli import cli, m as cli_m, u as cli_u
from flext_core import p, r, s
from flext_quality import c, m, t, u

logger = u.fetch_logger(__name__)


def _docs_root() -> Path:
    """Return the package root for documentation tooling."""
    return Path(__file__).resolve().parent


def _docs_config_file(filename: str) -> Path:
    """Return the absolute path for a docs settings file."""
    return _docs_root() / "settings" / filename


def _docs_reports_dir() -> Path:
    """Return the reports directory for documentation tooling."""
    return _docs_root() / "reports"


def _docs_backups_dir() -> Path:
    """Return the backups directory for documentation tooling."""
    return _docs_root() / "backups"


def _docs_logs_dir() -> Path:
    """Return the logs directory for documentation tooling."""
    return _docs_root() / "logs"


def _as_str(value: t.JsonValue | None, default: str) -> str:
    """Normalize unknown settings values to string."""
    return value if isinstance(value, str) else default


def _as_bool(value: t.JsonValue | None, /, *, default: bool) -> bool:
    """Normalize unknown settings values to bool."""
    return value if isinstance(value, bool) else default


def _as_int(value: t.JsonValue | None, default: int) -> int:
    """Normalize unknown settings values to int."""
    return value if isinstance(value, int) else default


def _as_str_list(
    value: t.JsonValue | None,
    default: t.StrSequence,
) -> t.StrSequence:
    """Normalize unknown settings values to t.StrSequence."""
    if isinstance(value, list):
        return default
    return default


class FlextQualityScheduledMaintenance:
    """Scheduled documentation maintenance system."""

    # Command parsing constants
    MIN_PYTHON_ARGS = 2  # python -m is minimum 2 parts
    MIN_GIT_ARGS = 2  # git <subcommand> is minimum 2 parts
    MIN_PYTHON_MODULE_INDEX = 2  # module name is at index 2 (python -m module_name)

    def __init__(
        self,
        config_path: str | None = None,
    ) -> None:
        """Initialize scheduled maintenance system.

        Args:
            config_path: Path to configuration file for maintenance schedule.

        """
        self.settings: m.Quality.MaintenanceConfig = self.get_default_config()
        self.load_config(config_path)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.reports_dir = Path(self.settings.reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Initialize results tracking
        self.results: m.Quality.ScheduleResults = m.Quality.ScheduleResults(
            start_time=datetime.now(UTC).isoformat(),
        )

    def load_config(self, config_path: str | None) -> None:
        """Load maintenance schedule configuration."""
        default_config = self.get_default_config()
        resolved_config_path = (
            Path(config_path)
            if config_path is not None
            else _docs_config_file("schedule_config.yaml")
        )
        try:
            loaded_untyped = u.Cli.yaml_load_mapping(
                resolved_config_path,
            )
            if u.mapping(loaded_untyped) and loaded_untyped:
                self.settings = self._merge_config(default_config, loaded_untyped)
            else:
                self.settings = default_config
        except FileNotFoundError:
            self.settings = default_config

    def _merge_config(
        self,
        base: m.Quality.MaintenanceConfig,
        overrides: t.JsonMapping,
    ) -> m.Quality.MaintenanceConfig:
        """Merge external settings mapping into default typed settings."""
        merged = base.model_dump()
        merged["enabled"] = _as_bool(overrides.get("enabled"), default=base.enabled)
        merged["reports_dir"] = _as_str(overrides.get("reports_dir"), base.reports_dir)
        merged["backup_dir"] = _as_str(overrides.get("backup_dir"), base.backup_dir)

        schedules_raw = overrides.get("schedules")
        if u.mapping(schedules_raw):
            schedules = {
                key: value.model_dump() for key, value in base.schedules.items()
            }
            for key, value in schedules_raw.items():
                if u.mapping(value) and key in schedules:
                    current = schedules[key]
                    updated = {
                        "enabled": _as_bool(
                            value.get("enabled"),
                            default=current["enabled"],
                        ),
                        "time": _as_str(value.get("time"), current["time"]),
                        "tasks": _as_str_list(value.get("tasks"), current["tasks"]),
                        "day": _as_str(value.get("day"), current.get("day") or "")
                        or None,
                    }
                    schedules[key] = updated
            merged["schedules"] = schedules

        tasks_raw = overrides.get("tasks")
        if u.mapping(tasks_raw):
            tasks = {key: value.model_dump() for key, value in base.tasks.items()}
            for key, value in tasks_raw.items():
                if u.mapping(value) and key in tasks:
                    current = tasks[key]
                    tasks[key] = {
                        "description": _as_str(
                            value.get("description"),
                            current["description"],
                        ),
                        "command": _as_str(
                            value.get("command"),
                            current["command"],
                        ),
                        "timeout": _as_int(value.get("timeout"), current["timeout"]),
                    }
            merged["tasks"] = tasks

        error_handling_raw = overrides.get("error_handling")
        if u.mapping(error_handling_raw):
            err_cfg = base.error_handling
            merged["error_handling"] = {
                "max_retries": _as_int(
                    error_handling_raw.get("max_retries"),
                    err_cfg.max_retries,
                ),
                "retry_delay": _as_int(
                    error_handling_raw.get("retry_delay"),
                    err_cfg.retry_delay,
                ),
                "fail_fast": _as_bool(
                    error_handling_raw.get("fail_fast"),
                    default=err_cfg.fail_fast,
                ),
                "notify_on_failure": _as_bool(
                    error_handling_raw.get("notify_on_failure"),
                    default=err_cfg.notify_on_failure,
                ),
            }

        logging_raw = overrides.get("logging")
        if u.mapping(logging_raw):
            log_cfg = base.logging
            merged["logging"] = {
                "enabled": _as_bool(
                    logging_raw.get("enabled"),
                    default=log_cfg.enabled,
                ),
                "log_file": _as_str(logging_raw.get("log_file"), log_cfg.log_file),
                "max_log_size": _as_str(
                    logging_raw.get("max_log_size"),
                    log_cfg.max_log_size,
                ),
                "retention_days": _as_int(
                    logging_raw.get("retention_days"),
                    log_cfg.retention_days,
                ),
            }

        return m.Quality.MaintenanceConfig.model_validate(merged)

    def get_default_config(self) -> m.Quality.MaintenanceConfig:
        """Default maintenance configuration."""
        reports_dir = str(_docs_reports_dir())
        backup_dir = str(_docs_backups_dir())
        latest_audit_report = str(_docs_reports_dir() / "latest_audit.json")
        return m.Quality.MaintenanceConfig.model_validate({
            "enabled": True,
            "reports_dir": reports_dir,
            "backup_dir": backup_dir,
            "schedules": {
                "daily_audit": {
                    "enabled": True,
                    "time": "09:00",
                    "tasks": ["audit_quick", "validate_links", "check_critical"],
                },
                "daily_optimize": {
                    "enabled": True,
                    "time": "02:00",  # Early morning
                    "tasks": ["optimize_formatting", "update_toc"],
                },
                "weekly_comprehensive": {
                    "enabled": True,
                    "day": "monday",
                    "time": "10:00",
                    "tasks": [
                        "audit_comprehensive",
                        "generate_report",
                        "notify_weekly",
                    ],
                },
                "monthly_deep_clean": {
                    "enabled": True,
                    "day": "1st",
                    "time": "11:00",
                    "tasks": [
                        "audit_comprehensive",
                        "optimize_full",
                        "generate_monthly_report",
                        "cleanup_old_reports",
                    ],
                },
            },
            "tasks": {
                "audit_quick": {
                    "description": "Quick daily audit for critical issues",
                    "command": f"python -m flext_quality.docs.scripts.audit --check-freshness --check-completeness --output {reports_dir}",
                    "timeout": 300,
                },
                "audit_comprehensive": {
                    "description": "Full comprehensive audit",
                    "command": f"python -m flext_quality.docs.scripts.audit --comprehensive --output {reports_dir}",
                    "timeout": 600,
                },
                "validate_links": {
                    "description": "Validate all links and references",
                    "command": f"python -m flext_quality.docs.scripts.validate --external-links --internal-links --images --output {reports_dir}",
                    "timeout": 300,
                },
                "check_critical": {
                    "description": "Check for critical issues and send alerts",
                    "command": f"python -m flext_quality.docs.notifications --audit-data {latest_audit_report}",
                    "timeout": 60,
                },
                "optimize_formatting": {
                    "description": "Auto-fix formatting issues",
                    "command": f"python -m flext_quality.docs.scripts.optimize --fix-formatting --backup --output {reports_dir}",
                    "timeout": 300,
                },
                "optimize_full": {
                    "description": "Full optimization suite",
                    "command": f"python -m flext_quality.docs.scripts.optimize --comprehensive --backup --output {reports_dir}",
                    "timeout": 600,
                },
                "update_toc": {
                    "description": "Update table of contents",
                    "command": f"python -m flext_quality.docs.scripts.optimize --update-toc --output {reports_dir}",
                    "timeout": 180,
                },
                "generate_report": {
                    "description": "Generate quality report",
                    "command": f"python -m flext_quality.docs.scripts.report --format html --output {reports_dir}",
                    "timeout": 120,
                },
                "generate_monthly_report": {
                    "description": "Generate comprehensive monthly report",
                    "command": f"python -m flext_quality.docs.scripts.report --monthly-trends --format html --output {reports_dir}",
                    "timeout": 180,
                },
                "notify_weekly": {
                    "description": "Send weekly notification",
                    "command": f"python -m flext_quality.docs.notifications --weekly-report {latest_audit_report}",
                    "timeout": 60,
                },
                "cleanup_old_reports": {
                    "description": "Clean up old report files",
                    "command": f'find {reports_dir} -name "*.json" -mtime +90 -delete',
                    "timeout": 30,
                },
            },
            "error_handling": {
                "max_retries": 3,
                "retry_delay": 60,
                "fail_fast": False,
                "notify_on_failure": True,
            },
            "logging": {
                "enabled": True,
                "log_file": str(_docs_logs_dir() / "scheduled_maintenance.log"),
                "max_log_size": "10MB",
                "retention_days": 30,
            },
        })

    def _get_task_names(self, schedule_key: str) -> t.StrSequence:
        """Extract task name list from settings for a schedule key."""
        schedules = self.settings.schedules
        schedule_entry = schedules.get(schedule_key)
        return schedule_entry.tasks if schedule_entry else []

    def run_daily_audit(self) -> bool:
        """Run daily audit tasks."""
        return self.run_tasks(self._get_task_names("daily_audit"))

    def run_daily_optimize(self) -> bool:
        """Run daily optimization tasks."""
        return self.run_tasks(self._get_task_names("daily_optimize"))

    def run_weekly_comprehensive(self) -> bool:
        """Run weekly comprehensive maintenance."""
        return self.run_tasks(self._get_task_names("weekly_comprehensive"))

    def run_monthly_deep_clean(self) -> bool:
        """Run monthly deep cleaning maintenance."""
        return self.run_tasks(self._get_task_names("monthly_deep_clean"))

    def run_tasks(self, task_names: t.StrSequence) -> bool:
        """Run a list of maintenance tasks."""
        success = True

        for task_name in task_names:
            task_cfg = self.settings.tasks.get(task_name)
            if task_cfg is not None:
                if self.run_single_task(task_cfg):
                    self.results.tasks_completed += 1
                else:
                    self.results.errors.append(f"Task {task_name} failed")
                    success = False

                if self.settings.error_handling.fail_fast:
                    break

        return success

    def run_single_task(self, task_config: m.Quality.ScheduleTaskConfig) -> bool:
        """Run a single maintenance task using appropriate Python libraries."""
        try:
            command = task_config.command
            description = task_config.description
            timeout = task_config.timeout

            # Parse command to determine type
            cmd_parts: t.StrSequence = shlex.split(command) if command else []

            if not cmd_parts:
                self.results.errors.append(f"Empty command in task: {description}")
                return False

            cmd_name = cmd_parts[0]

            # Route to appropriate handler based on command type
            handler = self._get_command_handler(cmd_name)
            if handler:
                return handler(cmd_parts, timeout, description)

            # If no specific handler, log unsupported command
            self.results.warnings.append(
                f"Unsupported command: {cmd_name} in task: {description}. "
                "Please install appropriate Python libraries or configure supported commands.",
            )
            return False

        except (OSError, RuntimeError, ValueError, KeyError) as e:
            self.results.errors.append(
                f"Task error: {task_config.description} - {e!s}",
            )
            return False

    def _get_command_handler(
        self,
        cmd_name: str,
    ) -> Callable[[t.StrSequence, int, str], bool] | None:
        """Get handler for command type."""
        handlers: t.MappingKV[str, Callable[[t.StrSequence, int, str], bool]] = {
            "python": self._handle_python_command,
            "pytest": self._handle_pytest_command,
            "make": self._handle_make_command,
            "git": self._handle_git_command,
            "echo": self._handle_echo_command,
        }
        handler: Callable[[t.StrSequence, int, str], bool] | None = handlers.get(
            cmd_name,
        )
        return handler

    def _handle_python_command(
        self,
        cmd_parts: t.StrSequence,
        timeout: int,
        description: str,
    ) -> bool:
        """Handle python -m commands."""
        try:
            if len(cmd_parts) < self.MIN_PYTHON_ARGS or cmd_parts[1] != "-m":
                self.results.warnings.append(
                    f"Invalid python command format in task: {description}",
                )
                return False

            module_name = (
                cmd_parts[self.MIN_PYTHON_MODULE_INDEX]
                if len(cmd_parts) > self.MIN_PYTHON_MODULE_INDEX
                else None
            )
            if module_name is None:
                self.results.warnings.append(
                    f"No module specified in task: {description}",
                )
                return False

            # For pytest
            if module_name == "pytest":
                return self._handle_pytest_command(cmd_parts[1:], timeout, description)

            # For other modules, use runpy
            mod_name = module_name

            def run_module() -> None:
                runpy.run_module(mod_name, run_name="__main__", alter_sys=True)

            return self._run_with_timeout(run_module, timeout, description)

        except (ImportError, ModuleNotFoundError, RuntimeError, OSError) as e:
            self.results.errors.append(
                f"Python command failed in {description}: {e!s}",
            )
            return False

    def _handle_pytest_command(
        self,
        cmd_parts: t.StrSequence,
        timeout: int,
        description: str,
    ) -> bool:
        """Handle pytest commands."""
        try:
            # Extract pytest arguments (skip 'pytest' itself)
            pytest_args = cmd_parts[1:] if cmd_parts[0] == "pytest" else cmd_parts

            def run_tests() -> None:
                exit_code = pytest.main(list(pytest_args))
                if exit_code != 0:
                    error_msg = f"pytest exited with code {exit_code}"
                    raise RuntimeError(error_msg)

            return self._run_with_timeout(run_tests, timeout, description)
        except (RuntimeError, OSError, ImportError) as e:
            self.results.errors.append(
                f"pytest command failed in {description}: {e!s}",
            )
            return False

    def _handle_make_command(
        self,
        cmd_parts: t.StrSequence,
        timeout: int,
        description: str,
    ) -> bool:
        """Handle make commands."""
        # Note: timeout parameter reserved for future make execution timeout implementation
        _ = timeout  # Reserved for future use

        try:
            makefile = self.project_root / "Makefile"
            if not makefile.exists():
                self.results.warnings.append(
                    f"Makefile not found for task: {description}",
                )
                return False

            # Parse make command
            empty_targets: t.StrSequence = []
            targets = cmd_parts[1:] if len(cmd_parts) > 1 else empty_targets

            # Execute make target by reading Makefile and running corresponding command
            if not targets:
                targets = ["default"]  # Use default target if none specified
            # For now, log a warning suggesting direct command execution
            self.results.warnings.append(
                f"Make command '{' '.join(cmd_parts)}' requires make tool. "
                f"For task: {description}, consider specifying the actual command directly.",
            )
            return False

        except (FileNotFoundError, OSError, RuntimeError) as e:
            self.results.errors.append(
                f"Make command failed in {description}: {e!s}",
            )
            return False

    def _handle_git_command(
        self,
        cmd_parts: t.StrSequence,
        timeout: int,
        description: str,
    ) -> bool:
        """Handle git commands using GitPython."""
        try:
            repo = Repo(self.project_root)
            git = repo.git

            # Extract git subcommand
            if len(cmd_parts) < self.MIN_GIT_ARGS:
                self.results.warnings.append(
                    f"Invalid git command format in task: {description}",
                )
                return False

            subcommand = cmd_parts[1]
            empty_args: t.StrSequence = []
            args = (
                cmd_parts[self.MIN_GIT_ARGS :]
                if len(cmd_parts) > self.MIN_GIT_ARGS
                else empty_args
            )

            def run_git_command() -> None:
                # Use repo.git.execute() for arbitrary git commands
                result = git.execute([subcommand, *args])
                if not result:
                    msg = f"git {subcommand} returned empty result"
                    raise RuntimeError(msg)

            return self._run_with_timeout(run_git_command, timeout, description)
        except InvalidGitRepositoryError:
            self.results.warnings.append(
                f"Not a git repository for task: {description}",
            )
            return False
        except c.EXC_OS_RUNTIME_VALUE as e:
            self.results.errors.append(
                f"Git command failed in {description}: {e!s}",
            )
            return False

    def _handle_echo_command(
        self,
        cmd_parts: t.StrSequence,
        timeout: int,
        description: str,
    ) -> bool:
        """Handle echo commands."""
        # Note: timeout parameter reserved for future echo execution timeout implementation
        _ = timeout  # Reserved for future use

        try:
            message = " ".join(cmd_parts[1:]) if len(cmd_parts) > 1 else ""
            logger.info(message)
            return True
        except c.EXC_OS_VALUE as e:
            self.results.errors.append(
                f"Echo command failed in {description}: {e!s}",
            )
            return False

    def _run_with_timeout(
        self,
        func: Callable[[], None],
        timeout: int,
        description: str,
    ) -> bool:
        """Run a function with timeout using threading."""
        try:
            success = False

            def run_with_result() -> None:
                nonlocal success
                try:
                    func()
                    success = True
                except (OSError, RuntimeError, ValueError, KeyError, ImportError):
                    success = False

            thread = threading.Thread(target=run_with_result, daemon=False)
            thread.start()
            thread.join(timeout=timeout)

            if thread.is_alive():
                self.results.errors.append(f"Task timeout: {description}")
                return False

            if not success:
                self.results.errors.append(f"Task failed: {description}")
                return False

            return success

        except c.EXC_OS_RUNTIME_VALUE as e:
            self.results.errors.append(
                f"Task execution error in {description}: {e!s}",
            )
            return False

    def schedule_tasks(self) -> None:
        """Schedule all maintenance tasks."""
        schedules = self.settings.schedules

        # Daily audit
        if schedules["daily_audit"].enabled:
            daily_audit_job: schedule.Job = schedule.every().day.at(
                schedules["daily_audit"].time,
            )
            daily_audit_do = getattr(daily_audit_job, "do", None)
            if callable(daily_audit_do):
                _ = daily_audit_do(self.run_daily_audit)

        # Daily optimization
        if schedules["daily_optimize"].enabled:
            daily_optimize_job: schedule.Job = schedule.every().day.at(
                schedules["daily_optimize"].time,
            )
            daily_optimize_do = getattr(daily_optimize_job, "do", None)
            if callable(daily_optimize_do):
                _ = daily_optimize_do(self.run_daily_optimize)

        # Weekly comprehensive
        if schedules["weekly_comprehensive"].enabled:
            day = schedules["weekly_comprehensive"].day
            time_str = schedules["weekly_comprehensive"].time

            if isinstance(day, str):
                getattr(schedule.every(), day).at(time_str).do(
                    self.run_weekly_comprehensive,
                )

        # Monthly deep clean
        if schedules["monthly_deep_clean"].enabled:
            # Schedule for the 1st of every month
            monthly_deep_clean_job: schedule.Job = schedule.every(4).weeks.at("11:00")
            monthly_deep_clean_do = getattr(monthly_deep_clean_job, "do", None)
            if callable(monthly_deep_clean_do):
                _ = monthly_deep_clean_do(self.run_monthly_deep_clean)

    def run_daemon(self) -> None:
        """Run the maintenance system as a daemon."""
        # Schedule all tasks
        self.schedule_tasks()

        # Show scheduled tasks
        for _job in schedule.jobs:
            pass

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.save_results()

    def run_manual(self, task_type: str) -> bool:
        """Run maintenance tasks manually."""
        task_map = {
            "daily": self.run_daily_audit,
            "optimize": self.run_daily_optimize,
            "weekly": self.run_weekly_comprehensive,
            "monthly": self.run_monthly_deep_clean,
            "all": lambda: all([
                self.run_daily_audit(),
                self.run_daily_optimize(),
                self.run_weekly_comprehensive(),
                self.run_monthly_deep_clean(),
            ]),
        }

        if task_type in task_map:
            success = task_map[task_type]()
            self.save_results()
            return success
        return False

    def save_results(self) -> None:
        """Save maintenance results to file."""
        self.results.end_time = datetime.now(UTC).isoformat()
        self.results.duration_seconds = int(
            (
                datetime.fromisoformat(self.results.end_time)
                - datetime.fromisoformat(self.results.start_time)
            ).total_seconds(),
        )

        results_file = (
            self.reports_dir
            / f"maintenance_results_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        )

        Path(results_file).write_text(
            self.results.model_dump_json(indent=2),
            encoding="utf-8",
        )


class _ScheduledMaintenanceCommand(s[bool]):
    """CLI command for FLEXT Quality scheduled documentation maintenance."""

    DEFAULT_CONFIG: ClassVar[str] = str(_docs_config_file("schedule_config.yaml"))

    settings_path: Annotated[
        str,
        cli_u.Field(
            default_factory=lambda: _ScheduledMaintenanceCommand.DEFAULT_CONFIG,
            alias="settings",
            description="Maintenance schedule configuration file",
        ),
    ]
    daemon: Annotated[
        bool,
        cli_u.Field(default=False, description="Run as daemon with scheduled tasks"),
    ] = False
    manual: Annotated[
        str | None,
        cli_u.Field(
            default=None,
            description="Run specific manual task: daily|optimize|weekly|monthly|all",
        ),
    ] = None
    list_schedules: Annotated[
        bool,
        cli_u.Field(default=False, description="List all configured schedules"),
    ] = False

    @override
    def execute(self) -> p.Result[bool]:
        """Dispatch to the appropriate maintenance action."""
        maintenance = FlextQualityScheduledMaintenance(self.settings_path)
        if self.list_schedules:
            for _schedule_config in maintenance.settings.schedules.values():
                pass
            return r[bool].ok(value=True)
        if self.daemon:
            maintenance.run_daemon()
            return r[bool].ok(value=True)
        if self.manual:
            return (
                r[bool].ok(value=True)
                if maintenance.run_manual(self.manual)
                else r[bool].fail(f"Manual task '{self.manual}' failed")
            )
        return r[bool].fail(
            "No action selected (use --daemon, --manual or --list-schedules)"
        )


def main(args: t.StrSequence | None = None) -> int:
    """Main entry point for scheduled maintenance via the canonical cli facade."""
    app = cli.create_app_with_common_params(
        name="flext-quality-scheduled-maintenance",
        help_text="FLEXT Quality Scheduled Documentation Maintenance",
    )
    cli.register_result_routes(
        app,
        [
            cli_m.Cli.ResultCommandRoute(
                name="run",
                help_text=(
                    "Run scheduled maintenance (use --daemon, --manual or "
                    "--list-schedules)"
                ),
                model_cls=_ScheduledMaintenanceCommand,
                handler=lambda params: params.execute(),
            ),
        ],
    )
    outcome = cli.execute_app(
        app,
        prog_name="flext-quality-scheduled-maintenance",
        args=list(args) if args is not None else sys.argv[1:],
    )
    return 0 if outcome.success else 1


if __name__ == "__main__":
    cli.exit(main())
