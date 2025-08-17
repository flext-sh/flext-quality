"""Enterprise Code Quality Analysis and Governance Service for FLEXT ecosystem."""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

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
)
from flext_quality.domain.quality_grade_calculator import (
    QualityGrade,
    QualityGradeCalculator,
)
from flext_quality.infrastructure.container import get_quality_container
from flext_quality.simple_api import QualityAPI
from flext_quality.metrics import QualityMetrics
from flext_quality.reports import QualityReport
from flext_quality.exceptions import (
    FlextQualityError as QualityError,
)
from flext_quality.web_interface import QualityWebInterface, main as quality_web_main
from flext_quality.cli import (
    another_function as _cli_another_function,
    analyze_project as _cli_analyze_project,
    main as cli_main,
    setup_logging as _cli_setup_logging,
)

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
    "DomainQualityReport",
    # Domain Utilities
    "QualityGrade",
    "QualityGradeCalculator",
    "FlextQualityDeprecationWarning",
    "FlextResult",
    "QualityAPI",
    "QualityError",
    "QualityMetrics",
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
    "cli_main",
    "_cli_analyze_project",
    "_cli_another_function",
    "_cli_setup_logging",
]
