"""Test assertion helpers for flext-quality.

Provides reusable assertion utilities for validating test data structures
across all test modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from tests import t, tm


def assert_is_dict(value: t.Scalar | Mapping[str, t.Scalar], _msg: str = "") -> None:
    """Assert that value is a dict."""
    tm.that(value, is_=dict)


def assert_is_list(value: t.Scalar | Sequence[t.Scalar], _msg: str = "") -> None:
    """Assert that value is a list."""
    tm.that(value, is_=list)


def assert_dict_structure(
    data: Mapping[str, t.Scalar],
    required_keys: Sequence[str],
    msg: str = "",
) -> None:
    """Assert that a dict contains all required keys."""
    missing = [k for k in required_keys if k not in data]
    if missing:
        tm.reject(msg or f"Missing keys: {missing}")


def assert_metrics_structure(metrics: Mapping[str, t.Scalar]) -> None:
    """Assert that metrics dict has expected structure."""
    tm.that(metrics, is_=dict)


def assert_issues_structure(issues: Sequence[t.Scalar]) -> None:
    """Assert that issues data has expected structure."""
    tm.that(issues, is_=list)


def assert_analysis_results_structure(results: Mapping[str, t.Scalar]) -> None:
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
