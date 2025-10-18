"""DRY typing helpers for tests.

This module provides reusable type-safe helpers to eliminate duplicate code
across test files while maintaining strict MyPy compliance.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeGuard, cast


def assert_is_dict(value: object) -> TypeGuard[dict[str, object]]:
    """Type-safe dict[str, object] assertion following Single Responsibility Principle.

    Args:
      value: Object to check

    Returns:
      TypeGuard confirming value is a dict

    Raises:
      AssertionError: If value is not a dict

    """
    assert isinstance(value, dict), f"Expected dict, got {type(value)}"
    return True


def assert_is_list(value: object) -> TypeGuard[list[object]]:
    """Type-safe list assertion following Single Responsibility Principle.

    Args:
      value: Object to check

    Returns:
      TypeGuard confirming value is a list

    Raises:
      AssertionError: If value is not a list

    """
    assert isinstance(value, list), f"Expected list, got {type(value)}"
    return True


def safe_dict_access(data: dict[str, object], key: str) -> object:
    """Type-safe dictionary access with proper error handling.

    Args:
      data: Object to access (must be a dict)
      key: Key to access

    Returns:
      Value from dict

    Raises:
      AssertionError: If data is not a dict[str, object] or key missing

    """
    assert key in data, f"Key '{key}' not found in dict"
    return data[key]


def safe_list_access(data: list[object], index: int) -> object:
    """Type-safe list access with proper error handling.

    Args:
      data: Object to access (must be a list)
      index: Index to access

    Returns:
      Value from list

    Raises:
      AssertionError: If data is not a list or index out of bounds

    """
    assert_is_list(data)
    assert 0 <= index < len(data), (
        f"Index {index} out of bounds for list of length {len(data)}"
    )
    return data[index]


def assert_dict_structure(
    data: dict[str, object],
    required_keys: list[str],
) -> dict[str, object]:
    """Assert that object is dict[str, object] with required keys - DRY pattern.

    Args:
      data: Object to check
      required_keys: Keys that must be present

    Returns:
      The validated dict

    Raises:
      AssertionError: If validation fails

    """
    for key in required_keys:
        assert key in data, f"Required key '{key}' missing from dict"
    return data


def assert_analysis_results_structure(results: object) -> dict[str, object]:
    """Assert analyzer results have expected structure - specialized helper.

    Args:
      results: Analyzer results to validate

    Returns:
      Validated results dict

    Raises:
      AssertionError: If structure is invalid

    """
    assert_is_dict(results)
    return assert_dict_structure(
        cast("dict[str, object]", results),
        ["metrics", "issues", "python_files"],
    )


def assert_metrics_structure(metrics: object) -> dict[str, object]:
    """Assert metrics have expected structure - specialized helper.

    Args:
      metrics: Metrics to validate

    Returns:
      Validated metrics dict

    Raises:
      AssertionError: If structure is invalid

    """
    assert_is_dict(metrics)
    return assert_dict_structure(
        cast("dict[str, object]", metrics),
        ["total_files", "total_lines_of_code"],
    )


def assert_issues_structure(issues: object) -> dict[str, object]:
    """Assert issues have expected structure - specialized helper.

    Args:
      issues: Issues to validate

    Returns:
      Validated issues dict

    Raises:
      AssertionError: If structure is invalid

    """
    assert_is_dict(issues)
    return assert_dict_structure(
        cast("dict[str, object]", issues),
        ["security", "complexity", "dead_code", "duplicates"],
    )
