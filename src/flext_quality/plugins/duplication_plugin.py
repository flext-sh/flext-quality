# VERIFIED_NEW_MODULE
# Verificação: _DuplicationAnalyzer existe em analyzer.py mas é classe interna.
# Este plugin expõe funcionalidade como API pública seguindo padrão FlextService.
"""Duplication Plugin - Code clone detection.

Detects duplicate code across Python files using line-based similarity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

from ..constants import FlextQualityConstants as c


class FlextDuplicationPlugin(FlextService[int]):
    """Code duplication detection plugin.

    Detects duplicate code using line-based similarity comparison.
    Uses SIMILARITY_THRESHOLD from constants for significant duplication.

    Usage:
        from flext_quality.plugins import FlextDuplicationPlugin

        plugin = FlextDuplicationPlugin()
        result = plugin.check([Path("file1.py"), Path("file2.py")])
        if result.is_success:
            for dup in result.value.duplicates:
                logger.info("%s <-> %s: %.1f%%", dup.file1, dup.file2, dup.similarity)
    """

    __slots__ = ("_logger",)

    @dataclass(frozen=True, slots=True)
    class DuplicatePair:
        """Represents a pair of files with duplication."""

        file1: Path
        file2: Path
        similarity: float
        shared_lines: int
        total_lines: int

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Result of duplication check."""

        duplicate_count: int
        files_checked: int
        duplicates: tuple[FlextDuplicationPlugin.DuplicatePair, ...] = field(
            default_factory=tuple
        )

    @dataclass(frozen=True, slots=True)
    class ProjectDuplicate:
        """Cross-project duplication with source identification."""

        file1_project: str
        file1_path: Path
        file2_project: str
        file2_path: Path
        similarity: float
        shared_lines: int
        consolidation_target: str  # Which project should own consolidated code

    @dataclass(frozen=True, slots=True)
    class WorkspaceCheckResult:
        """Result of workspace-wide duplication check."""

        total_projects: int
        total_duplicates: int
        cross_project_duplicates: int
        duplicates: tuple[FlextDuplicationPlugin.ProjectDuplicate, ...] = field(
            default_factory=tuple
        )

    @dataclass(frozen=True, slots=True)
    class TestDuplicate:
        """Test code duplication with consolidation strategy."""

        source_type: str  # "test-test", "test-src", "test-flext-tests"
        file1_project: str
        file1_path: Path
        file2_project: str
        file2_path: Path
        similarity: float
        shared_lines: int
        consolidation_target: str
        consolidation_strategy: str  # "extract-to-flext-tests", "refactor-src", "unify-locally"

    @dataclass(frozen=True, slots=True)
    class WorkspaceTestCheckResult:
        """Result of workspace test duplication check."""

        total_projects: int
        test_duplicates: int
        test_src_duplicates: int
        cross_project_test_duplicates: int
        duplicates: tuple[FlextDuplicationPlugin.TestDuplicate, ...] = field(
            default_factory=tuple
        )

    def __init__(self: Self) -> None:
        """Initialize duplication plugin."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[int]:
        """Satisfy FlextService contract."""
        return FlextResult[int].fail("Use check() method")

    def check(
        self: Self,
        files: list[Path],
        threshold: float | None = None,
    ) -> FlextResult[CheckResult]:
        """Check files for duplication.

        Args:
            files: Files to check for duplication.
            threshold: Similarity threshold (default: SIMILARITY_THRESHOLD).

        Returns:
            Check result with duplicate pairs.

        """
        if len(files) < c.Quality.Analysis.MIN_FILES_FOR_PAIR_COMPARISON:
            return FlextResult[FlextDuplicationPlugin.CheckResult].ok(
                FlextDuplicationPlugin.CheckResult(
                    duplicate_count=0,
                    files_checked=len(files),
                )
            )

        effective_threshold = (
            threshold
            if threshold is not None
            else c.Quality.Analysis.SIMILARITY_THRESHOLD
        )
        min_size = c.Quality.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK

        # Read file contents
        file_contents: dict[Path, str] = {}
        for f in files:
            if f.is_file():
                try:
                    content = f.read_text(encoding="utf-8")
                    if len(content.strip()) > min_size:
                        file_contents[f] = content
                except (OSError, UnicodeDecodeError):
                    continue

        # Compare all pairs
        duplicates: list[FlextDuplicationPlugin.DuplicatePair] = []
        file_list = list(file_contents.keys())

        for i, f1 in enumerate(file_list):
            for f2 in file_list[i + 1 :]:
                pair = self._analyze_pair(
                    f1,
                    file_contents[f1],
                    f2,
                    file_contents[f2],
                    effective_threshold,
                )
                if pair is not None:
                    duplicates.append(pair)

        self._logger.debug(
            "Duplication check: %d duplicates in %d files",
            len(duplicates),
            len(files),
        )

        return FlextResult[FlextDuplicationPlugin.CheckResult].ok(
            FlextDuplicationPlugin.CheckResult(
                duplicate_count=len(duplicates),
                files_checked=len(files),
                duplicates=tuple(duplicates),
            )
        )

    def _analyze_pair(
        self: Self,
        file1: Path,
        content1: str,
        file2: Path,
        content2: str,
        threshold: float,
    ) -> DuplicatePair | None:
        """Analyze a pair of files for duplication.

        Returns DuplicatePair if similarity exceeds threshold, else None.
        """
        lines1 = set(content1.splitlines())
        lines2 = set(content2.splitlines())

        if not lines1 or not lines2:
            return None

        shared = lines1 & lines2
        total = max(len(lines1), len(lines2))
        similarity = len(shared) / total

        if similarity > threshold:
            return FlextDuplicationPlugin.DuplicatePair(
                file1=file1,
                file2=file2,
                similarity=similarity,
                shared_lines=len(shared),
                total_lines=total,
            )

        return None

    def get_duplicate_count(
        self: Self,
        directory: Path,
    ) -> FlextResult[int]:
        """Get count of duplicate pairs in a directory.

        Convenience method for hook integration.

        Args:
            directory: Directory to scan for Python files.

        Returns:
            Count of duplicate pairs.

        """
        if not directory.is_dir():
            return FlextResult[int].fail(f"Not a directory: {directory}")

        # Collect Python files, excluding __pycache__ and .venv
        python_files: list[Path] = []
        for py_file in directory.rglob("*.py"):
            path_str = str(py_file)
            if "__pycache__" not in path_str and ".venv" not in path_str:
                python_files.append(py_file)

        result = self.check(python_files)
        if result.is_failure:
            return FlextResult[int].fail(result.error or "Check failed")

        return FlextResult[int].ok(result.value.duplicate_count)

    def check_workspace(
        self: Self,
        workspace_dir: Path,
        threshold: float | None = None,
    ) -> FlextResult[WorkspaceCheckResult]:
        """Check entire workspace for cross-project duplication.

        Scans all FLEXT project src/ directories and detects duplicates
        with tier-based consolidation suggestions per SOLID/DRY/SRP.

        Args:
            workspace_dir: FLEXT workspace root directory.
            threshold: Similarity threshold (default: SIMILARITY_THRESHOLD).

        Returns:
            Workspace check result with cross-project duplicates.

        """
        effective_threshold = (
            threshold
            if threshold is not None
            else c.Quality.Analysis.SIMILARITY_THRESHOLD
        )
        min_size = c.Quality.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK

        # Scan all projects and collect files with project info
        project_files: dict[str, list[tuple[Path, str]]] = {}
        for proj_dir in workspace_dir.glob("flext-*"):
            if not proj_dir.is_dir():
                continue
            src_dir = proj_dir / "src"
            if not src_dir.is_dir():
                continue

            proj_name = proj_dir.name
            project_files[proj_name] = []

            for py_file in src_dir.rglob("*.py"):
                path_str = str(py_file)
                if "__pycache__" in path_str or ".venv" in path_str:
                    continue
                try:
                    content = py_file.read_text(encoding="utf-8")
                    if len(content.strip()) > min_size:
                        project_files[proj_name].append((py_file, content))
                except (OSError, UnicodeDecodeError):
                    continue

        # Add client-a-* projects
        for proj_dir in workspace_dir.glob("client-a-*"):
            if not proj_dir.is_dir():
                continue
            src_dir = proj_dir / "src"
            if not src_dir.is_dir():
                continue

            proj_name = proj_dir.name
            project_files[proj_name] = []

            for py_file in src_dir.rglob("*.py"):
                path_str = str(py_file)
                if "__pycache__" in path_str or ".venv" in path_str:
                    continue
                try:
                    content = py_file.read_text(encoding="utf-8")
                    if len(content.strip()) > min_size:
                        project_files[proj_name].append((py_file, content))
                except (OSError, UnicodeDecodeError):
                    continue

        # Compare across projects
        duplicates: list[FlextDuplicationPlugin.ProjectDuplicate] = []
        projects = sorted(project_files.keys())

        for i, proj1 in enumerate(projects):
            for proj2 in projects[i + 1:]:
                files1 = project_files[proj1]
                files2 = project_files[proj2]

                for path1, content1 in files1:
                    for path2, content2 in files2:
                        pair = self._analyze_pair(
                            path1,
                            content1,
                            path2,
                            content2,
                            effective_threshold,
                        )
                        if pair is not None:
                            # Determine consolidation target using tier logic
                            target = self._get_consolidation_target(
                                proj1,
                                proj2,
                            )
                            dup = FlextDuplicationPlugin.ProjectDuplicate(
                                file1_project=proj1,
                                file1_path=pair.file1,
                                file2_project=proj2,
                                file2_path=pair.file2,
                                similarity=pair.similarity,
                                shared_lines=pair.shared_lines,
                                consolidation_target=target,
                            )
                            duplicates.append(dup)

        self._logger.debug(
            "Workspace check: %d cross-project duplicates in %d projects",
            len(duplicates),
            len(projects),
        )

        return FlextResult[FlextDuplicationPlugin.WorkspaceCheckResult].ok(
            FlextDuplicationPlugin.WorkspaceCheckResult(
                total_projects=len(projects),
                total_duplicates=len(duplicates),
                cross_project_duplicates=len([d for d in duplicates if d.file1_project != d.file2_project]),
                duplicates=tuple(duplicates),
            )
        )

    def _get_consolidation_target(
        self: Self,
        project1: str,
        project2: str,
    ) -> str:
        """Determine which project should own consolidated code (SOLID).

        Follows tier hierarchy:
        - Tier 0: flext-core (foundation)
        - Tier 1: flext-cli, flext-observability
        - Tier 2+: Others

        Lower tier (higher level) always wins to consolidate upward.
        """
        tier_order = [
            "flext-core",
            "flext-cli",
            "flext-observability",
        ]

        for tier_project in tier_order:
            if project1 == tier_project:
                return project1
            if project2 == tier_project:
                return project2

        # Both are same tier - use alphabetical order for consistency
        return min(project1, project2)

    def check_workspace_with_tests(
        self: Self,
        workspace_dir: Path,
        threshold: float | None = None,
    ) -> FlextResult[WorkspaceTestCheckResult]:
        """Check workspace for test code duplication.

        Analyzes tests/ across all projects with consolidation strategies:
        - tests vs tests (cross-project) → extract to flext-tests
        - tests vs src → refactor to avoid duplicating logic
        - tests vs tests (same project) → unify locally via fixtures

        Args:
            workspace_dir: FLEXT workspace root directory.
            threshold: Similarity threshold (default: SIMILARITY_THRESHOLD).

        Returns:
            Workspace test check result with consolidation strategies.

        """
        effective_threshold = (
            threshold
            if threshold is not None
            else c.Quality.Analysis.SIMILARITY_THRESHOLD
        )
        min_size = c.Quality.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK

        # Collect test files and src files with project info
        project_tests: dict[str, list[tuple[Path, str]]] = {}
        project_src: dict[str, list[tuple[Path, str]]] = {}
        flext_tests_files: list[tuple[Path, str]] = []

        # Scan all projects
        for proj_dir in sorted(list(workspace_dir.glob("flext-*")) + list(workspace_dir.glob("client-a-*"))):
            if not proj_dir.is_dir():
                continue

            proj_name = proj_dir.name

            # Collect tests
            tests_dir = proj_dir / "tests"
            if tests_dir.is_dir():
                project_tests[proj_name] = []
                for py_file in tests_dir.rglob("*.py"):
                    if "__pycache__" not in str(py_file):
                        try:
                            content = py_file.read_text(encoding="utf-8")
                            if len(content.strip()) > min_size:
                                project_tests[proj_name].append((py_file, content))
                        except (OSError, UnicodeDecodeError):
                            continue

            # Collect src files
            src_dir = proj_dir / "src"
            if src_dir.is_dir():
                project_src[proj_name] = []
                for py_file in src_dir.rglob("*.py"):
                    if "__pycache__" not in str(py_file):
                        try:
                            content = py_file.read_text(encoding="utf-8")
                            if len(content.strip()) > min_size:
                                project_src[proj_name].append((py_file, content))
                        except (OSError, UnicodeDecodeError):
                            continue

        # Collect flext-tests as reference
        flext_tests_dir = workspace_dir / "flext-core" / "src" / "flext_tests"
        if flext_tests_dir.is_dir():
            for py_file in flext_tests_dir.rglob("*.py"):
                if "__pycache__" not in str(py_file):
                    try:
                        content = py_file.read_text(encoding="utf-8")
                        if len(content.strip()) > min_size:
                            flext_tests_files.append((py_file, content))
                    except (OSError, UnicodeDecodeError):
                        continue

        # Analyze duplicates
        duplicates: list[FlextDuplicationPlugin.TestDuplicate] = []

        # 1. Test vs Test (within project)
        for proj_name, test_files in project_tests.items():
            for i, (path1, content1) in enumerate(test_files):
                for path2, content2 in test_files[i + 1:]:
                    pair = self._analyze_pair(
                        path1,
                        content1,
                        path2,
                        content2,
                        effective_threshold,
                    )
                    if pair is not None:
                        dup = FlextDuplicationPlugin.TestDuplicate(
                            source_type="test-test-local",
                            file1_project=proj_name,
                            file1_path=pair.file1,
                            file2_project=proj_name,
                            file2_path=pair.file2,
                            similarity=pair.similarity,
                            shared_lines=pair.shared_lines,
                            consolidation_target=proj_name,
                            consolidation_strategy="unify-locally",
                        )
                        duplicates.append(dup)

        # 2. Test vs Test (cross-project) - consolidate to flext-tests
        projects_with_tests = sorted(project_tests.keys())
        for i, proj1 in enumerate(projects_with_tests):
            for proj2 in projects_with_tests[i + 1:]:
                for path1, content1 in project_tests[proj1]:
                    for path2, content2 in project_tests[proj2]:
                        pair = self._analyze_pair(
                            path1,
                            content1,
                            path2,
                            content2,
                            effective_threshold,
                        )
                        if pair is not None:
                            dup = FlextDuplicationPlugin.TestDuplicate(
                                source_type="test-test-cross",
                                file1_project=proj1,
                                file1_path=pair.file1,
                                file2_project=proj2,
                                file2_path=pair.file2,
                                similarity=pair.similarity,
                                shared_lines=pair.shared_lines,
                                consolidation_target="flext-tests",
                                consolidation_strategy="extract-to-flext-tests",
                            )
                            duplicates.append(dup)

        # 3. Test vs flext-tests - prevent duplication
        for proj_name, test_files in project_tests.items():
            for path1, content1 in test_files:
                for path2, content2 in flext_tests_files:
                    pair = self._analyze_pair(
                        path1,
                        content1,
                        path2,
                        content2,
                        effective_threshold,
                    )
                    if pair is not None:
                        dup = FlextDuplicationPlugin.TestDuplicate(
                            source_type="test-flext-tests",
                            file1_project=proj_name,
                            file1_path=pair.file1,
                            file2_project="flext-tests",
                            file2_path=pair.file2,
                            similarity=pair.similarity,
                            shared_lines=pair.shared_lines,
                            consolidation_target="flext-tests",
                            consolidation_strategy="use-flext-tests",
                        )
                        duplicates.append(dup)

        # 4. Test vs Src - prevent duplicating business logic
        for proj_name, test_files in project_tests.items():
            if proj_name not in project_src:
                continue
            for path1, content1 in test_files:
                for path2, content2 in project_src[proj_name]:
                    pair = self._analyze_pair(
                        path1,
                        content1,
                        path2,
                        content2,
                        effective_threshold,
                    )
                    if pair is not None:
                        dup = FlextDuplicationPlugin.TestDuplicate(
                            source_type="test-src",
                            file1_project=proj_name,
                            file1_path=pair.file1,
                            file2_project=proj_name,
                            file2_path=pair.file2,
                            similarity=pair.similarity,
                            shared_lines=pair.shared_lines,
                            consolidation_target=proj_name,
                            consolidation_strategy="refactor-src",
                        )
                        duplicates.append(dup)

        # Count by type
        test_dups = sum(1 for d in duplicates if "test-test" in d.source_type)
        test_src_dups = sum(1 for d in duplicates if d.source_type == "test-src")
        cross_proj_dups = sum(
            1
            for d in duplicates
            if d.source_type == "test-test-cross"
        )

        self._logger.debug(
            "Test check: %d test dups, %d test-src dups, %d cross-project",
            test_dups,
            test_src_dups,
            cross_proj_dups,
        )

        return FlextResult[FlextDuplicationPlugin.WorkspaceTestCheckResult].ok(
            FlextDuplicationPlugin.WorkspaceTestCheckResult(
                total_projects=len(project_tests),
                test_duplicates=test_dups,
                test_src_duplicates=test_src_dups,
                cross_project_test_duplicates=cross_proj_dups,
                duplicates=tuple(duplicates),
            )
        )


__all__ = ["FlextDuplicationPlugin"]
