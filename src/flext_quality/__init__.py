"""FLEXT Quality - Enterprise Code Quality Analysis and Governance Service.

FLEXT Quality is an enterprise-grade quality governance service that provides
comprehensive code quality analysis, issue detection, and reporting capabilities
for the FLEXT ecosystem. Built with Clean Architecture and Domain-Driven Design
principles, it serves as the centralized quality control hub for all FLEXT projects.

Key Features:
    - Multi-backend analysis engine (AST, Ruff, MyPy, Bandit, Security)
    - Enterprise-grade quality metrics and scoring algorithms
    - Comprehensive reporting in multiple formats (HTML, JSON, PDF)
    - FLEXT ecosystem integration with cross-project analysis
    - Real-time quality monitoring and threshold enforcement
    - CI/CD pipeline integration with quality gates

Architecture:
    The service follows Clean Architecture with clear layer separation:
    - Domain Layer: Core business entities and quality analysis logic
    - Application Layer: Service orchestration and business workflows
    - Infrastructure Layer: External tool integration and data persistence
    - Presentation Layer: APIs, web interface, and reporting

Integration:
    - Built on flext-core foundation patterns (FlextResult, FlextEntity)
    - Integrates with flext-observability for monitoring and metrics
    - Provides APIs for flext-cli and flext-web integration
    - Supports workspace-wide analysis across 32+ FLEXT projects

Example:
    Basic usage with the simplified API:

    >>> from flext_quality import QualityAPI
    >>> api = QualityAPI()
    >>> result = await api.analyze_project("/path/to/project")
    >>> if result.success:
    ...     print(f"Quality Score: {result.data.overall_score}")
    ...     print(f"Issues Found: {len(result.data.issues)}")

Author: FLEXT Development Team
Version: 0.9.0
License: MIT
Copyright (c) 2025 FLEXT Team. All rights reserved.

"""

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
    "BaseModel",  # from flext_quality import BaseModel
    # Core Quality System (simplified access)
    "CodeAnalyzer",  # from flext_quality import CodeAnalyzer
    # Deprecation utilities
    "FlextQualityDeprecationWarning",
    "FlextResult",  # from flext_quality import FlextResult
    # Simple API Interface
    "QualityAPI",  # from flext_quality import QualityAPI
    # Core Patterns (from flext-core)
    "QualityBaseConfig",  # from flext_quality import QualityBaseConfig
    "QualityError",  # from flext_quality import QualityError
    "QualityMetrics",  # from flext_quality import QualityMetrics
    "QualityReport",  # from flext_quality import QualityReport
    "ValidationError",  # from flext_quality import ValidationError
    # Version
    "__version__",
    "__version_info__",
    # Command Line Interface
    "cli_main",  # from flext_quality import cli_main
]
