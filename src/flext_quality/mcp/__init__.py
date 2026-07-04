# AUTO-GENERATED FILE — Regenerate with: make gen
"""Mcp package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.mcp.server import (
        FlextQualityMcpServer as FlextQualityMcpServer,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".resources": ("resources",),
        ".server": ("FlextQualityMcpServer",),
        ".tools": ("tools",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
