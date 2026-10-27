# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.core import FlextQualityConfigManager
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts import (
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityDocumentationValidator,
    )
    from flext_quality.docs.tools import (
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
    )


__all__: tuple[str, ...] = (
    "FlextQualityConfigManager",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
    "FlextQualityLinkChecker",
    "FlextQualityScheduledMaintenance",
    "FlextQualityStyleValidator",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityConfigManager": ".core.maintenance",
        "FlextQualityDocumentationAuditor": ".scripts.audit",
        "FlextQualityDocumentationDashboard": ".dashboard",
        "FlextQualityDocumentationNotifier": ".notifications",
        "FlextQualityDocumentationOptimizer": ".scripts.optimize",
        "FlextQualityDocumentationReporter": ".scripts.report",
        "FlextQualityDocumentationValidator": ".scripts.validate",
        "FlextQualityLinkChecker": ".tools.link_checker",
        "FlextQualityScheduledMaintenance": ".scheduled_maintenance",
        "FlextQualityStyleValidator": ".tools.style_validator",
    }),
    public_exports=__all__,
)
