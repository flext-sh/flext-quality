# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality.docs import core, scripts, tools
    from flext_quality.docs.core.base_classes import (
        BaseAnalyzer,
        BaseAuditor,
        BaseReporter,
        BaseValidator,
        Config,
    )
    from flext_quality.docs.core.config_manager import (
        AuditRules,
        ConfigData,
        ConfigManager,
        ConfigPrimitive,
        ConfigSection,
        ConfigValue,
        RawConfigMap,
        RawSectionMap,
        RawSectionValue,
        StyleGuide,
    )
    from flext_quality.docs.core.file_discovery import (
        DocumentationFinder,
        FileStatistics,
    )
    from flext_quality.docs.dashboard import DocumentationDashboard
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        DocumentationNotifier,
        NotifierResults,
    )
    from flext_quality.docs.scheduled_maintenance import (
        ErrorHandlingConfig,
        LoggingConfig,
        MaintenanceConfig,
        ScheduledMaintenance,
        ScheduleEntry,
        ScheduleResults,
        ScheduleTaskConfig,
    )
    from flext_quality.docs.scripts.audit import (
        AuditorResults,
        AuditRulesConfig,
        ContentAnalysisConfig,
        ContentChecksConfig,
        DocumentationAuditor,
        LinkValidationConfig,
        MarkdownStyleConfig,
        QualityThresholdsConfig,
        SeverityLevelsConfig,
        StyleGuideConfig,
        ValidationConfig,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        DocumentationOptimizer,
        OptimizerResults,
    )
    from flext_quality.docs.scripts.report import (
        AuditSummary,
        DocumentationReporter,
        OptimizationSummary,
        Recommendation,
        ReportData,
        ReportValue,
        TrendData,
        TrendEntry,
        ValidationSummary,
    )
    from flext_quality.docs.scripts.validate import (
        ContentIssue,
        ContentMetrics,
        ContentValidator,
        ContentValidatorResults,
        LinkCheckResult,
        LinkRecord,
        LinkValidator,
        LinkValidatorResults,
        main,
    )
    from flext_quality.docs.tools.content_analyzer import (
        AnalysisDict,
        CompletenessDict,
        ConfigDict,
        ContentAnalyzer,
        IssueDict,
        MetricsDict,
        ReadabilityDict,
        RecommendationDict,
        StructureDict,
        analyze_file_content,
        analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        LinkChecker,
        LinkConfigDict,
        LinkInfoDict,
        LinkInfoDictRequired,
        LinkResultDict,
        LinkResultDictRequired,
        PerformanceMetricsDict,
        ResultsDict,
        validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        AccessibilityConfig,
        FileResults,
        FormattingConfig,
        HeadingsConfig,
        MarkdownConfig,
        StyleConfig,
        StyleIssue,
        StyleValidator,
        SummaryMetrics,
        ValidationResults,
        validate_file_style,
        validate_files_style,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AccessibilityConfig": (
        "flext_quality.docs.tools.style_validator",
        "AccessibilityConfig",
    ),
    "AnalysisDict": ("flext_quality.docs.tools.content_analyzer", "AnalysisDict"),
    "AuditRules": ("flext_quality.docs.core.config_manager", "AuditRules"),
    "AuditRulesConfig": ("flext_quality.docs.scripts.audit", "AuditRulesConfig"),
    "AuditSummary": ("flext_quality.docs.scripts.report", "AuditSummary"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "BaseAnalyzer": ("flext_quality.docs.core.base_classes", "BaseAnalyzer"),
    "BaseAuditor": ("flext_quality.docs.core.base_classes", "BaseAuditor"),
    "BaseReporter": ("flext_quality.docs.core.base_classes", "BaseReporter"),
    "BaseValidator": ("flext_quality.docs.core.base_classes", "BaseValidator"),
    "CompletenessDict": (
        "flext_quality.docs.tools.content_analyzer",
        "CompletenessDict",
    ),
    "Config": ("flext_quality.docs.core.base_classes", "Config"),
    "ConfigData": ("flext_quality.docs.core.config_manager", "ConfigData"),
    "ConfigDict": ("flext_quality.docs.tools.content_analyzer", "ConfigDict"),
    "ConfigManager": ("flext_quality.docs.core.config_manager", "ConfigManager"),
    "ConfigPrimitive": ("flext_quality.docs.core.config_manager", "ConfigPrimitive"),
    "ConfigSection": ("flext_quality.docs.core.config_manager", "ConfigSection"),
    "ConfigValue": ("flext_quality.docs.core.config_manager", "ConfigValue"),
    "ContentAnalysisConfig": (
        "flext_quality.docs.scripts.audit",
        "ContentAnalysisConfig",
    ),
    "ContentAnalyzer": ("flext_quality.docs.tools.content_analyzer", "ContentAnalyzer"),
    "ContentChecksConfig": ("flext_quality.docs.scripts.audit", "ContentChecksConfig"),
    "ContentIssue": ("flext_quality.docs.scripts.validate", "ContentIssue"),
    "ContentMetrics": ("flext_quality.docs.scripts.validate", "ContentMetrics"),
    "ContentValidator": ("flext_quality.docs.scripts.validate", "ContentValidator"),
    "ContentValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "ContentValidatorResults",
    ),
    "DocumentationAuditor": (
        "flext_quality.docs.scripts.audit",
        "DocumentationAuditor",
    ),
    "DocumentationDashboard": (
        "flext_quality.docs.dashboard",
        "DocumentationDashboard",
    ),
    "DocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "DocumentationFinder",
    ),
    "DocumentationNotifier": (
        "flext_quality.docs.notifications",
        "DocumentationNotifier",
    ),
    "DocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "DocumentationOptimizer",
    ),
    "DocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "DocumentationReporter",
    ),
    "ErrorHandlingConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ErrorHandlingConfig",
    ),
    "FileResults": ("flext_quality.docs.tools.style_validator", "FileResults"),
    "FileStatistics": ("flext_quality.docs.core.file_discovery", "FileStatistics"),
    "FormattingConfig": (
        "flext_quality.docs.tools.style_validator",
        "FormattingConfig",
    ),
    "HeadingsConfig": ("flext_quality.docs.tools.style_validator", "HeadingsConfig"),
    "IssueDict": ("flext_quality.docs.tools.content_analyzer", "IssueDict"),
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkChecker": ("flext_quality.docs.tools.link_checker", "LinkChecker"),
    "LinkConfigDict": ("flext_quality.docs.tools.link_checker", "LinkConfigDict"),
    "LinkInfoDict": ("flext_quality.docs.tools.link_checker", "LinkInfoDict"),
    "LinkInfoDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkInfoDictRequired",
    ),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkResultDict": ("flext_quality.docs.tools.link_checker", "LinkResultDict"),
    "LinkResultDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkResultDictRequired",
    ),
    "LinkValidationConfig": (
        "flext_quality.docs.scripts.audit",
        "LinkValidationConfig",
    ),
    "LinkValidator": ("flext_quality.docs.scripts.validate", "LinkValidator"),
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
    "MarkdownConfig": ("flext_quality.docs.tools.style_validator", "MarkdownConfig"),
    "MarkdownStyleConfig": ("flext_quality.docs.scripts.audit", "MarkdownStyleConfig"),
    "MetricsDict": ("flext_quality.docs.tools.content_analyzer", "MetricsDict"),
    "NotifierResults": ("flext_quality.docs.notifications", "NotifierResults"),
    "OptimizationSummary": ("flext_quality.docs.scripts.report", "OptimizationSummary"),
    "OptimizerResults": ("flext_quality.docs.scripts.optimize", "OptimizerResults"),
    "PerformanceMetricsDict": (
        "flext_quality.docs.tools.link_checker",
        "PerformanceMetricsDict",
    ),
    "QualityThresholdsConfig": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsConfig",
    ),
    "RawConfigMap": ("flext_quality.docs.core.config_manager", "RawConfigMap"),
    "RawSectionMap": ("flext_quality.docs.core.config_manager", "RawSectionMap"),
    "RawSectionValue": ("flext_quality.docs.core.config_manager", "RawSectionValue"),
    "ReadabilityDict": ("flext_quality.docs.tools.content_analyzer", "ReadabilityDict"),
    "Recommendation": ("flext_quality.docs.scripts.report", "Recommendation"),
    "RecommendationDict": (
        "flext_quality.docs.tools.content_analyzer",
        "RecommendationDict",
    ),
    "ReportData": ("flext_quality.docs.scripts.report", "ReportData"),
    "ReportValue": ("flext_quality.docs.scripts.report", "ReportValue"),
    "ResultsDict": ("flext_quality.docs.tools.link_checker", "ResultsDict"),
    "ScheduleEntry": ("flext_quality.docs.scheduled_maintenance", "ScheduleEntry"),
    "ScheduleResults": ("flext_quality.docs.scheduled_maintenance", "ScheduleResults"),
    "ScheduleTaskConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduleTaskConfig",
    ),
    "ScheduledMaintenance": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduledMaintenance",
    ),
    "SeverityLevelsConfig": (
        "flext_quality.docs.scripts.audit",
        "SeverityLevelsConfig",
    ),
    "StructureDict": ("flext_quality.docs.tools.content_analyzer", "StructureDict"),
    "StyleConfig": ("flext_quality.docs.tools.style_validator", "StyleConfig"),
    "StyleGuide": ("flext_quality.docs.core.config_manager", "StyleGuide"),
    "StyleGuideConfig": ("flext_quality.docs.scripts.audit", "StyleGuideConfig"),
    "StyleIssue": ("flext_quality.docs.tools.style_validator", "StyleIssue"),
    "StyleValidator": ("flext_quality.docs.tools.style_validator", "StyleValidator"),
    "SummaryMetrics": ("flext_quality.docs.tools.style_validator", "SummaryMetrics"),
    "TrendData": ("flext_quality.docs.scripts.report", "TrendData"),
    "TrendEntry": ("flext_quality.docs.scripts.report", "TrendEntry"),
    "ValidationConfig": ("flext_quality.docs.scripts.audit", "ValidationConfig"),
    "ValidationResults": (
        "flext_quality.docs.tools.style_validator",
        "ValidationResults",
    ),
    "ValidationSummary": ("flext_quality.docs.scripts.report", "ValidationSummary"),
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
    "AnalysisDict",
    "AuditRules",
    "AuditRulesConfig",
    "AuditSummary",
    "AuditorResults",
    "BaseAnalyzer",
    "BaseAuditor",
    "BaseReporter",
    "BaseValidator",
    "CompletenessDict",
    "Config",
    "ConfigData",
    "ConfigDict",
    "ConfigManager",
    "ConfigPrimitive",
    "ConfigSection",
    "ConfigValue",
    "ContentAnalysisConfig",
    "ContentAnalyzer",
    "ContentChecksConfig",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidator",
    "ContentValidatorResults",
    "DocumentationAuditor",
    "DocumentationDashboard",
    "DocumentationFinder",
    "DocumentationNotifier",
    "DocumentationOptimizer",
    "DocumentationReporter",
    "ErrorHandlingConfig",
    "FileResults",
    "FileStatistics",
    "FormattingConfig",
    "HeadingsConfig",
    "IssueDict",
    "LinkCheckResult",
    "LinkChecker",
    "LinkConfigDict",
    "LinkInfoDict",
    "LinkInfoDictRequired",
    "LinkRecord",
    "LinkResultDict",
    "LinkResultDictRequired",
    "LinkValidationConfig",
    "LinkValidator",
    "LinkValidatorResults",
    "LoggingConfig",
    "MaintenanceConfig",
    "MarkdownConfig",
    "MarkdownStyleConfig",
    "MetricsDict",
    "NotifierResults",
    "OptimizationSummary",
    "OptimizerResults",
    "PerformanceMetricsDict",
    "QualityThresholdsConfig",
    "RawConfigMap",
    "RawSectionMap",
    "RawSectionValue",
    "ReadabilityDict",
    "Recommendation",
    "RecommendationDict",
    "ReportData",
    "ReportValue",
    "ResultsDict",
    "ScheduleEntry",
    "ScheduleResults",
    "ScheduleTaskConfig",
    "ScheduledMaintenance",
    "SeverityLevelsConfig",
    "StructureDict",
    "StyleConfig",
    "StyleGuide",
    "StyleGuideConfig",
    "StyleIssue",
    "StyleValidator",
    "SummaryMetrics",
    "TrendData",
    "TrendEntry",
    "ValidationConfig",
    "ValidationResults",
    "ValidationSummary",
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


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
