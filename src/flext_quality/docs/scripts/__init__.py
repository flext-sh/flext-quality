# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Scripts package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_quality.docs.scripts.audit as _flext_quality_docs_scripts_audit

    audit = _flext_quality_docs_scripts_audit
    import flext_quality.docs.scripts.optimize as _flext_quality_docs_scripts_optimize
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor

    optimize = _flext_quality_docs_scripts_optimize
    import flext_quality.docs.scripts.report as _flext_quality_docs_scripts_report
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer,
    )

    report = _flext_quality_docs_scripts_report
    import flext_quality.docs.scripts.validate as _flext_quality_docs_scripts_validate
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter

    validate = _flext_quality_docs_scripts_validate
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
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
    )
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

__all__ = [
    "MIN_HEADINGS_FOR_TOC",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityLinkValidator",
    "audit",
    "c",
    "d",
    "e",
    "h",
    "m",
    "optimize",
    "p",
    "r",
    "report",
    "s",
    "t",
    "u",
    "validate",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
