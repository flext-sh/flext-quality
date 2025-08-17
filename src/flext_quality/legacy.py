"""Legacy compatibility facade for flext-quality.

This module provides backward compatibility for APIs that may have been refactored
or renamed during the Pydantic modernization process. It follows the same pattern
as flext-core's legacy.py to ensure consistent facade patterns across the ecosystem.

All imports here should be considered deprecated and may issue warnings.
Modern code should import directly from the appropriate modules.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Import modern implementations to re-export under legacy names
from flext_quality.exceptions import (
    FlextQualityAnalysisError,
    FlextQualityAuthenticationError,
    FlextQualityConfigurationError,
    FlextQualityConnectionError,
    FlextQualityError,
    FlextQualityGradeError,
    FlextQualityIssueError,
    FlextQualityMetricsError,
    FlextQualityProcessingError,
    FlextQualityReportError,
    FlextQualityRuleError,
    FlextQualityThresholdError,
    FlextQualityTimeoutError,
    FlextQualityValidationError,
)

# Import quality components for legacy aliases
try:
    from flext_quality.application.services import (
        FlextQualityAnalysisService,
        FlextQualityReportService,
    )
    from flext_quality.domain.entities import (
        FlextQualityAnalysis,
        FlextQualityIssue,
        FlextQualityProject,
    )
    from flext_quality.platform import FlextQualityPlatform
    from flext_quality.simple_api import (
        create_flext_quality_analysis,
        create_flext_quality_project,
        create_flext_quality_report,
        run_quality_analysis,
    )
except ImportError:
    # Handle missing modules gracefully for backward compatibility
    FlextQualityAnalysisService = FlextQualityReportService = None
    FlextQualityProject = FlextQualityAnalysis = FlextQualityIssue = (
        FlextQualityPlatform
    ) = None
    create_flext_quality_project = create_flext_quality_analysis = None
    create_flext_quality_report = run_quality_analysis = None


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy imports."""
    warnings.warn(
        f"{old_name} is deprecated, use {new_name} instead",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy aliases for common quality services - likely used names
def QualityService(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityAnalysisService."""
    _deprecation_warning("QualityService", "FlextQualityAnalysisService")
    if FlextQualityAnalysisService is None:
        msg = "FlextQualityAnalysisService not available"
        raise ImportError(msg)
    return FlextQualityAnalysisService(*args, **kwargs)


def QualityAnalyzer(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityPlatform."""
    _deprecation_warning("QualityAnalyzer", "FlextQualityPlatform")
    if FlextQualityPlatform is None:
        msg = "FlextQualityPlatform not available"
        raise ImportError(msg)
    return FlextQualityPlatform(*args, **kwargs)


def QualityReportService(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityReportService."""
    _deprecation_warning("QualityReportService", "FlextQualityReportService")
    if FlextQualityReportService is None:
        msg = "FlextQualityReportService not available"
        raise ImportError(msg)
    return FlextQualityReportService(*args, **kwargs)


def QualityProject(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityProject."""
    _deprecation_warning("QualityProject", "FlextQualityProject")
    if FlextQualityProject is None:
        msg = "FlextQualityProject not available"
        raise ImportError(msg)
    return FlextQualityProject(*args, **kwargs)


def QualityAnalysis(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityAnalysis."""
    _deprecation_warning("QualityAnalysis", "FlextQualityAnalysis")
    if FlextQualityAnalysis is None:
        msg = "FlextQualityAnalysis not available"
        raise ImportError(msg)
    return FlextQualityAnalysis(*args, **kwargs)


def QualityIssue(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityIssue."""
    _deprecation_warning("QualityIssue", "FlextQualityIssue")
    if FlextQualityIssue is None:
        msg = "FlextQualityIssue not available"
        raise ImportError(msg)
    return FlextQualityIssue(*args, **kwargs)


# Legacy factory function aliases
def create_quality_project(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_quality_project."""
    _deprecation_warning("create_quality_project", "create_flext_quality_project")
    if create_flext_quality_project is None:
        msg = "create_flext_quality_project not available"
        raise ImportError(msg)
    return create_flext_quality_project(*args, **kwargs)


def create_quality_analysis(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_quality_analysis."""
    _deprecation_warning("create_quality_analysis", "create_flext_quality_analysis")
    if create_flext_quality_analysis is None:
        msg = "create_flext_quality_analysis not available"
        raise ImportError(msg)
    return create_flext_quality_analysis(*args, **kwargs)


def create_quality_report(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_quality_report."""
    _deprecation_warning("create_quality_report", "create_flext_quality_report")
    if create_flext_quality_report is None:
        msg = "create_flext_quality_report not available"
        raise ImportError(msg)
    return create_flext_quality_report(*args, **kwargs)


def run_analysis(*args: object, **kwargs: object) -> object:
    """Legacy alias for run_quality_analysis."""
    _deprecation_warning("run_analysis", "run_quality_analysis")
    if run_quality_analysis is None:
        msg = "run_quality_analysis not available"
        raise ImportError(msg)
    return run_quality_analysis(*args, **kwargs)


# Legacy exception aliases (more concise names that were probably used)
def QualityError(*args: object, **kwargs: object) -> FlextQualityError:  # noqa: N802
    """Legacy alias for FlextQualityError."""
    _deprecation_warning("QualityError", "FlextQualityError")
    return FlextQualityError(*args, **kwargs)


def QualityAnalysisError(*args: object, **kwargs: object) -> FlextQualityAnalysisError:  # noqa: N802
    """Legacy alias for FlextQualityAnalysisError."""
    _deprecation_warning("QualityAnalysisError", "FlextQualityAnalysisError")
    return FlextQualityAnalysisError(*args, **kwargs)


def QualityReportError(*args: object, **kwargs: object) -> FlextQualityReportError:  # noqa: N802
    """Legacy alias for FlextQualityReportError."""
    _deprecation_warning("QualityReportError", "FlextQualityReportError")
    return FlextQualityReportError(*args, **kwargs)


def QualityValidationError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityValidationError:
    """Legacy alias for FlextQualityValidationError."""
    _deprecation_warning("QualityValidationError", "FlextQualityValidationError")
    return FlextQualityValidationError(*args, **kwargs)


def QualityConfigurationError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityConfigurationError:
    """Legacy alias for FlextQualityConfigurationError."""
    _deprecation_warning("QualityConfigurationError", "FlextQualityConfigurationError")
    return FlextQualityConfigurationError(*args, **kwargs)


def QualityConnectionError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityConnectionError:
    """Legacy alias for FlextQualityConnectionError."""
    _deprecation_warning("QualityConnectionError", "FlextQualityConnectionError")
    return FlextQualityConnectionError(*args, **kwargs)


def QualityProcessingError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityProcessingError:
    """Legacy alias for FlextQualityProcessingError."""
    _deprecation_warning("QualityProcessingError", "FlextQualityProcessingError")
    return FlextQualityProcessingError(*args, **kwargs)


def QualityAuthenticationError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityAuthenticationError:
    """Legacy alias for FlextQualityAuthenticationError."""
    _deprecation_warning(
        "QualityAuthenticationError", "FlextQualityAuthenticationError"
    )
    return FlextQualityAuthenticationError(*args, **kwargs)


def QualityTimeoutError(*args: object, **kwargs: object) -> FlextQualityTimeoutError:  # noqa: N802
    """Legacy alias for FlextQualityTimeoutError."""
    _deprecation_warning("QualityTimeoutError", "FlextQualityTimeoutError")
    return FlextQualityTimeoutError(*args, **kwargs)


def QualityMetricsError(*args: object, **kwargs: object) -> FlextQualityMetricsError:  # noqa: N802
    """Legacy alias for FlextQualityMetricsError."""
    _deprecation_warning("QualityMetricsError", "FlextQualityMetricsError")
    return FlextQualityMetricsError(*args, **kwargs)


def QualityGradeError(*args: object, **kwargs: object) -> FlextQualityGradeError:  # noqa: N802
    """Legacy alias for FlextQualityGradeError."""
    _deprecation_warning("QualityGradeError", "FlextQualityGradeError")
    return FlextQualityGradeError(*args, **kwargs)


def QualityRuleError(*args: object, **kwargs: object) -> FlextQualityRuleError:  # noqa: N802
    """Legacy alias for FlextQualityRuleError."""
    _deprecation_warning("QualityRuleError", "FlextQualityRuleError")
    return FlextQualityRuleError(*args, **kwargs)


def QualityIssueError(*args: object, **kwargs: object) -> FlextQualityIssueError:  # noqa: N802
    """Legacy alias for FlextQualityIssueError."""
    _deprecation_warning("QualityIssueError", "FlextQualityIssueError")
    return FlextQualityIssueError(*args, **kwargs)


def QualityThresholdError(  # noqa: N802
    *args: object, **kwargs: object
) -> FlextQualityThresholdError:
    """Legacy alias for FlextQualityThresholdError."""
    _deprecation_warning("QualityThresholdError", "FlextQualityThresholdError")
    return FlextQualityThresholdError(*args, **kwargs)


# Alternative naming patterns that might have been used
def FlextQualityManager(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityPlatform (alternate naming)."""
    _deprecation_warning("FlextQualityManager", "FlextQualityPlatform")
    if FlextQualityPlatform is None:
        msg = "FlextQualityPlatform not available"
        raise ImportError(msg)
    return FlextQualityPlatform(*args, **kwargs)


def SimpleQualityAnalyzer(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for FlextQualityPlatform (simple variant)."""
    _deprecation_warning("SimpleQualityAnalyzer", "FlextQualityPlatform")
    if FlextQualityPlatform is None:
        msg = "FlextQualityPlatform not available"
        raise ImportError(msg)
    return FlextQualityPlatform(*args, **kwargs)


# Legacy setup function aliases
def init_quality_system(*args: object, **kwargs: object) -> object:
    """Legacy alias for creating quality platform."""
    _deprecation_warning("init_quality_system", "create_flext_quality_platform")
    if FlextQualityPlatform is None:
        msg = "FlextQualityPlatform not available"
        raise ImportError(msg)
    return FlextQualityPlatform(*args, **kwargs)


def setup_quality_analysis(*args: object, **kwargs: object) -> object:
    """Legacy alias for creating quality platform."""
    _deprecation_warning("setup_quality_analysis", "create_flext_quality_platform")
    if FlextQualityPlatform is None:
        msg = "FlextQualityPlatform not available"
        raise ImportError(msg)
    return FlextQualityPlatform(*args, **kwargs)


# Export legacy aliases for backward compatibility
__all__ = [
    # Alternative naming patterns
    "FlextQualityManager",
    "QualityAnalysis",
    "QualityAnalysisError",
    "QualityAnalyzer",
    "QualityAuthenticationError",
    "QualityConfigurationError",
    "QualityConnectionError",
    # Legacy exception aliases (concise forms)
    "QualityError",
    "QualityGradeError",
    "QualityIssue",
    "QualityIssueError",
    "QualityMetricsError",
    "QualityProcessingError",
    "QualityProject",
    "QualityReportError",
    "QualityReportService",
    "QualityRuleError",
    # Legacy service aliases
    "QualityService",
    "QualityThresholdError",
    "QualityTimeoutError",
    "QualityValidationError",
    "SimpleQualityAnalyzer",
    "create_quality_analysis",
    # Legacy factory function aliases
    "create_quality_project",
    "create_quality_report",
    # Legacy setup functions
    "init_quality_system",
    "run_analysis",
    "setup_quality_analysis",
]
