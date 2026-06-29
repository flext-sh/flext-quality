# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td as td, tf as tf, tk as tk, tm as tm, tv as tv

    from flext_quality import d as d, e as e, h as h, r as r, x as x
    from tests.base import (
        TestsFlextQualityServiceBase as TestsFlextQualityServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextQualityConstants as TestsFlextQualityConstants,
        c as c,
    )
    from tests.helpers.assertions import (
        assert_analysis_results_structure as assert_analysis_results_structure,
        assert_dict_structure as assert_dict_structure,
        assert_is_dict as assert_is_dict,
        assert_is_list as assert_is_list,
        assert_issues_structure as assert_issues_structure,
        assert_metrics_structure as assert_metrics_structure,
    )
    from tests.models import TestsFlextQualityModels as TestsFlextQualityModels, m as m
    from tests.protocols import (
        TestsFlextQualityProtocols as TestsFlextQualityProtocols,
        p as p,
    )
    from tests.settings import TestsFlextQualitySettings as TestsFlextQualitySettings
    from tests.typings import TestsFlextQualityTypes as TestsFlextQualityTypes, t as t
    from tests.unit.test_api import TestsFlextQualityApi as TestsFlextQualityApi
    from tests.unit.test_basic import TestsFlextQualityBasic as TestsFlextQualityBasic
    from tests.unit.test_cli import TestsFlextQualityCli as TestsFlextQualityCli
    from tests.utilities import (
        TestsFlextQualityUtilities as TestsFlextQualityUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".helpers",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextQualityServiceBase",
                "s",
            ),
            ".constants": (
                "TestsFlextQualityConstants",
                "c",
            ),
            ".helpers.assertions": (
                "assert_analysis_results_structure",
                "assert_dict_structure",
                "assert_is_dict",
                "assert_is_list",
                "assert_issues_structure",
                "assert_metrics_structure",
            ),
            ".models": (
                "TestsFlextQualityModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextQualityProtocols",
                "p",
            ),
            ".settings": ("TestsFlextQualitySettings",),
            ".typings": (
                "TestsFlextQualityTypes",
                "t",
            ),
            ".unit.test_api": ("TestsFlextQualityApi",),
            ".unit.test_basic": ("TestsFlextQualityBasic",),
            ".unit.test_cli": ("TestsFlextQualityCli",),
            ".utilities": (
                "TestsFlextQualityUtilities",
                "u",
            ),
            "flext_quality": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextQualityApi",
    "TestsFlextQualityBasic",
    "TestsFlextQualityCli",
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
]
