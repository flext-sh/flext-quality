"""Shared documentation maintenance orchestrator facade."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from inspect import Parameter, signature
from typing import Any

from .profiles import PROFILE_ALIASES

DEFAULT_PROFILE = "advanced"


def _resolve_profile_module(profile: str) -> str:
    """Return the fully-qualified module path for a profile."""
    return PROFILE_ALIASES.get(profile, profile)


def _load_profile_handler(
    profile: str, module_name: str, attributes: tuple[str, ...]
) -> Callable[..., Any]:
    """Load the first available callable for a maintenance command."""
    module_path = _resolve_profile_module(profile)
    module = import_module(f"{module_path}.{module_name}")

    for attribute in attributes:
        handler = getattr(module, attribute, None)
        if callable(handler):
            return handler

    msg = (
        "Profile module '{module}.{name}' is missing required callable(s): "
        + ", ".join(attributes)
    ).format(module=module_path, name=module_name)
    raise RuntimeError(msg)


@dataclass
class DocumentationMaintenanceOrchestrator:
    """Facade delegating maintenance operations to a selected profile."""

    profile: str | None = None

    def __post_init__(self) -> None:
        """Initialize profile after dataclass creation."""
        if not self.profile:
            self.profile = os.getenv("FLEXT_DOC_PROFILE", DEFAULT_PROFILE)

    def run(self, command: str, **kwargs: object) -> object:
        """Dispatch a maintenance command to the selected profile handler."""
        module_candidates: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
            "comprehensive": (("maintain", ("run_comprehensive", "main")),),
            "audit": (
                ("audit", ("run_audit", "main")),
                ("maintain", ("run_audit", "run_comprehensive", "main")),
            ),
            "optimize": (
                ("optimize", ("run_optimization", "main")),
                ("maintain", ("run_optimization", "run_comprehensive", "main")),
            ),
            "report": (
                ("report", ("run_report", "main")),
                ("reporting", ("run_report", "main")),
            ),
            "sync": (
                ("sync", ("run_sync", "main")),
                ("synchronization", ("run_sync", "main")),
            ),
            "validate_links": (
                ("validate_links", ("run_link_validation", "main")),
                ("validation", ("run_link_validation", "main")),
            ),
            "validate_style": (
                ("validate_style", ("run_style_validation", "main")),
                ("validation", ("run_style_validation", "main")),
            ),
        }

        try:
            candidates = module_candidates[command]
        except KeyError as exc:
            msg = f"Unsupported maintenance command '{command}'"
            raise ValueError(msg) from exc

        last_error: Exception | None = None
        profile = self.profile or DEFAULT_PROFILE
        for module_name, attributes in candidates:
            try:
                handler = _load_profile_handler(profile, module_name, attributes)
                sig = signature(handler)
                if any(
                    parameter.kind == Parameter.VAR_KEYWORD
                    for parameter in sig.parameters.values()
                ):
                    filtered_kwargs = kwargs
                else:
                    filtered_kwargs = {
                        key: value
                        for key, value in kwargs.items()
                        if key in sig.parameters
                    }
                return handler(**filtered_kwargs)
            except (ModuleNotFoundError, RuntimeError) as exc:
                last_error = exc
                continue
        if last_error:
            msg = f"Profile '{profile}' does not implement command '{command}'"
            raise RuntimeError(msg) from last_error
        msg = f"Unable to execute command '{command}' for profile '{profile}'"
        raise RuntimeError(msg)


def run_operation(profile: str, command: str, **kwargs: object) -> object:
    """Convenience helper to run a maintenance command for a profile."""
    orchestrator = DocumentationMaintenanceOrchestrator(profile=profile)
    return orchestrator.run(command, **kwargs)
