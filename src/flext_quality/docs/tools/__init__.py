# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs.tools import content_analyzer, link_checker, style_validator
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityContentAnalyzer": "flext_quality.docs.tools.content_analyzer",
    "FlextQualityLinkChecker": "flext_quality.docs.tools.link_checker",
    "FlextQualityStyleValidator": "flext_quality.docs.tools.style_validator",
    "analyze_file_content": "flext_quality.docs.tools.content_analyzer",
    "analyze_files_content": "flext_quality.docs.tools.content_analyzer",
    "content_analyzer": "flext_quality.docs.tools.content_analyzer",
    "link_checker": "flext_quality.docs.tools.link_checker",
    "style_validator": "flext_quality.docs.tools.style_validator",
    "validate_file_style": "flext_quality.docs.tools.style_validator",
    "validate_files_style": "flext_quality.docs.tools.style_validator",
    "validate_links_sync": "flext_quality.docs.tools.link_checker",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
