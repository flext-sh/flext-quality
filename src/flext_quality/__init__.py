"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations
from flext_core import FlextTypes


"""FLEXT Quality - Code Quality Analysis System."""
"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


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
from flext_quality.utilities import (
    FlextAnalysisUtilities,
    FlextQualityUtilities,
    FlextReportUtilities,
    FlextTestUtilities,
)
from flext_quality.value_objects import *

# Specific imports to avoid conflicts
from flext_quality.web import FlextQualityWebInterface, web_main

# Note: __all__ is constructed dynamically at runtime from imported modules
# This pattern is necessary for library aggregation but causes pyright warnings
import flext_quality.analysis_types as _analysis_types
import flext_quality.analyzer as _analyzer
import flext_quality.api as _api
import flext_quality.ast_backend as _ast_backend
import flext_quality.ast_class_info as _ast_class_info
import flext_quality.ast_function_info as _ast_function_info
import flext_quality.backend_type as _backend_type
import flext_quality.base as _base
import flext_quality.cli as _cli
import flext_quality.config as _config
import flext_quality.constants as _constants
import flext_quality.container as _container
import flext_quality.entities as _entities
import flext_quality.exceptions as _exceptions
import flext_quality.external_backend as _external_backend
import flext_quality.fields as _fields
import flext_quality.grade_calculator as _grade_calculator
import flext_quality.handlers as _handlers
import flext_quality.metrics as _metrics
import flext_quality.models as _models
import flext_quality.ports as _ports
import flext_quality.reports as _reports
import flext_quality.services as _services
import flext_quality.typings as _typings
import flext_quality.utilities as _utilities
import flext_quality.value_objects as _value_objects
import flext_quality.web as _web

# Static __all__ list to satisfy Ruff PLE0605 requirement
# Essential exports - only explicitly imported items to avoid F405 errors
__all__ = [
    # Explicitly imported from web module
    "FlextQualityWebInterface",
    "web_main",
]
