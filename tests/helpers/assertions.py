"""Test assertion helpers for flext-quality.

Provides reusable assertion utilities for validating test data structures
across all test modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def assert_is_dict(value: object, msg: str = "") -> None:
    """Assert that value is a dict."""
    assert isinstance(value, dict), msg or f"Expected dict, got {type(value).__name__}"


def assert_is_list(value: object, msg: str = "") -> None:
    """Assert that value is a list."""
    assert isinstance(value, list), msg or f"Expected list, got {type(value).__name__}"


def assert_dict_structure(
    data: Mapping[str, Any],
    required_keys: Sequence[str],
    msg: str = "",
) -> None:
    """Assert that a dict contains all required keys."""
    missing = [k for k in required_keys if k not in data]
    assert not missing, msg or f"Missing keys: {missing}"


def assert_metrics_structure(metrics: Mapping[str, Any]) -> None:
    """Assert that metrics dict has expected structure."""
    assert isinstance(metrics, dict), f"Expected dict, got {type(metrics).__name__}"


def assert_issues_structure(issues: object) -> None:
    """Assert that issues data has expected structure."""
    assert isinstance(issues, list), f"Expected list, got {type(issues).__name__}"


def assert_analysis_results_structure(results: Mapping[str, Any]) -> None:
    """Assert that analysis results have expected structure."""
    assert isinstance(results, dict), f"Expected dict, got {type(results).__name__}"


def safe_dict_access(data: Mapping[str, Any], key: str, default: Any = None) -> Any:
    """Safely access a dict key with a default value."""
    return data.get(key, default)


def safe_list_access(data: Sequence[Any], index: int, default: Any = None) -> Any:
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
