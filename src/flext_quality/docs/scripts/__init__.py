# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Scripts package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.scripts import (
        audit as audit,
        optimize as optimize,
        report as report,
        validate as validate,
    )
    from flext_quality.docs.scripts.audit import (
        FlextQualityDocumentationAuditor as FlextQualityDocumentationAuditor,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC as MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer as FlextQualityDocumentationOptimizer,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter as FlextQualityDocumentationReporter,
        ReportValue as ReportValue,
    )
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator as FlextQualityContentValidator,
        FlextQualityLinkValidator as FlextQualityLinkValidator,
        main as main,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityContentValidator": [
        "flext_quality.docs.scripts.validate",
        "FlextQualityContentValidator",
    ],
    "FlextQualityDocumentationAuditor": [
        "flext_quality.docs.scripts.audit",
        "FlextQualityDocumentationAuditor",
    ],
    "FlextQualityDocumentationOptimizer": [
        "flext_quality.docs.scripts.optimize",
        "FlextQualityDocumentationOptimizer",
    ],
    "FlextQualityDocumentationReporter": [
        "flext_quality.docs.scripts.report",
        "FlextQualityDocumentationReporter",
    ],
    "FlextQualityLinkValidator": [
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ],
    "MIN_HEADINGS_FOR_TOC": [
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ],
    "ReportValue": ["flext_quality.docs.scripts.report", "ReportValue"],
    "audit": ["flext_quality.docs.scripts.audit", ""],
    "main": ["flext_quality.docs.scripts.validate", "main"],
    "optimize": ["flext_quality.docs.scripts.optimize", ""],
    "report": ["flext_quality.docs.scripts.report", ""],
    "validate": ["flext_quality.docs.scripts.validate", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityLinkValidator",
    "MIN_HEADINGS_FOR_TOC",
    "ReportValue",
    "audit",
    "main",
    "optimize",
    "report",
    "validate",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
