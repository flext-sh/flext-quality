# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs.scripts package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import FlextQualityDocumentationValidator


__all__: tuple[str, ...] = (
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityDocumentationAuditor": ".audit",
        "FlextQualityDocumentationOptimizer": ".optimize",
        "FlextQualityDocumentationReporter": ".report",
        "FlextQualityDocumentationValidator": ".validate",
    }),
    public_exports=__all__,
)
