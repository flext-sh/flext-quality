# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.tools import (
        content_analyzer as content_analyzer,
        link_checker as link_checker,
        style_validator as style_validator,
    )
    from flext_quality.docs.tools.content_analyzer import (
        FlextQualityContentAnalyzer as FlextQualityContentAnalyzer,
        analyze_file_content as analyze_file_content,
        analyze_files_content as analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker as FlextQualityLinkChecker,
        validate_links_sync as validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator as FlextQualityStyleValidator,
        validate_file_style as validate_file_style,
        validate_files_style as validate_files_style,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityContentAnalyzer": [
        "flext_quality.docs.tools.content_analyzer",
        "FlextQualityContentAnalyzer",
    ],
    "FlextQualityLinkChecker": [
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ],
    "FlextQualityStyleValidator": [
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
    ],
    "analyze_file_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ],
    "analyze_files_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ],
    "content_analyzer": ["flext_quality.docs.tools.content_analyzer", ""],
    "link_checker": ["flext_quality.docs.tools.link_checker", ""],
    "style_validator": ["flext_quality.docs.tools.style_validator", ""],
    "validate_file_style": [
        "flext_quality.docs.tools.style_validator",
        "validate_file_style",
    ],
    "validate_files_style": [
        "flext_quality.docs.tools.style_validator",
        "validate_files_style",
    ],
    "validate_links_sync": [
        "flext_quality.docs.tools.link_checker",
        "validate_links_sync",
    ],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityContentAnalyzer",
    "FlextQualityLinkChecker",
    "FlextQualityStyleValidator",
    "analyze_file_content",
    "analyze_files_content",
    "content_analyzer",
    "link_checker",
    "style_validator",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
