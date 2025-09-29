"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import exceptions
from flext_quality.__version__ import __version__, __version_info__
from flext_quality.analysis_types import (
    AnalysisResults,
    CodeIssue,
    ComplexityIssue,
    DeadCodeIssue,
    Dependency,
    DuplicationIssue,
    FileAnalysisResult,
    OverallMetrics,
    SecurityIssue,
    TestResults,
)
from flext_quality.analyzer import FlextQualityCodeAnalyzer as CodeAnalyzer
from flext_quality.api import FlextQualityAPI as QualityAPI
from flext_quality.ast_backend import (
    FlextQualityASTBackend as ASTBackend,
)
from flext_quality.backend_type import BackendType
from flext_quality.base import BaseAnalyzer
from flext_quality.cli import (
    analyze_project,
    another_function,
    main,
    quality_main,
    setup_logging,
)
from flext_quality.config import FlextQualityConfig
from flext_quality.container import get_quality_container
from flext_quality.entities import FlextQualityEntities
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
    exceptions_all,
)
from flext_quality.external_backend import (
    FlextQualityExternalBackend as ExternalBackend,
)
from flext_quality.grade_calculator import QualityGradeCalculator
from flext_quality.handlers import FlextQualityHandlers as FlextQualityHandler
from flext_quality.metrics import QualityMetrics
from flext_quality.models import FlextQualityReportModel
from flext_quality.protocols import FlextQualityProtocols
from flext_quality.reports import FlextQualityReportGenerator
from flext_quality.services import FlextQualityServices
from flext_quality.utilities import FlextQualityUtilities as QualityUtilities
from flext_quality.value_objects import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
    IssueLocation,
    QualityGrade,
    QualityScore,
)
from flext_quality.web import FlextQualityWebInterface as QualityWebInterface

AnalysisStatus = FlextQualityEntities.AnalysisStatus
QualityAnalysis = FlextQualityEntities.QualityAnalysis
QualityIssue = FlextQualityEntities.QualityIssue
QualityProject = FlextQualityEntities.QualityProject
QualityReport = FlextQualityEntities.QualityReport
QualityRule = FlextQualityEntities.QualityRule
# OverallMetrics imported directly above

__all__ = [
    "ASTBackend",
    "AnalysisResults",
    "AnalysisStatus",
    "BackendType",
    "BaseAnalyzer",
    "CodeAnalyzer",
    "CodeIssue",
    "ComplexityIssue",
    "ComplexityMetric",
    "CoverageMetric",
    "DeadCodeIssue",
    "Dependency",
    "DuplicationIssue",
    "DuplicationMetric",
    "ExternalBackend",
    "FileAnalysisResult",
    "FlextQualityAnalysisError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfig",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityError",
    "FlextQualityGradeError",
    "FlextQualityHandler",
    "FlextQualityMetricsError",
    "FlextQualityProcessingError",
    "FlextQualityProtocols",
    "FlextQualityReportError",
    "FlextQualityReportGenerator",
    "FlextQualityReportModel",
    "FlextQualityRuleError",
    "FlextQualityServices",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
    "IssueLocation",
    "IssueSeverity",
    "IssueType",
    "OverallMetrics",
    "QualityAPI",
    "QualityAnalysis",
    "QualityGrade",
    "QualityGradeCalculator",
    "QualityIssue",
    "QualityMetrics",
    "QualityProject",
    "QualityReport",
    "QualityRule",
    "QualityScore",
    "QualityUtilities",
    "QualityWebInterface",
    "SecurityIssue",
    "TestResults",
    "__version__",
    "__version_info__",
    "analyze_project",
    "another_function",
    "exceptions",
    "exceptions_all",
    "get_quality_container",
    "main",
    "quality_main",
    "setup_logging",
]
