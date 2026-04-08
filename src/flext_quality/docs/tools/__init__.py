# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityContentAnalyzer": (
        "flext_quality.docs.tools.content_analyzer",
        "FlextQualityContentAnalyzer",
    ),
    "FlextQualityLinkChecker": (
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ),
    "FlextQualityStyleValidator": (
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
