"""FLEXT Quality Types - Domain-specific quality analysis type definitions.

This module provides quality analysis-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextCore

# =============================================================================
# QUALITY-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for quality operations
# =============================================================================


# Quality domain TypeVars
class FlextQualityTypes:
    """Quality analysis-specific type definitions extending FlextCore.Types.

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
            str, str | int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type AnalysisMetrics = dict[
            str, float | int | dict[str, FlextCore.Types.JsonValue]
        ]
        type AnalysisResult = dict[str, bool | float | list[FlextCore.Types.Dict]]
        type AnalysisContext = dict[
            str, str | int | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type AnalysisReport = dict[str, str | int | float | list[FlextCore.Types.Dict]]
        type AnalysisThresholds = dict[str, float | int | bool]

    # =========================================================================
    # CODE QUALITY TYPES - Complex code quality assessment types
    # =========================================================================

    class Code:
        """Code quality assessment complex types."""

        type QualityScore = dict[str, float | int | FlextCore.Types.FloatDict]
        type QualityRules = list[dict[str, str | bool | int | float]]
        type QualityViolations = list[
            dict[str, str | int | dict[str, FlextCore.Types.JsonValue]]
        ]
        type Thresholds = dict[str, float | int | bool | FlextCore.Types.Dict]
        type QualityMetrics = dict[
            str, float | int | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type QualityReport = dict[str, str | float | list[FlextCore.Types.Dict]]

    # =========================================================================
    # METRICS COLLECTION TYPES - Complex metrics gathering types
    # =========================================================================

    class Metrics:
        """Quality metrics collection complex types."""

        type MetricsConfiguration = dict[
            str, bool | str | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type MetricsCollection = dict[
            str, float | int | dict[str, FlextCore.Types.JsonValue]
        ]
        type MetricsAggregation = dict[str, float | dict[str, float | int]]
        type MetricsReport = dict[str, str | float | list[FlextCore.Types.Dict]]
        type MetricsTrend = list[dict[str, str | float | int]]
        type MetricsThreshold = dict[str, float | int | bool]

    # =========================================================================
    # REPORTING TYPES - Complex quality reporting types
    # =========================================================================

    class Reporting:
        """Quality reporting complex types."""

        type ReportConfiguration = dict[
            str,
            str
            | bool
            | FlextCore.Types.StringList
            | dict[str, FlextCore.Types.ConfigValue],
        ]
        type ReportData = dict[
            str, str | float | list[dict[str, FlextCore.Types.JsonValue]]
        ]
        type ReportFormat = dict[str, str | bool | FlextCore.Types.Dict]
        type ReportTemplate = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type ReportExport = dict[str, str | bool | dict[str, FlextCore.Types.JsonValue]]
        type ReportDistribution = list[dict[str, str | FlextCore.Types.Dict]]

    # =========================================================================
    # ISSUE TRACKING TYPES - Complex issue management types
    # =========================================================================

    class IssueTracking:
        """Quality issue tracking complex types."""

        type IssueDefinition = dict[str, str | int | bool | FlextCore.Types.StringList]
        type IssueClassification = dict[
            str, str | int | dict[str, FlextCore.Types.JsonValue]
        ]
        type IssueResolution = dict[str, str | bool | FlextCore.Types.Dict]
        type IssueHistory = list[
            dict[str, str | int | dict[str, FlextCore.Types.JsonValue]]
        ]
        type IssuePriority = dict[str, str | int | float | bool]
        type IssueWorkflow = list[dict[str, str | FlextCore.Types.Dict]]

    # =========================================================================
    # TOOL INTEGRATION TYPES - Complex tool integration types
    # =========================================================================

    class ToolIntegration:
        """Quality tool integration complex types."""

        type ToolConfiguration = dict[
            str, str | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ToolExecution = dict[str, str | int | bool | FlextCore.Types.StringList]
        type ToolResult = dict[str, bool | str | dict[str, FlextCore.Types.JsonValue]]
        type ToolChain = list[dict[str, str | FlextCore.Types.Dict]]
        type ToolMetrics = dict[str, float | int | dict[str, FlextCore.Types.JsonValue]]
        type ToolIntegrationConfig = dict[
            str, str | bool | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]

    # =========================================================================
    # CORE TYPES - Essential Quality types extending FlextCore.Types
    # =========================================================================

    class Core:
        """Core Quality analysis types extending FlextCore.Types.

        Essential domain-specific types for quality analysis operations.
        Replaces generic FlextCore.Types.Dict with semantic quality types.
        """

        # Configuration and analysis types
        type ConfigDict = dict[str, FlextCore.Types.ConfigValue | object]
        type AnalysisDict = FlextCore.Types.Dict
        type ResultDict = FlextCore.Types.Dict
        type MetricsDict = FlextCore.Types.Dict

        # Quality assessment types
        type QualityDict = dict[str, float | int | bool | FlextCore.Types.Dict]
        type ThresholdDict = dict[str, bool | str | FlextCore.Types.Dict]
        type ReportDict = dict[str, str | float | list[FlextCore.Types.Dict]]
        type IssueDict = FlextCore.Types.Dict

        # Tool integration types
        type ToolDict = dict[str, str | FlextCore.Types.Dict]
        type SettingsDict = FlextCore.Types.Dict
        type ContextDict = FlextCore.Types.Dict
        type DataDict = FlextCore.Types.Dict

        # Collection types for quality operations
        type AnalysisList = list[AnalysisDict]
        type ResultList = list[ResultDict]
        type IssueList = list[IssueDict]
        type StringList = FlextCore.Types.StringList

    # =========================================================================
    # QUALITY PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project:
        """Quality-specific project types extending FlextCore.Types.Project.

        Adds quality/analysis-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Quality domain owns code quality and analysis-specific types.
        """

        # Quality-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
        type QualityProjectConfig = dict[str, FlextCore.Types.ConfigValue | object]
        type AnalysisConfig = dict[str, str | int | bool | FlextCore.Types.StringList]
        type Thresholds = dict[str, bool | str | FlextCore.Types.Dict]
        type MetricsConfig = dict[str, FlextCore.Types.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Quality TypeVars and types
# =============================================================================

__all__: FlextCore.Types.StringList = [
    "FlextQualityTypes",
]
