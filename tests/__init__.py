# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
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
            ".conftest": ("conftest",),
            ".constants": (
                "TestsFlextQualityConstants",
                "c",
            ),
            ".helpers": ("helpers",),
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
            ".unit": ("unit",),
            ".unit.test_api": ("TestsFlextQualityApi",),
            ".unit.test_basic": ("TestsFlextQualityBasic",),
            ".unit.test_cli": ("TestsFlextQualityCli",),
            ".utilities": (
                "TestsFlextQualityUtilities",
                "u",
            ),
            "flext_tests": (
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
