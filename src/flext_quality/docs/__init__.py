# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )


__all__: tuple[str, ...] = (
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityScheduledMaintenance",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityDocumentationDashboard": ".dashboard",
        "FlextQualityDocumentationNotifier": ".notifications",
        "FlextQualityScheduledMaintenance": ".scheduled_maintenance",
    }),
    public_exports=__all__,
)
