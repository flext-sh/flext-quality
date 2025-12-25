"""Test helpers for flext-quality tests.

Provides reusable test utilities and helpers for all test modules.
Consolidates typings, constants, models, and protocols in unified classes.

Uses standardized short names (m, t, c, p) for easy access in tests.
Helpers extend main classes and use same short names in place of base classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .assertions import (
    assert_analysis_results_structure,
    assert_dict_structure,
    assert_is_dict,
    assert_is_list,
    assert_issues_structure,
    assert_metrics_structure,
    safe_dict_access,
    safe_list_access,
)
from .constants import TestsConstants, c
from .models import TestsModels, m
from .protocols import TestsProtocols, p
from .typings import TestsTypings, t

__all__ = [
    "TestsConstants",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "c",
    "m",
    "p",
    "safe_dict_access",
    "safe_list_access",
    "t",
]
