"""Status manager for refactoring cycle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextResult as r, FlextService, FlextTypes as t

from flext_quality.constants import c
from flext_quality.models import m


class FlextQualityCycleServices(FlextService[bool]):
    """Services for managing the refactoring cycle."""

    auto_execute: ClassVar[bool] = False

    class StatusManager:
        """Manages the refactoring cycle status file."""

        def __init__(self, workspace_root: Path | None = None) -> None:
            """Initialize status manager.

            Args:
                workspace_root: Root of the FLEXT workspace. Defaults to ~/flext.

            """
            self.workspace_root = workspace_root or Path.home() / "flext"
            self.status_file = self.workspace_root / ".refactor-cycle-status.json"
            self._status: m.Quality.Cycle.CycleStatus | None = None

        @property
        def status(self) -> m.Quality.Cycle.CycleStatus:
            """Get current status, ensuring it's loaded."""
            if self._status is None:
                self._status = m.Quality.Cycle.CycleStatus()
            return self._status  # Type narrowed by if check above

        def load(self) -> r[m.Quality.Cycle.CycleStatus]:
            """Load status from file.

            Returns:
                FlextResult containing CycleStatus or error.

            """
            if not self.status_file.exists():
                self._status = m.Quality.Cycle.CycleStatus()
                return r[m.Quality.Cycle.CycleStatus].ok(self._status)

            try:
                content = self.status_file.read_text()
                data = json.loads(content)
                self._status = m.Quality.Cycle.CycleStatus.model_validate(data)
                return r[m.Quality.Cycle.CycleStatus].ok(self._status)
            except json.JSONDecodeError as e:
                return r[m.Quality.Cycle.CycleStatus].fail(
                    f"Invalid JSON in status file: {e}"
                )
            except Exception as e:
                return r[m.Quality.Cycle.CycleStatus].fail(
                    f"Failed to load status: {e}"
                )

        def save(self) -> r[bool]:
            """Save current status to file.

            Returns:
                FlextResult indicating success or failure.

            """
            try:
                self.status.last_updated = datetime.now(UTC)
                content = self.status.model_dump_json(indent=2)
                self.status_file.write_text(content)
                return r[bool].ok(True)
            except Exception as e:
                return r[bool].fail(f"Failed to save status: {e}")

        def initialize_cycle(self) -> r[m.Quality.Cycle.CycleStatus]:
            """Initialize a new refactoring cycle by scanning all projects.

            Returns:
                FlextResult containing initialized CycleStatus.

            """
            self._status = m.Quality.Cycle.CycleStatus(
                started_at=datetime.now(UTC),
                last_updated=datetime.now(UTC),
            )

            total_files = 0

            for project_name in c.Quality.Cycle.PROJECT_ORDER:
                project_path = self.workspace_root / project_name
                if not project_path.exists():
                    continue

                project_status = m.Quality.Cycle.ProjectStatus()

                for dir_name in c.Quality.Cycle.DIRECTORY_ORDER:
                    dir_path = project_path / dir_name.rstrip("/")
                    if not dir_path.exists():
                        continue

                    dir_status = m.Quality.Cycle.DirectoryStatus()

                    for py_file in sorted(dir_path.rglob("*.py")):
                        relative_path = py_file.relative_to(project_path)
                        file_key = f"{project_name}/{relative_path}"
                        dir_status.files[str(relative_path)] = (
                            m.Quality.Cycle.FileStatus()
                        )
                        self.status.files[file_key] = m.Quality.Cycle.FileStatus()
                        total_files += 1

                    if dir_status.files:
                        project_status.directories[dir_name] = dir_status

                if project_status.directories:
                    self.status.projects[project_name] = project_status

            self.status.statistics = m.Quality.Cycle.CycleStatistics(
                total_projects=len(self.status.projects),
                total_files=total_files,
            )

            if self.status.projects:
                first_project = next(
                    (
                        p
                        for p in c.Quality.Cycle.PROJECT_ORDER
                        if p in self.status.projects
                    ),
                    None,
                )
                if first_project:
                    self.status.current_project = first_project
                    first_file = self._get_next_file_in_project(first_project)
                    if first_file:
                        self.status.current_file = first_file

            save_result = self.save()
            if save_result.is_failure:
                return r[m.Quality.Cycle.CycleStatus].fail(
                    save_result.error or "Save failed"
                )

            return r[m.Quality.Cycle.CycleStatus].ok(self._status)

        def _get_next_file_in_project(self, project_name: str) -> str | None:
            """Get the next pending file in a project."""
            project = self.status.projects.get(project_name)
            if project is None:
                return None

            for dir_name in c.Quality.Cycle.DIRECTORY_ORDER:
                dir_status = project.directories.get(dir_name)
                if dir_status is None:
                    continue

                for file_name, file_status in sorted(dir_status.files.items()):
                    if file_status.status == c.Quality.Cycle.Status.PENDING:
                        return f"{project_name}/{file_name}"

            return None

        def get_next_file(self) -> r[str]:
            """Get the next file to process."""
            if self.status.current_file:
                file_status = self.status.files.get(self.status.current_file)
                if file_status and file_status.status == c.Quality.Cycle.Status.PENDING:
                    return r[str].ok(self.status.current_file)

            if self.status.current_project:
                next_file = self._get_next_file_in_project(self.status.current_project)
                if next_file:
                    self.status.current_file = next_file
                    self.save()
                    return r[str].ok(next_file)

                project = self.status.projects.get(self.status.current_project)
                if project:
                    project.status = c.Quality.Cycle.Status.COMPLETED
                    if self.status.statistics is not None:
                        self.status.statistics.completed_projects += 1

            for project_name in self.status.project_order:
                project = self.status.projects.get(project_name)
                if (
                    project is None
                    or project.status == c.Quality.Cycle.Status.COMPLETED
                ):
                    continue

                next_file = self._get_next_file_in_project(project_name)
                if next_file:
                    self.status.current_project = project_name
                    self.status.current_file = next_file
                    project.status = c.Quality.Cycle.Status.IN_PROGRESS
                    self.save()
                    return r[str].ok(next_file)

            return r[str].fail("All files have been processed")

        def mark_file_done(
            self,
            file_key: str,
            violations_found: int = 0,
            violations_fixed: int = 0,
            lint_before: int = 0,
            lint_after: int = 0,
        ) -> r[bool]:
            """Mark a file as completed."""
            file_status = self.status.files.get(file_key)
            if file_status is None:
                return r[bool].fail(f"File not found: {file_key}")

            file_status.status = c.Quality.Cycle.Status.COMPLETED
            file_status.violations_found = violations_found
            file_status.violations_fixed = violations_fixed
            file_status.lint_before = lint_before
            file_status.lint_after = lint_after
            file_status.processed_at = datetime.now(UTC)

            if self.status.statistics is not None:
                self.status.statistics.processed_files += 1
                self.status.statistics.fixed_violations += violations_fixed

            return self.save()

        def add_to_manual_review(
            self,
            file_key: str,
            issue_type: str,
            line: int,
            description: str,
        ) -> r[bool]:
            """Add a file to the manual review queue."""
            file_status = self.status.files.get(file_key)
            if file_status is None:
                return r[bool].fail(f"File not found: {file_key}")

            issue = m.Quality.Cycle.ManualReviewIssue(
                type=issue_type,
                line=line,
                description=description,
            )

            file_status.status = c.Quality.Cycle.Status.MANUAL_REVIEW
            file_status.manual_review.append(issue)

            existing_item = next(
                (
                    item
                    for item in self.status.manual_review_queue
                    if item.file == file_key
                ),
                None,
            )
            if existing_item:
                existing_item.issues.append(issue)
            else:
                self.status.manual_review_queue.append(
                    m.Quality.Cycle.ManualReviewQueueItem(
                        file=file_key, issues=[issue]
                    ),
                )

            if self.status.statistics is not None:
                self.status.statistics.pending_manual_review += 1

            return self.save()

        def register_pattern(
            self,
            pattern: str,
            file_key: str,
            severity: c.Quality.Cycle.Severity = c.Quality.Cycle.Severity.WARN,
            proposed_rule: str | None = None,
        ) -> r[bool]:
            """Register a discovered pattern."""
            existing = next(
                (p for p in self.status.discovered_patterns if p.pattern == pattern),
                None,
            )

            if existing:
                existing.occurrences += 1
                if file_key not in existing.files:
                    existing.files.append(file_key)
            else:
                new_pattern = m.Quality.Cycle.DiscoveredPattern(
                    pattern=pattern,
                    occurrences=1,
                    files=[file_key],
                    severity=severity,
                    proposed_rule=proposed_rule,
                )
                self.status.discovered_patterns.append(new_pattern)
                if self.status.statistics is not None:
                    self.status.statistics.discovered_patterns += 1

            return self.save()

        def get_status_summary(self) -> r[dict[str, t.GeneralValueType]]:
            """Get a summary of the current cycle status."""
            stats = self.status.statistics
            if stats is None:
                return r[dict[str, t.GeneralValueType]].fail("Statistics not available")
            progress = (
                (stats.processed_files / stats.total_files * 100)
                if stats.total_files > 0
                else 0
            )

            return r[dict[str, t.GeneralValueType]].ok({
                "started_at": (
                    str(self.status.started_at) if self.status.started_at else None
                ),
                "last_updated": (
                    str(self.status.last_updated)
                    if self.status.last_updated
                    else None
                ),
                "current_project": self.status.current_project,
                "current_file": self.status.current_file,
                "progress_percent": round(progress, 1),
                "projects": {
                    "total": stats.total_projects,
                    "completed": stats.completed_projects,
                },
                "files": {
                    "total": stats.total_files,
                    "processed": stats.processed_files,
                    "remaining": stats.total_files - stats.processed_files,
                },
                "violations": {
                    "fixed": stats.fixed_violations,
                },
                "manual_review_queue": stats.pending_manual_review,
                "discovered_patterns": stats.discovered_patterns,
            })

    @override
    def execute(self, data: t.GeneralValueType = None) -> r[bool]:
        """Execute services - returns True to indicate service is ready."""
        return r[bool].ok(True)


__all__ = ["FlextQualityCycleServices"]
