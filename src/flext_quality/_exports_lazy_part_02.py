# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_QUALITY_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        ".api": ("quality",),
        ".base": ("s",),
        ".cli": ("main",),
        ".constants": ("c",),
        ".docs.core.config_manager": ("FlextQualityValidationSettings",),
        ".mcp.server": ("get_server",),
        ".models": ("m",),
        ".protocols": ("p",),
        ".rules.validators": ("FlextQualityValidators",),
        ".typings": ("t",),
        ".utilities": ("u",),
    },
)

__all__: list[str] = ["FLEXT_QUALITY_LAZY_IMPORTS_PART_02"]
