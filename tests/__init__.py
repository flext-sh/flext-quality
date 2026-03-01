"""FLEXT Quality Tests - Test infrastructure and utilities.

Provides TestsFlextQuality classes extending FlextTests and FlextQuality for comprehensive testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from tests.constants import (
        TestsFlextQualityConstants,
        TestsFlextQualityConstants as c,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestsFlextQualityConstants": ("tests.constants", "TestsFlextQualityConstants"),
    "c": ("tests.constants", "TestsFlextQualityConstants"),
}

__all__ = [
    "TestsFlextQualityConstants",
    "c",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
