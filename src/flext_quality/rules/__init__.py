# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.rules package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators


__all__: tuple[str, ...] = (
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".engine": ("FlextQualityRulesEngine",),
            ".loader": ("FlextQualityRulesLoader",),
            ".validators": ("FlextQualityValidators",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
