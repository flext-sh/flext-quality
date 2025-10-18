"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_quality.__version__ import __version__, __version_info__

from .analysis_service import FlextQualityAnalysisService

# Core direct imports - no wrappers or aliases
from .analyzer import FlextQualityAnalyzer
from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .entities import FlextQualityEntities
from .exceptions import FlextQualityError
from .issue_service import FlextQualityIssueService
from .models import FlextQualityModels
from .project_service import FlextQualityProjectService
from .report_service import FlextQualityReportService
from .services import FlextQualityServices
from .value_objects import FlextQualityValueObjects

__all__ = [
    "FlextQualityAnalysisService",
    # Core FLEXT Quality classes - direct access only
    "FlextQualityAnalyzer",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityEntities",
    "FlextQualityError",
    "FlextQualityIssueService",
    "FlextQualityModels",
    "FlextQualityProjectService",
    "FlextQualityReportService",
    "FlextQualityServices",
    "FlextQualityValueObjects",
    "__version__",
    "__version_info__",
]
