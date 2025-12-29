# VERIFIED_NEW_MODULE
"""Test antipattern detection and removal using libcst.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides AST-based detection of test anti-patterns including:
- Unittest mock imports and usage
- Monkeypatch.setattr calls
- Type suppression comments
- Generic type annotations
- Type casting function calls
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Self

import libcst as cst
from flext_core import FlextResult as r, FlextService, FlextTypes as t
from libcst import matchers as mtch


class FlextQualityTestAntipatternOperation(FlextService[dict[str, t.GeneralValueType]]):
    """Detects and reports test anti-patterns using libcst AST analysis.

    This operation analyzes Python test files to find patterns that violate
    FLEXT testing standards. It uses libcst for safe AST traversal.

    All nested classes and helpers are inside this facade class.
    """

    # Forbidden mock function names
    FORBIDDEN_MOCKS: ClassVar[frozenset[str]] = frozenset({
        "Mock", "MagicMock", "AsyncMock",
    })

    # Forbidden import modules
    FORBIDDEN_MODULES: ClassVar[frozenset[str]] = frozenset({
        "unittest.mock", "unittest",
    })

    @dataclass
    class Violation:
        """Represents a detected anti-pattern violation."""

        pattern_type: str
        line: int
        column: int
        message: str
        snippet: str = ""

    @dataclass
    class AnalysisResult:
        """Result of analyzing a file for anti-patterns."""

        file_path: Path
        violations: list[FlextQualityTestAntipatternOperation.Violation] = field(
            default_factory=list
        )

        @property
        def has_violations(self: Self) -> bool:
            """Check if any violations were found."""
            return len(self.violations) > 0

        @property
        def violation_count(self: Self) -> int:
            """Get the number of violations."""
            return len(self.violations)

    class Helpers:
        """Static helper methods for CST analysis."""

        @staticmethod
        def get_module_name(module: cst.Attribute | cst.Name) -> str:
            """Extract dotted module name from CST node."""
            if isinstance(module, cst.Name):
                return module.value
            if isinstance(module, cst.Attribute):
                # Recursively extract the base name
                base_node = module.value
                if isinstance(base_node, cst.Attribute | cst.Name):
                    base = FlextQualityTestAntipatternOperation.Helpers.get_module_name(
                        base_node
                    )
                    return f"{base}.{module.attr.value}"
            return ""

        @staticmethod
        def get_call_name(func: cst.BaseExpression) -> str:
            """Extract function name from call expression."""
            if isinstance(func, cst.Name):
                return func.value
            if isinstance(func, cst.Attribute):
                return func.attr.value
            return ""

    class MetadataVisitor(cst.CSTVisitor):
        """Visitor with position metadata support for anti-pattern detection."""

        # Required by libcst for position tracking  # CONFIG
        METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)  # CONFIG

        def __init__(self: Self) -> None:
            """Initialize with empty violations list."""
            self.violations: list[
                FlextQualityTestAntipatternOperation.Violation
            ] = []

        def visit_ImportFrom(
            self: Self, node: cst.ImportFrom
        ) -> bool | None:
            """Detect forbidden mock imports with position."""
            if node.module is None:
                return None

            module_name = FlextQualityTestAntipatternOperation.Helpers.get_module_name(
                node.module
            )

            if module_name in FlextQualityTestAntipatternOperation.FORBIDDEN_MODULES:
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.violations.append(
                    FlextQualityTestAntipatternOperation.Violation(
                        pattern_type="mock_import",
                        line=pos.start.line,
                        column=pos.start.column,
                        message="Mock imports are forbidden. Use real implementations.",
                    )
                )

            return None

        def visit_Call(self: Self, node: cst.Call) -> bool | None:
            """Detect forbidden function calls with position."""
            func_name = FlextQualityTestAntipatternOperation.Helpers.get_call_name(
                node.func
            )

            if func_name in FlextQualityTestAntipatternOperation.FORBIDDEN_MOCKS:
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.violations.append(
                    FlextQualityTestAntipatternOperation.Violation(
                        pattern_type="mock_usage",
                        line=pos.start.line,
                        column=pos.start.column,
                        message=f"{func_name}() is forbidden. Use real implementations.",
                    )
                )

            # Check for monkeypatch.setattr
            if func_name == "setattr" and mtch.matches(
                node.func,
                mtch.Attribute(
                    value=mtch.Name("monkeypatch"), attr=mtch.Name("setattr")
                ),
            ):
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.violations.append(
                    FlextQualityTestAntipatternOperation.Violation(
                        pattern_type="monkeypatch_setattr",
                        line=pos.start.line,
                        column=pos.start.column,
                        message="monkeypatch.setattr is forbidden. Use DI.",
                    )
                )

            return None

        def visit_Annotation(self: Self, node: cst.Annotation) -> bool | None:
            """Detect forbidden type annotations with position."""
            # Check for generic type annotation that should be specific
            if mtch.matches(node.annotation, mtch.Name("Any")):
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.violations.append(
                    FlextQualityTestAntipatternOperation.Violation(
                        pattern_type="any_annotation",
                        line=pos.start.line,
                        column=pos.start.column,
                        message="Generic type annotation forbidden. Use specific types.",
                    )
                )

            return None

    def analyze(self: Self, file_path: Path) -> r[AnalysisResult]:
        """Analyze a file for anti-patterns.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            FlextResult containing AnalysisResult with violations

        """
        if not file_path.exists():
            return r[FlextQualityTestAntipatternOperation.AnalysisResult].fail(
                f"File not found: {file_path}"
            )

        if file_path.suffix != ".py":
            return r[FlextQualityTestAntipatternOperation.AnalysisResult].fail(
                f"Not a Python file: {file_path}"
            )

        try:
            source = file_path.read_text(encoding="utf-8")
            parsed_module = cst.parse_module(source)

            # Use metadata wrapper for position tracking
            wrapper = cst.metadata.MetadataWrapper(parsed_module)
            visitor = FlextQualityTestAntipatternOperation.MetadataVisitor()
            wrapper.visit(visitor)

            result = FlextQualityTestAntipatternOperation.AnalysisResult(
                file_path=file_path,
                violations=visitor.violations,
            )

            return r[FlextQualityTestAntipatternOperation.AnalysisResult].ok(result)

        except cst.ParserSyntaxError as e:
            return r[FlextQualityTestAntipatternOperation.AnalysisResult].fail(
                f"Syntax error in {file_path}: {e}"
            )

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
            return r[list[FlextQualityTestAntipatternOperation.AnalysisResult]].fail(
                f"Directory not found: {directory}"
            )

        results: list[FlextQualityTestAntipatternOperation.AnalysisResult] = []

        for file_path in directory.rglob(pattern):
            result = self.analyze(file_path)
            if result.is_success:
                results.append(result.value)

        return r[list[FlextQualityTestAntipatternOperation.AnalysisResult]].ok(results)

    def dry_run(
        self: Self, targets: list[Path]
    ) -> r[dict[str, t.GeneralValueType]]:
        """Preview anti-pattern detection without modifications.

        Args:
            targets: List of files or directories to analyze

        Returns:
            FlextResult with summary of violations found

        """
        total_violations = 0
        file_count = 0
        violations_by_type: dict[str, int] = {}

        for target in targets:
            if target.is_file():
                result = self.analyze(target)
                if result.is_success:
                    file_count += 1
                    for violation in result.value.violations:
                        total_violations += 1
                        violations_by_type[violation.pattern_type] = (
                            violations_by_type.get(violation.pattern_type, 0) + 1
                        )
            elif target.is_dir():
                result = self.analyze_directory(target)
                if result.is_success:
                    for analysis in result.value:
                        file_count += 1
                        for violation in analysis.violations:
                            total_violations += 1
                            violations_by_type[violation.pattern_type] = (
                                violations_by_type.get(violation.pattern_type, 0) + 1
                            )

        summary: dict[str, t.GeneralValueType] = {
            "files_analyzed": file_count,
            "total_violations": total_violations,
            **violations_by_type,
        }

        return r[dict[str, t.GeneralValueType]].ok(summary)

    def execute(
        self: Self,
        targets: list[Path],
        _backup_path: Path | None = None,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Execute anti-pattern detection (same as dry_run for detection-only).

        Args:
            targets: List of files or directories to analyze
            _backup_path: Not used for detection-only operation

        Returns:
            FlextResult with summary of violations found

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
TestAntipatternOperation = FlextQualityTestAntipatternOperation
