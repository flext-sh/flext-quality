"""FLEXT Quality - Python Code Quality Analysis Library.

Provides complete code quality analysis, metrics collection, and automated
quality assurance for FLEXT projects with proper domain-driven design patterns,
railway-oriented programming, and deep FLEXT ecosystem integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

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
from .compat import (
    FlextCodeQualityPlugin,
    FlextDuplicationPlugin,
    FlextHookValidator,
)
from .constants import FlextQualityConstants
from .container import get_quality_container
from .exceptions import FlextQualityExceptions
from .external_backend import FlextQualityExternalBackend as ExternalBackend
from .grade_calculator import FlextQualityGradeCalculator
from .handlers import FlextQualityHandlers
from .metrics import QualityMetrics
from .models import FlextQualityModels
from .reports import FlextQualityReportGenerator, ReportFormat, ReportThresholds
from .services import FlextQualityServices
from .settings import FlextQualitySettings
from .tools.quality_operations import FlextQualityOperations
from .web import FlextQualityWeb as FlextQualityWebInterface

# Direct constant imports for convenience
HIGH_ISSUE_THRESHOLD = FlextQualityConstants.Quality.Analysis.HIGH_ISSUE_THRESHOLD
HTML_ISSUE_LIMIT = FlextQualityConstants.Quality.Analysis.HTML_ISSUE_LIMIT
ISSUE_PREVIEW_LIMIT = FlextQualityConstants.Quality.Analysis.ISSUE_PREVIEW_LIMIT
MIN_COVERAGE_THRESHOLD = FlextQualityConstants.Quality.Analysis.MIN_COVERAGE_THRESHOLD
MIN_SCORE_THRESHOLD = FlextQualityConstants.Quality.Analysis.MIN_SCORE_THRESHOLD


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
    "BackendType",
    "BaseAnalyzer",
    "ExternalBackend",
    "FlextCodeQualityPlugin",
    "FlextDuplicationPlugin",
    "FlextHookValidator",
    "FlextQuality",
    "FlextQualityAnalyzer",
    "FlextQualityConstants",
    "FlextQualityExceptions",
    "FlextQualityGradeCalculator",
    "FlextQualityHandlers",
    "FlextQualityModels",
    "FlextQualityOperations",
    "FlextQualityReportGenerator",
    "FlextQualityServices",
    "FlextQualitySettings",
    "FlextQualityWebInterface",
    "QualityHelperCommands",
    "QualityMetrics",
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
