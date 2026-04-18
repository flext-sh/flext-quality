# AUTO-GENERATED FILE — Regenerate with: make gen
"""Scripts package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".audit": ("FlextQualityDocumentationAuditor",),
        ".optimize": ("FlextQualityDocumentationOptimizer",),
        ".report": ("FlextQualityDocumentationReporter",),
        ".validate": (
            "FlextQualityContentValidator",
            "FlextQualityLinkValidator",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityLinkValidator",
]
