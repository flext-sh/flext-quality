"""Shared documentation maintenance orchestrator facade."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any

from .profiles import PROFILE_ALIASES

DEFAULT_PROFILE = "advanced"


def _resolve_profile_module(profile: str) -> str:
    """Return the fully-qualified module path for a profile."""
    return PROFILE_ALIASES.get(profile, profile)


def _load_profile_callable(profile: str, attribute: str) -> Callable[..., Any]:
    """Load a callable attribute from the selected profile module."""
    module_path = _resolve_profile_module(profile)
    module = import_module(f"{module_path}.{attribute}")
    if not hasattr(module, "main"):
        msg = (
            f"Profile module '{module_path}.{attribute}' is missing a 'main' entrypoint"
        )
        raise RuntimeError(msg)
    return getattr(module, "main")


@dataclass
class DocumentationMaintenanceOrchestrator:
    """Facade delegating maintenance operations to a selected profile."""

    profile: str | None = None

    def __post_init__(self) -> None:
        if not self.profile:
            self.profile = os.getenv("FLEXT_DOC_PROFILE", DEFAULT_PROFILE)

    def run(self, command: str, **kwargs: Any) -> Any:
        """Dispatch a maintenance command to the selected profile handler."""
        module_candidates: dict[str, tuple[str, ...]] = {
            "comprehensive": ("maintain",),
            "audit": ("audit", "maintain"),
            "optimize": ("optimize", "optimization"),
            "report": ("report", "reporting"),
            "sync": ("sync", "synchronization"),
            "validate_links": ("validate_links", "validation"),
            "validate_style": ("validate_style", "validation"),
        }

        try:
            candidates = module_candidates[command]
        except KeyError as exc:
            msg = f"Unsupported maintenance command '{command}'"
            raise ValueError(msg) from exc

        last_error: Exception | None = None
        profile = self.profile or DEFAULT_PROFILE
        for module_name in candidates:
            try:
                handler = _load_profile_callable(profile, module_name)
                return handler(**kwargs)
            except ModuleNotFoundError as exc:
                last_error = exc
                continue
        if last_error:
            msg = f"Profile '{profile}' does not implement command '{command}'"
            raise RuntimeError(msg) from last_error
        msg = f"Unable to execute command '{command}' for profile '{profile}'"
        raise RuntimeError(msg)


def run_operation(profile: str, command: str, **kwargs: Any) -> Any:
    """Convenience helper to run a maintenance command for a profile."""
    orchestrator = DocumentationMaintenanceOrchestrator(profile=profile)
    return orchestrator.run(command, **kwargs)
