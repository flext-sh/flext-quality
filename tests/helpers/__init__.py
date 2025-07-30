"""Test helpers package following SOLID principles."""

from .typing_helpers import (
    assert_analysis_results_structure,
    assert_dict_structure,
    assert_is_dict,
    assert_is_list,
    assert_issues_structure,
    assert_metrics_structure,
    safe_dict_access,
    safe_list_access,
)

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
