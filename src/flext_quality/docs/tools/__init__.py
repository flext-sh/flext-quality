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
    from flext_quality import content_analyzer, link_checker, style_validator
    from flext_quality.content_analyzer import (
        MIN_ARGS,
        FlextQualityContentAnalyzer,
        analyze_files_content,
        analyzer,
        issues,
        recommendations,
        suggestions,
    )
    from flext_quality.link_checker import (
        FlextQualityLinkChecker,
        checker,
        context,
        error_msg,
        file,
        main,
        status,
        test_links,
        text,
        type as type_,
        url,
    )
    from flext_quality.style_validator import (
        FlextQualityStyleValidator,
        config_path,
        file_path,
        issue_types,
        key,
        paths,
        results,
        reverse,
        save_report,
        sorted_issues,
        v_type,
        validate_files_style,
        validator,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextQualityContentAnalyzer": "flext_quality.content_analyzer",
    "FlextQualityLinkChecker": "flext_quality.link_checker",
    "FlextQualityStyleValidator": "flext_quality.style_validator",
    "MIN_ARGS": "flext_quality.content_analyzer",
    "analyze_files_content": "flext_quality.content_analyzer",
    "analyzer": "flext_quality.content_analyzer",
    "c": ("flext_core.constants", "FlextConstants"),
    "checker": "flext_quality.link_checker",
    "config_path": "flext_quality.style_validator",
    "content_analyzer": "flext_quality.content_analyzer",
    "context": "flext_quality.link_checker",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_msg": "flext_quality.link_checker",
    "file": "flext_quality.link_checker",
    "file_path": "flext_quality.style_validator",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "issue_types": "flext_quality.style_validator",
    "issues": "flext_quality.content_analyzer",
    "key": "flext_quality.style_validator",
    "link_checker": "flext_quality.link_checker",
    "m": ("flext_core.models", "FlextModels"),
    "main": "flext_quality.link_checker",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "paths": "flext_quality.style_validator",
    "r": ("flext_core.result", "FlextResult"),
    "recommendations": "flext_quality.content_analyzer",
    "results": "flext_quality.style_validator",
    "reverse": "flext_quality.style_validator",
    "s": ("flext_core.service", "FlextService"),
    "save_report": "flext_quality.style_validator",
    "sorted_issues": "flext_quality.style_validator",
    "status": "flext_quality.link_checker",
    "style_validator": "flext_quality.style_validator",
    "suggestions": "flext_quality.content_analyzer",
    "t": ("flext_core.typings", "FlextTypes"),
    "test_links": "flext_quality.link_checker",
    "text": "flext_quality.link_checker",
    "type": "flext_quality.link_checker",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "url": "flext_quality.link_checker",
    "v_type": "flext_quality.style_validator",
    "validate_files_style": "flext_quality.style_validator",
    "validator": "flext_quality.style_validator",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
