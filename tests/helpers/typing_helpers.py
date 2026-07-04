"""DRY typing helpers for tests.

This module provides reusable type-safe helpers to eliminate duplicate code
across test files while maintaining strict MyPy compliance.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeIs

if TYPE_CHECKING:
    from tests.typings import t


def assert_is_dict(
    value: t.Scalar | t.ScalarMapping,
) -> TypeIs[t.ScalarMapping]:
    """Type-safe t.JsonMapping assertion following Single Responsibility Principle.

    Args:
      value: Object to check

    Returns:
      TypeGuard confirming value is a dict

    Raises:
      AssertionError: If value is not a dict

    """
    assert isinstance(value, dict), f"Expected dict, got {type(value)}"
    return True


def assert_is_list(value: t.Scalar | t.ScalarList) -> TypeIs[t.ScalarList]:
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


def assert_dict_structure(
    data: t.ScalarMapping,
    required_keys: t.StrSequence,
) -> t.ScalarMapping:
    """Assert that t.JsonValue is dict with required keys - DRY pattern.

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


def assert_analysis_results_structure(
    results: t.ScalarMapping,
) -> t.ScalarMapping:
    """Assert analyzer results have expected structure - specialized helper.

    Args:
      results: Analyzer results to validate

    Returns:
      Validated results dict

    Raises:
      AssertionError: If structure is invalid

    """
    if not assert_is_dict(results):
        raise AssertionError(f"Expected dict, got {type(results)}")
    return assert_dict_structure(results, ["metrics", "issues", "python_files"])


def assert_metrics_structure(metrics: t.ScalarMapping) -> t.ScalarMapping:
    """Assert metrics have expected structure - specialized helper.

    Args:
      metrics: Metrics to validate

    Returns:
      Validated metrics dict

    Raises:
      AssertionError: If structure is invalid

    """
    if not assert_is_dict(metrics):
        raise AssertionError(f"Expected dict, got {type(metrics)}")
    return assert_dict_structure(metrics, ["total_files", "total_lines_of_code"])


def assert_issues_structure(issues: t.ScalarMapping) -> t.ScalarMapping:
    """Assert issues have expected structure - specialized helper.

    Args:
      issues: Issues to validate

    Returns:
      Validated issues dict

    Raises:
      AssertionError: If structure is invalid

    """
    if not assert_is_dict(issues):
        raise AssertionError(f"Expected dict, got {type(issues)}")
    return assert_dict_structure(
        issues,
        ["security", "complexity", "dead_code", "duplicates"],
    )
