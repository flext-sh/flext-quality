"""Enterprise Code Quality Analysis and Governance Service for FLEXT ecosystem."""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Core FlextCore patterns (root namespace imports)
from flext_core import FlextResult

# Direct imports - no fallbacks allowed per CLAUDE.md
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.metrics import QualityMetrics
from flext_quality.reports import QualityReport
from flext_quality.exceptions import (
    FlextQualityError as QualityError,
)

try:
    __version__ = importlib.metadata.version("flext-quality")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextQualityDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Quality import changes.

    This warning is raised when deprecated import paths are used, guiding
    developers to use the simplified public API instead of internal modules.
    All deprecated imports will be removed in version 1.0.0.
    """


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Display deprecation warning for import paths with migration guidance.

    Args:
        old_import: The deprecated import path being used
        new_import: The recommended replacement import path

    Note:
        This function formats and displays user-friendly deprecation warnings
        that include the old path, recommended replacement, version information,
        and links to migration documentation.

    """
    message_parts = [
        f"DEPRECATED IMPORT: {old_import}",
        f"USE INSTEAD: {new_import}",
        "This will be removed in version 1.0.0",
        "See FLEXT Quality docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextQualityDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Core patterns - already imported from flext_core above

# Core quality exports - moved to top per linting rules

# Simple API exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_quality.simple_api import QualityAPI

# CLI exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_quality.cli import main as cli_main

# ================================
# PUBLIC API EXPORTS
# ================================

__all__: list[str] = [
    "CodeAnalyzer",
    "FlextQualityDeprecationWarning",
    "FlextResult",
    "QualityAPI",
    "QualityError",
    "QualityMetrics",
    "QualityReport",
    "__version__",
    "__version_info__",
    "annotations",
    "cli_main",
]
