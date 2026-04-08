# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tools package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityContentAnalyzer": ".content_analyzer",
    "FlextQualityLinkChecker": ".link_checker",
    "FlextQualityStyleValidator": ".style_validator",
    "analyze_file_content": ".content_analyzer",
    "analyze_files_content": ".content_analyzer",
    "validate_file_style": ".style_validator",
    "validate_files_style": ".style_validator",
    "validate_links_sync": ".link_checker",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
