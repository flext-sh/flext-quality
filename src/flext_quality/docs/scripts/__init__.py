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
        AuditorResults,
        AuditRulesDict,
        ContentAnalysisDict,
        ContentChecksDict,
        DocumentationAuditor,
        LinkValidationDict,
        MetricsDict,
        QualityThresholdsDict,
        SeverityLevelsDict,
        ValidationConfigDict,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        DocumentationOptimizer,
    )
    from flext_quality.docs.scripts.report import (
        AuditSummary,
        DocumentationReporter,
        OptimizationSummary,
        Recommendation,
        ReportData,
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
        LinkCheckResult as r,
        LinkRecord,
        LinkValidator,
        LinkValidatorResults,
        main,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AuditRulesDict": ("flext_quality.docs.scripts.audit", "AuditRulesDict"),
    "AuditSummary": ("flext_quality.docs.scripts.report", "AuditSummary"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "ContentAnalysisDict": ("flext_quality.docs.scripts.audit", "ContentAnalysisDict"),
    "ContentChecksDict": ("flext_quality.docs.scripts.audit", "ContentChecksDict"),
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
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkValidationDict": ("flext_quality.docs.scripts.audit", "LinkValidationDict"),
    "LinkValidator": ("flext_quality.docs.scripts.validate", "LinkValidator"),
    "LinkValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "LinkValidatorResults",
    ),
    "MIN_HEADINGS_FOR_TOC": (
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ),
    "MetricsDict": ("flext_quality.docs.scripts.audit", "MetricsDict"),
    "OptimizationSummary": ("flext_quality.docs.scripts.report", "OptimizationSummary"),
    "QualityThresholdsDict": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsDict",
    ),
    "Recommendation": ("flext_quality.docs.scripts.report", "Recommendation"),
    "ReportData": ("flext_quality.docs.scripts.report", "ReportData"),
    "SeverityLevelsDict": ("flext_quality.docs.scripts.audit", "SeverityLevelsDict"),
    "SummaryMetrics": ("flext_quality.docs.scripts.report", "SummaryMetrics"),
    "TrendData": ("flext_quality.docs.scripts.report", "TrendData"),
    "TrendEntry": ("flext_quality.docs.scripts.report", "TrendEntry"),
    "ValidationConfigDict": (
        "flext_quality.docs.scripts.audit",
        "ValidationConfigDict",
    ),
    "ValidationSummary": ("flext_quality.docs.scripts.report", "ValidationSummary"),
    "main": ("flext_quality.docs.scripts.validate", "main"),
    "r": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
}

__all__ = [
    "MIN_HEADINGS_FOR_TOC",
    "AuditRulesDict",
    "AuditSummary",
    "AuditorResults",
    "ContentAnalysisDict",
    "ContentChecksDict",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidator",
    "ContentValidatorResults",
    "DocumentationAuditor",
    "DocumentationOptimizer",
    "DocumentationReporter",
    "LinkCheckResult",
    "LinkRecord",
    "LinkValidationDict",
    "LinkValidator",
    "LinkValidatorResults",
    "MetricsDict",
    "OptimizationSummary",
    "QualityThresholdsDict",
    "Recommendation",
    "ReportData",
    "SeverityLevelsDict",
    "SummaryMetrics",
    "TrendData",
    "TrendEntry",
    "ValidationConfigDict",
    "ValidationSummary",
    "main",
    "r",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
