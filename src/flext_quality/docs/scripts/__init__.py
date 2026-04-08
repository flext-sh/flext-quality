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
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
