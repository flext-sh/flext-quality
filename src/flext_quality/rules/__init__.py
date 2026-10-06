# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.rules package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators


__all__: tuple[str, ...] = (
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityRulesEngine": ".engine",
        "FlextQualityRulesLoader": ".loader",
        "FlextQualityValidators": ".validators",
    }),
    public_exports=__all__,
)
