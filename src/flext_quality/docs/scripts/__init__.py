# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Scripts package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityContentValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityContentValidator",
    ),
    "FlextQualityDocumentationAuditor": (
        "flext_quality.docs.scripts.audit",
        "FlextQualityDocumentationAuditor",
    ),
    "FlextQualityDocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "FlextQualityDocumentationOptimizer",
    ),
    "FlextQualityDocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "FlextQualityDocumentationReporter",
    ),
    "FlextQualityLinkValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ),
    "MIN_HEADINGS_FOR_TOC": (
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ),
    "audit": "flext_quality.docs.scripts.audit",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "optimize": "flext_quality.docs.scripts.optimize",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "report": "flext_quality.docs.scripts.report",
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate": "flext_quality.docs.scripts.validate",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
