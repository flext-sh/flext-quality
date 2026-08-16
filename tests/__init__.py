# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from .base import TestsFlextQualityServiceBase, TestsFlextQualityServiceBase as s
    from .constants import TestsFlextQualityConstants, TestsFlextQualityConstants as c
    from .models import TestsFlextQualityModels, TestsFlextQualityModels as m
    from .protocols import TestsFlextQualityProtocols, TestsFlextQualityProtocols as p
    from .settings import TestsFlextQualitySettings
    from .typings import TestsFlextQualityTypes, TestsFlextQualityTypes as t
    from .utilities import TestsFlextQualityUtilities, TestsFlextQualityUtilities as u
__all__: tuple[str, ...] = (
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextQualityServiceBase", "s"),
            ".constants": ("TestsFlextQualityConstants", "c"),
            ".models": ("TestsFlextQualityModels", "m"),
            ".protocols": ("TestsFlextQualityProtocols", "p"),
            ".settings": ("TestsFlextQualitySettings",),
            ".typings": ("TestsFlextQualityTypes", "t"),
            ".utilities": ("TestsFlextQualityUtilities", "u"),
            "flext_tests": ("d", "e", "h", "r", "td", "tf", "tk", "tm", "tv", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
