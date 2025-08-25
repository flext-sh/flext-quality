"""FLEXT Quality - Code Quality Analysis System.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

# ruff: noqa: F403
# Import all from each module following flext-core pattern
from flext_quality.__version__ import *
from flext_quality.analysis_types import *
from flext_quality.analyzer import *
from flext_quality.api import *
from flext_quality.ast_backend import *
from flext_quality.ast_class_info import *
from flext_quality.ast_function_info import *
from flext_quality.backend_type import *
from flext_quality.base import *
from flext_quality.cli import *
from flext_quality.config import *
from flext_quality.constants import *
from flext_quality.container import *
from flext_quality.entities import *
from flext_quality.exceptions import *
from flext_quality.external_backend import *
from flext_quality.fields import *
from flext_quality.grade_calculator import *
from flext_quality.handlers import *
from flext_quality.metrics import *
from flext_quality.models import *
from flext_quality.ports import *
# Specific imports to avoid conflicts
from flext_quality.reports import (
    FlextQualityReportGenerator,
    ISSUE_PREVIEW_LIMIT,
    HTML_ISSUE_LIMIT,
    HIGH_ISSUE_THRESHOLD,
    MIN_COVERAGE_THRESHOLD,
    MIN_SCORE_THRESHOLD,
    HIGH_TYPE_ERROR_THRESHOLD,
)
from flext_quality.services import *
from flext_quality.typings import *
# Specific imports to avoid conflicts
from flext_quality.utilities import FlextQualityUtilities, FlextReportUtilities, FlextTestUtilities, FlextAnalysisUtilities
from flext_quality.value_objects import *
# Specific imports to avoid conflicts  
from flext_quality.web import FlextQualityWebInterface, web_main

# Note: __all__ is constructed dynamically at runtime from imported modules
# This pattern is necessary for library aggregation but causes pyright warnings
__all__: list[str] = []
