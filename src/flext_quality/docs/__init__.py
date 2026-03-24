# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs import core, scripts, tools
    from flext_quality.docs.core.base_classes import (
        Config,
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
    )
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier,
        NotifierResults,
    )
    from flext_quality.docs.scheduled_maintenance import (
        ErrorHandlingConfig,
        FlextQualityScheduledMaintenance,
        LoggingConfig,
        MaintenanceConfig,
        ScheduleEntry,
        ScheduleResults,
        ScheduleTaskConfig,
    )
    from flext_quality.docs.scripts.audit import (
        AccessibilityConfig,
        AuditMetrics,
        AuditorResults,
        AuditRecommendation,
        AuditRulesConfig,
        ContentAnalysisConfig,
        ContentChecksConfig,
        FlextQualityDocumentationAuditor,
        FormattingConfig,
        LinkValidationConfig,
        MarkdownStyleConfig,
        QualityThresholdsConfig,
        SeverityLevelsConfig,
        StyleGuideConfig,
        ValidationConfig,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer,
        OptimizerResults,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter,
        ReportValue,
    )
    from flext_quality.docs.scripts.validate import (
        ContentIssue,
        ContentMetrics,
        ContentValidatorResults,
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
        LinkCheckResult,
        LinkRecord,
        LinkValidatorResults,
        main,
    )
    from flext_quality.docs.tools.content_analyzer import (
        FlextQualityContentAnalyzer,
        analyze_file_content,
        analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker,
        validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator,
        validate_file_style,
        validate_files_style,
    )

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "AccessibilityConfig": ("flext_quality.docs.scripts.audit", "AccessibilityConfig"),
    "AuditMetrics": ("flext_quality.docs.scripts.audit", "AuditMetrics"),
    "AuditRecommendation": ("flext_quality.docs.scripts.audit", "AuditRecommendation"),
    "AuditRulesConfig": ("flext_quality.docs.scripts.audit", "AuditRulesConfig"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "Config": ("flext_quality.docs.core.base_classes", "Config"),
    "ContentAnalysisConfig": (
        "flext_quality.docs.scripts.audit",
        "ContentAnalysisConfig",
    ),
    "ContentChecksConfig": ("flext_quality.docs.scripts.audit", "ContentChecksConfig"),
    "ContentIssue": ("flext_quality.docs.scripts.validate", "ContentIssue"),
    "ContentMetrics": ("flext_quality.docs.scripts.validate", "ContentMetrics"),
    "ContentValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "ContentValidatorResults",
    ),
    "ErrorHandlingConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ErrorHandlingConfig",
    ),
    "FlextQualityAuditRules": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityAuditRules",
    ),
    "FlextQualityBaseAnalyzer": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAnalyzer",
    ),
    "FlextQualityBaseAuditor": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAuditor",
    ),
    "FlextQualityBaseReporter": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ),
    "FlextQualityBaseValidator": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ),
    "FlextQualityConfigManager": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ),
    "FlextQualityContentAnalyzer": (
        "flext_quality.docs.tools.content_analyzer",
        "FlextQualityContentAnalyzer",
    ),
    "FlextQualityContentValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityContentValidator",
    ),
    "FlextQualityDocumentationAuditor": (
        "flext_quality.docs.scripts.audit",
        "FlextQualityDocumentationAuditor",
    ),
    "FlextQualityDocumentationDashboard": (
        "flext_quality.docs.dashboard",
        "FlextQualityDocumentationDashboard",
    ),
    "FlextQualityDocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityDocumentationFinder",
    ),
    "FlextQualityDocumentationNotifier": (
        "flext_quality.docs.notifications",
        "FlextQualityDocumentationNotifier",
    ),
    "FlextQualityDocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "FlextQualityDocumentationOptimizer",
    ),
    "FlextQualityDocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "FlextQualityDocumentationReporter",
    ),
    "FlextQualityFileStatistics": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityFileStatistics",
    ),
    "FlextQualityLinkChecker": (
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ),
    "FlextQualityLinkValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ),
    "FlextQualityScheduledMaintenance": (
        "flext_quality.docs.scheduled_maintenance",
        "FlextQualityScheduledMaintenance",
    ),
    "FlextQualityStyleGuide": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ),
    "FlextQualityStyleValidator": (
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
    ),
    "FlextQualityValidationConfig": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ),
    "FormattingConfig": ("flext_quality.docs.scripts.audit", "FormattingConfig"),
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkValidationConfig": (
        "flext_quality.docs.scripts.audit",
        "LinkValidationConfig",
    ),
    "LinkValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "LinkValidatorResults",
    ),
    "LoggingConfig": ("flext_quality.docs.scheduled_maintenance", "LoggingConfig"),
    "MAX_BROKEN_LINKS_TO_SHOW": (
        "flext_quality.docs.notifications",
        "MAX_BROKEN_LINKS_TO_SHOW",
    ),
    "MIN_HEADINGS_FOR_TOC": (
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ),
    "MaintenanceConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "MaintenanceConfig",
    ),
    "MarkdownStyleConfig": ("flext_quality.docs.scripts.audit", "MarkdownStyleConfig"),
    "NotifierResults": ("flext_quality.docs.notifications", "NotifierResults"),
    "OptimizerResults": ("flext_quality.docs.scripts.optimize", "OptimizerResults"),
    "QualityThresholdsConfig": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsConfig",
    ),
    "ReportValue": ("flext_quality.docs.scripts.report", "ReportValue"),
    "ScheduleEntry": ("flext_quality.docs.scheduled_maintenance", "ScheduleEntry"),
    "ScheduleResults": ("flext_quality.docs.scheduled_maintenance", "ScheduleResults"),
    "ScheduleTaskConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduleTaskConfig",
    ),
    "SeverityLevelsConfig": (
        "flext_quality.docs.scripts.audit",
        "SeverityLevelsConfig",
    ),
    "StyleGuideConfig": ("flext_quality.docs.scripts.audit", "StyleGuideConfig"),
    "ValidationConfig": ("flext_quality.docs.scripts.audit", "ValidationConfig"),
    "analyze_file_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ),
    "analyze_files_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ),
    "core": ("flext_quality.docs.core", ""),
    "main": ("flext_quality.docs.scripts.validate", "main"),
    "scripts": ("flext_quality.docs.scripts", ""),
    "tools": ("flext_quality.docs.tools", ""),
    "validate_file_style": (
        "flext_quality.docs.tools.style_validator",
        "validate_file_style",
    ),
    "validate_files_style": (
        "flext_quality.docs.tools.style_validator",
        "validate_files_style",
    ),
    "validate_links_sync": (
        "flext_quality.docs.tools.link_checker",
        "validate_links_sync",
    ),
}

