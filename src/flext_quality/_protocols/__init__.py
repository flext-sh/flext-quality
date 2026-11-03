# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._protocols.base import FlextQualityProtocolsBase
    from flext_quality._protocols.flextqualitymodels_part_01 import (
        FlextQualityProtocolsFlextqualitymodelsPart01,
    )
    from flext_quality._protocols.flextqualitymodels_part_02 import (
        FlextQualityProtocolsFlextqualitymodelsPart02,
    )
    from flext_quality._protocols.quality import FlextQualityProtocolsQuality


__all__: tuple[str, ...] = (
    "FlextQualityProtocolsBase",
    "FlextQualityProtocolsFlextqualitymodelsPart01",
    "FlextQualityProtocolsFlextqualitymodelsPart02",
    "FlextQualityProtocolsQuality",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextQualityProtocolsBase": ".base",
        "FlextQualityProtocolsFlextqualitymodelsPart01": ".flextqualitymodels_part_01",
        "FlextQualityProtocolsFlextqualitymodelsPart02": ".flextqualitymodels_part_02",
        "FlextQualityProtocolsQuality": ".quality",
    },
    public_exports=__all__,
)
