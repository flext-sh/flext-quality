# AUTO-GENERATED FILE — Regenerate with: make gen
"""Helpers package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.tests.helpers.assertions import (
        assert_analysis_results_structure as assert_analysis_results_structure,
        assert_dict_structure as assert_dict_structure,
        assert_is_dict as assert_is_dict,
        assert_is_list as assert_is_list,
        assert_issues_structure as assert_issues_structure,
        assert_metrics_structure as assert_metrics_structure,
    )
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
