# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Scripts package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs.scripts.audit import *
    from flext_quality.docs.scripts.optimize import *
    from flext_quality.docs.scripts.report import *
    from flext_quality.docs.scripts.validate import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityContentValidator": "flext_quality.docs.scripts.validate",
    "FlextQualityDocumentationAuditor": "flext_quality.docs.scripts.audit",
    "FlextQualityDocumentationOptimizer": "flext_quality.docs.scripts.optimize",
    "FlextQualityDocumentationReporter": "flext_quality.docs.scripts.report",
    "FlextQualityLinkValidator": "flext_quality.docs.scripts.validate",
    "MIN_HEADINGS_FOR_TOC": "flext_quality.docs.scripts.optimize",
    "ReportValue": "flext_quality.docs.scripts.report",
    "audit": "flext_quality.docs.scripts.audit",
    "main": "flext_quality.docs.scripts.validate",
    "optimize": "flext_quality.docs.scripts.optimize",
    "report": "flext_quality.docs.scripts.report",
    "validate": "flext_quality.docs.scripts.validate",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
