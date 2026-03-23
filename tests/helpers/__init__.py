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
    from flext_core import FlextTypes

    from flext_quality import c, d, e, h, m, p, r, s, t, u, x
    from tests.helpers.constants import TestsConstants
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
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
    from tests.helpers.typings import TestsTypings

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
    "c": ("flext_quality", "c"),
    "d": ("flext_quality", "d"),
    "e": ("flext_quality", "e"),
    "h": ("flext_quality", "h"),
    "m": ("flext_quality", "m"),
    "p": ("flext_quality", "p"),
    "r": ("flext_quality", "r"),
    "s": ("flext_quality", "s"),
    "safe_dict_access": ("tests.helpers.typing_helpers", "safe_dict_access"),
    "safe_list_access": ("tests.helpers.typing_helpers", "safe_list_access"),
    "t": ("flext_quality", "t"),
    "u": ("flext_quality", "u"),
    "x": ("flext_quality", "x"),
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


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
