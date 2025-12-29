# VERIFIED_NEW_MODULE
"""Namespace refactoring integration - orchestrates existing tools for FLEXT namespace fixes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Orchestrates existing flext-quality tools and Rope library for namespace refactoring:
- Uses FlextQualityPythonTools for Rope-based AST analysis
- Uses FlextQualityOptimizerOperations for syntax modernization
- Uses FlextQualityBatchOperations for batch workflow (dry-run, backup, exec, rollback)

This module is a thin integration layer - actual work is delegated to existing tools.
"""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes as t
from pydantic import ConfigDict
from rope.base import libutils
from rope.base.project import Project as RopeProject
from rope.contrib.findit import find_occurrences as rope_find_occurrences
from rope.refactor.rename import Rename

from flext_quality.constants import c
from flext_quality.tools.batch_backup import FlextQualityBatchBackup


class FlextQualityNamespaceRefactoring(FlextService[dict[str, t.GeneralValueType]]):
    """Namespace refactoring orchestrator - integrates existing tools.

    Provides:
    - Scope selection (project, directory, workspace)
    - Rope-based rename operations
    - Batch operation workflow integration
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    class Scope:
        """Scope selection for batch refactoring targets."""

        def __init__(self: Self) -> None:
            """Initialize scope selector."""
            self._logger = FlextLogger(__name__)
            self._workspace_root = Path(c.Quality.Refactoring.WORKSPACE_ROOT)

        def get_files(
            self: Self,
            *,
            project: str | None = None,
            scope: str = "src",
            workspace: bool = False,
        ) -> list[Path]:
            """Get Python files matching the specified scope."""
            files: list[Path] = []

            if workspace:
                projects = list(c.Quality.Refactoring.PROJECTS)
            elif project:
                projects = [project]
            else:
                self._logger.warning("No project or workspace specified")
                return files

            directories = c.Quality.Refactoring.SCOPE_DIRECTORIES.get(
                scope,
                ("src/",),
            )

            for proj in projects:
                project_path = self._workspace_root / proj
                if not project_path.exists():
                    self._logger.warning("Project not found: %s", proj)
                    continue

                for dir_suffix in directories:
                    dir_path = project_path / dir_suffix
                    if dir_path.exists():
                        files.extend(dir_path.rglob("*.py"))

            self._logger.info("Found %d Python files", len(files))
            return sorted(files)

        def get_core_modules(self: Self, project: str) -> list[Path]:
            """Get core namespace modules for a project."""
            project_path = self._workspace_root / project / "src"
            if not project_path.exists():
                return []

            core_modules = [
                "constants.py",
                "typings.py",
                "protocols.py",
                "models.py",
                "utilities.py",
                "settings.py",
            ]

            files: list[Path] = []
            for module in core_modules:
                files.extend(project_path.rglob(module))

            return sorted(files)

    class RopeIntegration:
        """Rope library integration for AST-based refactoring."""

        def __init__(self: Self) -> None:
            """Initialize Rope integration."""
            self._logger = FlextLogger(__name__)
            self._backup = FlextQualityBatchBackup()

        def rename(
            self: Self,
            project_path: Path,
            old_name: str,
            new_name: str,
            *,
            dry_run: bool = False,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Execute Rope-based rename across project.

            Args:
                project_path: Root path of project.
                old_name: Current name to rename.
                new_name: New name.
                dry_run: If True, preview only.

            Returns:
                FlextResult with affected files.

            """
            rope_project = RopeProject(str(project_path))

            try:
                # Find resource containing the definition
                resource = self._find_resource(rope_project, project_path, old_name)
                if resource is None:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Could not find definition of '{old_name}'"
                    )

                # Find offset in resource
                offset = self._find_offset(resource, old_name)
                if offset is None:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Could not find '{old_name}' in {resource.path}"
                    )

                # Create rename refactoring
                rename = Rename(rope_project, resource, offset)
                changes = rename.get_changes(new_name)

                affected = [str(r.path) for r in changes.get_changed_resources()]

                if dry_run:
                    return FlextResult[dict[str, t.GeneralValueType]].ok({
                        "mode": "dry-run",
                        "old_name": old_name,
                        "new_name": new_name,
                        "affected_files": affected,
                        "count": len(affected),
                    })

                # Apply changes
                rope_project.do(changes)

                return FlextResult[dict[str, t.GeneralValueType]].ok({
                    "mode": "executed",
                    "old_name": old_name,
                    "new_name": new_name,
                    "modified_files": affected,
                    "count": len(affected),
                })

            except Exception as e:
                self._logger.exception("Rope rename failed")
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Rope rename failed: {e}"
                )
            finally:
                rope_project.close()

        def analyze(
            self: Self,
            path: Path,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Analyze file structure using Rope.

            Args:
                path: File to analyze.

            Returns:
                FlextResult with module structure info.

            """
            if not path.exists() or not path.is_file():
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid path: {path}"
                )

            rope_project = RopeProject(str(path.parent))

            try:
                resource = libutils.path_to_resource(rope_project, str(path))
                if resource is None:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Could not load resource: {path}"
                    )

                pymodule = rope_project.get_pymodule(resource)
                try:
                    defined_names = pymodule.get_defined_names()
                except AttributeError:
                    defined_names = {}

                names: list[dict[str, str]] = []
                for name, pyname in defined_names.items():
                    if not name.startswith("_"):
                        names.append({
                            "name": name,
                            "type": type(pyname).__name__,
                        })

                return FlextResult[dict[str, t.GeneralValueType]].ok({
                    "module": path.stem,
                    "path": str(path),
                    "defined_names": names,
                    "count": len(names),
                })

            except Exception as e:
                self._logger.exception("Rope analysis failed")
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Rope analysis failed: {e}"
                )
            finally:
                rope_project.close()

        def find_occurrences(
            self: Self,
            project_path: Path,
            file_path: Path,
            name: str,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Find all occurrences of a symbol using Rope.

            Args:
                project_path: Root path of Rope project.
                file_path: File containing the symbol.
                name: Name of the symbol to find.

            Returns:
                FlextResult with occurrence locations.

            """
            rope_project = RopeProject(str(project_path))
            try:
                rel_path = str(file_path.relative_to(project_path))
                resource = rope_project.get_resource(rel_path)
                source = resource.read()

                offset = source.find(name)
                if offset == -1:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"Symbol '{name}' not found in {file_path}"
                    )

                occurrences = rope_find_occurrences(rope_project, resource, offset)
                locations: list[dict[str, t.GeneralValueType]] = [
                    {
                        "file": str(occ.resource.path),
                        "offset": occ.offset,
                        "unsure": occ.unsure,
                    }
                    for occ in occurrences
                ]

                return FlextResult[dict[str, t.GeneralValueType]].ok({
                    "operation": "find_occurrences",
                    "name": name,
                    "count": len(locations),
                    "locations": locations,
                    "status": "success",
                })
            except Exception as e:
                self._logger.exception("Rope find_occurrences failed")
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Find occurrences failed: {e}"
                )
            finally:
                rope_project.close()

        def _find_resource(
            self: Self,
            project: RopeProject,
            project_path: Path,
            name: str,
        ) -> t.GeneralValueType:
            """Find resource containing a name definition."""
            src_path = project_path / "src"
            search_paths = [src_path] if src_path.exists() else [project_path]

            for search_path in search_paths:
                for py_file in search_path.rglob("*.py"):
                    if py_file.name.startswith("__"):
                        continue
                    try:
                        content = py_file.read_text()
                        if f"class {name}" in content or f"def {name}" in content:
                            rel_path = py_file.relative_to(project_path)
                            return project.get_resource(str(rel_path))
                    except (OSError, UnicodeDecodeError):
                        continue
            return None

        def _find_offset(
            self: Self,
            resource: t.GeneralValueType,
            name: str,
        ) -> int | None:
            """Find offset of a name in resource."""
            content = resource.read()

            # Look for class definition
            class_idx = content.find(f"class {name}")
            if class_idx >= 0:
                return class_idx + 6  # After "class "

            # Look for function definition
            def_idx = content.find(f"def {name}")
            if def_idx >= 0:
                return def_idx + 4  # After "def "

            # Look for assignment
            assign_idx = content.find(f"{name} =")
            if assign_idx >= 0:
                return assign_idx

            return None

    class Operations:
        """Batch operations implementing BatchOperation protocol."""

        def __init__(self: Self) -> None:
            """Initialize operations."""
            self._logger = FlextLogger(__name__)
            self._backup = FlextQualityBatchBackup()
            self._rope = FlextQualityNamespaceRefactoring.RopeIntegration()

        def dry_run(
            self: Self,
            targets: list[Path],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Preview analysis of target files."""
            results: list[dict[str, t.GeneralValueType]] = []

            for path in targets:
                if not path.exists():
                    continue

                result = self._rope.analyze(path)
                if result.is_success and result.value:
                    results.append(result.value)

            return FlextResult[dict[str, t.GeneralValueType]].ok({
                "files_analyzed": len(results),
                "results": results,
            })

        def backup(
            self: Self,
            targets: list[Path],
        ) -> FlextResult[Path]:
            """Create backup of target files."""
            return self._backup.manager.create(targets)

        def execute(
            self: Self,
            targets: list[Path],
            backup_path: Path | None,
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Execute namespace analysis on targets."""
            results: list[dict[str, t.GeneralValueType]] = []

            for path in targets:
                if not path.exists():
                    continue

                result = self._rope.analyze(path)
                if result.is_success and result.value:
                    results.append(result.value)

            return FlextResult[dict[str, t.GeneralValueType]].ok({
                "files_processed": len(results),
                "backup_path": str(backup_path) if backup_path else None,
                "results": results,
            })

        def rollback(
            self: Self,
            backup_path: Path,
        ) -> FlextResult[bool]:
            """Restore from backup."""
            return self._backup.manager.restore(backup_path)

    def __init__(self: Self) -> None:
        """Initialize namespace refactoring service."""
        super().__init__()
        self.scope = self.Scope()
        self.rope = self.RopeIntegration()
        self.operations = self.Operations()
        self._logger = FlextLogger(__name__)

    def execute(
        self: Self,
        **_kwargs: t.GeneralValueType,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute namespace refactoring service."""
        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "service": "namespace_refactoring",
            "status": "ready",
            "capabilities": [
                "scope_selection",
                "rope_rename",
                "rope_analyze",
                "rope_find_occurrences",
            ],
        })


__all__ = ["FlextQualityNamespaceRefactoring"]
