"""Rules engine - YAML-based declarative rules system."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextQualityRulesEngine": ("flext_quality.rules.engine", "FlextQualityRulesEngine"),
    "FlextQualityRulesLoader": ("flext_quality.rules.loader", "FlextQualityRulesLoader"),
    "FlextQualityValidators": ("flext_quality.rules.validators", "FlextQualityValidators"),
}

__all__ = [
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
