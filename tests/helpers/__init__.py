# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.helpers package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from tests.helpers.assertions import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
    )


__all__: tuple[str, ...] = (
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "assert_analysis_results_structure": ".assertions",
        "assert_dict_structure": ".assertions",
        "assert_is_dict": ".assertions",
        "assert_is_list": ".assertions",
        "assert_issues_structure": ".assertions",
        "assert_metrics_structure": ".assertions",
    }),
    public_exports=__all__,
)
