"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextTypes as t
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


# Runtime alias for simplified usage
p = FlextQualityProtocols

__all__ = [
    "FlextQualityProtocols",
    "p",
]
