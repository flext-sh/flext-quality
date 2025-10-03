"""Test helpers package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_core import FlextTypes

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

__all__: FlextTypes.StringList = [
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "safe_dict_access",
    "safe_list_access",
]
