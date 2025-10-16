"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextProtocols, FlextResult

from .models import FlextQualityModels
from .typings import FlextQualityTypes


class FlextQualityProtocols(FlextProtocols):
    """Quality analysis protocol definitions."""

    class QualityAnalyzer(Protocol):
        """Protocol for quality analysis operations."""

        def analyze_project(
            self,
            project_path: str,
            config: FlextQualityTypes.Analysis.AnalysisConfiguration | None = None,
        ) -> FlextResult[FlextQualityModels.AnalysisResults]:
            """Analyze a project for quality metrics."""
            ...

    class QualityReporter(Protocol):
        """Protocol for quality reporting operations."""

        def generate_report(
            self,
            analysis_results: FlextQualityModels.AnalysisResults,
            format_type: str = "html",
        ) -> FlextResult[str]:
            """Generate a quality report from analysis results."""
            ...

    class QualityValidator(Protocol):
        """Protocol for quality validation operations."""

        def validate_thresholds(
            self,
            analysis_results: FlextQualityModels.AnalysisResults,
            thresholds: FlextQualityTypes.Analysis.AnalysisThresholds,
        ) -> FlextResult[bool]:
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
        ) -> FlextResult[object]:
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
        ) -> FlextResult[object]:
            """Optimize module with dry-run support."""
            ...

    class QualityChecker(Protocol):
        """Quality checking protocol."""

        def check(
            self,
            project_path: str,
            config: dict[str, object] | None = None,
        ) -> FlextResult[object]:
            """Run quality checks."""
            ...

    class Validator(Protocol):
        """Validation protocol."""

        def validate(
            self,
            target_path: str,
        ) -> FlextResult[object]:
            """Validate target."""
            ...

    class ArchitectureAnalyzer(Protocol):
        """Architecture analysis protocol."""

        def analyze(
            self,
            project_path: str,
        ) -> FlextResult[object]:
            """Analyze architecture."""
            ...

    class DependencyManager(Protocol):
        """Dependency management protocol."""

        def manage(
            self,
            project_path: str,
            operation: str,
        ) -> FlextResult[object]:
            """Manage dependencies."""
            ...


__all__ = ["FlextQualityProtocols"]
