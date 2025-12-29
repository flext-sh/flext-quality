# VERIFIED_NEW_MODULE
"""Test structure validation using FlextQualityASTBackend.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides AST-based validation of test structure:
- Verifies src/ modules have corresponding test files
- Detects missing test coverage for modules
- Generates coverage reports for test structure
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult as r, FlextService, FlextTypes as t

from flext_quality.ast_backend import FlextQualityASTBackend


class FlextQualityTestStructureOperation(FlextService[dict[str, t.GeneralValueType]]):
    """Validates test structure against source modules using AST analysis.

    This operation analyzes Python projects to verify that source modules
    have corresponding test files. Uses FlextQualityASTBackend for AST analysis.

    All nested classes and helpers are inside this facade class.
    """

    @dataclass
    class ModuleCoverage:
        """Represents test coverage status for a source module."""

        module_name: str
        module_path: Path
        has_test: bool
        test_path: Path | None = None
        class_count: int = 0
        function_count: int = 0

    @dataclass
    class AnalysisResult:
        """Result of analyzing test structure."""

        project_path: Path
        modules: list[FlextQualityTestStructureOperation.ModuleCoverage] = field(
            default_factory=list
        )

        @property
        def covered_count(self: Self) -> int:
            """Get count of modules with tests."""
            return sum(1 for m in self.modules if m.has_test)

        @property
        def uncovered_count(self: Self) -> int:
            """Get count of modules without tests."""
            return sum(1 for m in self.modules if not m.has_test)

        @property
        def coverage_percent(self: Self) -> float:
            """Get test coverage percentage."""
            if not self.modules:
                return 100.0
            return (self.covered_count / len(self.modules)) * 100

        @property
        def uncovered_modules(self: Self) -> list[str]:
            """Get list of module names without tests."""
            return [m.module_name for m in self.modules if not m.has_test]

    class Helpers:
        """Static helper methods for structure analysis."""

        @staticmethod
        def get_test_file_name(module_name: str) -> str:
            """Generate expected test file name for a module."""
            return f"test_{module_name}.py"

        @staticmethod
        def is_testable_module(file_path: Path) -> bool:
            """Check if a module should have tests."""
            name = file_path.stem
            # Skip private modules, conftest, and __init__
            if name.startswith("_"):
                return False
            return name not in {"conftest", "__init__"}

        @staticmethod
        def find_test_directories(project_path: Path) -> list[Path]:
            """Find all test directories in a project."""
            # Find tests/ directories
            test_dirs = [d for d in project_path.rglob("tests") if d.is_dir()]
            # Also check for test/ (singular), avoiding duplicates
            test_dirs.extend(
                d
                for d in project_path.rglob("test")
                if d.is_dir() and d not in test_dirs
            )
            return test_dirs

    def __init__(self: Self) -> None:
        """Initialize structure operation."""
        super().__init__()
        self._ast_backend = FlextQualityASTBackend()
        self._logger = FlextLogger(__name__)

    def analyze_project(self: Self, project_path: Path) -> r[AnalysisResult]:
        """Analyze test structure for a project.

        Args:
            project_path: Path to the project root

        Returns:
            FlextResult containing AnalysisResult with coverage info

        """
        if not project_path.exists():
            return r[FlextQualityTestStructureOperation.AnalysisResult].fail(
                f"Project path not found: {project_path}"
            )

        src_path = project_path / "src"
        if not src_path.exists():
            # Try without src/ directory
            src_path = project_path

        # Find all test directories
        test_dirs = self.Helpers.find_test_directories(project_path)

        # Collect all test files
        test_files: set[str] = set()
        for test_dir in test_dirs:
            test_files.update(
                test_file.stem for test_file in test_dir.rglob("test_*.py")
            )

        # Analyze source modules
        modules: list[FlextQualityTestStructureOperation.ModuleCoverage] = []

        for py_file in src_path.rglob("*.py"):
            if not self.Helpers.is_testable_module(py_file):
                continue

            module_name = py_file.stem
            expected_test = f"test_{module_name}"

            # Get module info using AST
            module_info = self._analyze_module(py_file)

            has_test = expected_test in test_files
            test_path = None

            if has_test:
                # Find the actual test file path
                for test_dir in test_dirs:
                    potential_test = test_dir / f"{expected_test}.py"
                    if potential_test.exists():
                        test_path = potential_test
                        break
                    # Also check subdirectories
                    for subtest in test_dir.rglob(f"{expected_test}.py"):
                        test_path = subtest
                        break

            modules.append(
                self.ModuleCoverage(
                    module_name=module_name,
                    module_path=py_file,
                    has_test=has_test,
                    test_path=test_path,
                    class_count=module_info.get("class_count", 0),
                    function_count=module_info.get("function_count", 0),
                )
            )

        analysis_result = FlextQualityTestStructureOperation.AnalysisResult(
            project_path=project_path,
            modules=modules,
        )

        return r[FlextQualityTestStructureOperation.AnalysisResult].ok(analysis_result)

    def _analyze_module(self: Self, file_path: Path) -> dict[str, int]:
        """Analyze a module using AST backend.

        Returns default counts if file cannot be read or parsed.
        """
        default_counts = {"class_count": 0, "function_count": 0}

        if not file_path.exists():
            self._logger.debug("File does not exist: %s", file_path)
            return default_counts

        source = file_path.read_text(encoding="utf-8")
        result = self._ast_backend.analyze(source, file_path)

        if result.is_failure:
            self._logger.debug(
                "AST analysis failed for %s: %s", file_path, result.error
            )
            return default_counts

        if not result.value:
            return default_counts

        classes = result.value.get("classes", [])
        functions = result.value.get("functions", [])
        return {
            "class_count": len(classes) if isinstance(classes, list) else 0,
            "function_count": len(functions) if isinstance(functions, list) else 0,
        }

    def dry_run(self: Self, targets: list[Path]) -> r[dict[str, t.GeneralValueType]]:
        """Preview test structure analysis without modifications.

        Args:
            targets: List of project directories to analyze

        Returns:
            FlextResult with summary of structure analysis

        """
        all_results: list[dict[str, t.GeneralValueType]] = []
        total_modules = 0
        total_covered = 0
        total_uncovered = 0

        for target in targets:
            if not target.is_dir():
                continue

            result = self.analyze_project(target)
            if result.is_success:
                analysis = result.value
                total_modules += len(analysis.modules)
                total_covered += analysis.covered_count
                total_uncovered += analysis.uncovered_count

                all_results.append({
                    "project": str(target),
                    "total_modules": len(analysis.modules),
                    "covered": analysis.covered_count,
                    "uncovered": analysis.uncovered_count,
                    "coverage_percent": round(analysis.coverage_percent, 2),
                    "uncovered_modules": analysis.uncovered_modules,
                })

        overall_coverage = (
            (total_covered / total_modules * 100) if total_modules > 0 else 100.0
        )

        summary: dict[str, t.GeneralValueType] = {
            "projects_analyzed": len(all_results),
            "total_modules": total_modules,
            "total_covered": total_covered,
            "total_uncovered": total_uncovered,
            "overall_coverage_percent": round(overall_coverage, 2),
            "results": all_results,
        }

        return r[dict[str, t.GeneralValueType]].ok(summary)

    def run(
        self: Self,
        targets: list[Path],
        _backup_path: Path | None = None,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Run test structure analysis (same as dry_run for detection-only).

        Args:
            targets: List of project directories to analyze
            _backup_path: Not used for detection-only operation

        Returns:
            FlextResult with summary of structure analysis

        """
        # Detection-only operation - same as dry_run
        return self.dry_run(targets)

    def execute(self: Self) -> r[dict[str, t.GeneralValueType]]:
        """Execute the service operation.

        Implementation of FlextService abstract method.
        Uses current directory as default target.

        Returns:
            FlextResult with operation summary

        """
        return self.dry_run([Path.cwd()])

    def rollback(self: Self, _backup_path: Path) -> r[dict[str, t.GeneralValueType]]:
        """Rollback not applicable for detection-only operation.

        Args:
            _backup_path: Backup path (not used)

        Returns:
            FlextResult indicating rollback not applicable

        """
        return r[dict[str, t.GeneralValueType]].ok({
            "status": "not_applicable",
            "message": "Detection-only operation has no changes to rollback",
        })


# Short alias for convenience
TestStructureOperation = FlextQualityTestStructureOperation
