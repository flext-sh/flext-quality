# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_QUALITY_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        ".api": ("quality",),
        ".base": ("s",),
        ".rules": ("rules",),
        ".typings": ("t",),
        ".utilities": ("u",),
        "flext_core._root_typing_parts": (
            "r",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_QUALITY_LAZY_IMPORTS_PART_02"]
