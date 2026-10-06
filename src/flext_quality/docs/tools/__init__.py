# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs.tools package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator


__all__: tuple[str, ...] = ("FlextQualityLinkChecker", "FlextQualityStyleValidator")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityLinkChecker": ".link_checker",
        "FlextQualityStyleValidator": ".style_validator",
    }),
    public_exports=__all__,
)
