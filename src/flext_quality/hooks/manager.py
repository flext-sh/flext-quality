"""Hook lifecycle manager."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import final

from flext_core import r
from flext_quality import FlextQualityBaseHook, c, t


@final
class FlextQualityHookManager:
    """Manages hook lifecycle and execution."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize hook manager with optional config path."""
        self._hooks: MutableMapping[
            c.Quality.HookEvent,
            MutableSequence[FlextQualityBaseHook],
        ] = {}
        self._config_path = config_path

    def execute(
        self,
        event: str,
        input_data: t.Quality.HookInput,
    ) -> r[t.Quality.HookOutput]:
        """Execute all hooks for an event."""
        try:
            hook_event = c.Quality.HookEvent(event)
        except ValueError:
            return r[t.Quality.HookOutput].fail(f"Unknown event: {event}")
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
        return r[t.Quality.HookOutput].ok({"continue": True})

    def get_config(self) -> Mapping[str, Sequence[t.ContainerMapping]]:
        """Get hooks configuration as dict."""
        return {
            event.value: [{"matcher": h.matcher} for h in hooks]
            for event, hooks in self._hooks.items()
        }

    def get_config_json(self) -> str:
        """Get hooks configuration as JSON."""
        return t.CONTAINER_MAPPING_ADAPTER.dump_json(
            dict(self.get_config()),
            indent=c.Quality.Defaults.JSON_INDENT,
        ).decode("utf-8")

    def register(self, hook: FlextQualityBaseHook) -> r[bool]:
        """Register a hook."""
        event = hook.event
        if event not in self._hooks:
            self._hooks[event] = list[FlextQualityBaseHook]()
        self._hooks[event].append(hook)
        return r[bool].ok(value=True)
