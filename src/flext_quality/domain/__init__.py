"""Domain Layer - Core Business Logic for FLEXT Quality Analysis.

This module contains the core domain entities, value objects, and service ports
that define the business logic for quality analysis within the FLEXT ecosystem.
Follows Clean Architecture and Domain-Driven Design principles with strict
separation from infrastructure concerns.

Key Components:
    - QualityProject: Represents a code project under quality analysis
    - QualityAnalysis: Encapsulates a single analysis run with metrics
    - QualityIssue: Individual quality issues detected during analysis
    - QualityReport: Generated quality reports in various formats
    - QualityRule: Configuration rules for quality analysis

Value Objects:
    - QualityScore: Immutable quality scoring with grade calculations
    - ComplexityMetric: Code complexity measurements and thresholds
    - CoverageMetric: Test coverage statistics and requirements
    - DuplicationMetric: Code duplication detection and analysis
    - IssueSeverity: Classification of issue severity levels

Service Ports:
    - AnalysisService: Core analysis orchestration interface
    - MetricsCollectorService: Quality metrics collection interface
    - ReportGeneratorService: Quality report generation interface
    - SecurityAnalyzerService: Security analysis and vulnerability detection

Architecture:
    Built on flext-core foundation patterns with no code duplication.
    Uses FlextEntity for domain entities and FlextResult for operation results.
    Implements dependency inversion with service ports and adapters.

Integration:
    - Built on flext-core.domain patterns for consistency
    - Integrates with flext-observability for domain event monitoring
    - Provides interfaces for infrastructure layer implementations

Author: FLEXT Development Team
Version: 0.9.0
"""

from __future__ import annotations

# Import domain entities
from flext_quality.domain.entities import (
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
    QualityRule,
)

# Import domain services
from flext_quality.domain.ports import (
    AnalysisService,
    ComplexityAnalyzerService,
    DeadCodeDetectorService,
    DuplicateDetectorService,
    LintingService,
    MetricsCollectorService,
    ReportGeneratorService,
    SecurityAnalyzerService,
)

# Import value objects
from flext_quality.domain.value_objects import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    FilePath,
    IssueLocation,
    IssueSeverity,
    IssueType,
    QualityGrade,
    QualityScore,
)

__all__ = [
    # Domain Services
    "AnalysisService",
    "ComplexityAnalyzerService",
    # Value Objects
    "ComplexityMetric",
    "CoverageMetric",
    "DeadCodeDetectorService",
    "DuplicateDetectorService",
    "DuplicationMetric",
    "FilePath",
    "IssueLocation",
    "IssueSeverity",
    "IssueType",
    "LintingService",
    "MetricsCollectorService",
    # Entities
    "QualityAnalysis",
    "QualityGrade",
    "QualityIssue",
    "QualityProject",
    "QualityReport",
    "QualityRule",
    "QualityScore",
    "ReportGeneratorService",
    "SecurityAnalyzerService",
]
