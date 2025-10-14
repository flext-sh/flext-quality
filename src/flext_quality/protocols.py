"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextCore

from .models import FlextQualityModels


class FlextQualityProtocols(FlextCore.Protocols):
    """Quality analysis protocol definitions."""

    class QualityAnalyzer(Protocol):
        """Protocol for quality analysis operations."""

        def analyze_project(
            self,
            project_path: str,
            config: FlextQualityModels.Analysis.AnalysisConfiguration | None = None,
        ) -> FlextCore.Result[FlextQualityModels.AnalysisResults]:
            """Analyze a project for quality metrics."""
            ...

    class QualityReporter(Protocol):
        """Protocol for quality reporting operations."""

        def generate_report(
            self,
            analysis_results: FlextQualityModels.AnalysisResults,
            format_type: str = "html",
        ) -> FlextCore.Result[str]:
            """Generate a quality report from analysis results."""
            ...

    class QualityValidator(Protocol):
        """Protocol for quality validation operations."""

        def validate_thresholds(
            self,
            analysis_results: FlextQualityModels.AnalysisResults,
            thresholds: FlextQualityModels.Analysis.AnalysisThresholds,
        ) -> FlextCore.Result[bool]:
            """Validate analysis results against quality thresholds."""
            ...

    # ==== INTERNAL TOOLS PROTOCOLS (from flext_tools migration) ====

    class GitService(Protocol):
        """Git service protocol for quality tools."""

        def execute(
            self,
            repo_path: str,
            *,
            dry_run: bool = True,
            temp_path: str | None = None,
        ) -> FlextCore.Result[object]:
            """Execute git operation with dry-run support."""
            ...

    class OptimizationStrategy(Protocol):
        """Module optimization strategy protocol."""

        def optimize(
            self,
            module_path: str,
            *,
            dry_run: bool = True,
            temp_path: str | None = None,
        ) -> FlextCore.Result[object]:
            """Optimize module with dry-run support."""
            ...

    class QualityChecker(Protocol):
        """Quality checking protocol."""

        def check(
            self,
            project_path: str,
            config: dict[str, object] | None = None,
        ) -> FlextCore.Result[object]:
            """Run quality checks."""
            ...

    class Validator(Protocol):
        """Validation protocol."""

        def validate(
            self,
            target_path: str,
        ) -> FlextCore.Result[object]:
            """Validate target."""
            ...

    class ArchitectureAnalyzer(Protocol):
        """Architecture analysis protocol."""

        def analyze(
            self,
            project_path: str,
        ) -> FlextCore.Result[object]:
            """Analyze architecture."""
            ...

    class DependencyManager(Protocol):
        """Dependency management protocol."""

        def manage(
            self,
            project_path: str,
            operation: str,
        ) -> FlextCore.Result[object]:
            """Manage dependencies."""
            ...


__all__ = ["FlextQualityProtocols"]
