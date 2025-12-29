# VERIFIED_NEW_MODULE
"""Descoberta automática de projetos FLEXT via gitmodules e pyproject.toml.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides automatic discovery of FLEXT projects in a workspace by:
1. Parsing .gitmodules for git submodule paths
2. Scanning workspace directories for pyproject.toml files
3. Ordering projects by their dependencies using topological sort
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import ClassVar, Self

from flext_core import FlextResult as r, FlextService


class FlextWorkspaceDiscovery(FlextService[list[str]]):
    """Descobre projetos FLEXT e ordena por dependências.

    Descoberta:
    1. .gitmodules - Parse submodule paths para flext-*
    2. pyproject.toml scan - Projetos adicionais no workspace

    Ordenação:
    - Parse dependências de pyproject.toml
    - Topological sort por dependências
    - Foundation projects sempre primeiro
    """

    FOUNDATION_PROJECTS: ClassVar[tuple[str, ...]] = ("flext-core", "flext-cli")
    GITMODULES_PATH_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^\s*path\s*=\s*(.+?)\s*$", re.MULTILINE
    )

    class GitmodulesParser:
        """Parser para .gitmodules."""

        @staticmethod
        def parse(gitmodules_path: Path) -> r[list[str]]:
            """Extrai paths de submodules do arquivo .gitmodules.

            Args:
                gitmodules_path: Path to .gitmodules file

            Returns:
                List of submodule path names

            """
            if not gitmodules_path.exists():
                return r[list[str]].ok([])

            content = gitmodules_path.read_text(encoding="utf-8")
            matches = FlextWorkspaceDiscovery.GITMODULES_PATH_PATTERN.findall(content)
            return r[list[str]].ok(matches)

    class PyprojectParser:
        """Parser para pyproject.toml."""

        @staticmethod
        def parse_dependencies(pyproject_path: Path) -> r[list[str]]:
            """Extrai dependências flext-* de pyproject.toml.

            Supports both PEP 621 [project.dependencies] and
            Poetry [tool.poetry.dependencies] formats.

            Args:
                pyproject_path: Path to pyproject.toml file

            Returns:
                List of flext-* dependency names (normalized to use hyphens)

            """
            if not pyproject_path.exists():
                return r[list[str]].ok([])

            try:
                content = pyproject_path.read_text(encoding="utf-8")
                data = tomllib.loads(content)
            except (OSError, tomllib.TOMLDecodeError):
                return r[list[str]].ok([])

            deps: list[str] = []

            # [project.dependencies] - PEP 621 format
            if "project" in data and "dependencies" in data["project"]:
                for dep in data["project"]["dependencies"]:
                    # Handle formats like "flext-core>=0.1.0" or "flext-core @ file:..."
                    if isinstance(dep, str) and (
                        dep.startswith("flext-") or dep.startswith("flext_")
                    ):
                        # Extract just the package name
                        name = dep.split()[0].split("@")[0].split("[")[0]
                        name = name.split(">=")[0].split("<=")[0].split("==")[0]
                        name = name.split(">")[0].split("<")[0].split("~=")[0]
                        deps.append(name.replace("_", "-"))

            # [tool.poetry.dependencies] - Poetry format
            if "tool" in data and "poetry" in data["tool"]:
                poetry_deps = data["tool"]["poetry"].get("dependencies", {})
                for name in poetry_deps:
                    if name.startswith("flext-") or name.startswith("flext_"):
                        deps.append(name.replace("_", "-"))

            return r[list[str]].ok(deps)

        @staticmethod
        def is_flext_project(pyproject_path: Path) -> bool:
            """Verifica se projeto depende de flext-core.

            A project is considered a FLEXT project if it has flext-core
            as a dependency.

            Args:
                pyproject_path: Path to pyproject.toml file

            Returns:
                True if project depends on flext-core

            """
            result = FlextWorkspaceDiscovery.PyprojectParser.parse_dependencies(
                pyproject_path
            )
            if result.is_failure:
                return False
            return "flext-core" in result.value

    class DependencyOrderer:
        """Ordena projetos por dependências (topological sort)."""

        @staticmethod
        def order(
            projects: list[str],
            dependencies: dict[str, list[str]],
            foundation: tuple[str, ...],
        ) -> r[list[str]]:
            """Topological sort com foundation primeiro.

            Uses Kahn's algorithm for topological sorting, ensuring:
            1. Foundation projects come first
            2. Dependencies are processed before dependents
            3. Cycles are handled gracefully (remaining items added at end)

            Args:
                projects: List of all project names
                dependencies: Map of project -> list of its dependencies
                foundation: Tuple of foundation projects to prioritize

            Returns:
                Ordered list of project names

            """
            if not projects:
                return r[list[str]].ok([])

            # Build in-degree map (count of dependencies for each project)
            in_degree: dict[str, int] = dict.fromkeys(projects, 0)

            for project, deps in dependencies.items():
                if project not in in_degree:
                    continue
                for dep in deps:
                    if dep in projects:
                        in_degree[project] = in_degree.get(project, 0) + 1

            # Kahn's algorithm - start with nodes having no dependencies
            queue = [p for p in projects if in_degree.get(p, 0) == 0]
            result: list[str] = []

            while queue:
                # Sort queue to ensure foundation comes first, then by original order
                queue.sort(
                    key=lambda p: (
                        0 if p in foundation else 1,
                        foundation.index(p) if p in foundation else 999,
                        projects.index(p) if p in projects else 999,
                    )
                )
                node = queue.pop(0)
                result.append(node)

                # Decrease in-degree for projects that depend on this node
                for project, deps in dependencies.items():
                    if node in deps and project in in_degree:
                        in_degree[project] -= 1
                        if in_degree[project] == 0 and project not in result:
                            queue.append(project)

            # Add any remaining projects (cycles or isolated)
            for p in projects:
                if p not in result:
                    result.append(p)

            return r[list[str]].ok(result)

    def __init__(self: Self, workspace_root: Path | None = None) -> None:
        """Initialize discovery service.

        Args:
            workspace_root: Path to workspace root. Defaults to ~/flext

        """
        super().__init__()
        self._workspace_root = workspace_root or Path.home() / "flext"

    def execute(self: Self) -> r[list[str]]:
        """Execute discovery and return ordered projects.

        Returns:
            Ordered list of project names

        """
        return self.get_ordered_projects()

    def discover_from_gitmodules(self: Self) -> r[list[str]]:
        """Descobre projetos de .gitmodules.

        Returns:
            List of submodule paths from .gitmodules

        """
        gitmodules = self._workspace_root / ".gitmodules"
        return self.GitmodulesParser.parse(gitmodules)

    def discover_from_workspace(self: Self) -> r[list[str]]:
        """Descobre projetos adicionais com pyproject.toml.

        Scans workspace directories for projects that:
        1. Have a pyproject.toml file
        2. Depend on flext-core

        Returns:
            List of additional project directory names

        """
        projects: list[str] = []

        if not self._workspace_root.exists():
            return r[list[str]].ok([])

        for item in self._workspace_root.iterdir():
            if not item.is_dir():
                continue
            # Skip hidden directories and common non-project dirs
            if item.name.startswith(".") or item.name in {"node_modules", "__pycache__"}:
                continue
            pyproject = item / "pyproject.toml"
            if pyproject.exists() and self.PyprojectParser.is_flext_project(pyproject):
                projects.append(item.name)

        return r[list[str]].ok(projects)

    def build_dependency_graph(
        self: Self,
        projects: list[str],
    ) -> r[dict[str, list[str]]]:
        """Constrói grafo de dependências.

        Args:
            projects: List of project names to analyze

        Returns:
            Map of project -> list of its flext-* dependencies

        """
        graph: dict[str, list[str]] = {}

        for project in projects:
            pyproject = self._workspace_root / project / "pyproject.toml"
            result = self.PyprojectParser.parse_dependencies(pyproject)
            if result.is_success:
                # Filter to only include known projects
                deps = [d for d in result.value if d in projects]
                graph[project] = deps
            else:
                graph[project] = []

        return r[dict[str, list[str]]].ok(graph)

    def get_ordered_projects(self: Self) -> r[list[str]]:
        """Retorna projetos ordenados por dependências.

        Discovery process:
        1. Parse .gitmodules for submodule paths
        2. Scan workspace for additional FLEXT projects
        3. Combine and deduplicate
        4. Build dependency graph from pyproject.toml files
        5. Topological sort with foundation projects first

        Returns:
            Ordered list of project names (foundation first, then by dependencies)

        """
        # Discover from gitmodules
        gitmodules_result = self.discover_from_gitmodules()
        gitmodules_projects = (
            gitmodules_result.value if gitmodules_result.is_success else []
        )

        # Discover additional from workspace
        workspace_result = self.discover_from_workspace()
        workspace_projects = (
            workspace_result.value if workspace_result.is_success else []
        )

        # Combine and dedupe (preserve order, gitmodules first)
        all_projects = list(dict.fromkeys(gitmodules_projects + workspace_projects))

        if not all_projects:
            return r[list[str]].failure("No projects discovered")

        # Build dependency graph
        graph_result = self.build_dependency_graph(all_projects)
        if graph_result.is_failure:
            # Return unordered if graph fails
            return r[list[str]].ok(all_projects)

        # Order by dependencies
        return self.DependencyOrderer.order(
            all_projects,
            graph_result.value,
            self.FOUNDATION_PROJECTS,
        )


__all__ = ["FlextWorkspaceDiscovery"]