__all__ = [
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
    "AccessibilityConfig",
    "AuditMetrics",
    "AuditRecommendation",
    "AuditRulesConfig",
    "AuditorResults",
    "Config",
    "ContentAnalysisConfig",
    "ContentChecksConfig",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidatorResults",
    "ErrorHandlingConfig",
    "FlextQualityAuditRules",
    "FlextQualityBaseAnalyzer",
    "FlextQualityBaseAuditor",
    "FlextQualityBaseReporter",
    "FlextQualityBaseValidator",
    "FlextQualityConfigManager",
    "FlextQualityContentAnalyzer",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationFinder",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityFileStatistics",
    "FlextQualityLinkChecker",
    "FlextQualityLinkValidator",
    "FlextQualityScheduledMaintenance",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityValidationConfig",
    "FormattingConfig",
    "LinkCheckResult",
    "LinkRecord",
    "LinkValidationConfig",
    "LinkValidatorResults",
    "LoggingConfig",
    "MaintenanceConfig",
    "MarkdownStyleConfig",
    "NotifierResults",
    "OptimizerResults",
    "QualityThresholdsConfig",
    "ReportValue",
    "ScheduleEntry",
    "ScheduleResults",
    "ScheduleTaskConfig",
    "SeverityLevelsConfig",
    "StyleGuideConfig",
    "ValidationConfig",
    "analyze_file_content",
    "analyze_files_content",
    "core",
    "main",
    "scripts",
    "tools",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
