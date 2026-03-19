# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
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

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality.decorators import d
    from flext_quality.exceptions import e
    from flext_quality.handlers import h
    from flext_quality.mixins import x
    from flext_quality.result import r
    from flext_quality.service import s
    from flext_quality.utilities import u

    from .constants import TestsConstants, c
    from .models import TestsModels, m
    from .protocols import TestsProtocols, p
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
    from .typings import TestsTypings, t

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestsConstants": ("tests.helpers.constants", "TestsConstants"),
    "TestsModels": ("tests.helpers.models", "TestsModels"),
    "TestsProtocols": ("tests.helpers.protocols", "TestsProtocols"),
    "TestsTypings": ("tests.helpers.typings", "TestsTypings"),
    "assert_analysis_results_structure": (
        "tests.helpers.typing_helpers",
        "assert_analysis_results_structure",
    ),
    "assert_dict_structure": ("tests.helpers.typing_helpers", "assert_dict_structure"),
    "assert_is_dict": ("tests.helpers.typing_helpers", "assert_is_dict"),
    "assert_is_list": ("tests.helpers.typing_helpers", "assert_is_list"),
    "assert_issues_structure": (
        "tests.helpers.typing_helpers",
        "assert_issues_structure",
    ),
    "assert_metrics_structure": (
        "tests.helpers.typing_helpers",
        "assert_metrics_structure",
    ),
    "c": ("tests.helpers.constants", "c"),
    "d": ("flext_quality.decorators", "d"),
    "e": ("flext_quality.exceptions", "e"),
    "h": ("flext_quality.handlers", "h"),
    "m": ("tests.helpers.models", "m"),
    "p": ("tests.helpers.protocols", "p"),
    "r": ("flext_quality.result", "r"),
    "s": ("flext_quality.service", "s"),
    "safe_dict_access": ("tests.helpers.typing_helpers", "safe_dict_access"),
    "safe_list_access": ("tests.helpers.typing_helpers", "safe_list_access"),
    "t": ("tests.helpers.typings", "t"),
    "u": ("flext_quality.utilities", "u"),
    "x": ("flext_quality.mixins", "x"),
}

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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "safe_dict_access",
    "safe_list_access",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
