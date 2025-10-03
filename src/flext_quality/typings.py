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

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from flext_core import FlextModels, FlextTypes
from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
)

# =============================================================================
# QUALITY-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for quality operations
# =============================================================================


# Quality domain TypeVars
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
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type AnalysisMetrics = dict[str, float | int | dict[str, FlextTypes.JsonValue]]
        type AnalysisResult = dict[str, bool | float | list[FlextTypes.Dict]]
        type AnalysisContext = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type AnalysisReport = dict[str, str | int | float | list[FlextTypes.Dict]]
        type AnalysisThresholds = dict[str, float | int | bool]

    # =========================================================================
    # CODE QUALITY TYPES - Complex code quality assessment types
    # =========================================================================

    class CodeQuality:
        """Code quality assessment complex types."""

        type QualityScore = dict[str, float | int | FlextTypes.FloatDict]
        type QualityRules = list[dict[str, str | bool | int | float]]
        type QualityViolations = list[
            dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        ]
        type QualityThresholds = dict[str, float | int | bool | FlextTypes.Dict]
        type QualityMetrics = dict[
            str, float | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type QualityReport = dict[str, str | float | list[FlextTypes.Dict]]

    # =========================================================================
    # METRICS COLLECTION TYPES - Complex metrics gathering types
    # =========================================================================

    class Metrics:
        """Quality metrics collection complex types."""

        type MetricsConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.ConfigValue]
        ]
        type MetricsCollection = dict[
            str, float | int | dict[str, FlextTypes.JsonValue]
        ]
        type MetricsAggregation = dict[str, float | dict[str, float | int]]
        type MetricsReport = dict[str, str | float | list[FlextTypes.Dict]]
        type MetricsTrend = list[dict[str, str | float | int]]
        type MetricsThreshold = dict[str, float | int | bool]

    # =========================================================================
    # REPORTING TYPES - Complex quality reporting types
    # =========================================================================

    class Reporting:
        """Quality reporting complex types."""

        type ReportConfiguration = dict[
            str, str | bool | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type ReportData = dict[str, str | float | list[dict[str, FlextTypes.JsonValue]]]
        type ReportFormat = dict[str, str | bool | FlextTypes.Dict]
        type ReportTemplate = dict[str, str | FlextTypes.StringList | FlextTypes.Dict]
        type ReportExport = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
        type ReportDistribution = list[dict[str, str | FlextTypes.Dict]]

    # =========================================================================
    # ISSUE TRACKING TYPES - Complex issue management types
    # =========================================================================

    class IssueTracking:
        """Quality issue tracking complex types."""

        type IssueDefinition = dict[str, str | int | bool | FlextTypes.StringList]
        type IssueClassification = dict[
            str, str | int | dict[str, FlextTypes.JsonValue]
        ]
        type IssueResolution = dict[str, str | bool | FlextTypes.Dict]
        type IssueHistory = list[dict[str, str | int | dict[str, FlextTypes.JsonValue]]]
        type IssuePriority = dict[str, str | int | float | bool]
        type IssueWorkflow = list[dict[str, str | FlextTypes.Dict]]

    # =========================================================================
    # TOOL INTEGRATION TYPES - Complex tool integration types
    # =========================================================================

    class ToolIntegration:
        """Quality tool integration complex types."""

        type ToolConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type ToolExecution = dict[str, str | int | bool | FlextTypes.StringList]
        type ToolResult = dict[str, bool | str | dict[str, FlextTypes.JsonValue]]
        type ToolChain = list[dict[str, str | FlextTypes.Dict]]
        type ToolMetrics = dict[str, float | int | dict[str, FlextTypes.JsonValue]]
        type ToolIntegrationConfig = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]

    # =========================================================================
    # ANALYSIS RESULT TYPES - Complex analysis result model types
    # =========================================================================

    class AnalysisResults(FlextModels.Value):
        """Complete analysis results containing all metrics and issues."""

        overall_metrics: "OverallMetrics" = Field(
            default_factory=dict,
            description="Overall analysis metrics",
        )
        file_metrics: list[FlextQualityTypes.FileAnalysisResult] = Field(
            default_factory=list,
            description="Per-file analysis results",
        )
        code_issues: list[FlextQualityTypes.CodeIssue] = Field(
            default_factory=list,
            description="Code quality issues found",
        )
        complexity_issues: list[FlextQualityTypes.ComplexityIssue] = Field(
            default_factory=list,
            description="Complexity issues found",
        )
        security_issues: list[FlextQualityTypes.SecurityIssue] = Field(
            default_factory=list,
            description="Security issues found",
        )
        dead_code_issues: list[FlextQualityTypes.DeadCodeIssue] = Field(
            default_factory=list,
            description="Dead code issues found",
        )
        duplication_issues: list[FlextQualityTypes.DuplicationIssue] = Field(
            default_factory=list,
            description="Code duplication issues found",
        )
        dependencies: list[FlextQualityTypes.Dependency] = Field(
            default_factory=list,
            description="Project dependencies analysis",
        )
        test_results: FlextQualityTypes.TestResults | None = Field(
            default=None,
            description="Test results if available",
        )
        analysis_config: FlextQualityTypes.Core.AnalysisDict = Field(
            default_factory=dict,
            description="Configuration used for analysis",
        )
        analysis_timestamp: str = Field(
            default_factory=lambda: datetime.now(UTC).isoformat(),
            description="When analysis was performed",
        )

        @property
        def total_issues(self) -> int:
            """Total number of issues found across all categories."""
            return (
                len(self.code_issues)
                + len(self.complexity_issues)
                + len(self.security_issues)
                + len(self.dead_code_issues)
                + len(self.duplication_issues)
            )

        def get_quality_score(self) -> float:
            """Calculate overall quality score."""
            return self.overall_metrics.quality_score

    class FileAnalysisResult(FlextModels.Value):
        """Result of analyzing a single file."""

        file_path: Path = Field(..., description="Path to the analyzed file")
        lines_of_code: int = Field(default=0, ge=0, description="Total lines of code")
        complexity_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Complexity score",
        )
        security_issues: int = Field(
            default=0,
            ge=0,
            description="Number of security issues",
        )
        style_issues: int = Field(default=0, ge=0, description="Number of style issues")
        dead_code_lines: int = Field(default=0, ge=0, description="Lines of dead code")

    class CodeIssue(BaseModel):
        """General code quality issue."""

        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        issue_type: str = Field(..., description="Type of code issue")
        message: str = Field(..., description="Human-readable issue message")
        severity: IssueSeverity = Field(
            default=IssueSeverity.MEDIUM,
            description="Issue severity level",
        )
        rule_id: str = Field(..., description="Rule identifier")
        code_snippet: str | None = Field(default=None, description="Code snippet")

    class ComplexityIssue(BaseModel):
        """Represents a complexity issue in code."""

        file_path: str = Field(..., description="File where issue was found")
        function_name: str = Field(..., description="Function with complexity issue")
        line_number: int = Field(..., ge=1, description="Line number of function")
        complexity_value: int = Field(
            ...,
            ge=1,
            description="Cyclomatic complexity value",
        )
        message: str = Field(..., description="Human-readable issue message")
        issue_type: str = Field(
            default="high_complexity",
            description="Type of complexity issue",
        )
        severity: IssueSeverity = Field(
            default=IssueSeverity.MEDIUM,
            description="Issue severity level",
        )

    class SecurityIssue(FlextModels.Value):
        """Represents a security issue found in code."""

        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        issue_type: str = Field(..., description="Type of security issue")
        description: str = Field(..., description="Detailed issue description")
        message: str = Field(..., description="Human-readable issue message")
        rule_id: str = Field(..., description="Security rule identifier")
        severity: IssueSeverity = Field(
            default=IssueSeverity.HIGH,
            description="Security issue severity",
        )
        confidence: str = Field(
            default="MEDIUM",
            description="Confidence level of detection",
        )

    class DeadCodeIssue(FlextModels.Value):
        """Represents dead/unused code found during analysis."""

        file_path: str = Field(..., description="File containing dead code")
        line_number: int = Field(..., ge=1, description="Line number of dead code")
        end_line_number: int = Field(
            ...,
            ge=1,
            description="End line number of dead code",
        )
        issue_type: str = Field(..., description="Type of dead code")
        code_type: str = Field(
            ...,
            description="Type of code element (function, class, etc)",
        )
        code_snippet: str = Field(..., description="The unused code snippet")
        message: str = Field(..., description="Human-readable issue message")
        severity: IssueSeverity = Field(
            default=IssueSeverity.LOW,
            description="Dead code severity",
        )

    class DuplicationIssue(FlextModels.Value):
        """Represents code duplication detected in analysis."""

        files: FlextTypes.StringList = Field(
            ...,
            description="Files containing duplicated code",
        )
        line_ranges: list[tuple[int, int]] = Field(
            ...,
            description="Line ranges of duplicate code",
        )
        duplicate_lines: int = Field(..., ge=1, description="Number of duplicate lines")
        similarity: float = Field(
            ...,
            ge=0.0,
            le=100.0,
            description="Similarity score (0.0 to 100.0)",
        )
        similarity_percent: float = Field(
            ...,
            ge=0.0,
            le=100.0,
            description="Percentage similarity",
        )
        message: str = Field(..., description="Human-readable duplication message")
        severity: IssueSeverity = Field(
            default=IssueSeverity.MEDIUM,
            description="Duplication severity",
        )

    class Dependency(BaseModel):
        """Project dependency information."""

        name: str = Field(..., description="Dependency name")
        version: str = Field(..., description="Dependency version")
        type: str = Field(default="runtime", description="Dependency type")
        vulnerabilities: FlextTypes.StringList = Field(
            default_factory=list,
            description="Known vulnerabilities",
        )
        license: str | None = Field(default=None, description="License information")
        is_dev: bool = Field(default=False, description="Development dependency")

    class TestResults(BaseModel):
        """Test execution results."""

        total_tests: int = Field(default=0, description="Total number of tests")
        passed_tests: int = Field(default=0, description="Number of passed tests")
        failed_tests: int = Field(default=0, description="Number of failed tests")
        skipped_tests: int = Field(default=0, description="Number of skipped tests")
        test_duration: float = Field(default=0.0, description="Total test duration")
        coverage_percentage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Code coverage percentage",
        )
        test_errors: FlextTypes.StringList = Field(
            default_factory=list,
            description="Test execution errors",
        )

    class OverallMetrics(FlextModels.Value):
        """Overall metrics for the entire analysis."""

        files_analyzed: int = Field(default=0, ge=0, description="Total files analyzed")
        total_lines: int = Field(default=0, ge=0, description="Total lines of code")
        functions_count: int = Field(default=0, ge=0, description="Total functions")
        classes_count: int = Field(default=0, ge=0, description="Total classes")
        average_complexity: float = Field(
            default=0.0,
            ge=0.0,
            description="Average cyclomatic complexity",
        )
        max_complexity: float = Field(
            default=0.0,
            ge=0.0,
            description="Maximum complexity found",
        )
        # Quality scores
        quality_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Overall quality score",
        )
        coverage_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Code coverage score",
        )
        security_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Security quality score",
        )
        maintainability_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Maintainability score",
        )
        complexity_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Complexity score",
        )

    # =========================================================================
    # CORE TYPES - Essential Quality types extending FlextTypes
    # =========================================================================

    class Core(FlextTypes):
        """Core Quality analysis types extending FlextTypes.

        Essential domain-specific types for quality analysis operations.
        Replaces generic FlextTypes.Dict with semantic quality types.
        """

        # Configuration and analysis types
        type ConfigDict = dict[str, FlextTypes.ConfigValue | object]
        type AnalysisDict = FlextTypes.Dict
        type ResultDict = FlextTypes.Dict
        type MetricsDict = FlextTypes.Dict

        # Quality assessment types
        type QualityDict = dict[str, float | int | bool | FlextTypes.Dict]
        type ThresholdDict = dict[str, bool | str | FlextTypes.Dict]
        type ReportDict = dict[str, str | float | list[FlextTypes.Dict]]
        type IssueDict = FlextTypes.Dict

        # Tool integration types
        type ToolDict = dict[str, str | FlextTypes.Dict]
        type SettingsDict = FlextTypes.Dict
        type ContextDict = FlextTypes.Dict
        type DataDict = FlextTypes.Dict

        # Collection types for quality operations
        type AnalysisList = list[AnalysisDict]
        type ResultList = list[ResultDict]
        type IssueList = list[IssueDict]
        type StringList = FlextTypes.StringList

    # =========================================================================
    # QUALITY PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Quality-specific project types extending FlextTypes.Project.

        Adds quality/analysis-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Quality domain owns code quality and analysis-specific types.
        """

        # Quality-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
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
        type QualityProjectConfig = dict[str, FlextTypes.ConfigValue | object]
        type AnalysisConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type QualityThresholds = dict[str, bool | str | FlextTypes.Dict]
        type MetricsConfig = dict[str, FlextTypes.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Quality TypeVars and types
# =============================================================================

__all__: FlextTypes.StringList = [
    "FlextQualityTypes",
]
