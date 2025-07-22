"""FLEXT Quality - Enterprise Code Quality Analysis with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Code Quality Analysis with simplified public API:
- All common imports available from root: from flext_quality import QualityAPI
- Built on flext-core foundation for robust quality analysis
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Import from flext-core for foundational patterns
from flext_core import BaseConfig, DomainBaseModel, ServiceResult

try:
    __version__ = importlib.metadata.version("flext-quality")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextQualityDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Quality import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT Quality docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextQualityDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Foundation patterns - ALWAYS from flext-core
from flext_core import (
    BaseConfig as QualityBaseConfig,  # Configuration base
    DomainBaseModel as BaseModel,  # Base for quality models
    DomainError as QualityError,  # Quality-specific errors
    ValidationError as ValidationError,  # Validation errors
)

# Core quality exports - simplified imports
try:
    from flext_quality.analyzer import CodeAnalyzer
    from flext_quality.metrics import QualityMetrics
    from flext_quality.reports import QualityReport
except ImportError:
    # Core layer not yet fully refactored - provide placeholders
    CodeAnalyzer = None
    QualityMetrics = None
    QualityReport = None

# Simple API exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_quality.simple_api import QualityAPI

# CLI exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_quality.cli import main as cli_main

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "BaseModel",  # from flext_quality import BaseModel
    # Core Quality System (simplified access)
    "CodeAnalyzer",  # from flext_quality import CodeAnalyzer
    # Deprecation utilities
    "FlextQualityDeprecationWarning",
    # Simple API Interface
    "QualityAPI",  # from flext_quality import QualityAPI
    # Core Patterns (from flext-core)
    "QualityBaseConfig",  # from flext_quality import QualityBaseConfig
    "QualityError",  # from flext_quality import QualityError
    "QualityMetrics",  # from flext_quality import QualityMetrics
    "QualityReport",  # from flext_quality import QualityReport
    "ServiceResult",  # from flext_quality import ServiceResult
    "ValidationError",  # from flext_quality import ValidationError
    # Version
    "__version__",
    "__version_info__",
    # Command Line Interface
    "cli_main",  # from flext_quality import cli_main
]
