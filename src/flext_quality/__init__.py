"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.__version__ import __version__, __version_info__

# from flext_quality.analysis_types import QualityAnalysisType, QualityMetricType  # Temporarily disabled - these don't exist
from flext_quality.config import FlextQualityConfig
from flext_quality.exceptions import FlextQualityError, FlextQualityValidationError
from flext_quality.grade_calculator import QualityGradeCalculator
from flext_quality.handlers import FlextQualityHandler
from flext_quality.models import QualityMetric, QualityReport
from flext_quality.ports import QualityAnalysisPort
from flext_quality.reports import QualityReportGenerator
from flext_quality.services import FlextQualityService
from flext_quality.utilities import QualityUtilities
from flext_quality.value_objects import QualityScore, QualityThreshold
from flext_quality.web import FlextQualityWebInterface

__all__ = [
    "FlextQualityConfig",
    "FlextQualityError",
    "FlextQualityHandler",
    "FlextQualityService",
    "FlextQualityValidationError",
    "FlextQualityWebInterface",
    "QualityAnalysisPort",
    # "QualityAnalysisType",  # Disabled - doesn't exist
    "QualityGradeCalculator",
    "QualityMetric",
    # "QualityMetricType",  # Disabled - doesn't exist
    "QualityReport",
    "QualityReportGenerator",
    "QualityScore",
    "QualityThreshold",
    "QualityUtilities",
    "__version__",
    "__version_info__",
]
