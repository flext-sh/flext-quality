"""Documentation maintenance profile registry."""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from types import ModuleType

_ADVANCED_MODULE = "flext_quality.docs_maintenance.profiles.advanced"

PROFILE_ALIASES: dict[str, str] = {
    "advanced": _ADVANCED_MODULE,
    "default": _ADVANCED_MODULE,
    "grpc": _ADVANCED_MODULE,  # Backward compatibility for legacy envs
}


def get_profile_module(profile: str) -> ModuleType:
    """Return the module implementing a maintenance profile."""
    module_path = PROFILE_ALIASES.get(profile, profile)
    return import_module(module_path)


def get_profile_callable(profile: str, attribute: str) -> Callable[..., Any]:
    """Return a callable attribute from a profile module."""
    module = get_profile_module(profile)
    try:
        return getattr(module, attribute)
    except AttributeError as exc:
        msg = f"Profile '{profile}' does not provide callable '{attribute}'"
        raise RuntimeError(msg) from exc


__all__ = ["PROFILE_ALIASES", "get_profile_callable", "get_profile_module"]
