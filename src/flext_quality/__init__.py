"""FLEXT Quality - Python Code Quality Analysis Library.

Provides complete code quality analysis, metrics collection, and automated
quality assurance for FLEXT projects with proper domain-driven design patterns,
railway-oriented programming, and deep FLEXT ecosystem integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

# All imports at the top - in order
from flext_quality.__version__ import __version__, __version_info__

from .analyzer import FlextQualityAnalyzer
from .api import FlextQuality
from .ast_backend import FlextQualityASTBackend as ASTBackend
from .backend_type import BackendType
from .base import FlextQualityAnalyzer as BaseAnalyzer
from .cli import (
    analyze_project,
    another_function,
    main,
    setup_logging,
)
from .cli_helpers import QualityHelperCommands
from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .container import get_quality_container
from .exceptions import FlextQualityExceptions
from .external_backend import FlextQualityExternalBackend as ExternalBackend
from .grade_calculator import FlextQualityGradeCalculator
from .handlers import FlextQualityHandlers
from .metrics import QualityMetrics
from .models import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    FlextQualityModels,
    IssueLocation,
    QualityScore,
)
from .reports import FlextQualityReportGenerator, ReportFormat, ReportThresholds
from .services import FlextQualityServices
from .web import FlextQualityWeb as FlextQualityWebInterface

# Direct constant imports for convenience
HIGH_ISSUE_THRESHOLD = FlextQualityConstants.Analysis.HIGH_ISSUE_THRESHOLD
HTML_ISSUE_LIMIT = FlextQualityConstants.Analysis.HTML_ISSUE_LIMIT
ISSUE_PREVIEW_LIMIT = FlextQualityConstants.Analysis.ISSUE_PREVIEW_LIMIT
MIN_COVERAGE_THRESHOLD = FlextQualityConstants.Analysis.MIN_COVERAGE_THRESHOLD
MIN_SCORE_THRESHOLD = FlextQualityConstants.Analysis.MIN_SCORE_THRESHOLD

# =========================================================================
# COMPATIBILITY EXPORTS (for test migration and backward compatibility)
# =========================================================================

# Model enums
IssueSeverity = FlextQualityModels.IssueSeverity
IssueType = FlextQualityModels.IssueType
AnalysisStatus = FlextQualityModels.AnalysisStatus
FlextAnalysisStatus = FlextQualityModels.AnalysisStatus
QualityGrade = FlextQualityModels.QualityGrade

# Service exports (all use same service class)
QualityProjectService = FlextQualityServices
QualityAnalysisService = FlextQualityServices
QualityIssueService = FlextQualityServices
QualityReportService = FlextQualityServices

# Entity model exports
QualityProject = FlextQualityModels.ProjectModel
QualityAnalysis = FlextQualityModels.AnalysisModel
QualityIssue = FlextQualityModels.IssueModel
QualityRule = FlextQualityModels.RuleModel
# QualityReport is the generator for backward compatibility
QualityReport = FlextQualityReportGenerator

# Analysis results exports
AnalysisResults = FlextQualityModels.AnalysisResults
OverallMetrics = FlextQualityModels.OverallMetrics
FileAnalysisResult = FlextQualityModels.AnalysisResults
DuplicationIssue = FlextQualityModels.IssueModel

# Backend exports
CodeAnalyzer = FlextQualityAnalyzer

# Grade calculator exports
QualityGradeCalculator = FlextQualityGradeCalculator

# =========================================================================
# PUBLIC API - FLEXT patterns only
# =========================================================================

__all__ = [
    "HIGH_ISSUE_THRESHOLD",
    "HTML_ISSUE_LIMIT",
    "ISSUE_PREVIEW_LIMIT",
    "MIN_COVERAGE_THRESHOLD",
    "MIN_SCORE_THRESHOLD",
    "ASTBackend",
    "AnalysisResults",
    "AnalysisStatus",
    "BackendType",
    "BaseAnalyzer",
    "CodeAnalyzer",
    "ComplexityMetric",
    "CoverageMetric",
    "DuplicationIssue",
    "DuplicationMetric",
    "ExternalBackend",
    "FileAnalysisResult",
    "FlextAnalysisStatus",
    "FlextQuality",
    "FlextQualityAnalyzer",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityExceptions",
    "FlextQualityHandlers",
    "FlextQualityModels",
    "FlextQualityReportGenerator",
    "FlextQualityServices",
    "FlextQualityWebInterface",
    "IssueLocation",
    "IssueSeverity",
    "IssueType",
    "OverallMetrics",
    "QualityAnalysis",
    "QualityAnalysisService",
    "QualityGrade",
    "QualityGradeCalculator",
    "QualityHelperCommands",
    "QualityIssue",
    "QualityIssueService",
    "QualityMetrics",
    "QualityProject",
    "QualityProjectService",
    "QualityReport",
    "QualityReportService",
    "QualityRule",
    "QualityScore",
    "ReportFormat",
    "ReportThresholds",
    "__version__",
    "__version_info__",
    "analyze_project",
    "another_function",
    "get_quality_container",
    "main",
    "setup_logging",
]
