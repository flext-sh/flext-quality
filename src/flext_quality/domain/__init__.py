
"""Domain layer for FLEXT-QUALITY.

Using flext-core patterns - NO duplication, clean architecture.
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
    # Entities
    "QualityAnalysis",
    "QualityProject",
    "QualityReport",
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
    "QualityGrade",
    "QualityIssue",
    "QualityRule",
    "QualityScore",
    "ReportGeneratorService",
    "SecurityAnalyzerService",
]
