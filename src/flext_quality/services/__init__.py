# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Services - Business logic layer (Tier 3)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality.services.cli import (
        FlextQualityCliService,
        FlextQualityCliService as s,
        main,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextQualityCliService": ("flext_quality.services.cli", "FlextQualityCliService"),
    "main": ("flext_quality.services.cli", "main"),
    "s": ("flext_quality.services.cli", "FlextQualityCliService"),
}

__all__ = [
    "FlextQualityCliService",
    "main",
    "s",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
