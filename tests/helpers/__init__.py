"""Test helpers for flext-quality tests.

Provides reusable test utilities and helpers for all test modules.
Consolidates typings, constants, models, and protocols in unified classes.

Uses standardized short names (m, t, c, p) for easy access in tests.
Helpers extend main classes and use same short names in place of base classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from assertions import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        safe_dict_access,
        safe_list_access,
    )
    from constants import TestsConstants, TestsConstants as c
    from models import TestsModels, TestsModels as m
    from protocols import TestsProtocols, TestsProtocols as p
    from typings import TestsTypings, t

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestsConstants": ("constants", "TestsConstants"),
    "TestsModels": ("models", "TestsModels"),
    "TestsProtocols": ("protocols", "TestsProtocols"),
    "TestsTypings": ("typings", "TestsTypings"),
    "assert_analysis_results_structure": (
        "assertions",
        "assert_analysis_results_structure",
    ),
    "assert_dict_structure": ("assertions", "assert_dict_structure"),
    "assert_is_dict": ("assertions", "assert_is_dict"),
    "assert_is_list": ("assertions", "assert_is_list"),
    "assert_issues_structure": ("assertions", "assert_issues_structure"),
    "assert_metrics_structure": ("assertions", "assert_metrics_structure"),
    "c": ("constants", "TestsConstants"),
    "m": ("models", "TestsModels"),
    "p": ("protocols", "TestsProtocols"),
    "safe_dict_access": ("assertions", "safe_dict_access"),
    "safe_list_access": ("assertions", "safe_list_access"),
    "t": ("typings", "t"),
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
    "m",
    "p",
    "safe_dict_access",
    "safe_list_access",
    "t",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
