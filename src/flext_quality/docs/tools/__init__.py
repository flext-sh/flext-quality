# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tools package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".content_analyzer": (
            "FlextQualityContentAnalyzer",
            "analyze_file_content",
            "analyze_files_content",
        ),
        ".link_checker": (
            "FlextQualityLinkChecker",
            "validate_links_sync",
        ),
        ".style_validator": (
            "FlextQualityStyleValidator",
            "validate_file_style",
            "validate_files_style",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
