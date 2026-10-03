# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs import core, scripts, tools
    from flext_quality.docs.core.config_manager import FlextQualityConfigManager
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import FlextQualityDocumentationValidator
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator


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
    "core",
    "scripts",
    "tools",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".core": ("core",),
            ".core.config_manager": ("FlextQualityConfigManager",),
            ".dashboard": ("FlextQualityDocumentationDashboard",),
            ".notifications": ("FlextQualityDocumentationNotifier",),
            ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".scripts": ("scripts",),
            ".scripts.audit": ("FlextQualityDocumentationAuditor",),
            ".scripts.optimize": ("FlextQualityDocumentationOptimizer",),
            ".scripts.report": ("FlextQualityDocumentationReporter",),
            ".scripts.validate": ("FlextQualityDocumentationValidator",),
            ".tools": ("tools",),
            ".tools.link_checker": ("FlextQualityLinkChecker",),
            ".tools.style_validator": ("FlextQualityStyleValidator",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
