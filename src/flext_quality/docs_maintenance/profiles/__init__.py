"""Documentation maintenance profile registry."""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import Any

PROFILE_ALIASES: dict[str, str] = {
    "advanced": "flext_quality.docs_maintenance.profiles.advanced",
    "grpc": "flext_quality.docs_maintenance.profiles.grpc",
    "default": "flext_quality.docs_maintenance.profiles.advanced",
}


def get_profile_module(profile: str) -> Any:
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
