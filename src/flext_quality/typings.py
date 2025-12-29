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

from flext_core import FlextTypes
from pydantic import Field

# =============================================================================
# QUALITY MODULE-LEVEL TYPEVARS
# =============================================================================

T = TypeVar("T")
FlextQualityScoreT = TypeVar("FlextQualityScoreT", bound=float)

# =============================================================================
# QUALITY-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for quality operations
# =============================================================================


# Quality domain TypeVars
class FlextQualityTypes(FlextTypes):
    """Quality analysis-specific type definitions extending t.

    Domain-specific type system for code quality analysis operations.
    Contains ONLY complex quality-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # BASE TYPES - Foundational type aliases for Quality domain
    # =========================================================================

    class Base:
        """Foundational type aliases for Quality domain."""

        type ScoreRange = Annotated[float, Field(ge=0.0, le=100.0)]
        type Timestamp = datetime
        type PositiveInt = Annotated[int, Field(ge=1)]

    # =========================================================================
    # QUALITY ANALYSIS TYPES - Complex analysis operation types
    # =========================================================================

    class Analysis:
        """Quality analysis complex types."""

        type AnalysisConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type AnalysisMetrics = dict[
            str, float | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type AnalysisResult = dict[
            str, bool | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]
        type AnalysisContext = dict[
            str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type AnalysisReport = dict[
            str, str | int | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]
        type AnalysisThresholds = dict[str, float | int | bool]

    # =========================================================================
    # CODE QUALITY TYPES - Complex code quality assessment types
    # =========================================================================

    class Code:
        """Code quality assessment complex types."""

        type QualityScore = dict[str, float | int | dict[str, float]]
        type QualityRules = list[dict[str, str | bool | int | float]]
        type QualityViolations = list[
            dict[str, str | int | dict[str, FlextTypes.GeneralValueType]]
        ]
        type Thresholds = dict[
            str, float | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type QualityMetrics = dict[
            str, float | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type QualityReport = dict[
            str, str | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]

    # =========================================================================
    # METRICS COLLECTION TYPES - Complex metrics gathering types
    # =========================================================================

    class Metrics:
        """Quality metrics collection complex types."""

        type MetricsConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type MetricsCollection = dict[
            str, float | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type MetricsAggregation = dict[str, float | dict[str, float | int]]
        type MetricsReport = dict[
            str, str | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]
        type MetricsTrend = list[dict[str, str | float | int]]
        type MetricsThreshold = dict[str, float | int | bool]

    # =========================================================================
    # REPORTING TYPES - Complex quality reporting types
    # =========================================================================

    class Reporting:
        """Quality reporting complex types."""

        type ReportConfiguration = dict[
            str,
            str | bool | list[str] | dict[str, FlextTypes.GeneralValueType],
        ]
        type ReportData = dict[
            str, str | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]
        type ReportFormat = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ReportTemplate = dict[
            str, str | list[str] | dict[str, FlextTypes.GeneralValueType]
        ]
        type ReportExport = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ReportDistribution = list[
            dict[str, str | dict[str, FlextTypes.GeneralValueType]]
        ]

    # =========================================================================
    # ISSUE TRACKING TYPES - Complex issue management types
    # =========================================================================

    class IssueTracking:
        """Quality issue tracking complex types."""

        type IssueDefinition = dict[str, str | int | bool | list[str]]
        type IssueClassification = dict[
            str, str | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type IssueResolution = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type IssueHistory = list[
            dict[str, str | int | dict[str, FlextTypes.GeneralValueType]]
        ]
        type IssuePriority = dict[str, str | int | float | bool]
        type IssueWorkflow = list[
            dict[str, str | dict[str, FlextTypes.GeneralValueType]]
        ]

    # =========================================================================
    # TOOL INTEGRATION TYPES - Complex tool integration types
    # =========================================================================

    class ToolIntegration:
        """Quality tool integration complex types."""

        type ToolConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ToolExecution = dict[str, str | int | bool | list[str]]
        type ToolResult = dict[str, bool | str | dict[str, FlextTypes.GeneralValueType]]
        type ToolChain = list[dict[str, str | dict[str, FlextTypes.GeneralValueType]]]
        type ToolMetrics = dict[
            str, float | int | dict[str, FlextTypes.GeneralValueType]
        ]
        type ToolIntegrationConfig = dict[
            str,
            str | bool | list[str] | dict[str, FlextTypes.GeneralValueType],
        ]

        # JSON-compatible types for integrations and API communication
        type JsonCompatValue = (
            str | int | float | bool | list[object] | dict[str, object] | None
        )
        type JsonCompatDict = dict[str, JsonCompatValue]

    # =========================================================================
    # CORE TYPES - Essential Quality types extending t
    # =========================================================================

    class QualityCore:
        """Core Quality analysis types.

        Essential domain-specific types for quality analysis operations.
        """

        # Configuration and analysis types
        type ConfigDict = dict[str, FlextTypes.GeneralValueType]
        type AnalysisDict = dict[str, FlextTypes.GeneralValueType]
        type ResultDict = dict[str, FlextTypes.GeneralValueType]
        type MetricsDict = dict[str, FlextTypes.GeneralValueType]

        # Quality assessment types
        type QualityDict = dict[
            str, float | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type ThresholdDict = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type ReportDict = dict[
            str, str | float | list[dict[str, FlextTypes.GeneralValueType]]
        ]
        type IssueDict = dict[str, FlextTypes.GeneralValueType]

        # Tool integration types
        type ToolDict = dict[str, str | dict[str, FlextTypes.GeneralValueType]]
        type SettingsDict = dict[str, FlextTypes.GeneralValueType]
        type ContextDict = dict[str, FlextTypes.GeneralValueType]
        type DataDict = dict[str, FlextTypes.GeneralValueType]

        # Collection types for quality operations
        type AnalysisList = list[AnalysisDict]
        type ResultList = list[ResultDict]
        type IssueList = list[IssueDict]
        type StringList = list[str]

    # =========================================================================
    # LITERAL TYPES - StrEnum-based Literal types for type safety
    # =========================================================================

    class Literals:
        """Literal types based on StrEnum members for type safety.

        All Literal types reference StrEnum members to avoid string duplication (DRY principle).
        Using PEP 695 type statement for better type checking and IDE support.
        """

        # Analysis status literal - references AnalysisStatus StrEnum members
        type AnalysisStatusLiteral = Literal[
            "queued",
            "analyzing",
            "completed",
            "failed",
        ]

        # Issue severity literal - references IssueSeverity StrEnum members
        type IssueSeverityLiteral = Literal[
            "critical",
            "high",
            "medium",
            "low",
            "info",
        ]

        # Issue type literal - references IssueType StrEnum members
        type IssueTypeLiteral = Literal[
            "security",
            "complexity",
            "duplication",
            "coverage",
            "style",
            "bug",
            "performance",
            "maintainability",
        ]

        # Report format literal - references ReportFormat StrEnum members
        type ReportFormatLiteral = Literal[
            "html",
            "json",
            "pdf",
            "csv",
            "xml",
            "markdown",
        ]

        # Backend type literal - references BackendType StrEnum members
        type BackendTypeLiteral = Literal[
            "ast",
            "external",
            "hybrid",
        ]

        # Language literal - references Language StrEnum members
        type LanguageLiteral = Literal[
            "python",
            "javascript",
            "typescript",
            "java",
            "go",
            "rust",
        ]

        # Check status literal - references CheckStatus StrEnum members
        type CheckStatusLiteral = Literal[
            "passed",
            "failed",
            "warning",
        ]

        # Log level literal (reusing from flext-core)
        type LogLevelLiteral = FlextTypes.Settings.LogLevel

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
        type QualityProjectConfig = dict[str, FlextTypes.GeneralValueType]
        type AnalysisConfig = dict[str, str | int | bool | list[str]]
        type Thresholds = dict[str, bool | str | dict[str, FlextTypes.GeneralValueType]]
        type MetricsConfig = dict[str, FlextTypes.GeneralValueType]

    class Quality:
        """Quality types namespace for cross-project access.

        Provides organized access to all Quality types for other FLEXT projects.
        Usage: Other projects can reference `t.Quality.Analysis.*`, `t.Quality.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_quality.typings import t
            config: t.Quality.Analysis.AnalysisConfiguration = ...
            score: t.Quality.Code.QualityScore = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """


# Alias for simplified usage
t = FlextQualityTypes

# Namespace composition via class inheritance
# Quality namespace provides access to nested classes through inheritance
# Access patterns:
# - t.Quality.* for Quality-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

# =============================================================================
# MODULE-LEVEL RE-EXPORTS - For backward compatibility
# =============================================================================

ScoreRange = t.Base.ScoreRange
Timestamp = t.Base.Timestamp
PositiveInt = t.Base.PositiveInt

__all__ = [
    "FlextQualityScoreT",
    "FlextQualityTypes",
    "PositiveInt",
    "ScoreRange",
    # Module-level type aliases
    "T",
    "Timestamp",
    "t",
]
