"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import exceptions
from flext_quality.__version__ import __version__, __version_info__
from flext_quality.analysis_types import OverallMetrics

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

# CLI functions (re-enabled for testing compatibility)
from flext_quality.cli import (
    analyze_project,
    another_function,
    main,
    quality_main,
    setup_logging,
)

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

# Models and metrics
from flext_quality.models import FlextQualityReportModel

# Reports
from flext_quality.reports import FlextQualityReportGenerator

# Services
from flext_quality.services import FlextQualityServices

# Utilities and exceptions
from flext_quality.utilities import FlextQualityUtilities as QualityUtilities

# Value objects
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
from flext_quality.web import QualityWebInterface

__all__ = [
    "ASTBackend",
    "ASTVisitor",
    "AnalysisStatus",
    "BackendType",
    "BaseAnalyzer",
    "CodeAnalyzer",
    "ComplexityMetric",
    "CoverageMetric",
    "DuplicationMetric",
    "ExternalBackend",
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
    "QualityConfig",
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
