"""Hook lifecycle manager."""

from __future__ import annotations

from typing import override

import json
from collections.abc import Mapping
from pathlib import Path
from typing import final

from flext_core import r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.hooks.base import BaseHookImpl
from flext_quality.typings import HookInput, HookOutput


@final
class HookManager:
    """Manages hook lifecycle and execution."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize hook manager with optional config path."""
        self._hooks: dict[c.Quality.HookEvent, list[BaseHookImpl]] = {}
        self._config_path = config_path

    def register(self, hook: BaseHookImpl) -> r[bool]:
        """Register a hook."""
        event = hook.event
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(hook)
        return r[bool].ok(value=True)

    def execute(self, event: str, input_data: HookInput) -> r[HookOutput]:
        """Execute all hooks for an event."""
        try:
            hook_event = c.Quality.HookEvent(event)
        except ValueError:
            return r[HookOutput].fail(f"Unknown event: {event}")

        hooks = self._hooks.get(hook_event, [])

        for hook in hooks:
            if not hook.should_run(input_data):
                continue

            result = hook.execute(input_data)
            if result.is_failure:
                return result

            output = result.value
            if not output.get("continue", True):
                return result

        return r[HookOutput].ok({"continue": True})

    def get_config(self) -> Mapping[str, list[Mapping[str, object]]]:
        """Get hooks configuration as dict."""
        return {
            event.value: [{"matcher": h.matcher} for h in hooks]
            for event, hooks in self._hooks.items()
        }

    def get_config_json(self) -> str:
        """Get hooks configuration as JSON."""
        return json.dumps(self.get_config(), indent=2)
