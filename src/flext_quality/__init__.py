"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.__version__ import __version__, __version_info__

# Core analyzer and backends
from flext_quality.analyzer import FlextQualityCodeAnalyzer as CodeAnalyzer

# API and handlers
from flext_quality.api import FlextQualityAPI as QualityAPI

# AST utilities
from flext_quality.ast_backend import (
    ASTVisitor,
    FlextQualityASTBackend as ASTBackend,
)
from flext_quality.backend_type import BackendType
from flext_quality.base import BaseAnalyzer

# CLI functions (temporarily disabled due to flext-cli integration issues)
# from flext_quality.cli import analyze_project, main
# Configuration and containers
from flext_quality.config import FlextQualityConfig, FlextQualityConfig as QualityConfig
from flext_quality.container import get_quality_container

# Domain entities
from flext_quality.entities import (
    FlextAnalysisStatus as AnalysisStatus,
    FlextQualityAnalysis as QualityAnalysis,
    FlextQualityIssue as QualityIssue,
    FlextQualityProject as QualityProject,
    FlextQualityReport as QualityReport,
    FlextQualityRule as QualityRule,
)
from flext_quality.exceptions import FlextQualityError, FlextQualityValidationError
from flext_quality.external_backend import (
    FlextQualityExternalBackend as ExternalBackend,
)
from flext_quality.grade_calculator import QualityGradeCalculator
from flext_quality.handlers import FlextQualityHandlers as FlextQualityHandler
from flext_quality.metrics import QualityMetrics

# Models and metrics
from flext_quality.models import FlextQualityReportModel

# Reports
from flext_quality.reports import FlextQualityReportGenerator

# Services
from flext_quality.services import (
    BasicQualityAnalysisService as QualityAnalysisService,
    BasicQualityIssueService as QualityIssueService,
    BasicQualityProjectService as FlextQualityService,
    BasicQualityProjectService as QualityProjectService,
    BasicQualityReportService as QualityReportService,
)

# Utilities and exceptions
from flext_quality.utilities import FlextQualityUtilities as QualityUtilities

# Value objects
from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
    QualityScore,
)

__all__ = [
    "ASTBackend",
    "ASTVisitor",
    "AnalysisStatus",
    "BackendType",
    "BaseAnalyzer",
    # Core analyzer and backends
    "CodeAnalyzer",
    "ExternalBackend",
    # Configuration and containers
    "FlextQualityConfig",
    "FlextQualityError",
    "FlextQualityHandler",
    # Reports
    "FlextQualityReportGenerator",
    # Models and metrics
    "FlextQualityReportModel",
    "FlextQualityService",
    "FlextQualityValidationError",
    "IssueSeverity",
    "IssueType",
    # API and handlers
    "QualityAPI",
    "QualityAnalysis",
    "QualityAnalysisService",
    "QualityConfig",
    "QualityGradeCalculator",
    "QualityIssue",
    "QualityIssueService",
    "QualityMetrics",
    # Domain entities
    "QualityProject",
    # Services
    "QualityProjectService",
    "QualityReport",
    "QualityReportService",
    "QualityRule",
    # Value objects
    "QualityScore",
    # CLI functions (temporarily disabled)
    # "analyze_project",
    # "main",
    # Utilities and exceptions
    "QualityUtilities",
    # Version info
    "__version__",
    "__version_info__",
    "get_quality_container",
]
