# VERIFIED_NEW_MODULE
"""Test inheritance detection and fixing using libcst and Rope.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides AST-based detection of test class inheritance issues:
- Test classes missing proper base class inheritance
- Classes using wrong test base classes
- Detection of patterns that should inherit from flext_tests bases
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Self

import libcst as cst
from flext_core import FlextResult as r, FlextService, FlextTypes as t
from rope.base import libutils
from rope.base.project import Project as RopeProject


class FlextQualityTestInheritanceOperation(FlextService[dict[str, t.GeneralValueType]]):
    """Detects and fixes test class inheritance issues using libcst and Rope.

    This operation analyzes Python test files to find classes that should
    inherit from FLEXT test base classes but don't. Uses libcst for safe
    AST traversal with position tracking and Rope for refactoring.

    All nested classes and helpers are inside this facade class.
    """

    # Expected base classes for test files
    EXPECTED_BASE_CLASSES: ClassVar[frozenset[str]] = frozenset({
        "FlextTestsServiceBase",
        "s",  # Short alias for FlextTestsServiceBase
    })

    # Patterns that indicate a test class
    TEST_CLASS_PATTERNS: ClassVar[frozenset[str]] = frozenset({
        "Test",
        "test_",
    })

    # Base classes that indicate proper inheritance
    VALID_TEST_BASES: ClassVar[frozenset[str]] = frozenset({
        "FlextTestsServiceBase",
        "s",
        "flext_t.FlextTestsServiceBase",
        "flext_tests.s",
    })

    @dataclass
    class InheritanceIssue:
        """Represents a detected inheritance issue."""

        class_name: str
        line: int
        column: int
        current_bases: list[str]
        suggested_base: str
        message: str
        file_path: str = ""

    @dataclass
    class AnalysisResult:
        """Result of analyzing a file for inheritance issues."""

        file_path: Path
        issues: list[FlextQualityTestInheritanceOperation.InheritanceIssue] = field(
            default_factory=list
        )

        @property
        def has_issues(self: Self) -> bool:
            """Check if any issues were found."""
            return len(self.issues) > 0

        @property
        def issue_count(self: Self) -> int:
            """Get the number of issues."""
            return len(self.issues)

    class MetadataVisitor(cst.MetadataDependent):
        """Visitor with position metadata support for inheritance detection."""

        # Required by libcst MetadataDependent  # CONFIG
        METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)  # CONFIG

        def __init__(self: Self, file_path: str) -> None:
            """Initialize with file path for context."""
            self.issues: list[
                FlextQualityTestInheritanceOperation.InheritanceIssue
            ] = []
            self.file_path = file_path

        def visit_ClassDef(self: Self, node: cst.ClassDef) -> bool | None:
            """Detect test classes missing proper inheritance."""
            class_name = node.name.value

            # Check if this looks like a test class
            is_test_class = any(
                pattern in class_name
                for pattern in FlextQualityTestInheritanceOperation.TEST_CLASS_PATTERNS
            )

            if not is_test_class:
                return None

            # Get current base classes
            current_bases = self._extract_base_classes(node)

            # Check if any valid test base is present
            has_valid_base = any(
                base in FlextQualityTestInheritanceOperation.VALID_TEST_BASES
                for base in current_bases
            )

            if not has_valid_base and current_bases != ["object"]:
                # This test class is missing proper inheritance
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.issues.append(
                    FlextQualityTestInheritanceOperation.InheritanceIssue(
                        class_name=class_name,
                        line=pos.start.line,
                        column=pos.start.column,
                        current_bases=current_bases,
                        suggested_base="s",
                        message=f"Test class '{class_name}' should inherit from 's' (FlextTestsServiceBase)",
                        file_path=self.file_path,
                    )
                )

            return None

        def _extract_base_classes(self: Self, node: cst.ClassDef) -> list[str]:
            """Extract base class names from a class definition."""
            if not node.bases:
                return []

            bases: list[str] = []
            for arg in node.bases:
                base_name = self._get_base_name(arg.value)
                if base_name:
                    bases.append(base_name)
            return bases

        def _get_base_name(self: Self, node: cst.BaseExpression) -> str:
            """Extract name from base class expression."""
            if isinstance(node, cst.Name):
                return node.value
            if isinstance(node, cst.Attribute):
                return f"{self._get_base_name(node.value)}.{node.attr.value}"
            return ""

    class RopeIntegration:
        """Rope library integration for inheritance refactoring."""

        def analyze_class(
            self: Self,
            project_path: Path,
            file_path: Path,
            class_name: str,
        ) -> r[dict[str, t.GeneralValueType]]:
            """Analyze a class using Rope to get detailed info.

            Args:
                project_path: Root path of project.
                file_path: Path to the file containing the class.
                class_name: Name of the class to analyze.

            Returns:
                FlextResult with class information.

            """
            rope_project = RopeProject(str(project_path))

            try:
                resource = libutils.path_to_resource(rope_project, str(file_path))
                if resource is None:
                    return r[dict[str, t.GeneralValueType]].fail(
                        f"Could not load resource: {file_path}"
                    )

                pymodule = rope_project.get_pymodule(resource)
                try:
                    defined_names = pymodule.get_defined_names()
                except AttributeError:
                    defined_names = {}

                if class_name not in defined_names:
                    return r[dict[str, t.GeneralValueType]].fail(
                        f"Class '{class_name}' not found in {file_path}"
                    )

                return r[dict[str, t.GeneralValueType]].ok({
                    "class_name": class_name,
                    "file_path": str(file_path),
                    "found": True,
                })

            except Exception as e:
                return r[dict[str, t.GeneralValueType]].fail(
                    f"Rope analysis failed: {e}"
                )
            finally:
                rope_project.close()

    def analyze(self: Self, file_path: Path) -> r[AnalysisResult]:
        """Analyze a file for inheritance issues.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            FlextResult containing AnalysisResult with issues

        """
        if not file_path.exists():
            return r[self.AnalysisResult].fail(f"File not found: {file_path}")

        if file_path.suffix != ".py":
            return r[self.AnalysisResult].fail(f"Not a Python file: {file_path}")

        # Only analyze test files
        if not file_path.name.startswith("test_"):
            return r[self.AnalysisResult].ok(
                self.AnalysisResult(file_path=file_path, issues=[])
            )

        try:
            source = file_path.read_text(encoding="utf-8")
            module = cst.parse_module(source)

            # Use metadata wrapper for position tracking
            wrapper = cst.metadata.MetadataWrapper(module)
            visitor = self.MetadataVisitor(str(file_path))
            wrapper.visit(visitor)

            result = self.AnalysisResult(
                file_path=file_path,
                issues=visitor.issues,
            )

            return r[self.AnalysisResult].ok(result)

        except cst.ParserSyntaxError as e:
            return r[self.AnalysisResult].fail(f"Syntax error in {file_path}: {e}")

    def analyze_directory(
        self: Self,
        directory: Path,
        pattern: str = "test_*.py",
    ) -> r[list[AnalysisResult]]:
        """Analyze all test files in a directory.

        Args:
            directory: Directory to search for test files
            pattern: Glob pattern for test files

        Returns:
            FlextResult containing list of AnalysisResults

        """
        if not directory.exists():
            return r[list[self.AnalysisResult]].fail(
                f"Directory not found: {directory}"
            )

        results: list[self.AnalysisResult] = []

        for file_path in directory.rglob(pattern):
            result = self.analyze(file_path)
            if result.is_success:
                results.append(result.value)

        return r[list[self.AnalysisResult]].ok(results)

    def dry_run(
        self: Self, targets: list[Path]
    ) -> r[dict[str, t.GeneralValueType]]:
        """Preview inheritance issue detection without modifications.

        Args:
            targets: List of files or directories to analyze

        Returns:
            FlextResult with summary of issues found

        """
        total_issues = 0
        file_count = 0
        issues_by_class: dict[str, int] = {}
        all_issues: list[dict[str, t.GeneralValueType]] = []

        for target in targets:
            if target.is_file():
                result = self.analyze(target)
                if result.is_success:
                    file_count += 1
                    for issue in result.value.issues:
                        total_issues += 1
                        issues_by_class[issue.class_name] = (
                            issues_by_class.get(issue.class_name, 0) + 1
                        )
                        all_issues.append({
                            "class": issue.class_name,
                            "file": issue.file_path,
                            "line": issue.line,
                            "current_bases": issue.current_bases,
                            "suggested": issue.suggested_base,
                        })
            elif target.is_dir():
                result = self.analyze_directory(target)
                if result.is_success:
                    for analysis in result.value:
                        file_count += 1
                        for issue in analysis.issues:
                            total_issues += 1
                            issues_by_class[issue.class_name] = (
                                issues_by_class.get(issue.class_name, 0) + 1
                            )
                            all_issues.append({
                                "class": issue.class_name,
                                "file": str(analysis.file_path),
                                "line": issue.line,
                                "current_bases": issue.current_bases,
                                "suggested": issue.suggested_base,
                            })

        summary: dict[str, t.GeneralValueType] = {
            "files_analyzed": file_count,
            "total_issues": total_issues,
            "issues": all_issues,
            "classes_affected": list(issues_by_class.keys()),
        }

        return r[dict[str, t.GeneralValueType]].ok(summary)

    def execute(
        self: Self,
        targets: list[Path],
        _backup_path: Path | None = None,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Execute inheritance issue detection (same as dry_run for detection-only).

        Args:
            targets: List of files or directories to analyze
            _backup_path: Not used for detection-only operation

        Returns:
            FlextResult with summary of issues found

        """
        # Detection-only operation - same as dry_run
        return self.dry_run(targets)

    def rollback(
        self: Self, _backup_path: Path
    ) -> r[dict[str, t.GeneralValueType]]:
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
TestInheritanceOperation = FlextQualityTestInheritanceOperation
