# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from flext_quality import (
        FlextQuality,
        FlextQualityCli,
        FlextQualityConfig,
        FlextQualityConstants,
        FlextQualityModels,
        FlextQualityModelsConfig,
        FlextQualityProtocols,
        FlextQualityServiceBase,
        FlextQualitySettings,
        FlextQualityTypes,
        FlextQualityUtilities,
        FlextQualityVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        main,
        quality,
        settings,
    )
    from tests.base import TestsFlextQualityServiceBase, s
    from tests.constants import TestsFlextQualityConstants, c
    from tests.helpers import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
    )
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.settings import TestsFlextQualitySettings
    from tests.typings import TestsFlextQualityTypes, t
    from tests.utilities import TestsFlextQualityUtilities, u


__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityCli",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityModels",
    "FlextQualityModelsConfig",
    "FlextQualityProtocols",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityVersion",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextQuality": "flext_quality",
        "FlextQualityCli": "flext_quality",
        "FlextQualityConfig": "flext_quality",
        "FlextQualityConstants": "flext_quality",
        "FlextQualityModels": "flext_quality",
        "FlextQualityModelsConfig": "flext_quality",
        "FlextQualityProtocols": "flext_quality",
        "FlextQualityServiceBase": "flext_quality",
        "FlextQualitySettings": "flext_quality",
        "FlextQualityTypes": "flext_quality",
        "FlextQualityUtilities": "flext_quality",
        "FlextQualityVersion": "flext_quality",
        "TestsFlextQualityConstants": ".constants",
        "TestsFlextQualityModels": ".models",
        "TestsFlextQualityProtocols": ".protocols",
        "TestsFlextQualityServiceBase": ".base",
        "TestsFlextQualitySettings": ".settings",
        "TestsFlextQualityTypes": ".typings",
        "TestsFlextQualityUtilities": ".utilities",
        "__author__": "flext_quality",
        "__author_email__": "flext_quality",
        "__description__": "flext_quality",
        "__license__": "flext_quality",
        "__title__": "flext_quality",
        "__url__": "flext_quality",
        "__version__": "flext_quality",
        "__version_info__": "flext_quality",
        "api": "flext_tests",
        "assert_analysis_results_structure": ".helpers",
        "assert_dict_structure": ".helpers",
        "assert_is_dict": ".helpers",
        "assert_is_list": ".helpers",
        "assert_issues_structure": ".helpers",
        "assert_metrics_structure": ".helpers",
        "c": ".constants",
        "config": "flext_quality",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_quality",
        "p": ".protocols",
        "quality": "flext_quality",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_quality",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
