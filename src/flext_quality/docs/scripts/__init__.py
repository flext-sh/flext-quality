# AUTO-GENERATED FILE — Regenerate with: make gen
"""Scripts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.scripts.audit import (
        FlextQualityDocumentationAuditor as FlextQualityDocumentationAuditor,
    )
    from flext_quality.docs.scripts.optimize import (
        FlextQualityDocumentationOptimizer as FlextQualityDocumentationOptimizer,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter as FlextQualityDocumentationReporter,
    )
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator as FlextQualityContentValidator,
        FlextQualityDocumentationValidator as FlextQualityDocumentationValidator,
        FlextQualityLinkValidator as FlextQualityLinkValidator,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".audit": ("FlextQualityDocumentationAuditor",),
        ".optimize": ("FlextQualityDocumentationOptimizer",),
        ".report": ("FlextQualityDocumentationReporter",),
        ".validate": (
            "FlextQualityContentValidator",
            "FlextQualityDocumentationValidator",
            "FlextQualityLinkValidator",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
