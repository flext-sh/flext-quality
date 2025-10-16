"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult

from flext_quality.__version__ import __version__, __version_info__

# Import specific types from the nested class
from .analysis_types import FlextQualityAnalysisTypes

# Core imports - moved to specific imports below to avoid circular import
# Main modules
from .analyzer import FlextQualityAnalyzer as CodeAnalyzer
from .api import FlextQuality as FlextQuality, FlextQuality as QualityAPI
from .ast_backend import FlextQualityASTBackend as ASTBackend
from .ast_class_info import FlextQualityASTClassInfo
from .ast_function_info import FlextQualityASTFunctionInfo
from .backend_type import BackendType
from .base import BaseAnalyzer

# CLI imports are lazy to avoid flext_cli dependency issues
# Use: from .cli import main
# Instead of: from flext_quality import main
from .cli import another_function, main, setup_logging
from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .container import get_quality_container
from .entities import FlextQualityEntities
from .exceptions import (
    FlextQualityAnalysisError,
    FlextQualityAuthenticationError,
    FlextQualityConfigurationError,
    FlextQualityConnectionError,
    FlextQualityError,
    FlextQualityExceptions,
    FlextQualityGradeError,
    FlextQualityMetricsError,
    FlextQualityProcessingError,
    FlextQualityReportError,
    FlextQualityRuleError,
    FlextQualityTimeoutError,
    FlextQualityValidationError,
)
from .external_backend import FlextQualityExternalBackend as ExternalBackend
from .grade_calculator import FlextQualityGradeCalculator as QualityGradeCalculator
from .handlers import FlextQualityHandlers as FlextQualityHandler, GenerateReportHandler

try:
    from .integrations import FlextQualityIntegrations
except ImportError:  # Optional dependency
    FlextQualityIntegrations = None
from .metrics import QualityMetrics
from .models import FlextQualityModels
from .protocols import FlextQualityProtocols
from .reports import (
    HIGH_ISSUE_THRESHOLD,
    HTML_ISSUE_LIMIT,
    ISSUE_PREVIEW_LIMIT,
    FlextQualityReportGenerator,
)
from .services import FlextQualityServices

# Service aliases for backward compatibility
QualityAnalysisService = FlextQualityServices.AnalysisService
QualityIssueService = FlextQualityServices.IssueService
QualityProjectService = FlextQualityServices.ProjectService
QualityReportService = FlextQualityServices.ReportService

# Type system and aliases
from .typings import FlextQualityTypes
from .utilities import FlextQualityUtilities as QualityUtilities
from .value_objects import FlextQualityValueObjects
from .version import VERSION, FlextQualityVersion

# Backward compatibility aliases for tests
IssueSeverity = FlextQualityValueObjects.IssueSeverity
IssueType = FlextQualityValueObjects.IssueType
AnalysisStatus = FlextQualityEntities.AnalysisStatus
ComplexityMetric = FlextQualityValueObjects.ComplexityMetric
CoverageMetric = FlextQualityValueObjects.CoverageMetric
DuplicationMetric = FlextQualityValueObjects.DuplicationMetric
IssueLocation = FlextQualityValueObjects.IssueLocation
QualityGrade = FlextQualityValueObjects.Grade
QualityScore = FlextQualityValueObjects.Score
FlextAnalysisStatus = FlextQualityEntities.AnalysisStatus  # Alias
AnalyzeProjectHandler = FlextQualityHandler  # Alias
AnalysisResults = FlextQualityModels.AnalysisResults

# Entity aliases for backward compatibility
QualityAnalysis = FlextQualityEntities.Analysis
QualityIssue = FlextQualityEntities.Issue
QualityProject = FlextQualityEntities.Project
QualityReport = FlextQualityEntities.Report
QualityRule = FlextQualityEntities.Rule

# Model aliases for backward compatibility
DuplicationIssue = FlextQualityModels.DuplicationIssue
FileAnalysisResult = FlextQualityModels.FileAnalysisResult
OverallMetrics = FlextQualityModels.OverallMetrics

# Handler aliases for backward compatibility
RunLintingHandler = FlextQualityHandler

# Conditional web interface alias
try:
    FlextQualityWebInterface = FlextQualityWeb  # Alias
except NameError:
    FlextQualityWebInterface = None


# Convenience function for analyze_project
def analyze_project(project_path: str) -> FlextResult:
    """Convenience function to analyze a project."""
    analyzer = CodeAnalyzer(project_path)
    return analyzer.analyze_project()


try:
    from .web import FlextQualityWeb
except ImportError:  # Optional dependency
    FlextQualityWeb = None

__all__ = [
    "HIGH_ISSUE_THRESHOLD",
    "HTML_ISSUE_LIMIT",
    "VERSION",
    "ASTBackend",
    "AnalysisResults",
    "AnalysisStatus",
    "AnalyzeProjectHandler",
    # Additional exports for tests and examples
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
    "FlextQualityASTClassInfo",
    "FlextQualityASTFunctionInfo",
    "FlextQualityAnalysisError",
    "FlextQualityAnalysisTypes",
    "FlextQualityAuthenticationError",
    "FlextQualityConfig",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityConstants",
    "FlextQualityEntities",
    "FlextQualityError",
    "FlextQualityExceptions",
    "FlextQualityGradeError",
    "FlextQualityHandler",
    "FlextQualityIntegrations",
    "FlextQualityMetricsError",
    "FlextQualityModels",
    "FlextQualityProcessingError",
    "FlextQualityProtocols",
    "FlextQualityReportError",
    "FlextQualityReportGenerator",
    "FlextQualityRuleError",
    "FlextQualityServices",
    "FlextQualityTimeoutError",
    "FlextQualityTypes",
    "FlextQualityValidationError",
    "FlextQualityValueObjects",
    "FlextQualityVersion",
    "FlextQualityWeb",
    "FlextQualityWebInterface",
    "GenerateReportHandler",
    "ISSUE_PREVIEW_LIMIT",
    "IssueLocation",
    "OverallMetrics",
    "RunLintingHandler",
    # Backward compatibility aliases
    "IssueSeverity",
    "IssueType",
    "QualityAPI",
    # Entity aliases for backward compatibility
    "QualityAnalysis",
    "QualityAnalysisService",
    "QualityGrade",
    "QualityGradeCalculator",
    "QualityIssue",
    "QualityIssueService",
    "QualityMetrics",
    "QualityProject",
    "QualityProjectService",
    "QualityReport",
    "QualityReportService",
    "QualityRule",
    "QualityScore",
    "QualityUtilities",
    "__version__",
    "__version_info__",
    "analyze_project",
    "another_function",
    "get_quality_container",
    "main",
    "setup_logging", "ISSUE_PREVIEW_LIMIT",
]
