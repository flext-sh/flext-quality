"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

from flext_core import FlextResult, FlextTypes as t
from flext_core.protocols import FlextProtocols as p_core


class FlextQualityProtocols(p_core):
    """Unified quality protocols extending p_core.

    Extends p_core to inherit all foundation protocols (Result, Service, etc.)
    and adds quality-specific protocols in the Quality namespace.

    Architecture:
    - EXTENDS: p_core (inherits Foundation, Domain, Application, etc.)
    - ADDS: Quality-specific protocols in Quality namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_quality.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Quality-specific protocols
    analyzer: p.Quality.QualityAnalyzer
    reporter: p.Quality.QualityReporter
    """

    class Quality:
        """Quality domain-specific protocols."""

        @runtime_checkable
        class QualityAnalyzer(Protocol):
            """Protocol for quality analysis operations."""

            def analyze_project(
                self,
                project_path: str,
                config: Mapping[str, t.GeneralValueType] | None = None,
            ) -> p_core.Result[Mapping[str, t.GeneralValueType]]:
                """Analyze a project for quality metrics."""
                ...  # INTERFACE

        @runtime_checkable
        class QualityReporter(Protocol):
            """Protocol for quality reporting operations."""

            def generate_report(
                self,
                analysis_results: Mapping[str, t.GeneralValueType],
                format_type: str = "html",
            ) -> p_core.Result[str]:
                """Generate a quality report from analysis results."""
                ...  # INTERFACE

        @runtime_checkable
        class QualityValidator(Protocol):
            """Protocol for quality validation operations."""

            def validate_thresholds(
                self,
                analysis_results: Mapping[str, t.GeneralValueType],
                thresholds: Mapping[str, t.GeneralValueType],
            ) -> p_core.Result[bool]:
                """Validate analysis results against quality thresholds."""
                ...  # INTERFACE

        @runtime_checkable
        class GitService(Protocol):
            """Git service protocol for quality tools."""

            def execute(
                self,
                repo_path: str,
                *,
                dry_run: bool = True,
                temp_path: str | None = None,
            ) -> p_core.Result[t.GeneralValueType]:
                """Execute git operation with dry-run support."""
                ...  # INTERFACE

        @runtime_checkable
        class OptimizationStrategy(Protocol):
            """Module optimization strategy protocol."""

            def optimize(
                self,
                module_path: str,
                *,
                dry_run: bool = True,
                temp_path: str | None = None,
            ) -> p_core.Result[t.GeneralValueType]:
                """Optimize module with dry-run support."""
                ...  # INTERFACE

        @runtime_checkable
        class QualityChecker(Protocol):
            """Quality checking protocol."""

            def check(
                self,
                project_path: str,
                config: dict[str, t.GeneralValueType] | None = None,
            ) -> p_core.Result[t.GeneralValueType]:
                """Run quality checks."""
                ...  # INTERFACE

        @runtime_checkable
        class Validator(Protocol):
            """Validation protocol."""

            def validate(
                self,
                target_path: str,
            ) -> p_core.Result[t.GeneralValueType]:
                """Validate target."""
                ...  # INTERFACE

        @runtime_checkable
        class ArchitectureAnalyzer(Protocol):
            """Architecture analysis protocol."""

            def analyze(
                self,
                project_path: str,
            ) -> p_core.Result[t.GeneralValueType]:
                """Analyze architecture."""
                ...  # INTERFACE

        @runtime_checkable
        class DependencyManager(Protocol):
            """Dependency management protocol."""

            def manage(
                self,
                project_path: str,
                operation: str,
            ) -> p_core.Result[t.GeneralValueType]:
                """Manage dependencies."""
                ...  # INTERFACE

        @runtime_checkable
        class IssueProtocol(Protocol):
            """Protocol for code quality issues - enables type-safe access."""

            @property
            def severity(self) -> str:
                """Issue severity level."""
                ...  # INTERFACE

            @property
            def message(self) -> str:
                """Issue description message."""
                ...  # INTERFACE

            @property
            def file_path(self) -> str:
                """File path containing the issue."""
                ...  # INTERFACE

            @property
            def line_number(self) -> int | None:
                """Line number of the issue (optional)."""
                ...  # INTERFACE

        @runtime_checkable
        class OperationExecutor(Protocol):
            """Protocol for batch operations that can be executed on files.

            Replaces Callable[[Path], FlextResult[bool]] to satisfy FLEXT
            architecture rules (use Protocol instead of Callable).

            Usage:
                class MyFixer:
                    def __call__(self, file_path: Path) -> p.Result[bool]:
                        # Fix something in the file
                        return r.ok(True)

                fixer: p.Quality.OperationExecutor = MyFixer()
            """

            def __call__(
                self,
                file_path: t.GeneralValueType,
            ) -> p_core.Result[bool]:
                """Execute operation on a file.

                Args:
                    file_path: Path to file to operate on

                Returns:
                    Result[bool] indicating success

                """
                ...  # INTERFACE

        @runtime_checkable
        class JsonParserProtocol(Protocol):
            """Protocol for JSON output parsers used in tool backends.

            This protocol defines the interface for parsing JSON output from
            external quality tools (ruff, mypy, bandit, etc.) into structured
            issue dictionaries.

            Usage:
                def my_parser(stdout: str) -> list[dict[str, t.GeneralValueType]]:
                    return json.loads(stdout) if stdout.strip() else []

                # my_parser satisfies JsonParserProtocol
            """

            def __call__(
                self,
                stdout: str,
            ) -> list[dict[str, t.GeneralValueType]]:
                """Parse JSON output from tool stdout.

                Args:
                    stdout: Raw stdout string from tool execution

                Returns:
                    List of parsed issue dictionaries

                """
                ...  # INTERFACE

        @runtime_checkable
        class FixFunction(Protocol):
            """Protocol for fix functions used in fix_with_validation.

            This protocol defines the interface for functions that apply fixes
            to files with FlextResult[bool] return type.

            Usage:
                def my_fix(file_path: str) -> FlextResult[bool]:
                    # Apply fix to file
                    return FlextResult[bool].ok(True)

                # my_fix satisfies FixFunction protocol
            """

            def __call__(self, file_path: str) -> p_core.Result[bool]:
                """Apply fix to a file.

                Args:
                    file_path: Path to the file to fix.

                Returns:
                    FlextResult[bool] indicating success or failure.

                """
                ...  # INTERFACE

        @runtime_checkable
        class BatchOperation(Protocol):
            """Protocol for batch operations with validation.

            Provides a standardized interface for fix scripts and hooks
            that need dry-run, backup, execute, and rollback capabilities.

            All methods return FlextResult for consistent error handling.

            Usage:
                class MyBatchOperation:
                    def dry_run(self, targets: list[Path]) -> FlextResult[dict]:
                        # Preview changes
                        ...

                    def backup(self, targets: list[Path]) -> FlextResult[Path]:
                        # Create backup
                        ...

                    def execute(
                        self,
                        targets: list[Path],
                        backup_path: Path | None,
                    ) -> FlextResult[dict]:
                        # Apply changes
                        ...

                    def rollback(self, backup_path: Path) -> FlextResult[bool]:
                        # Restore from backup
                        ...
            """

            def dry_run(
                self,
                targets: list[Path],
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                """Preview changes without modifying files.

                Args:
                    targets: List of file paths to analyze.

                Returns:
                    FlextResult with preview information (files, changes, etc).

                """
                ...  # INTERFACE

            def backup(
                self,
                targets: list[Path],
            ) -> FlextResult[Path]:
                """Create timestamped backup of target files.

                Args:
                    targets: List of file paths to backup.

                Returns:
                    FlextResult with path to backup archive.

                """
                ...  # INTERFACE

            def execute(
                self,
                targets: list[Path],
                backup_path: Path | None,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                """Execute operation with validation.

                Args:
                    targets: List of file paths to modify.
                    backup_path: Optional path to backup for rollback.

                Returns:
                    FlextResult with execution results.

                """
                ...  # INTERFACE

            def rollback(
                self,
                backup_path: Path,
            ) -> FlextResult[bool]:
                """Restore files from backup.

                Args:
                    backup_path: Path to backup archive.

                Returns:
                    FlextResult indicating success or failure.

                """
                ...  # INTERFACE


# Runtime alias for simplified usage
p = FlextQualityProtocols

__all__ = [
    "FlextQualityProtocols",
    "p",
]
