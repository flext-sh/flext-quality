# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Test helpers for flext-quality tests.

Provides reusable test utilities and helpers for all test modules.
Consolidates typings, constants, models, and protocols in unified classes.

Uses standardized short names (m, t, c, p) for easy access in tests.
Helpers extend main classes and use same short names in place of base classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality import d as d, e as e, h as h, r as r, s as s, u as u, x as x
    from tests.helpers import (
        assertions as assertions,
        constants as constants,
        models as models,
        protocols as protocols,
        typing_helpers as typing_helpers,
        typings as typings,
    )
    from tests.helpers.constants import TestsConstants as TestsConstants, c as c
    from tests.helpers.models import TestsModels as TestsModels, m as m
    from tests.helpers.protocols import TestsProtocols as TestsProtocols, p as p
    from tests.helpers.typing_helpers import (
        assert_analysis_results_structure as assert_analysis_results_structure,
        assert_dict_structure as assert_dict_structure,
        assert_is_dict as assert_is_dict,
        assert_is_list as assert_is_list,
        assert_issues_structure as assert_issues_structure,
        assert_metrics_structure as assert_metrics_structure,
        safe_dict_access as safe_dict_access,
        safe_list_access as safe_list_access,
    )
    from tests.helpers.typings import TestsTypings as TestsTypings, t as t

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestsConstants": ["tests.helpers.constants", "TestsConstants"],
    "TestsModels": ["tests.helpers.models", "TestsModels"],
    "TestsProtocols": ["tests.helpers.protocols", "TestsProtocols"],
    "TestsTypings": ["tests.helpers.typings", "TestsTypings"],
    "assert_analysis_results_structure": [
        "tests.helpers.typing_helpers",
        "assert_analysis_results_structure",
    ],
    "assert_dict_structure": ["tests.helpers.typing_helpers", "assert_dict_structure"],
    "assert_is_dict": ["tests.helpers.typing_helpers", "assert_is_dict"],
    "assert_is_list": ["tests.helpers.typing_helpers", "assert_is_list"],
    "assert_issues_structure": [
        "tests.helpers.typing_helpers",
        "assert_issues_structure",
    ],
    "assert_metrics_structure": [
        "tests.helpers.typing_helpers",
        "assert_metrics_structure",
    ],
    "assertions": ["tests.helpers.assertions", ""],
    "c": ["tests.helpers.constants", "c"],
    "constants": ["tests.helpers.constants", ""],
    "d": ["flext_quality", "d"],
    "e": ["flext_quality", "e"],
    "h": ["flext_quality", "h"],
    "m": ["tests.helpers.models", "m"],
    "models": ["tests.helpers.models", ""],
    "p": ["tests.helpers.protocols", "p"],
    "protocols": ["tests.helpers.protocols", ""],
    "r": ["flext_quality", "r"],
    "s": ["flext_quality", "s"],
    "safe_dict_access": ["tests.helpers.typing_helpers", "safe_dict_access"],
    "safe_list_access": ["tests.helpers.typing_helpers", "safe_list_access"],
    "t": ["tests.helpers.typings", "t"],
    "typing_helpers": ["tests.helpers.typing_helpers", ""],
    "typings": ["tests.helpers.typings", ""],
    "u": ["flext_quality", "u"],
    "x": ["flext_quality", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "assertions",
    "c",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "safe_dict_access",
    "safe_list_access",
    "t",
    "typing_helpers",
    "typings",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
