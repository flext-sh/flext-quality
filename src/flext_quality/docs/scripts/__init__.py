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
    from flext_quality import audit, optimize, report, validate
    from flext_quality.audit import (
        FlextQualityDocumentationAuditor,
        critical,
        critical_high_issues,
        high,
        quality_score,
        severity_breakdown,
        should_fail,
    )
    from flext_quality.optimize import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer,
        doc_files,
        run_any_optimization,
    )
    from flext_quality.report import FlextQualityDocumentationReporter
    from flext_quality.validate import (
        FlextQualityLinkValidator,
        main,
        project_root,
        run_any_check,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextQualityDocumentationAuditor": "flext_quality.audit",
    "FlextQualityDocumentationOptimizer": "flext_quality.optimize",
    "FlextQualityDocumentationReporter": "flext_quality.report",
    "FlextQualityLinkValidator": "flext_quality.validate",
    "MIN_HEADINGS_FOR_TOC": "flext_quality.optimize",
    "audit": "flext_quality.audit",
    "c": ("flext_core.constants", "FlextConstants"),
    "critical": "flext_quality.audit",
    "critical_high_issues": "flext_quality.audit",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "doc_files": "flext_quality.optimize",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "high": "flext_quality.audit",
    "m": ("flext_core.models", "FlextModels"),
    "main": "flext_quality.validate",
    "optimize": "flext_quality.optimize",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "project_root": "flext_quality.validate",
    "quality_score": "flext_quality.audit",
    "r": ("flext_core.result", "FlextResult"),
    "report": "flext_quality.report",
    "run_any_check": "flext_quality.validate",
    "run_any_optimization": "flext_quality.optimize",
    "s": ("flext_core.service", "FlextService"),
    "severity_breakdown": "flext_quality.audit",
    "should_fail": "flext_quality.audit",
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate": "flext_quality.validate",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
