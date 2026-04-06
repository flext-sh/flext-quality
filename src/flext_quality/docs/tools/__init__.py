# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_quality.docs.tools.content_analyzer as _flext_quality_docs_tools_content_analyzer

    content_analyzer = _flext_quality_docs_tools_content_analyzer
    import flext_quality.docs.tools.link_checker as _flext_quality_docs_tools_link_checker
    from flext_quality.docs.tools.content_analyzer import (
        FlextQualityContentAnalyzer,
        analyze_file_content,
        analyze_files_content,
    )

    link_checker = _flext_quality_docs_tools_link_checker
    import flext_quality.docs.tools.style_validator as _flext_quality_docs_tools_style_validator
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker,
        validate_links_sync,
    )

    style_validator = _flext_quality_docs_tools_style_validator
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator,
        validate_file_style,
        validate_files_style,
    )
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
    "c": ("flext_core.constants", "FlextConstants"),
    "content_analyzer": "flext_quality.docs.tools.content_analyzer",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "link_checker": "flext_quality.docs.tools.link_checker",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "style_validator": "flext_quality.docs.tools.style_validator",
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
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
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextQualityContentAnalyzer",
    "FlextQualityLinkChecker",
    "FlextQualityStyleValidator",
    "analyze_file_content",
    "analyze_files_content",
    "c",
    "content_analyzer",
    "d",
    "e",
    "h",
    "link_checker",
    "m",
    "p",
    "r",
    "s",
    "style_validator",
    "t",
    "u",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
