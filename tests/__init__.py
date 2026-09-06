# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import helpers as helpers
    from . import unit as unit
    from flext_quality import FlextQualityConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from .base import TestsFlextQualityServiceBase, TestsFlextQualityServiceBase as s
    from .conftest import set_test_environment
    from .constants import TestsFlextQualityConstants, TestsFlextQualityConstants as c
    from .helpers.assertions import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
    )
    from .models import TestsFlextQualityModels, TestsFlextQualityModels as m
    from .protocols import TestsFlextQualityProtocols, TestsFlextQualityProtocols as p
    from .settings import TestsFlextQualitySettings
    from .typings import TestsFlextQualityTypes, TestsFlextQualityTypes as t
    from .utilities import TestsFlextQualityUtilities, TestsFlextQualityUtilities as u
__all__: tuple[str, ...] = (
    "FlextQualityConstants",
    "FlextTestsConstants",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "c",
    "d",
    "e",
    "h",
    "helpers",
    "m",
    "p",
    "r",
    "s",
    "set_test_environment",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextQualityServiceBase", "s"),
            ".conftest": ("set_test_environment",),
            ".constants": ("TestsFlextQualityConstants", "c"),
            ".helpers": ("helpers",),
            ".helpers.assertions": (
                "assert_analysis_results_structure",
                "assert_dict_structure",
                "assert_is_dict",
                "assert_is_list",
                "assert_issues_structure",
                "assert_metrics_structure",
            ),
            ".models": ("TestsFlextQualityModels", "m"),
            ".protocols": ("TestsFlextQualityProtocols", "p"),
            ".settings": ("TestsFlextQualitySettings",),
            ".typings": ("TestsFlextQualityTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextQualityUtilities", "u"),
            "flext_quality": ("FlextQualityConstants",),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
