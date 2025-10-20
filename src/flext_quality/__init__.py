"""FLEXT Quality - Enterprise-Grade Python Code Quality Analysis Library.

Provides comprehensive code quality analysis, metrics collection, and automated
quality assurance for FLEXT projects with proper domain-driven design patterns,
railway-oriented programming, and deep FLEXT ecosystem integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_quality.__version__ import __version__, __version_info__

from .analyzer import FlextQualityAnalyzer

# =========================================================================
# CORE FLEXT QUALITY API - Direct imports only, no aliases or wrappers
# =========================================================================
from .api import FlextQuality
from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .exceptions import FlextQualityExceptions
from .models import FlextQualityModels
from .services import FlextQualityServices

# =========================================================================
# TEMPORARY TEST COMPATIBILITY EXPORTS (for test migration)
# These are temporary - tests should use FlextQualityModels.* directly
# =========================================================================
IssueSeverity = FlextQualityModels.IssueSeverity
IssueType = FlextQualityModels.IssueType
AnalysisStatus = FlextQualityModels.AnalysisStatus
FlextAnalysisStatus = FlextQualityModels.AnalysisStatus  # Old name compat
QualityGrade = FlextQualityModels.QualityGrade

# Service compat exports - deprecated, use FlextQualityServices().service_name instead
QualityProjectService = None  # Placeholder
QualityAnalysisService = None  # Placeholder
QualityIssueService = None  # Placeholder
QualityReportService = None  # Placeholder

# Entity model compat exports - deprecated, use FlextQualityModels.* directly
QualityProject = FlextQualityModels.ProjectModel
QualityAnalysis = FlextQualityModels.AnalysisModel
QualityIssue = FlextQualityModels.IssueModel
QualityReport = FlextQualityModels.ReportModel
QualityRule = None  # Placeholder - no equivalent in new models

# Analysis results compat - deprecated, use FlextQualityModels.AnalysisResults directly
AnalysisResults = FlextQualityModels.AnalysisResults
FileAnalysisResult = FlextQualityModels.AnalysisResults
DuplicationIssue = FlextQualityModels.IssueModel

# Backend compat exports - deprecated, use FlextQualityAnalyzer directly
ASTBackend = None  # Placeholder
ExternalBackend = None  # Placeholder
BaseAnalyzer = None  # Placeholder
BackendType = None  # Placeholder
CodeAnalyzer = FlextQualityAnalyzer  # Direct mapping

# =========================================================================
# PUBLIC API - FLEXT patterns only, ZERO aliases, ZERO wrappers
# =========================================================================

__all__ = [
    # Core components
    "ASTBackend",
    "AnalysisResults",
    "AnalysisStatus",
    "BackendType",
    "BaseAnalyzer",
    "CodeAnalyzer",
    "DuplicationIssue",
    "ExternalBackend",
    "FileAnalysisResult",
    "FlextAnalysisStatus",
    "FlextQuality",
    "FlextQualityAnalyzer",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityExceptions",
    "FlextQualityModels",
    "FlextQualityServices",
    # Model enums
    "IssueSeverity",
    "IssueType",
    "QualityAnalysis",
    "QualityAnalysisService",
    "QualityGrade",
    "QualityIssue",
    "QualityIssueService",
    # Entity models
    "QualityProject",
    "QualityProjectService",
    # Services
    "QualityReport",
    "QualityReportService",
    "QualityRule",
    # Version info
    "__version__",
    "__version_info__",
]
