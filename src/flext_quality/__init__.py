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

# from flext_quality.handlers import FlextQualityHandler  # Temporarily disabled - doesn't exist
from flext_quality.models import (
    FlextQualityReportModel,  # QualityMetric, QualityReport don't exist
)

# from flext_quality.ports import QualityAnalysisPort  # Temporarily disabled - doesn't exist
# from flext_quality.reports import QualityReportGenerator  # Temporarily disabled - doesn't exist
from flext_quality.services import BasicQualityProjectService as FlextQualityService
from flext_quality.utilities import FlextQualityUtilities as QualityUtilities
from flext_quality.value_objects import QualityScore  # QualityThreshold doesn't exist

# from flext_quality.web import FlextQualityWebInterface  # Temporarily disabled - circular import

__all__ = [
    "FlextQualityConfig",
    "FlextQualityError",
    "FlextQualityReportModel",
    "FlextQualityService",
    "FlextQualityValidationError",
    "QualityGradeCalculator",
    "QualityScore",
    "QualityUtilities",
    "__version__",
    "__version_info__",
]
