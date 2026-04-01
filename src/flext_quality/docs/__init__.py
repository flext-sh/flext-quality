# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs.core import *
    from flext_quality.docs.dashboard import *
    from flext_quality.docs.notifications import *
    from flext_quality.docs.scheduled_maintenance import *
    from flext_quality.docs.scripts import *
    from flext_quality.docs.tools import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_quality.docs.core",
        "flext_quality.docs.scripts",
        "flext_quality.docs.tools",
    ),
    {
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
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
