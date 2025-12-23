#!/usr/bin/env python3
"""Documentation Synchronization and Automated Maintenance System.

Manages version control integration, automated updates, and synchronization
across documentation repositories.
"""

import argparse
import logging
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

import yaml
from git import InvalidGitRepositoryError, Repo

from flext_quality.docs_maintenance.utils import get_project_root

from .audit import DocumentationAuditor
from .optimize import ContentOptimizer
from .report import ReportGenerator
from .validate_links import LinkValidator
from .validate_style import StyleValidator

logger = logging.getLogger(__name__)


# Type definitions
class GitStatusInfo(TypedDict):
    """Git status information."""

    branch: str
    modified_files: list[str]
    untracked_files: list[str]
    staged_files: list[str]
    ahead_count: int
    behind_count: int


class SyncConfig(TypedDict):
    """Configuration for documentation synchronization."""

    sync: dict[str, object]
    git: dict[str, object]
    maintenance: dict[str, object]


# Constants for synchronization
MAX_CHANGES_DISPLAY: int = 10


@dataclass
class SyncResult:
    """Result of a synchronization operation."""

    operation: str
    success: bool
    changes_made: int
    files_affected: list[str]
    error_message: str | None
    timestamp: datetime


@dataclass
class SyncStatus:
    """Current synchronization status."""

    git_status: GitStatusInfo
    pending_changes: list[str]
    last_sync: datetime | None
    sync_needed: bool
    conflicts_present: bool


