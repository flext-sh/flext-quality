# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextQualityConstants": ".constants",
        "TestsFlextQualityModels": ".models",
        "TestsFlextQualityProtocols": ".protocols",
        "TestsFlextQualityServiceBase": ".base",
        "TestsFlextQualitySettings": ".settings",
        "TestsFlextQualityTypes": ".typings",
        "TestsFlextQualityUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "helpers": ".helpers",
        "m": ".models",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "unit": ".unit",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
