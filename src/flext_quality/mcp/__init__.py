# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.mcp package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.mcp.resources import FlextQualityMcpResources
    from flext_quality.mcp.server import FlextQualityMcpServer
    from flext_quality.mcp.tools import FlextQualityMcpTools


__all__: tuple[str, ...] = (
    "FlextQualityMcpResources",
    "FlextQualityMcpServer",
    "FlextQualityMcpTools",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityMcpResources": ".resources",
        "FlextQualityMcpServer": ".server",
        "FlextQualityMcpTools": ".tools",
    }),
    public_exports=__all__,
)
