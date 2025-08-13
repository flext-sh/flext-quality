"""FLEXT Quality - Enterprise Code Quality Analysis and Governance Service for FLEXT ecosystem.

This module provides comprehensive code quality analysis, governance, and monitoring
capabilities for the entire FLEXT ecosystem. Built with Clean Architecture and
Domain-Driven Design principles, it serves as the centralized quality control hub
providing enterprise-grade analysis across 32+ FLEXT projects.

The service implements sophisticated quality analysis algorithms, multi-backend
integration, and comprehensive reporting to maintain high code quality standards
throughout the FLEXT data integration platform.

Architecture (Clean Architecture + DDD):
    - Domain Layer: Quality analysis entities, metrics, and business rules
    - Application Layer: Analysis orchestration services and workflow management
    - Infrastructure Layer: Tool integration (Ruff, MyPy, Bandit) and data persistence
    - Presentation Layer: REST APIs, web interfaces, and comprehensive reporting

Key Features:
    - Multi-Backend Analysis: Integrated analysis using AST, Ruff, MyPy, Bandit, and security scanners
    - Quality Metrics: Enterprise-grade scoring algorithms with customizable thresholds
    - Comprehensive Reporting: Multi-format reports (HTML, JSON, PDF) with trend analysis
    - FLEXT Integration: Cross-project analysis with ecosystem-aware quality assessment
    - Real-Time Monitoring: Continuous quality monitoring with alerting and notifications
    - CI/CD Integration: Quality gates with automated pass/fail determination
    - Pattern Recognition: Intelligent detection of code patterns and anti-patterns
    - Remediation Guidance: Actionable recommendations for quality improvements

Analysis Capabilities:
    - Code Style: PEP8 compliance, formatting, and style consistency
    - Type Safety: MyPy analysis with strict type checking
    - Security: Vulnerability scanning and security best practice validation
    - Complexity: Cyclomatic complexity, maintainability metrics
    - Testing: Test coverage analysis and quality assessment
    - Documentation: Docstring coverage and quality validation
    - Dependencies: Dependency analysis and security vulnerability scanning

Quality Metrics:
    - Overall Quality Score: Composite quality rating (0-100)
    - Technical Debt Index: Quantified technical debt measurement
    - Maintainability Rating: Code maintainability assessment
    - Security Rating: Security posture evaluation
    - Test Quality Score: Testing completeness and effectiveness

FLEXT Ecosystem Integration:
    - Built on flext-core foundation patterns (FlextResult, FlextEntity, FlextContainer)
    - Integrates with flext-observability for monitoring and metrics collection
    - Provides REST APIs for flext-cli and flext-web integration
    - Supports workspace-wide analysis across all FLEXT projects
    - Leverages flext-auth for secure access control and audit logging

Example:
    Basic project analysis with comprehensive quality assessment:

    >>> from flext_quality import FlextQualityAPI, FlextQualityConfig
    >>> from flext_core import FlextResult
    >>>
    >>> # Configure quality analysis service
    >>> config = FlextQualityConfig(
    ...     analysis_backends=["ruff", "mypy", "bandit"],
    ...     quality_threshold=80.0,
    ...     enable_security_scan=True,
    ... )
    >>>
    >>> # Initialize API and analyze project
    >>> api = FlextQualityAPI(config)
    >>> result = await api.analyze_project("/path/to/flext-project")
    >>> if result.is_success:
    ...     analysis = result.data
    ...     print(f"Quality Score: {analysis.overall_score}/100")
    ...     print(f"Issues Found: {len(analysis.issues)}")
    ...     print(f"Security Vulnerabilities: {analysis.security_score}")

    Ecosystem-wide quality analysis:

    >>> # Analyze entire FLEXT ecosystem
    >>> ecosystem_result = await api.analyze_ecosystem("/home/user/flext")
    >>> if ecosystem_result.is_success:
    ...     ecosystem_quality = ecosystem_result.data
    ...     for project in ecosystem_quality.projects:
    ...         print(f"{project.name}: {project.quality_score}/100")
    ...     print(f"Ecosystem Average: {ecosystem_quality.average_score}")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

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
    "BaseModel",
    "CodeAnalyzer",
    "FlextQualityDeprecationWarning",
    "FlextResult",
    "QualityAPI",
    "QualityBaseConfig",
    "QualityError",
    "QualityMetrics",
    "QualityReport",
    "ValidationError",
    "__version__",
    "__version_info__",
    "annotations",
    "cli_main",
]
