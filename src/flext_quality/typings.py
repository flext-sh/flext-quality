"""FLEXT Quality Types - Domain-specific quality analysis type definitions.

This module provides quality analysis-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypeVar

from pydantic import Field

# =============================================================================
# QUALITY MODULE-LEVEL TYPE ALIASES
# =============================================================================

T = TypeVar("T")
ScoreT = TypeVar("ScoreT", bound=float)

# Advanced validation using Python 3.13+ syntax
type ScoreRange = Annotated[float, Field(ge=0.0, le=100.0)]
# Timestamp - use in Field(default_factory=...) context
type Timestamp = datetime

# Simple type aliases for common patterns
type PositiveInt = Annotated[int, Field(ge=1)]

# =============================================================================
# QUALITY-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for quality operations
# =============================================================================


# Quality domain TypeVars
class FlextQualityTypes:
    """Quality analysis-specific type definitions extending t.

    Domain-specific type system for code quality analysis operations.
    Contains ONLY complex quality-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # QUALITY ANALYSIS TYPES - Complex analysis operation types
    # =========================================================================

    class Analysis:
        """Quality analysis complex types."""

        type AnalysisConfiguration = dict[str, str | int | bool | dict[str, object]]
        type AnalysisMetrics = dict[str, float | int | dict[str, object]]
        type AnalysisResult = dict[str, bool | float | list[dict[str, object]]]
        type AnalysisContext = dict[str, str | int | bool | dict[str, object]]
        type AnalysisReport = dict[str, str | int | float | list[dict[str, object]]]
        type AnalysisThresholds = dict[str, float | int | bool]

    # =========================================================================
    # CODE QUALITY TYPES - Complex code quality assessment types
    # =========================================================================

    class Code:
        """Code quality assessment complex types."""

        type QualityScore = dict[str, float | int | dict[str, float]]
        type QualityRules = list[dict[str, str | bool | int | float]]
        type QualityViolations = list[dict[str, str | int | dict[str, object]]]
        type Thresholds = dict[str, float | int | bool | dict[str, object]]
        type QualityMetrics = dict[str, float | int | bool | dict[str, object]]
        type QualityReport = dict[str, str | float | list[dict[str, object]]]

    # =========================================================================
    # METRICS COLLECTION TYPES - Complex metrics gathering types
    # =========================================================================

    class Metrics:
        """Quality metrics collection complex types."""

        type MetricsConfiguration = dict[str, bool | str | int | dict[str, object]]
        type MetricsCollection = dict[str, float | int | dict[str, object]]
        type MetricsAggregation = dict[str, float | dict[str, float | int]]
        type MetricsReport = dict[str, str | float | list[dict[str, object]]]
        type MetricsTrend = list[dict[str, str | float | int]]
        type MetricsThreshold = dict[str, float | int | bool]

    # =========================================================================
    # REPORTING TYPES - Complex quality reporting types
    # =========================================================================

    class Reporting:
        """Quality reporting complex types."""

        type ReportConfiguration = dict[
            str,
            str | bool | list[str] | dict[str, object],
        ]
        type ReportData = dict[str, str | float | list[dict[str, object]]]
        type ReportFormat = dict[str, str | bool | dict[str, object]]
        type ReportTemplate = dict[str, str | list[str] | dict[str, object]]
        type ReportExport = dict[str, str | bool | dict[str, object]]
        type ReportDistribution = list[dict[str, str | dict[str, object]]]

    # =========================================================================
    # ISSUE TRACKING TYPES - Complex issue management types
    # =========================================================================

    class IssueTracking:
        """Quality issue tracking complex types."""

        type IssueDefinition = dict[str, str | int | bool | list[str]]
        type IssueClassification = dict[str, str | int | dict[str, object]]
        type IssueResolution = dict[str, str | bool | dict[str, object]]
        type IssueHistory = list[dict[str, str | int | dict[str, object]]]
        type IssuePriority = dict[str, str | int | float | bool]
        type IssueWorkflow = list[dict[str, str | dict[str, object]]]

    # =========================================================================
    # TOOL INTEGRATION TYPES - Complex tool integration types
    # =========================================================================

    class ToolIntegration:
        """Quality tool integration complex types."""

        type ToolConfiguration = dict[str, str | bool | dict[str, object]]
        type ToolExecution = dict[str, str | int | bool | list[str]]
        type ToolResult = dict[str, bool | str | dict[str, object]]
        type ToolChain = list[dict[str, str | dict[str, object]]]
        type ToolMetrics = dict[str, float | int | dict[str, object]]
        type ToolIntegrationConfig = dict[
            str, str | bool | list[str] | dict[str, object]
        ]

    # =========================================================================
    # CORE TYPES - Essential Quality types extending t
    # =========================================================================

    class Core:
        """Core Quality analysis types.

        Essential domain-specific types for quality analysis operations.
        """

        # Configuration and analysis types
        type ConfigDict = dict[str, object]
        type AnalysisDict = dict[str, object]
        type ResultDict = dict[str, object]
        type MetricsDict = dict[str, object]

        # Quality assessment types
        type QualityDict = dict[str, float | int | bool | dict[str, object]]
        type ThresholdDict = dict[str, bool | str | dict[str, object]]
        type ReportDict = dict[str, str | float | list[dict[str, object]]]
        type IssueDict = dict[str, object]

        # Tool integration types
        type ToolDict = dict[str, str | dict[str, object]]
        type SettingsDict = dict[str, object]
        type ContextDict = dict[str, object]
        type DataDict = dict[str, object]

        # Collection types for quality operations
        type AnalysisList = list[AnalysisDict]
        type ResultList = list[ResultDict]
        type IssueList = list[IssueDict]
        type StringList = list[str]

    # =========================================================================
    # QUALITY PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """Quality-specific project types.

        Provides quality/analysis-specific project types.
        Quality domain owns code quality and analysis-specific types.
        """

        # Quality-specific project types extending the generic ones
        type QualityProjectType = Literal[
            # Generic types inherited from t
            "library",
            "application",
            "service",
            # Quality-specific types
            "quality-analyzer",
            "code-analysis",
            "quality-dashboard",
            "metrics-collector",
            "quality-gateway",
            "analysis-engine",
            "quality-reporter",
            "code-scanner",
            "quality-monitor",
            "compliance-checker",
            "quality-validator",
            "audit-system",
            "quality-api",
            "analysis-service",
            "code-quality",
            "quality-platform",
        ]

        # Quality-specific project configurations
        type QualityProjectConfig = dict[str, object]
        type AnalysisConfig = dict[str, str | int | bool | list[str]]
        type Thresholds = dict[str, bool | str | dict[str, object]]
        type MetricsConfig = dict[str, object]


# =============================================================================
# PUBLIC API EXPORTS - Quality TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextQualityTypes",
    "ScoreRange",
    "ScoreT",
    # Module-level type aliases
    "T",
    "Timestamp",
]
