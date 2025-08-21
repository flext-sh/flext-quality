"""Enterprise Code Quality Analysis and Governance Service for FLEXT ecosystem."""

from __future__ import annotations

import importlib.metadata

# Core FlextCore patterns (root namespace imports)
from flext_core import FlextResult

# Direct imports - no fallbacks allowed per CLAUDE.md
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.backends.ast_backend import ASTBackend, ASTVisitor
from flext_quality.backends.base import BackendType, BaseAnalyzer
from flext_quality.backends.external_backend import ExternalBackend
from flext_quality.application.services import (
    LintingServiceImpl,
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
    SecurityAnalyzerServiceImpl,
)
from flext_quality.application.handlers import (
    AnalyzeProjectHandler,
    GenerateReportHandler,
    RunLintingHandler,
    RunSecurityCheckHandler,
)
from flext_quality.domain.entities import (
    AnalysisStatus,
    IssueSeverity,
    IssueType,
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport as DomainQualityReport,
    QualityRule,
)
from flext_quality.domain.grade_calculator import (
    QualityGrade,
    QualityGradeCalculator,
)
from flext_quality.domain.value_objects import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    FilePath,
    IssueLocation,
    QualityScore,
)
from flext_quality.analysis_types import (
    AnalysisResults,
    OverallMetrics,
    FileAnalysisResult,
    ComplexityIssue,
    SecurityIssue,
    DeadCodeIssue,
    DuplicationIssue,
)
from flext_quality.utilities import (
    FlextTestUtilities,
    FlextQualityUtilities,
    FlextAnalysisUtilities,
    FlextReportUtilities,
)
from flext_quality.infrastructure.container import get_quality_container
from flext_quality.api import QualityAPI
from flext_quality.metrics import QualityMetrics
from flext_quality.reports import (
    QualityReport,
    HIGH_ISSUE_THRESHOLD,
    HTML_ISSUE_LIMIT,
    ISSUE_PREVIEW_LIMIT,
    MIN_COVERAGE_THRESHOLD,
    MIN_SCORE_THRESHOLD,
)
from flext_quality.exceptions import (
    FlextQualityAnalysisError,
    FlextQualityAuthenticationError,
    FlextQualityConfigurationError,
    FlextQualityConnectionError,
    FlextQualityError,
    FlextQualityGradeError,
    FlextQualityMetricsError,
    FlextQualityProcessingError,
    FlextQualityReportError,
    FlextQualityRuleError,
    FlextQualityTimeoutError,
    FlextQualityValidationError,
)
from flext_quality import exceptions
from flext_quality.web import QualityWebInterface, main as quality_web_main
from flext_quality.cli import (
    analyze_project,
    another_function,
    main,
    setup_logging,
)
from flext_quality import config
from flext_quality.config import QualityConfig
from flext_quality.constants import FlextQualityConstants

try:
    __version__ = importlib.metadata.version("flext-quality")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextQualityDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Quality import changes.

    This warning is raised when deprecated import patterns are used.
    """


# Export clean, professional public API
__all__: list[str] = [
    # Backends (root import for tests/examples)
    "ASTBackend",
    "ASTVisitor",
    "BackendType",
    "BaseAnalyzer",
    "ExternalBackend",
    "CodeAnalyzer",
    # Application Services
    "LintingServiceImpl",
    "QualityAnalysisService",
    "QualityIssueService",
    "QualityProjectService",
    "QualityReportService",
    "SecurityAnalyzerServiceImpl",
    # Application Handlers
    "AnalyzeProjectHandler",
    "GenerateReportHandler",
    "RunLintingHandler",
    "RunSecurityCheckHandler",
    # Domain Entities
    "AnalysisStatus",
    "IssueSeverity",
    "IssueType",
    "QualityProject",
    "QualityAnalysis",
    "QualityIssue",
    "QualityRule",
    "DomainQualityReport",
    # Domain Utilities
    "QualityGrade",
    "QualityGradeCalculator",
    "FlextQualityDeprecationWarning",
    "FlextResult",
    "QualityAPI",
    "QualityMetrics",
    # Exceptions
    "FlextQualityAnalysisError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityError",
    "FlextQualityGradeError",
    "FlextQualityMetricsError",
    "FlextQualityProcessingError",
    "FlextQualityReportError",
    "FlextQualityRuleError",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
    "exceptions",
    "QualityReport",
    # Infrastructure
    "get_quality_container",
    "__version__",
    "__version_info__",
    "annotations",
    # Web interface
    "QualityWebInterface",
    "quality_web_main",
    # CLI surface (re-exported at root for tests/examples)
    "analyze_project",
    "another_function",
    "main",
    "setup_logging",
    # Configuration
    "config",
    "QualityConfig",
    "FlextQualityConstants",
    # Value Objects
    "ComplexityMetric",
    "CoverageMetric",
    "DuplicationMetric",
    "FilePath",
    "IssueLocation",
    "QualityScore",
    # Analysis Types
    "AnalysisResults",
    "OverallMetrics",
    "FileAnalysisResult",
    "ComplexityIssue",
    "SecurityIssue",
    "DeadCodeIssue",
    "DuplicationIssue",
    # Utilities
    "FlextTestUtilities",
    "FlextQualityUtilities",
    "FlextAnalysisUtilities",
    "FlextReportUtilities",
    # Report Constants
    "HIGH_ISSUE_THRESHOLD",
    "HTML_ISSUE_LIMIT",
    "ISSUE_PREVIEW_LIMIT",
    "MIN_COVERAGE_THRESHOLD",
    "MIN_SCORE_THRESHOLD",
]
