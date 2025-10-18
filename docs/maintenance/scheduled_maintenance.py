#!/usr/bin/env python3
"""FLEXT Quality Scheduled Documentation Maintenance.

Automated scheduled maintenance system for regular documentation quality checks,
optimizations, and reporting. Designed to run as a cron job or scheduled task.
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import schedule
import yaml


class ScheduledMaintenance:
    """Scheduled documentation maintenance system."""

    def __init__(
        self, config_path: str = "docs/maintenance/config/schedule_config.yaml"
    ) -> None:
        """Initialize scheduled maintenance system.

        Args:
            config_path: Path to configuration file for maintenance schedule.

        """
        self.load_config(config_path)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.reports_dir = Path(
            self.config.get("reports_dir", "docs/maintenance/reports/")
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

    def get_default_config(self) -> dict[str, object]:
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
        """Run a single maintenance task."""
        try:
            # Change to project root directory
            result = subprocess.run(  # noqa: S602
                task_config["command"],
                check=False,
                shell=True,
                cwd=self.project_root,
                timeout=task_config.get("timeout", 300),
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return True
            self.results["warnings"].append(
                f"Task failed: {task_config['description']} - {result.stderr}"
            )
            return False

        except subprocess.TimeoutExpired:
            self.results["errors"].append(f"Task timeout: {task_config['description']}")
            return False
        except Exception as e:
            self.results["errors"].append(
                f"Task error: {task_config['description']} - {e!s}"
            )
            return False

    def schedule_tasks(self) -> None:
        """Schedule all maintenance tasks."""
        schedules = self.config["schedules"]

        # Daily audit
        if schedules["daily_audit"]["enabled"]:
            schedule.every().day.at(schedules["daily_audit"]["time"]).do(
                self.run_daily_audit
            )

        # Daily optimization
        if schedules["daily_optimize"]["enabled"]:
            schedule.every().day.at(schedules["daily_optimize"]["time"]).do(
                self.run_daily_optimize
            )

        # Weekly comprehensive
        if schedules["weekly_comprehensive"]["enabled"]:
            day = schedules["weekly_comprehensive"]["day"]
            time_str = schedules["weekly_comprehensive"]["time"]

            getattr(schedule.every(), day).at(time_str).do(
                self.run_weekly_comprehensive
            )

        # Monthly deep clean
        if schedules["monthly_deep_clean"]["enabled"]:
            # Schedule for the 1st of every month
            schedule.every().month.at("01 11:00").do(self.run_monthly_deep_clean)

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
        self.results["duration_seconds"] = (
            datetime.fromisoformat(self.results["end_time"])
            - datetime.fromisoformat(self.results["start_time"])
        ).total_seconds()

        results_file = (
            self.reports_dir
            / f"maintenance_results_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        )

        with Path(results_file).open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)


def main() -> None:
    """Main entry point for scheduled maintenance."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Scheduled Documentation Maintenance"
    )
    parser.add_argument(
        "--config",
        default="docs/maintenance/config/schedule_config.yaml",
        help="Maintenance schedule configuration file",
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Run as daemon with scheduled tasks"
    )
    parser.add_argument(
        "--manual",
        choices=["daily", "optimize", "weekly", "monthly", "all"],
        help="Run specific maintenance tasks manually",
    )
    parser.add_argument(
        "--list-schedules", action="store_true", help="List all configured schedules"
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
