"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

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
                config: Mapping[str, object] | None = None,
            ) -> p_core.Result[Mapping[str, object]]:
                """Analyze a project for quality metrics."""
                ...

        @runtime_checkable
        class QualityReporter(Protocol):
            """Protocol for quality reporting operations."""

            def generate_report(
                self,
                analysis_results: Mapping[str, object],
                format_type: str = "html",
            ) -> p_core.Result[str]:
                """Generate a quality report from analysis results."""
                ...

        @runtime_checkable
        class QualityValidator(Protocol):
            """Protocol for quality validation operations."""

            def validate_thresholds(
                self,
                analysis_results: Mapping[str, object],
                thresholds: Mapping[str, object],
            ) -> p_core.Result[bool]:
                """Validate analysis results against quality thresholds."""
                ...

        @runtime_checkable
        class GitService(Protocol):
            """Git service protocol for quality tools."""

            def execute(
                self,
                repo_path: str,
                *,
                dry_run: bool = True,
                temp_path: str | None = None,
            ) -> p_core.Result[object]:
                """Execute git operation with dry-run support."""
                ...

        @runtime_checkable
        class OptimizationStrategy(Protocol):
            """Module optimization strategy protocol."""

            def optimize(
                self,
                module_path: str,
                *,
                dry_run: bool = True,
                temp_path: str | None = None,
            ) -> p_core.Result[object]:
                """Optimize module with dry-run support."""
                ...

        @runtime_checkable
        class QualityChecker(Protocol):
            """Quality checking protocol."""

            def check(
                self,
                project_path: str,
                config: dict[str, object] | None = None,
            ) -> p_core.Result[object]:
                """Run quality checks."""
                ...

        @runtime_checkable
        class Validator(Protocol):
            """Validation protocol."""

            def validate(
                self,
                target_path: str,
            ) -> p_core.Result[object]:
                """Validate target."""
                ...

        @runtime_checkable
        class ArchitectureAnalyzer(Protocol):
            """Architecture analysis protocol."""

            def analyze(
                self,
                project_path: str,
            ) -> p_core.Result[object]:
                """Analyze architecture."""
                ...

        @runtime_checkable
        class DependencyManager(Protocol):
            """Dependency management protocol."""

            def manage(
                self,
                project_path: str,
                operation: str,
            ) -> p_core.Result[object]:
                """Manage dependencies."""
                ...

        @runtime_checkable
        class IssueProtocol(Protocol):
            """Protocol for code quality issues - enables type-safe access."""

            @property
            def severity(self) -> object:
                """Issue severity level."""
                ...

            @property
            def message(self) -> str:
                """Issue description message."""
                ...

            @property
            def file_path(self) -> str:
                """File path containing the issue."""
                ...

            @property
            def line_number(self) -> int | None:
                """Line number of the issue (optional)."""
                ...


# Runtime alias for simplified usage
p = FlextQualityProtocols

__all__ = [
    "FlextQualityProtocols",
    "p",
]
