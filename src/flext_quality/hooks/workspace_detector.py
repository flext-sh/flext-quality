"""FLEXT Workspace Detector - Identify and analyze workspace context.

Provides workspace detection and context gathering for hooks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes as t

from flext_quality.hooks.models import WorkspaceContext


class WorkspaceDetector(FlextService[WorkspaceContext]):
    """Workspace detection service for hook operations.

    Identifies workspace type, project structure, and context information.

    Workspace Types:
    - 'flext': FLEXT ecosystem project (~/flext/)
    - 'invest': Investment-related project
    - 'global': General workspace

    Usage:
        from flext_quality.hooks.workspace_detector import WorkspaceDetector

        detector = WorkspaceDetector()
        result = detector.detect(Path("/some/path"))

        if result.is_success:
            context = result.unwrap()
            print(f"Project: {context.project_name}")
    """

    def __init__(self: Self) -> None:
        """Initialize workspace detector."""
        super().__init__()

    def execute(
        self: Self,
        **_kwargs: t.GeneralValueType,
    ) -> FlextResult[WorkspaceContext]:
        """Execute workspace detector service - FlextService interface.

        Returns:
            FlextResult with empty context

        """
        return FlextResult[WorkspaceContext].ok(
            WorkspaceContext(
                project_name="unknown",
                project_path=str(Path.cwd()),
                workspace_type="global",
            )
        )

    def detect(
        self: Self,
        start_path: Path | str | None = None,
    ) -> FlextResult[WorkspaceContext]:
        """Detect workspace context from a starting path.

        Args:
            start_path: Starting path (defaults to current directory)

        Returns:
            FlextResult with WorkspaceContext

        """
        if start_path is None:
            start_path = Path.cwd()
        else:
            start_path = Path(start_path)

        # Ensure it's a directory
        if start_path.is_file():
            start_path = start_path.parent

        # Find project root by looking for CLAUDE.md or pyproject.toml
        project_root = self._find_project_root(start_path)

        # Detect workspace type
        workspace_type = self._detect_workspace_type(project_root)

        # Extract project name from path
        project_name = project_root.name

        # Check for metadata files
        has_claude_md = (project_root / "CLAUDE.md").exists()
        has_pyproject = (project_root / "pyproject.toml").exists()
        has_git_repo = (project_root / ".git").exists()

        # Get Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        context = WorkspaceContext(
            project_name=project_name,
            project_path=str(project_root),
            workspace_type=workspace_type,
            has_claude_md=has_claude_md,
            has_pyproject=has_pyproject,
            has_git_repo=has_git_repo,
            python_version=python_version,
        )

        return FlextResult[WorkspaceContext].ok(context)

    def _find_project_root(self: Self, start_path: Path) -> Path:
        """Find project root by looking for marker files.

        Looks for (in order):
        1. CLAUDE.md (project-specific config)
        2. pyproject.toml (Python project marker)
        3. .git (git repository)
        4. Returns start_path if nothing found

        Args:
            start_path: Path to start searching from

        Returns:
            Path to project root

        """
        current = start_path

        # Search up to 10 levels
        for _ in range(10):
            # Check for project markers
            if (current / "CLAUDE.md").exists():
                return current
            if (current / "pyproject.toml").exists():
                return current
            if (current / ".git").exists():
                return current

            # Move to parent
            parent = current.parent
            if parent == current:
                # Reached filesystem root
                break
            current = parent

        # Return start path if no root found
        return start_path

    def _detect_workspace_type(self: Self, project_root: Path) -> str:
        """Detect workspace type from project structure.

        Args:
            project_root: Path to project root

        Returns:
            Workspace type ('flext', 'invest', or 'global')

        """
        # Check for FLEXT markers
        if project_root.name == "flext":
            return "flext"

        if (project_root / "CLAUDE.md").exists():
            try:
                claude_md = (project_root / "CLAUDE.md").read_text()
                if "FLEXT" in claude_md:
                    return "flext"
                if "invest" in claude_md.lower():
                    return "invest"
            except Exception:
                pass

        # Check for invest markers
        if project_root.name == "invest":
            return "invest"

        # Default to global
        return "global"

    def get_project_config(
        self: Self,
        project_path: Path | str,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Get project configuration from CLAUDE.md.

        Args:
            project_path: Path to project

        Returns:
            FlextResult with configuration dict

        """
        project_path = Path(project_path)
        claude_md = project_path / "CLAUDE.md"

        if not claude_md.exists():
            return FlextResult[dict[str, t.GeneralValueType]].ok({})

        try:
            content = claude_md.read_text()
            # Extract metadata from CLAUDE.md header
            config: dict[str, t.GeneralValueType] = {}

            # Look for key-value pairs in the format: **Key**: value
            for line in content.split("\n")[:20]:  # Check first 20 lines
                if ":" in line and "**" in line:
                    try:
                        # Simple extraction of key-value from markdown
                        key_part = line.split("**")[1]
                        value_part = line.split(": ", 1)[1].strip()
                        config[key_part] = value_part
                    except (IndexError, ValueError):
                        pass

            return FlextResult[dict[str, t.GeneralValueType]].ok(config)

        except Exception as e:
            return FlextResult[dict[str, t.GeneralValueType]].error(
                f"Failed to read CLAUDE.md: {e!s}"
            )

    def is_flext_workspace(
        self: Self,
        project_path: Path | str | None = None,
    ) -> bool:
        """Check if path is in a FLEXT workspace.

        Args:
            project_path: Path to check (defaults to current directory)

        Returns:
            True if in FLEXT workspace

        """
        result = self.detect(project_path)
        if result.is_success:
            context = result.unwrap()
            return context.workspace_type == "flext"
        return False


__all__ = ["WorkspaceDetector"]
