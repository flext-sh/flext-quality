# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Scripts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality.docs.scripts.audit import (
        AccessibilityConfig,
        AuditorResults,
        AuditRulesConfig,
        ContentAnalysisConfig,
        ContentChecksConfig,
        DocumentationAuditor,
        FormattingConfig,
        LinkValidationConfig,
        MarkdownStyleConfig,
        MetricsDict,
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
        SummaryMetrics,
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

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AccessibilityConfig": ("flext_quality.docs.scripts.audit", "AccessibilityConfig"),
    "AuditRulesConfig": ("flext_quality.docs.scripts.audit", "AuditRulesConfig"),
    "AuditSummary": ("flext_quality.docs.scripts.report", "AuditSummary"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "ContentAnalysisConfig": (
        "flext_quality.docs.scripts.audit",
        "ContentAnalysisConfig",
    ),
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
    "DocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "DocumentationOptimizer",
    ),
    "DocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "DocumentationReporter",
    ),
    "FormattingConfig": ("flext_quality.docs.scripts.audit", "FormattingConfig"),
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkValidationConfig": (
        "flext_quality.docs.scripts.audit",
        "LinkValidationConfig",
    ),
    "LinkValidator": ("flext_quality.docs.scripts.validate", "LinkValidator"),
    "LinkValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "LinkValidatorResults",
    ),
    "MIN_HEADINGS_FOR_TOC": (
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ),
    "MarkdownStyleConfig": ("flext_quality.docs.scripts.audit", "MarkdownStyleConfig"),
    "MetricsDict": ("flext_quality.docs.scripts.audit", "MetricsDict"),
    "OptimizationSummary": ("flext_quality.docs.scripts.report", "OptimizationSummary"),
    "OptimizerResults": ("flext_quality.docs.scripts.optimize", "OptimizerResults"),
    "QualityThresholdsConfig": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsConfig",
    ),
    "Recommendation": ("flext_quality.docs.scripts.report", "Recommendation"),
    "ReportData": ("flext_quality.docs.scripts.report", "ReportData"),
    "ReportValue": ("flext_quality.docs.scripts.report", "ReportValue"),
    "SeverityLevelsConfig": (
        "flext_quality.docs.scripts.audit",
        "SeverityLevelsConfig",
    ),
    "StyleGuideConfig": ("flext_quality.docs.scripts.audit", "StyleGuideConfig"),
    "SummaryMetrics": ("flext_quality.docs.scripts.report", "SummaryMetrics"),
    "TrendData": ("flext_quality.docs.scripts.report", "TrendData"),
    "TrendEntry": ("flext_quality.docs.scripts.report", "TrendEntry"),
    "ValidationConfig": ("flext_quality.docs.scripts.audit", "ValidationConfig"),
    "ValidationSummary": ("flext_quality.docs.scripts.report", "ValidationSummary"),
    "main": ("flext_quality.docs.scripts.validate", "main"),
}

__all__ = [
    "MIN_HEADINGS_FOR_TOC",
    "AccessibilityConfig",
    "AuditRulesConfig",
    "AuditSummary",
    "AuditorResults",
    "ContentAnalysisConfig",
    "ContentChecksConfig",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidator",
    "ContentValidatorResults",
    "DocumentationAuditor",
    "DocumentationOptimizer",
    "DocumentationReporter",
    "FormattingConfig",
    "LinkCheckResult",
    "LinkRecord",
    "LinkValidationConfig",
    "LinkValidator",
    "LinkValidatorResults",
    "MarkdownStyleConfig",
    "MetricsDict",
    "OptimizationSummary",
    "OptimizerResults",
    "QualityThresholdsConfig",
    "Recommendation",
    "ReportData",
    "ReportValue",
    "SeverityLevelsConfig",
    "StyleGuideConfig",
    "SummaryMetrics",
    "TrendData",
    "TrendEntry",
    "ValidationConfig",
    "ValidationSummary",
    "main",
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
