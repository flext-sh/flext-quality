# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tools package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

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

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "AccessibilityConfig": (
        "flext_quality.docs.tools.style_validator",
        "AccessibilityConfig",
    ),
    "AnalysisDict": ("flext_quality.docs.tools.content_analyzer", "AnalysisDict"),
    "CompletenessDict": (
        "flext_quality.docs.tools.content_analyzer",
        "CompletenessDict",
    ),
    "ConfigDict": ("flext_quality.docs.tools.content_analyzer", "ConfigDict"),
    "ContentAnalyzer": ("flext_quality.docs.tools.content_analyzer", "ContentAnalyzer"),
    "FileResults": ("flext_quality.docs.tools.style_validator", "FileResults"),
    "FormattingConfig": (
        "flext_quality.docs.tools.style_validator",
        "FormattingConfig",
    ),
    "HeadingsConfig": ("flext_quality.docs.tools.style_validator", "HeadingsConfig"),
    "IssueDict": ("flext_quality.docs.tools.content_analyzer", "IssueDict"),
    "LinkChecker": ("flext_quality.docs.tools.link_checker", "LinkChecker"),
    "LinkConfigDict": ("flext_quality.docs.tools.link_checker", "LinkConfigDict"),
    "LinkInfoDict": ("flext_quality.docs.tools.link_checker", "LinkInfoDict"),
    "LinkInfoDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkInfoDictRequired",
    ),
    "LinkResultDict": ("flext_quality.docs.tools.link_checker", "LinkResultDict"),
    "LinkResultDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkResultDictRequired",
    ),
    "MarkdownConfig": ("flext_quality.docs.tools.style_validator", "MarkdownConfig"),
    "MetricsDict": ("flext_quality.docs.tools.content_analyzer", "MetricsDict"),
    "PerformanceMetricsDict": (
        "flext_quality.docs.tools.link_checker",
        "PerformanceMetricsDict",
    ),
    "ReadabilityDict": ("flext_quality.docs.tools.content_analyzer", "ReadabilityDict"),
    "RecommendationDict": (
        "flext_quality.docs.tools.content_analyzer",
        "RecommendationDict",
    ),
    "ResultsDict": ("flext_quality.docs.tools.link_checker", "ResultsDict"),
    "StructureDict": ("flext_quality.docs.tools.content_analyzer", "StructureDict"),
    "StyleConfig": ("flext_quality.docs.tools.style_validator", "StyleConfig"),
    "StyleIssue": ("flext_quality.docs.tools.style_validator", "StyleIssue"),
    "StyleValidator": ("flext_quality.docs.tools.style_validator", "StyleValidator"),
    "SummaryMetrics": ("flext_quality.docs.tools.style_validator", "SummaryMetrics"),
    "ValidationResults": (
        "flext_quality.docs.tools.style_validator",
        "ValidationResults",
    ),
    "analyze_file_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ),
    "analyze_files_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ),
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
    "AccessibilityConfig",
    "AnalysisDict",
    "CompletenessDict",
    "ConfigDict",
    "ContentAnalyzer",
    "FileResults",
    "FormattingConfig",
    "HeadingsConfig",
    "IssueDict",
    "LinkChecker",
    "LinkConfigDict",
    "LinkInfoDict",
    "LinkInfoDictRequired",
    "LinkResultDict",
    "LinkResultDictRequired",
    "MarkdownConfig",
    "MetricsDict",
    "PerformanceMetricsDict",
    "ReadabilityDict",
    "RecommendationDict",
    "ResultsDict",
    "StructureDict",
    "StyleConfig",
    "StyleIssue",
    "StyleValidator",
    "SummaryMetrics",
    "ValidationResults",
    "analyze_file_content",
    "analyze_files_content",
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
