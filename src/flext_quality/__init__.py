"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.__version__ import __version__, __version_info__

from typing import Final

# Import specific types from the nested class
from .analysis_types import FlextQualityAnalysisTypes

# Core imports - moved to specific imports below to avoid circular import
# Main modules
from .analyzer import FlextQualityAnalyzer as CodeAnalyzer
from .api import FlextQuality as FlextQuality, FlextQuality as QualityAPI
from .ast_backend import FlextQualityASTBackend as ASTBackend
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
from .external_backend import FlextQualityExternalBackend as ExternalBackend
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
from .value_objects import FlextQualityValueObjects
from .version import VERSION, FlextQualityVersion
from .web import FlextQualityWeb

__all__ = [
    "ASTBackend",
    # Additional exports for tests and examples
    "BackendType",
    "BaseAnalyzer",
    "CodeAnalyzer",
    "ExternalBackend",
    "FlextQuality",
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
    "FlextQualityReportModel",
    "FlextQualityRuleError",
    "FlextQualityServices",
    "FlextQualityTimeoutError",
    "FlextQualityTypes",
    "FlextQualityValidationError",
    "FlextQualityValueObjects",
    "FlextQualityWeb",
    "QualityAPI",
    "QualityGradeCalculator",
    "QualityMetrics",
    "QualityUtilities",
    "__version__",
    "__version_info__",
    "get_quality_container",
    # CLI functions removed from __all__ - import directly from .cli if needed
]
