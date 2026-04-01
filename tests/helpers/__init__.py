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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality import d, e, h, r, s, u, x
    from tests.helpers import (
        assertions,
        constants,
        models,
        protocols,
        typing_helpers,
        typings,
    )
    from tests.helpers.constants import TestsConstants, c
    from tests.helpers.models import TestsModels, m
    from tests.helpers.protocols import TestsProtocols, p
    from tests.helpers.typing_helpers import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        safe_dict_access,
        safe_list_access,
    )
    from tests.helpers.typings import TestsTypings, t

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestsConstants": "tests.helpers.constants",
    "TestsModels": "tests.helpers.models",
    "TestsProtocols": "tests.helpers.protocols",
    "TestsTypings": "tests.helpers.typings",
    "assert_analysis_results_structure": "tests.helpers.typing_helpers",
    "assert_dict_structure": "tests.helpers.typing_helpers",
    "assert_is_dict": "tests.helpers.typing_helpers",
    "assert_is_list": "tests.helpers.typing_helpers",
    "assert_issues_structure": "tests.helpers.typing_helpers",
    "assert_metrics_structure": "tests.helpers.typing_helpers",
    "assertions": "tests.helpers.assertions",
    "c": "tests.helpers.constants",
    "constants": "tests.helpers.constants",
    "d": "flext_quality",
    "e": "flext_quality",
    "h": "flext_quality",
    "m": "tests.helpers.models",
    "models": "tests.helpers.models",
    "p": "tests.helpers.protocols",
    "protocols": "tests.helpers.protocols",
    "r": "flext_quality",
    "s": "flext_quality",
    "safe_dict_access": "tests.helpers.typing_helpers",
    "safe_list_access": "tests.helpers.typing_helpers",
    "t": "tests.helpers.typings",
    "typing_helpers": "tests.helpers.typing_helpers",
    "typings": "tests.helpers.typings",
    "u": "flext_quality",
    "x": "flext_quality",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
