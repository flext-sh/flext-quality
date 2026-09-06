# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs.scripts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .audit import FlextQualityDocumentationAuditor
    from .optimize import FlextQualityDocumentationOptimizer
    from .report import FlextQualityDocumentationReporter
    from .validate import FlextQualityDocumentationValidator
__all__: tuple[str, ...] = (
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".audit": ("FlextQualityDocumentationAuditor",),
            ".optimize": ("FlextQualityDocumentationOptimizer",),
            ".report": ("FlextQualityDocumentationReporter",),
            ".validate": ("FlextQualityDocumentationValidator",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
