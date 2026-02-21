"""DRY typing helpers for tests.

This module provides reusable type-safe helpers to eliminate duplicate code
across test files while maintaining strict MyPy compliance.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeGuard

from flext_core import t


def assert_is_dict(value: object) -> TypeGuard[dict[str, t.GeneralValueType]]:
    """Type-safe dict[str, t.GeneralValueType] assertion following Single Responsibility Principle.

    Args:
      value: Object to check

    Returns:
      TypeGuard confirming value is a dict

    Raises:
      AssertionError: If value is not a dict

    """
    assert isinstance(value, dict), f"Expected dict, got {type(value)}"
    return True


def assert_is_list(value: object) -> TypeGuard[list[t.GeneralValueType]]:
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


def safe_dict_access(
    data: dict[str, t.GeneralValueType], key: str
) -> t.GeneralValueType:
    """Type-safe dictionary access with proper error handling.

    Args:
      data: Object to access (must be a dict)
      key: Key to access

    Returns:
      Value from dict

    Raises:
      AssertionError: If data is not a dict[str, t.GeneralValueType] or key missing

    """
    assert key in data, f"Key '{key}' not found in dict"
    return data[key]


def safe_list_access(data: list[t.GeneralValueType], index: int) -> t.GeneralValueType:
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
    data: dict[str, t.GeneralValueType],
    required_keys: list[str],
) -> dict[str, t.GeneralValueType]:
    """Assert that object is dict[str, t.GeneralValueType] with required keys - DRY pattern.

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


def assert_analysis_results_structure(results: object) -> dict[str, t.GeneralValueType]:
    """Assert analyzer results have expected structure - specialized helper.

    Args:
      results: Analyzer results to validate

    Returns:
      Validated results dict

    Raises:
      AssertionError: If structure is invalid

    """
    # Type narrowing via TypeGuard - assert_is_dict confirms results is dict
    if not assert_is_dict(results):
        raise AssertionError(f"Expected dict, got {type(results)}")
    # Type narrowing: results is now dict[str, t.GeneralValueType] after TypeGuard
    return assert_dict_structure(
        results,
        ["metrics", "issues", "python_files"],
    )


def assert_metrics_structure(metrics: object) -> dict[str, t.GeneralValueType]:
    """Assert metrics have expected structure - specialized helper.

    Args:
      metrics: Metrics to validate

    Returns:
      Validated metrics dict

    Raises:
      AssertionError: If structure is invalid

    """
    # Type narrowing via TypeGuard - assert_is_dict confirms metrics is dict
    if not assert_is_dict(metrics):
        raise AssertionError(f"Expected dict, got {type(metrics)}")
    # Type narrowing: metrics is now dict[str, t.GeneralValueType] after TypeGuard
    return assert_dict_structure(
        metrics,
        ["total_files", "total_lines_of_code"],
    )


def assert_issues_structure(issues: object) -> dict[str, t.GeneralValueType]:
    """Assert issues have expected structure - specialized helper.

    Args:
      issues: Issues to validate

    Returns:
      Validated issues dict

    Raises:
      AssertionError: If structure is invalid

    """
    # Type narrowing via TypeGuard - assert_is_dict confirms issues is dict
    if not assert_is_dict(issues):
        raise AssertionError(f"Expected dict, got {type(issues)}")
    # Type narrowing: issues is now dict[str, t.GeneralValueType] after TypeGuard
    return assert_dict_structure(
        issues,
        ["security", "complexity", "dead_code", "duplicates"],
    )
