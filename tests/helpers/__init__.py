# AUTO-GENERATED FILE — Regenerate with: make gen
"""Helpers package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".assertions": (
            "assert_analysis_results_structure",
            "assert_dict_structure",
            "assert_is_dict",
            "assert_is_list",
            "assert_issues_structure",
            "assert_metrics_structure",
        ),
        ".typing_helpers": ("typing_helpers",),
        "flext_tests": (
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
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
