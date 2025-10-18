"""FLEXT Quality Project Service - Focused project management service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)

from .entities import FlextQualityEntities

# Direct access to entities (no wrappers)
Project = FlextQualityEntities.Project


class FlextQualityProjectService(FlextService[None]):
    """Service for managing quality projects using flext-core patterns.

    Single responsibility: Project lifecycle management
    """

    def __init__(self) -> None:
        """Initialize project service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    @override
    def execute(self, data: object) -> FlextResult[None]:
        """Execute service operation - not used for this service type."""
        return FlextResult[None].fail(
            "ProjectService does not support execute operation"
        )

    def create_project(
        self,
        name: str,
        project_path: str,
        repository_url: str | None = None,
        config_path: str | None = None,
        language: str = "python",
        *,
        auto_analyze: bool = True,
        _min_coverage: float = 95.0,
        _max_complexity: int = 10,
        _max_duplication: float = 5.0,
    ) -> FlextResult[Project]:
        """Create a new quality project."""
        try:
            # Create project entity
            project = Project(
                name=name,
                project_path=str(project_path),
                repository_url=repository_url,
                config_path=str(config_path) if config_path else None,
                language=language,
                auto_analyze=auto_analyze,
            )

            self.logger.info("Created project: %s", project.name)
            return FlextResult[FlextQualityEntities.Project].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to create project")
            return FlextResult[FlextQualityEntities.Project].fail(
                f"Failed to create project: {e}",
            )

    def get_project(self, project_id: str) -> FlextResult[Project]:
        """Get a project by ID."""
        try:
            # Note: This would need access to a project repository
            # For now, return not found
            return FlextResult[Project].fail(
                f"Project not found: {project_id}",
            )
        except Exception as e:
            self.logger.exception(f"Failed to get project {project_id}")
            return FlextResult[Project].fail(
                f"Failed to get project: {e}",
            )

    def list_projects(self) -> FlextResult[list[Project]]:
        """List all projects."""
        try:
            # Note: This would need access to a project repository
            # For now, return empty list
            projects = []
            return FlextResult[list[Project]].ok(projects)
        except Exception as e:
            self.logger.exception("Failed to list projects")
            return FlextResult[list[Project]].fail(
                f"Failed to list projects: {e}",
            )

    def update_project(
        self, project_id: str, updates: dict[str, object]
    ) -> FlextResult[Project]:
        """Update a project."""
        try:
            # Note: This would need access to a project repository
            # For now, return not found
            return FlextResult[Project].fail(
                f"Project not found: {project_id}",
            )
        except Exception as e:
            self.logger.exception(f"Failed to update project {project_id}")
            return FlextResult[Project].fail(
                f"Failed to update project: {e}",
            )

    def delete_project(self, project_id: str) -> FlextResult[bool]:
        """Delete a project."""
        try:
            # Note: This would need access to a project repository
            # For now, return not found
            return FlextResult[bool].fail("Project not found")
        except Exception as e:
            self.logger.exception(f"Failed to delete project {project_id}")
            return FlextResult[bool].fail(f"Failed to delete project: {e}")
