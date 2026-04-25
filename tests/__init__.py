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
    from flext_tests import td, tf, tk, tm, tv

    from flext_quality import d, e, h, r, s, x
    from tests.conftest import MockQualityAnalyzer, MockReportGenerator
    from tests.constants import TestsFlextQualityConstants, c
    from tests.helpers.assertions import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
    )
    from tests.helpers.constants import TestsConstants
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.typings import TestsFlextQualityTypes, t
    from tests.unit.test_api import TestsFlextQualityApi
    from tests.unit.test_basic import TestsFlextQualityBasic
    from tests.unit.test_cli import TestsFlextQualityCli
    from tests.utilities import TestsFlextQualityUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".helpers",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".conftest": (
                "MockQualityAnalyzer",
                "MockReportGenerator",
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
            ".helpers.constants": ("TestsConstants",),
            ".helpers.models": ("TestsModels",),
            ".helpers.protocols": ("TestsProtocols",),
            ".helpers.typings": ("TestsTypings",),
            ".models": (
                "TestsFlextQualityModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextQualityProtocols",
                "p",
            ),
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
                "s",
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
    "MockQualityAnalyzer",
    "MockReportGenerator",
    "TestsConstants",
    "TestsFlextQualityApi",
    "TestsFlextQualityBasic",
    "TestsFlextQualityCli",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
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
