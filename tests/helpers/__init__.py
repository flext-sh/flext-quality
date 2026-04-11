# AUTO-GENERATED FILE — Regenerate with: make gen
"""Helpers package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".assertions": ("assertions",),
        ".constants": (
            "TestsConstants",
            "c",
        ),
        ".models": (
            "TestsModels",
            "m",
        ),
        ".protocols": (
            "TestsProtocols",
            "p",
        ),
        ".typing_helpers": ("typing_helpers",),
        ".typings": (
            "TestsTypings",
            "t",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