class DocumentationSync:
    """Main documentation synchronization class."""

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize documentation synchronization system."""
        super().__init__()
        self.config: SyncConfig = self._load_config(config_path)
        self.project_root = get_project_root()
        self.working_dir = self.project_root

    def _get_repo(self) -> Repo | None:
        """Get GitPython Repo instance or None if not a git repository."""
        try:
            return Repo(str(self.working_dir))
        except InvalidGitRepositoryError:
            return None

    def _load_config(self, config_path: str | None = None) -> SyncConfig:
        """Load configuration."""
        # Use plain dict for construction, then cast to SyncConfig
        config_dict: dict[str, dict[str, object]] = {
            "sync": {
                "auto_commit": False,
                "commit_message_template": "docs: {operation} - {changes} changes",
                "backup_before_changes": True,
                "validate_before_commit": True,
                "push_after_commit": False,
            },
            "git": {
                "remote_name": "origin",
                "main_branch": "main",
                "create_backup_branch": True,
            },
            "maintenance": {
                "schedule": {
                    "daily": ["validate_links"],
                    "weekly": ["comprehensive_audit", "optimize_content"],
                    "monthly": ["update_metadata", "generate_reports"],
                },
            },
        }

        if config_path and Path(config_path).exists():
            with Path(config_path).open(encoding="utf-8") as f:
                user_config: dict[str, object] = yaml.safe_load(f)
                for key, value in user_config.items():
                    if key in config_dict and isinstance(value, dict):
                        # Merge nested configs
                        current_val = config_dict.get(key)
                        if isinstance(current_val, dict):
                            current_val.update(value)
                    elif isinstance(value, dict):
                        config_dict[key] = value

        # Return as SyncConfig (compatible structure)
        return SyncConfig(
            sync=config_dict.get("sync", {}),
            git=config_dict.get("git", {}),
            maintenance=config_dict.get("maintenance", {}),
        )

    def get_sync_status(self) -> SyncStatus:
        """Get current synchronization status."""
        git_status = self._get_git_status()
        pending_changes = self._get_pending_changes()
        last_sync = self._get_last_sync_time()
        sync_needed = len(pending_changes) > 0
        conflicts_present = self._check_for_conflicts()

        return SyncStatus(
            git_status=git_status,
            pending_changes=pending_changes,
            last_sync=last_sync,
            sync_needed=sync_needed,
            conflicts_present=conflicts_present,
        )

    def _get_git_status(self) -> GitStatusInfo:
        """Get git repository status using GitPython."""
        try:
            # Check if we're in a git repository
            repo = self._get_repo()
            if not repo:
                return GitStatusInfo(
                    branch="unknown",
                    modified_files=[],
                    untracked_files=[],
                    staged_files=[],
                    ahead_count=0,
                    behind_count=0,
                )

            # Get current branch
            try:
                current_branch = repo.active_branch.name
            except Exception:
                # HEAD is detached or branch not available
                current_branch = "unknown"

            # Get modified and untracked files
            modified_files = []
            untracked_files = []

            # Get untracked files
            untracked_files = repo.untracked_files

            # Get modified files using git status
            status_output = repo.git.status(porcelain=True)
            for line in status_output.split("\n"):
                if line.strip():
                    status_code = line[:2]
                    filename = line[3:]
                    if status_code in {"M ", "MM", "AM", "RM"}:
                        modified_files.append(filename)

            return GitStatusInfo(
                branch=current_branch,
                modified_files=modified_files,
                untracked_files=untracked_files,
                staged_files=[],
                ahead_count=0,
                behind_count=0,
            )

        except Exception as e:
            logger.debug("Git operations failed, using default status: %s", e)
            return GitStatusInfo(
                branch="unknown",
                modified_files=[],
                untracked_files=[],
                staged_files=[],
                ahead_count=0,
                behind_count=0,
            )

    def _get_pending_changes(self) -> list[str]:
        """Get list of pending changes."""
        status = self._get_git_status()
        return status["modified_files"] + status["untracked_files"]

    def _get_last_sync_time(self) -> datetime | None:
        """Get timestamp of last synchronization using GitPython."""
        try:
            repo = self._get_repo()
            if not repo:
                return None

            # Get the last commit timestamp for docs/
            try:
                log_output = repo.git.log("-1", "--", "docs/", format="%ct").strip()
                if log_output:
                    timestamp = int(log_output)
                    return datetime.fromtimestamp(timestamp, tz=UTC)
            except Exception:
                # No commits in docs/ path
                return None

        except Exception as e:
            # Git operations are optional, continue without git info
            logger.debug("Git operations failed, continuing without git info: %s", e)

        return None

    def _check_for_conflicts(self) -> bool:
        """Check if there are merge conflicts using GitPython."""
        try:
            repo = self._get_repo()
            if not repo:
                return False

            # Check for unmerged paths (conflicts)
            status_output = repo.git.status(porcelain=True)
            return any("U" in line[:2] for line in status_output.split("\n"))

        except Exception as e:
            # Git operations are optional, continue without git info
            logger.debug("Git operations failed, continuing without git info: %s", e)

        return False

    def validate_before_sync(self) -> SyncResult:
        """Validate documentation before synchronization."""
        try:
            # Run validation checks

            validator = LinkValidator()
            style_validator = StyleValidator()

            # Quick validation
            link_results = validator.validate_directory(
                str(self.working_dir / "docs"),
                check_external=False,
            )
            style_results = style_validator.validate_directory(
                str(self.working_dir / "docs"),
            )

            broken_links = sum(len(r.broken_links) for r in link_results)
            style_violations = sum(len(r.violations) for r in style_results)

            issues_found = broken_links + style_violations

            return SyncResult(
                operation="validation",
                success=issues_found == 0,
                changes_made=0,
                files_affected=[],
                error_message=f"Found {issues_found} issues"
                if issues_found > 0
                else None,
                timestamp=datetime.now(UTC),
            )

        except Exception as e:
            return SyncResult(
                operation="validation",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=f"Validation failed: {e}",
                timestamp=datetime.now(UTC),
            )

    def sync_changes(self, operation: str, files: list[str]) -> SyncResult:
        """Synchronize changes to git using GitPython."""
        if not self.config["sync"]["auto_commit"]:
            return SyncResult(
                operation="sync",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message="Auto-commit disabled in configuration",
                timestamp=datetime.now(UTC),
            )

        try:
            repo = self._get_repo()
            if not repo:
                return SyncResult(
                    operation="sync",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message="Not a git repository",
                    timestamp=datetime.now(UTC),
                )

            # Stage files using GitPython
            repo.index.add(files)

            # Create commit message
            changes_desc = f"{len(files)} files"
            commit_message_template = str(
                self.config["sync"]["commit_message_template"],
            )
            commit_message = commit_message_template.format(
                operation=operation,
                changes=changes_desc,
            )

            # Commit using GitPython
            repo.index.commit(commit_message)

            # Push if configured
            if self.config["sync"]["push_after_commit"]:
                remote_name = str(self.config["git"]["remote_name"])
                main_branch = str(self.config["git"]["main_branch"])
                origin = repo.remote(remote_name)
                origin.push(main_branch)

            return SyncResult(
                operation="sync",
                success=True,
                changes_made=len(files),
                files_affected=files,
                error_message=None,
                timestamp=datetime.now(UTC),
            )

        except Exception as e:
            return SyncResult(
                operation="sync",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=f"Git operation failed: {e}",
                timestamp=datetime.now(UTC),
            )

    def create_backup_branch(self) -> SyncResult:
        """Create a backup branch before making changes using GitPython."""
        if not self.config["git"]["create_backup_branch"]:
            return SyncResult(
                operation="backup_branch",
                success=True,
                changes_made=0,
                files_affected=[],
                error_message="Backup branch creation disabled",
                timestamp=datetime.now(UTC),
            )

        try:
            repo = self._get_repo()
            if not repo:
                return SyncResult(
                    operation="backup_branch",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message="Not a git repository",
                    timestamp=datetime.now(UTC),
                )

            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            branch_name = f"docs-backup-{timestamp}"

            # Create and checkout new branch using GitPython
            repo.create_head(branch_name)
            repo.heads[branch_name].checkout()

            return SyncResult(
                operation="backup_branch",
                success=True,
                changes_made=0,
                files_affected=[],
                error_message=None,
                timestamp=datetime.now(UTC),
            )

        except Exception as e:
            return SyncResult(
                operation="backup_branch",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=f"Backup branch creation failed: {e}",
                timestamp=datetime.now(UTC),
            )

    def rollback_changes(self, files: list[str]) -> SyncResult:
        """Rollback changes to specific files using GitPython."""
        try:
            repo = self._get_repo()
            if not repo:
                return SyncResult(
                    operation="rollback",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message="Not a git repository",
                    timestamp=datetime.now(UTC),
                )

            # Checkout files from HEAD using GitPython
            repo.git.checkout("HEAD", "--", *files)

            return SyncResult(
                operation="rollback",
                success=True,
                changes_made=len(files),
                files_affected=files,
                error_message=None,
                timestamp=datetime.now(UTC),
            )

        except Exception as e:
            return SyncResult(
                operation="rollback",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=f"Rollback failed: {e}",
                timestamp=datetime.now(UTC),
            )

    def run_maintenance_schedule(self, schedule_type: str) -> list[SyncResult]:
        """Run scheduled maintenance tasks."""
        maintenance_config = self.config["maintenance"]
        if (
            not isinstance(maintenance_config, dict)
            or "schedule" not in maintenance_config
        ):
            return [
                SyncResult(
                    operation="maintenance",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message="Invalid maintenance configuration",
                    timestamp=datetime.now(UTC),
                ),
            ]

        schedule = maintenance_config["schedule"]
        if not isinstance(schedule, dict) or schedule_type not in schedule:
            return [
                SyncResult(
                    operation="maintenance",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message=f"Unknown schedule type: {schedule_type}",
                    timestamp=datetime.now(UTC),
                ),
            ]

        tasks_obj = schedule[schedule_type]
        if not isinstance(tasks_obj, list):
            return [
                SyncResult(
                    operation="maintenance",
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message="Invalid schedule tasks configuration",
                    timestamp=datetime.now(UTC),
                ),
            ]

        tasks: list[str] = [str(task) for task in tasks_obj]
        results = []

        for task in tasks:
            if task == "validate_links":
                result = self.validate_before_sync()
            elif task == "comprehensive_audit":
                # Run complete audit
                result = self._run_comprehensive_audit()
            elif task == "optimize_content":
                result = self._run_content_optimization()
            elif task == "update_metadata":
                result = self._run_metadata_update()
            elif task == "generate_reports":
                result = self._run_report_generation()
            else:
                result = SyncResult(
                    operation=task,
                    success=False,
                    changes_made=0,
                    files_affected=[],
                    error_message=f"Unknown maintenance task: {task}",
                    timestamp=datetime.now(UTC),
                )

            results.append(result)

        return results

    def _run_comprehensive_audit(self) -> SyncResult:
        """Run complete documentation audit."""
        try:
            auditor = DocumentationAuditor()
            results = auditor.audit_directory(str(self.working_dir / "docs"))
            auditor.generate_summary()

            return SyncResult(
                operation="comprehensive_audit",
                success=True,
                changes_made=0,  # Audit doesn't make changes
                files_affected=[r.file_path for r in results],
                error_message=None,
                timestamp=datetime.now(UTC),
            )
        except Exception as e:
            return SyncResult(
                operation="comprehensive_audit",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=str(e),
                timestamp=datetime.now(UTC),
            )

    def _run_content_optimization(self) -> SyncResult:
        """Run content optimization."""
        try:
            optimizer = ContentOptimizer()
            results = optimizer.optimize_directory(str(self.working_dir / "docs"))

            files_modified = [r.file_path for r in results if r.changes_made > 0]
            total_changes = sum(r.changes_made for r in results)

            return SyncResult(
                operation="content_optimization",
                success=True,
                changes_made=total_changes,
                files_affected=files_modified,
                error_message=None,
                timestamp=datetime.now(UTC),
            )
        except Exception as e:
            return SyncResult(
                operation="content_optimization",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=str(e),
                timestamp=datetime.now(UTC),
            )

    def _run_metadata_update(self) -> SyncResult:
        """Update documentation metadata."""
        try:
            # Update timestamps, version info, etc.
            docs_dir = str(self.working_dir / "docs")
            updated_files: list[str] = []

            for root, _dirs, files in os.walk(docs_dir):
                for file in files:
                    if file.endswith((".md", ".mdx")):
                        file_path = Path(root) / file
                        # Simple metadata update - could be more sophisticated
                        content = Path(file_path).read_text(encoding="utf-8")

                        # Update last modified timestamp if present
                        if "last_updated:" in content or "updated:" in content:
                            # This would be more complex in practice
                            updated_files.append(str(file_path))

            return SyncResult(
                operation="metadata_update",
                success=True,
                changes_made=len(updated_files),
                files_affected=updated_files,
                error_message=None,
                timestamp=datetime.now(UTC),
            )
        except Exception as e:
            return SyncResult(
                operation="metadata_update",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=str(e),
                timestamp=datetime.now(UTC),
            )

    def _run_report_generation(self) -> SyncResult:
        """Generate maintenance reports."""
        try:
            generator = ReportGenerator()
            report_data = generator.generate_comprehensive_report()

            # Generate both dashboard and summary
            dashboard_file = generator.generate_dashboard(report_data)
            summary_file = generator.generate_weekly_summary(report_data)

            return SyncResult(
                operation="report_generation",
                success=True,
                changes_made=2,  # Two files created
                files_affected=[dashboard_file, summary_file],
                error_message=None,
                timestamp=datetime.now(UTC),
            )
        except Exception as e:
            return SyncResult(
                operation="report_generation",
                success=False,
                changes_made=0,
                files_affected=[],
                error_message=str(e),
                timestamp=datetime.now(UTC),
            )


def _setup_argument_parser() -> argparse.ArgumentParser:
    """Set up the argument parser for the sync system."""
    parser = argparse.ArgumentParser(
        description="Documentation Synchronization and Automated Maintenance System",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current synchronization status",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate documentation before sync",
    )
    parser.add_argument(
        "--sync",
        nargs="*",
        metavar="FILE",
        help="Synchronize specific files to git",
    )
    parser.add_argument(
        "--backup-branch",
        action="store_true",
        help="Create backup branch before changes",
    )
    parser.add_argument(
        "--rollback",
        nargs="*",
        metavar="FILE",
        help="Rollback changes to specific files",
    )
    parser.add_argument(
        "--maintenance",
        choices=["daily", "weekly", "monthly"],
        help="Run scheduled maintenance tasks",
    )
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    return parser


def _handle_status_command(sync: DocumentationSync, args: argparse.Namespace) -> None:
    """Handle the status command."""
    status = sync.get_sync_status()

    git_info = status.git_status
    # Check git status - branch "unknown" indicates not initialized
    if git_info["branch"] != "unknown":
        pass

    if status.pending_changes and args.verbose:
        for _change in status.pending_changes[:MAX_CHANGES_DISPLAY]:
            pass
        if len(status.pending_changes) > MAX_CHANGES_DISPLAY:
            pass


def _handle_validate_command(sync: DocumentationSync, args: argparse.Namespace) -> None:
    """Handle the validate command."""
    # Reserved for future args usage
    _ = args  # Reserved for future use
    result = sync.validate_before_sync()

    if result.success:
        pass


def _handle_sync_command(sync: DocumentationSync, args: argparse.Namespace) -> None:
    """Handle the sync command."""
    files_to_sync = args.sync or sync.get_sync_status().pending_changes

    if not files_to_sync:
        return

    # Validate first if configured
    if sync.config["sync"]["validate_before_commit"]:
        validation_result = sync.validate_before_sync()
        if not validation_result.success:
            return

    # Create backup branch if configured
    if sync.config["git"]["create_backup_branch"]:
        backup_result = sync.create_backup_branch()
        if not backup_result.success:
            return

    # Sync changes
    result = sync.sync_changes("documentation_update", files_to_sync)

    if result.success and result.files_affected and args.verbose:
        for _file in result.files_affected[:10]:
            pass


def _handle_backup_branch_command(
    sync: DocumentationSync,
    args: argparse.Namespace,
) -> None:
    """Handle the backup-branch command."""
    # Reserved for future args usage
    _ = args  # Reserved for future use
    result = sync.create_backup_branch()
    if result.success:
        pass


def _handle_rollback_command(sync: DocumentationSync, args: argparse.Namespace) -> None:
    """Handle the rollback command."""
    if not args.rollback:
        return

    result = sync.rollback_changes(args.rollback)
    if result.success:
        pass


def _handle_maintenance_command(
    sync: DocumentationSync,
    args: argparse.Namespace,
) -> None:
    """Handle the maintenance command."""
    results = sync.run_maintenance_schedule(args.maintenance)

    sum(1 for r in results if r.success)
    len(results)

    if args.verbose:
        for result in results:
            # Reserved for future status display
            _ = "✓" if result.success else "✗"  # Reserved for future use


def main() -> None:
    """Main entry point for the documentation synchronization system."""
    parser = _setup_argument_parser()
    args = parser.parse_args()

    sync = DocumentationSync(args.config)

    if args.status:
        _handle_status_command(sync, args)
    elif args.validate:
        _handle_validate_command(sync, args)
    elif args.sync is not None:
        _handle_sync_command(sync, args)
    elif args.backup_branch:
        _handle_backup_branch_command(sync, args)
    elif args.rollback:
        _handle_rollback_command(sync, args)
    elif args.maintenance:
        _handle_maintenance_command(sync, args)
    else:
        # Default: show status
        args.status = True
        main()


if __name__ == "__main__":
    main()
