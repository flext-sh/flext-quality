"""Test assertion helpers for flext-quality.

Provides reusable assertion utilities for validating test data structures
across all test modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import tm

from tests import t


def assert_is_dict(value: t.Scalar | t.ScalarMapping, msg: str = "") -> None:
    """Assert that value is a dict."""
    tm.that(value, is_=dict)


def assert_is_list(value: t.Scalar | t.ScalarList, msg: str = "") -> None:
    """Assert that value is a list."""
    tm.that(value, is_=list)


def assert_dict_structure(
    data: t.ScalarMapping,
    required_keys: t.StrSequence,
    msg: str = "",
) -> None:
    """Assert that a dict contains all required keys."""
    missing = [k for k in required_keys if k not in data]
    assert not missing, msg or f"Missing keys: {missing}"


def assert_metrics_structure(metrics: t.ScalarMapping) -> None:
    """Assert that metrics dict has expected structure."""
    tm.that(metrics, is_=dict)


def assert_issues_structure(issues: t.ScalarList) -> None:
    """Assert that issues data has expected structure."""
    tm.that(issues, is_=list)


def assert_analysis_results_structure(results: t.ScalarMapping) -> None:
    """Assert that analysis results have expected structure."""
    tm.that(results, is_=dict)


__all__: list[str] = [
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
]
