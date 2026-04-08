# AUTO-GENERATED FILE — Regenerate with: make gen
from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityContentValidator": ".validate",
    "FlextQualityDocumentationAuditor": ".audit",
    "FlextQualityDocumentationOptimizer": ".optimize",
    "FlextQualityDocumentationReporter": ".report",
    "FlextQualityLinkValidator": ".validate",
    "MIN_HEADINGS_FOR_TOC": ".optimize",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
