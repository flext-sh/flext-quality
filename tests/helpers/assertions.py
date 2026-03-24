"""Test assertion helpers for flext-quality.

Provides reusable assertion utilities for validating test data structures
across all test modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import t


def assert_is_dict(value: t.Scalar | t.ScalarMapping, msg: str = "") -> None:
    """Assert that value is a dict."""
    assert isinstance(value, dict), msg or f"Expected dict, got {type(value).__name__}"


def assert_is_list(value: t.Scalar | Sequence[t.Scalar], msg: str = "") -> None:
    """Assert that value is a list."""
    assert isinstance(value, list), msg or f"Expected list, got {type(value).__name__}"


def assert_dict_structure(
    data: Mapping[str, t.Scalar], required_keys: Sequence[str], msg: str = ""
) -> None:
    """Assert that a dict contains all required keys."""
    missing = [k for k in required_keys if k not in data]
    assert not missing, msg or f"Missing keys: {missing}"


def assert_metrics_structure(metrics: Mapping[str, t.Scalar]) -> None:
    """Assert that metrics dict has expected structure."""
    assert isinstance(metrics, dict), f"Expected dict, got {type(metrics).__name__}"


def assert_issues_structure(issues: Sequence[t.Scalar]) -> None:
    """Assert that issues data has expected structure."""
    assert isinstance(issues, list), f"Expected list, got {type(issues).__name__}"


def assert_analysis_results_structure(results: Mapping[str, t.Scalar]) -> None:
    """Assert that analysis results have expected structure."""
    assert isinstance(results, dict), f"Expected dict, got {type(results).__name__}"


def safe_dict_access(
    data: Mapping[str, t.Scalar],
    key: str,
    default: t.Scalar | None = None,
) -> t.Scalar | None:
    """Safely access a dict key with a default value."""
    return data.get(key, default)


def safe_list_access(
    data: Sequence[t.Scalar],
    index: int,
    default: t.Scalar | None = None,
) -> t.Scalar | None:
    """Safely access a list index with a default value."""
    try:
        return data[index]
    except IndexError:
        return default


__all__ = [
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "safe_dict_access",
    "safe_list_access",
]
