# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit tests for flext-quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from .test_api import (
        TestFlextQualityAPI,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
    )
    from .test_basic import test_basic
    from .test_cli import (
        TestFlextQualityCliService,
        TestFlextQualityCliService as s,
        TestMainFunction,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextQualityAPI": ("tests.unit.test_api", "TestFlextQualityAPI"),
    "TestFlextQualityCliService": ("tests.unit.test_cli", "TestFlextQualityCliService"),
    "TestFlextQualityHookExecution": (
        "tests.unit.test_api",
        "TestFlextQualityHookExecution",
    ),
    "TestFlextQualityRulesConfig": (
        "tests.unit.test_api",
        "TestFlextQualityRulesConfig",
    ),
    "TestFlextQualitySingleton": ("tests.unit.test_api", "TestFlextQualitySingleton"),
    "TestFlextQualityStdinProcessing": (
        "tests.unit.test_api",
        "TestFlextQualityStdinProcessing",
    ),
    "TestFlextQualityValidation": ("tests.unit.test_api", "TestFlextQualityValidation"),
    "TestMainFunction": ("tests.unit.test_cli", "TestMainFunction"),
    "s": ("tests.unit.test_cli", "TestFlextQualityCliService"),
    "test_basic": ("tests.unit.test_basic", "test_basic"),
}

__all__ = [
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "s",
    "test_basic",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
