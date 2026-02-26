#!/usr/bin/env python3
"""FLEXT Quality Scheduled Documentation Maintenance.

Automated scheduled maintenance system for regular documentation quality checks,
optimizations, and reporting. Designed to run as a cron job or scheduled task.
"""

import argparse
import json
import runpy
import shlex
import sys
import threading
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import schedule
import yaml
from git import InvalidGitRepositoryError, Repo


class ScheduledMaintenance:
    """Scheduled documentation maintenance system."""

    # Command parsing constants
    MIN_PYTHON_ARGS = 2  # python -m is minimum 2 parts
    MIN_GIT_ARGS = 2  # git <subcommand> is minimum 2 parts
    MIN_PYTHON_MODULE_INDEX = 2  # module name is at index 2 (python -m module_name)

    def __init__(
        self,
        config_path: str = "docs/maintenance/config/schedule_config.yaml",
    ) -> None:
        """Initialize scheduled maintenance system.

        Args:
            config_path: Path to configuration file for maintenance schedule.

        """
        self.load_config(config_path)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.reports_dir = Path(
            self.config.get("reports_dir", "docs/maintenance/reports/"),
        )
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Initialize results tracking
        self.results = {
            "start_time": datetime.now(UTC).isoformat(),
            "tasks_completed": 0,
            "errors": [],
            "warnings": [],
        }

    def load_config(self, config_path: str) -> None:
        """Load maintenance schedule configuration."""
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = self.get_default_config()

    def get_default_config(self) -> dict[str, Any]:
        """Default maintenance configuration."""
        return {
            "enabled": True,
            "reports_dir": "docs/maintenance/reports/",
            "backup_dir": "docs/maintenance/backups/",
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
                    "command": "python docs/maintenance/scripts/audit.py --check-freshness --check-completeness --output docs/maintenance/reports/",
                    "timeout": 300,
                },
                "audit_comprehensive": {
                    "description": "Full comprehensive audit",
                    "command": "python docs/maintenance/scripts/audit.py --comprehensive --output docs/maintenance/reports/",
                    "timeout": 600,
                },
                "validate_links": {
                    "description": "Validate all links and references",
                    "command": "python docs/maintenance/scripts/validate.py --external-links --internal-links --images --output docs/maintenance/reports/",
                    "timeout": 300,
                },
                "check_critical": {
                    "description": "Check for critical issues and send alerts",
                    "command": "python docs/maintenance/notifications.py --audit-data docs/maintenance/reports/latest_audit.json",
                    "timeout": 60,
                },
                "optimize_formatting": {
                    "description": "Auto-fix formatting issues",
                    "command": "python docs/maintenance/scripts/optimize.py --fix-formatting --backup --output docs/maintenance/reports/",
                    "timeout": 300,
                },
                "optimize_full": {
                    "description": "Full optimization suite",
                    "command": "python docs/maintenance/scripts/optimize.py --comprehensive --backup --output docs/maintenance/reports/",
                    "timeout": 600,
                },
                "update_toc": {
                    "description": "Update table of contents",
                    "command": "python docs/maintenance/scripts/optimize.py --update-toc --output docs/maintenance/reports/",
                    "timeout": 180,
                },
                "generate_report": {
                    "description": "Generate quality report",
                    "command": "python docs/maintenance/scripts/report.py --format html --output docs/maintenance/reports/",
                    "timeout": 120,
                },
                "generate_monthly_report": {
                    "description": "Generate comprehensive monthly report",
                    "command": "python docs/maintenance/scripts/report.py --monthly-trends --format html --output docs/maintenance/reports/",
                    "timeout": 180,
                },
                "notify_weekly": {
                    "description": "Send weekly notification",
                    "command": "python docs/maintenance/notifications.py --weekly-report docs/maintenance/reports/latest_audit.json",
                    "timeout": 60,
                },
                "cleanup_old_reports": {
                    "description": "Clean up old report files",
                    "command": 'find docs/maintenance/reports/ -name "*.json" -mtime +90 -delete',
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
                "log_file": "docs/maintenance/logs/scheduled_maintenance.log",
                "max_log_size": "10MB",
                "retention_days": 30,
            },
        }

    def run_daily_audit(self) -> bool:
        """Run daily audit tasks."""
        return self.run_tasks(self.config["schedules"]["daily_audit"]["tasks"])

    def run_daily_optimize(self) -> bool:
        """Run daily optimization tasks."""
        return self.run_tasks(self.config["schedules"]["daily_optimize"]["tasks"])

    def run_weekly_comprehensive(self) -> bool:
        """Run weekly comprehensive maintenance."""
        return self.run_tasks(self.config["schedules"]["weekly_comprehensive"]["tasks"])

    def run_monthly_deep_clean(self) -> bool:
        """Run monthly deep cleaning maintenance."""
        return self.run_tasks(self.config["schedules"]["monthly_deep_clean"]["tasks"])

    def run_tasks(self, task_names: list[str]) -> bool:
        """Run a list of maintenance tasks."""
        success = True

        for task_name in task_names:
            if task_name in self.config["tasks"]:
                task_config = self.config["tasks"][task_name]

                if self.run_single_task(task_config):
                    self.results["tasks_completed"] += 1
                else:
                    self.results["errors"].append(f"Task {task_name} failed")
                    success = False

                    if self.config["error_handling"]["fail_fast"]:
                        break

        return success

    def run_single_task(self, task_config: dict) -> bool:
        """Run a single maintenance task using appropriate Python libraries."""
        try:
            command = task_config["command"]
            description = task_config["description"]
            timeout = task_config.get("timeout", 300)

            # Parse command to determine type
            cmd_parts = shlex.split(command) if isinstance(command, str) else command

            if not cmd_parts:
                self.results["errors"].append(f"Empty command in task: {description}")
                return False

            cmd_name = cmd_parts[0]

            # Route to appropriate handler based on command type
            handler = self._get_command_handler(cmd_name)
            if handler:
                return handler(cmd_parts, timeout, description)

            # If no specific handler, log unsupported command
            self.results["warnings"].append(
                f"Unsupported command: {cmd_name} in task: {description}. "
                "Please install appropriate Python libraries or configure supported commands.",
            )
            return False

        except Exception as e:
            self.results["errors"].append(
                f"Task error: {task_config.get('description', 'unknown')} - {e!s}",
            )
            return False

    def _get_command_handler(
        self,
        cmd_name: str,
    ) -> Callable[[list[str], int, str], bool] | None:
        """Get handler for command type."""
        handlers: dict[str, Callable] = {
            "python": self._handle_python_command,
            "pytest": self._handle_pytest_command,
            "make": self._handle_make_command,
            "git": self._handle_git_command,
            "echo": self._handle_echo_command,
        }
        return handlers.get(cmd_name)

    def _handle_python_command(
        self,
        cmd_parts: list[str],
        timeout: int,
        description: str,
    ) -> bool:
        """Handle python -m commands."""
        try:
            if len(cmd_parts) < self.MIN_PYTHON_ARGS or cmd_parts[1] != "-m":
                self.results["warnings"].append(
                    f"Invalid python command format in task: {description}",
                )
                return False

            module_name = (
                cmd_parts[self.MIN_PYTHON_MODULE_INDEX]
                if len(cmd_parts) > self.MIN_PYTHON_MODULE_INDEX
                else None
            )
            if module_name is None:
                self.results["warnings"].append(
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

        except Exception as e:
            self.results["errors"].append(
                f"Python command failed in {description}: {e!s}",
            )
            return False

    def _handle_pytest_command(
        self,
        cmd_parts: list[str],
        timeout: int,
        description: str,
    ) -> bool:
        """Handle pytest commands."""
        try:
            # Extract pytest arguments (skip 'pytest' itself)
            pytest_args = cmd_parts[1:] if cmd_parts[0] == "pytest" else cmd_parts

            def run_tests() -> None:
                exit_code = pytest.main(pytest_args)
                if exit_code != 0:
                    error_msg = f"pytest exited with code {exit_code}"
                    raise RuntimeError(error_msg)

            return self._run_with_timeout(run_tests, timeout, description)

        except ImportError:
            self.results["warnings"].append(
                f"pytest not available for task: {description}. Install with: pip install pytest",
            )
            return False
        except Exception as e:
            self.results["errors"].append(
                f"pytest command failed in {description}: {e!s}",
            )
            return False

    def _handle_make_command(
        self,
        cmd_parts: list[str],
        timeout: int,
        description: str,
    ) -> bool:
        """Handle make commands."""
        # Note: timeout parameter reserved for future make execution timeout implementation
        _ = timeout  # Reserved for future use

        try:
            makefile = self.project_root / "Makefile"
            if not makefile.exists():
                self.results["warnings"].append(
                    f"Makefile not found for task: {description}",
                )
                return False

            # Parse make command
            targets = cmd_parts[1:] if len(cmd_parts) > 1 else []

            # Execute make target by reading Makefile and running corresponding command
            if not targets:
                targets = ["default"]  # Use default target if none specified
            # For now, log a warning suggesting direct command execution
            self.results["warnings"].append(
                f"Make command '{' '.join(cmd_parts)}' requires make tool. "
                f"For task: {description}, consider specifying the actual command directly.",
            )
            return False

        except Exception as e:
            self.results["errors"].append(
                f"Make command failed in {description}: {e!s}",
            )
            return False

    def _handle_git_command(
        self,
        cmd_parts: list[str],
        timeout: int,
        description: str,
    ) -> bool:
        """Handle git commands using GitPython."""
        try:
            repo = Repo(self.project_root)
            git = repo.git

            # Extract git subcommand
            if len(cmd_parts) < self.MIN_GIT_ARGS:
                self.results["warnings"].append(
                    f"Invalid git command format in task: {description}",
                )
                return False

            subcommand = cmd_parts[1]
            args = (
                cmd_parts[self.MIN_GIT_ARGS :]
                if len(cmd_parts) > self.MIN_GIT_ARGS
                else []
            )

            def run_git_command() -> None:
                # Use repo.git.execute() for arbitrary git commands
                result = git.execute([subcommand] + args)
                if not result:
                    msg = f"git {subcommand} returned empty result"
                    raise RuntimeError(msg)

            return self._run_with_timeout(run_git_command, timeout, description)

        except ImportError:
            self.results["warnings"].append(
                f"GitPython not available for task: {description}. Install with: pip install GitPython",
            )
            return False
        except InvalidGitRepositoryError:
            self.results["warnings"].append(
                f"Not a git repository for task: {description}",
            )
            return False
        except Exception as e:
            self.results["errors"].append(f"Git command failed in {description}: {e!s}")
            return False

    def _handle_echo_command(
        self,
        cmd_parts: list[str],
        timeout: int,
        description: str,
    ) -> bool:
        """Handle echo commands."""
        # Note: timeout parameter reserved for future echo execution timeout implementation
        _ = timeout  # Reserved for future use

        try:
            message = " ".join(cmd_parts[1:]) if len(cmd_parts) > 1 else ""
            print(message)
            return True
        except Exception as e:
            self.results["errors"].append(
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
            result_container: dict[str, Any] = {"success": False, "exception": None}

            def run_with_result() -> None:
                try:
                    func()
                    result_container["success"] = True
                except Exception as e:
                    result_container["exception"] = e

            thread = threading.Thread(target=run_with_result, daemon=False)
            thread.start()
            thread.join(timeout=timeout)

            if thread.is_alive():
                self.results["errors"].append(f"Task timeout: {description}")
                return False

            if result_container["exception"]:
                self.results["errors"].append(
                    f"Task failed: {description} - {result_container['exception']!s}",
                )
                return False

            return result_container["success"]

        except Exception as e:
            self.results["errors"].append(
                f"Task execution error in {description}: {e!s}",
            )
            return False

    def schedule_tasks(self) -> None:
        """Schedule all maintenance tasks."""
        schedules = self.config["schedules"]

        # Daily audit
        if schedules["daily_audit"]["enabled"]:
            schedule.every().day.at(schedules["daily_audit"]["time"]).do(
                self.run_daily_audit,
            )

        # Daily optimization
        if schedules["daily_optimize"]["enabled"]:
            schedule.every().day.at(schedules["daily_optimize"]["time"]).do(
                self.run_daily_optimize,
            )

        # Weekly comprehensive
        if schedules["weekly_comprehensive"]["enabled"]:
            day = schedules["weekly_comprehensive"]["day"]
            time_str = schedules["weekly_comprehensive"]["time"]

            getattr(schedule.every(), day).at(time_str).do(
                self.run_weekly_comprehensive,
            )

        # Monthly deep clean
        if schedules["monthly_deep_clean"]["enabled"]:
            # Schedule for the 1st of every month
            schedule.every(4).weeks.at("11:00").do(self.run_monthly_deep_clean)

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
        self.results["end_time"] = datetime.now(UTC).isoformat()
        self.results["duration_seconds"] = int(
            (
                datetime.fromisoformat(self.results["end_time"])
                - datetime.fromisoformat(self.results["start_time"])
            ).total_seconds()
        )

        results_file = (
            self.reports_dir
            / f"maintenance_results_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        )

        with Path(results_file).open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)


def main() -> None:
    """Main entry point for scheduled maintenance."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Scheduled Documentation Maintenance",
    )
    parser.add_argument(
        "--config",
        default="docs/maintenance/config/schedule_config.yaml",
        help="Maintenance schedule configuration file",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as daemon with scheduled tasks",
    )
    parser.add_argument(
        "--manual",
        choices=["daily", "optimize", "weekly", "monthly", "all"],
        help="Run specific maintenance tasks manually",
    )
    parser.add_argument(
        "--list-schedules",
        action="store_true",
        help="List all configured schedules",
    )

    args = parser.parse_args()

    maintenance = ScheduledMaintenance(args.config)

    if args.list_schedules:
        for schedule_config in maintenance.config["schedules"].values():
            if schedule_config["enabled"]:
                pass

    elif args.daemon:
        maintenance.run_daemon()

    elif args.manual:
        success = maintenance.run_manual(args.manual)
        if success:
            pass
        else:
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
