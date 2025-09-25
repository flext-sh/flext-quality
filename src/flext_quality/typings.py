"""FLEXT Quality Types - Domain-specific quality analysis type definitions.

This module provides quality analysis-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeVar

from flext_core import FlextTypes

# =============================================================================
# QUALITY-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for quality operations
# =============================================================================

# Quality domain TypeVars
TQualityAnalysis = TypeVar("TQualityAnalysis")
TQualityProject = TypeVar("TQualityProject")
TQualityReport = TypeVar("TQualityReport")
TQualityRule = TypeVar("TQualityRule")
TQualityMetric = TypeVar("TQualityMetric")
TQualityIssue = TypeVar("TQualityIssue")
TQualityScore = TypeVar("TQualityScore")
TCodeAnalyzer = TypeVar("TCodeAnalyzer")


class FlextQualityTypes(FlextTypes):
    """Quality analysis-specific type definitions extending FlextTypes.

    Domain-specific type system for code quality analysis operations.
    Contains ONLY complex quality-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # QUALITY ANALYSIS TYPES - Complex analysis operation types
    # =========================================================================

    class Analysis:
        """Quality analysis complex types."""

        type AnalysisConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type AnalysisMetrics = dict[
            str, float | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type AnalysisResult = dict[str, bool | float | list[dict[str, object]]]
        type AnalysisContext = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type AnalysisReport = dict[str, str | int | float | list[dict[str, object]]]
        type AnalysisThresholds = dict[str, float | int | bool]

    # =========================================================================
    # CODE QUALITY TYPES - Complex code quality assessment types
    # =========================================================================

    class CodeQuality:
        """Code quality assessment complex types."""

        type QualityScore = dict[str, float | int | dict[str, float]]
        type QualityRules = list[dict[str, str | bool | int | float]]
        type QualityViolations = list[
            dict[str, str | int | dict[str, FlextTypes.Core.JsonValue]]
        ]
        type QualityThresholds = dict[str, float | int | bool | dict[str, object]]
        type QualityMetrics = dict[
            str, float | int | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type QualityReport = dict[str, str | float | list[dict[str, object]]]

    # =========================================================================
    # METRICS COLLECTION TYPES - Complex metrics gathering types
    # =========================================================================

    class Metrics:
        """Quality metrics collection complex types."""

        type MetricsConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type MetricsCollection = dict[
            str, float | int | dict[str, FlextTypes.Core.JsonValue]
        ]
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
            str, str | bool | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ReportData = dict[
            str, str | float | list[dict[str, FlextTypes.Core.JsonValue]]
        ]
        type ReportFormat = dict[str, str | bool | dict[str, object]]
        type ReportTemplate = dict[str, str | list[str] | dict[str, object]]
        type ReportExport = dict[str, str | bool | dict[str, FlextTypes.Core.JsonValue]]
        type ReportDistribution = list[dict[str, str | dict[str, object]]]

    # =========================================================================
    # ISSUE TRACKING TYPES - Complex issue management types
    # =========================================================================

    class IssueTracking:
        """Quality issue tracking complex types."""

        type IssueDefinition = dict[str, str | int | bool | list[str]]
        type IssueClassification = dict[
            str, str | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type IssueResolution = dict[str, str | bool | dict[str, object]]
        type IssueHistory = list[
            dict[str, str | int | dict[str, FlextTypes.Core.JsonValue]]
        ]
        type IssuePriority = dict[str, str | int | float | bool]
        type IssueWorkflow = list[dict[str, str | dict[str, object]]]

    # =========================================================================
    # TOOL INTEGRATION TYPES - Complex tool integration types
    # =========================================================================

    class ToolIntegration:
        """Quality tool integration complex types."""

        type ToolConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ToolExecution = dict[str, str | int | bool | list[str]]
        type ToolResult = dict[str, bool | str | dict[str, FlextTypes.Core.JsonValue]]
        type ToolChain = list[dict[str, str | dict[str, object]]]
        type ToolMetrics = dict[str, float | int | dict[str, FlextTypes.Core.JsonValue]]
        type ToolIntegrationConfig = dict[
            str, str | bool | list[str] | dict[str, object]
        ]


# =============================================================================
# PUBLIC API EXPORTS - Quality TypeVars and types
# =============================================================================

__all__: list[str] = [
    # Quality Types class
    "FlextQualityTypes",
    # Quality-specific TypeVars
    "TCodeAnalyzer",
    "TQualityAnalysis",
    "TQualityIssue",
    "TQualityMetric",
    "TQualityProject",
    "TQualityReport",
    "TQualityRule",
    "TQualityScore",
]
