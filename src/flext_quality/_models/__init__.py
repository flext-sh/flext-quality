# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._models.flextqualitymodels_part_01 import (
        FlextQualityModelsPart01,
    )
    from flext_quality._models.flextqualitymodels_part_02 import (
        FlextQualityModelsPart02,
    )


__all__: tuple[str, ...] = ("FlextQualityModelsPart01", "FlextQualityModelsPart02")

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".flextqualitymodels_part_01": ("FlextQualityModelsPart01",),
            ".flextqualitymodels_part_02": ("FlextQualityModelsPart02",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
