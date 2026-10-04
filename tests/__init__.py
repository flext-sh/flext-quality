# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from tests import helpers, unit
    from tests.base import TestsFlextQualityServiceBase, s
    from tests.constants import TestsFlextQualityConstants, c
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.settings import TestsFlextQualitySettings
    from tests.typings import TestsFlextQualityTypes, t
    from tests.utilities import TestsFlextQualityUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "api",
    "c",
    "d",
    "e",
    "h",
    "helpers",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextQualityServiceBase", "s"),
            ".constants": ("TestsFlextQualityConstants", "c"),
            ".helpers": ("helpers",),
            ".models": ("TestsFlextQualityModels", "m"),
            ".protocols": ("TestsFlextQualityProtocols", "p"),
            ".settings": ("TestsFlextQualitySettings",),
            ".typings": ("TestsFlextQualityTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextQualityUtilities", "u"),
            "flext_tests": ("api", "d", "e", "h", "r", "td", "tf", "tk", "tm", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
