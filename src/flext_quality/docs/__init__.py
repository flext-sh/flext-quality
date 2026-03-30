# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs import (
        core,
        dashboard,
        notifications,
        scheduled_maintenance,
        scripts,
        tools,
    )
    from flext_quality.docs.core import base_classes, config_manager, file_discovery
    from flext_quality.docs.core.base_classes import *
    from flext_quality.docs.core.config_manager import *
    from flext_quality.docs.core.file_discovery import *
    from flext_quality.docs.dashboard import *
    from flext_quality.docs.notifications import *
    from flext_quality.docs.scheduled_maintenance import *
    from flext_quality.docs.scripts import audit, optimize, report, validate
    from flext_quality.docs.scripts.audit import *
    from flext_quality.docs.scripts.optimize import *
    from flext_quality.docs.scripts.report import *
    from flext_quality.docs.scripts.validate import *
    from flext_quality.docs.tools import content_analyzer, link_checker, style_validator
    from flext_quality.docs.tools.content_analyzer import *
    from flext_quality.docs.tools.link_checker import *
    from flext_quality.docs.tools.style_validator import *

from flext_quality.docs.core import _LAZY_IMPORTS as _CORE_LAZY
from flext_quality.docs.scripts import _LAZY_IMPORTS as _SCRIPTS_LAZY
from flext_quality.docs.tools import _LAZY_IMPORTS as _TOOLS_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_CORE_LAZY,
    **_SCRIPTS_LAZY,
    **_TOOLS_LAZY,
    "FlextQualityDocumentationDashboard": "flext_quality.docs.dashboard",
    "FlextQualityDocumentationNotifier": "flext_quality.docs.notifications",
    "FlextQualityScheduledMaintenance": "flext_quality.docs.scheduled_maintenance",
    "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.docs.notifications",
    "core": "flext_quality.docs.core",
    "dashboard": "flext_quality.docs.dashboard",
    "logger": "flext_quality.docs.scheduled_maintenance",
    "notifications": "flext_quality.docs.notifications",
    "scheduled_maintenance": "flext_quality.docs.scheduled_maintenance",
    "scripts": "flext_quality.docs.scripts",
    "tools": "flext_quality.docs.tools",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
