"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

# Core imports - moved to specific imports below to avoid circular import
# Main modules
from .analyzer import FlextQualityAnalyzer as CodeAnalyzer
from .api import FlextQualityAPI as QualityAPI
from .ast_backend import (
    FlextQualityASTBackend as ASTBackend,
)
from .backend_type import BackendType
from .base import BaseAnalyzer

# CLI imports are lazy to avoid flext_cli dependency issues
# Use: from .cli import main
# Instead of: from flext_quality import main
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
from .external_backend import (
    FlextQualityExternalBackend as ExternalBackend,
)
from .grade_calculator import QualityGradeCalculator
from .handlers import FlextQualityHandlers as FlextQualityHandler
from .integrations import FlextQualityIntegrations
from .metrics import QualityMetrics
from .models import FlextQualityModels, FlextQualityReportModel
from .protocols import FlextQualityProtocols
from .reports import FlextQualityReportGenerator
from .services import FlextQualityServices

# Type system and aliases
from .typings import FlextQualityTypes
from .utilities import FlextQualityUtilities as QualityUtilities
from .value_objects import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
    IssueLocation,
    QualityGrade,
    QualityScore,
)
from .version import VERSION, FlextQualityVersion
from .web import FlextQualityWebInterface as QualityWebInterface

# Type aliases for backward compatibility (deprecated - use FlextQualityTypes.*)
AnalysisResults = FlextQualityTypes.AnalysisResults
CodeIssue = FlextQualityTypes.CodeIssue
ComplexityIssue = FlextQualityTypes.ComplexityIssue
DeadCodeIssue = FlextQualityTypes.DeadCodeIssue
Dependency = FlextQualityTypes.Dependency
DuplicationIssue = FlextQualityTypes.DuplicationIssue
FileAnalysisResult = FlextQualityTypes.FileAnalysisResult
OverallMetrics = FlextQualityTypes.OverallMetrics
SecurityIssue = FlextQualityTypes.SecurityIssue
TestResults = FlextQualityTypes.TestResults

# Entity aliases
AnalysisStatus = FlextQualityEntities.AnalysisStatus
QualityAnalysis = FlextQualityEntities.QualityAnalysis
QualityIssue = FlextQualityEntities.QualityIssue
QualityProject = FlextQualityEntities.QualityProject
QualityReport = FlextQualityEntities.QualityReport
QualityRule = FlextQualityEntities.QualityRule

PROJECT_VERSION: Final[FlextQualityVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
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
    "FlextQualityConstants",
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
    "FlextQualityReportModel",
    "FlextQualityRuleError",
    "FlextQualityServices",
    "FlextQualityTimeoutError",
    "FlextQualityTypes",
    "FlextQualityValidationError",
    "FlextQualityVersion",
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
    "exceptions_all",
    "get_quality_container",
    # CLI functions removed from __all__ - import directly from .cli if needed
]
