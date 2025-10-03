"""FLEXT Quality Protocols - Protocol definitions for quality analysis interfaces.

This module defines protocols for quality analysis operations following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextResult
from flext_quality.typings import FlextQualityTypes


class FlextQualityProtocols:
    """Quality analysis protocol definitions."""

    class QualityAnalyzer(Protocol):
        """Protocol for quality analysis operations."""

        def analyze_project(
            self,
            project_path: str,
            config: FlextQualityTypes.Analysis.AnalysisConfiguration | None = None,
        ) -> FlextResult[FlextQualityTypes.AnalysisResults]:
            """Analyze a project for quality metrics."""
            ...

    class QualityReporter(Protocol):
        """Protocol for quality reporting operations."""

        def generate_report(
            self,
            analysis_results: FlextQualityTypes.AnalysisResults,
            format_type: str = "html",
        ) -> FlextResult[str]:
            """Generate a quality report from analysis results."""
            ...

    class QualityValidator(Protocol):
        """Protocol for quality validation operations."""

        def validate_thresholds(
            self,
            analysis_results: FlextQualityTypes.AnalysisResults,
            thresholds: FlextQualityTypes.Analysis.AnalysisThresholds,
        ) -> FlextResult[bool]:
            """Validate analysis results against quality thresholds."""
            ...


__all__ = ["FlextQualityProtocols"]
