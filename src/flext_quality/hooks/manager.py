"""Hook lifecycle manager.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import MutableMapping, MutableSequence, Sequence
from typing import TYPE_CHECKING, final

from flext_quality import c, p, r, t, u
from flext_quality.hooks import FlextQualityBaseHook

if TYPE_CHECKING:
    from pathlib import Path


@final
class FlextQualityHookManager:
    """Manages hook lifecycle and execution."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize hook manager with optional settings path.

        Args:
            config_path: Optional path to the hooks configuration file.

        """
        self._hooks: MutableMapping[
            c.Quality.HookEvent,
            MutableSequence[FlextQualityBaseHook],
        ] = {}
        self._config_path = config_path

    def execute(self, event: str, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        """Execute all hooks registered for an event.

        Args:
            event: Hook event name (a ``c.Quality.HookEvent`` value).
            input_data: Hook input payload forwarded to each hook.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        try:
            hook_event = c.Quality.HookEvent(event)
        except ValueError:
            return r[t.JsonMapping].fail(f"Unknown event: {event}")
        hooks = self._hooks.get(hook_event, [])
        for hook in hooks:
            if not hook.should_run(input_data):
                continue
            result = hook.execute(input_data)
            if result.failure:
                return result
            output = result.value
            if not output.get("continue", True):
                return result
        return r[t.JsonMapping].ok({"continue": True})

    def fetch_config(self) -> t.JsonMapping:
        """Return the hooks configuration as a mapping.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        config: t.JsonDict = {}
        for event, hooks in self._hooks.items():
            hook_entries: t.JsonValueList = []
            for hook in hooks:
                matcher = hook.matcher
                matcher_value: t.JsonValue
                if isinstance(matcher, Sequence) and not isinstance(matcher, str):
                    matcher_value = u.normalize_to_json_value(list(matcher))
                else:
                    matcher_value = matcher
                hook_entries.append({"matcher": matcher_value})
            config[event.value] = hook_entries
        return config

    def fetch_config_json(self) -> str:
        """Return the hooks configuration as a JSON string.

        Returns:
            The resulting ``str``.

        """
        config_json: str = (
            u
            .json_mapping_adapter()
            .dump_json(dict(self.fetch_config()), indent=c.Quality.JSON_INDENT)
            .decode("utf-8")
        )
        return config_json

    def register(self, hook: FlextQualityBaseHook) -> p.Result[bool]:
        """Register a hook for its event.

        Args:
            hook: Hook instance registered under its ``event``.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        event = hook.event
        if event not in self._hooks:
            self._hooks[event] = list[FlextQualityBaseHook]()
        self._hooks[event].append(hook)
        return r[bool].ok(value=True)


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityHookManager"]
