"""Hook lifecycle manager."""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import final

from flext_quality import FlextQualityBaseHook, c, p, r, t


@final
class FlextQualityHookManager:
    """Manages hook lifecycle and execution."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize hook manager with optional settings path."""
        self._hooks: MutableMapping[
            c.Quality.HookEvent,
            MutableSequence[FlextQualityBaseHook],
        ] = {}
        self._config_path = config_path

    def execute(
        self,
        event: str,
        input_data: t.Quality.HookInput,
    ) -> p.Result[t.Quality.HookOutput]:
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
            if result.failure:
                return result
            output = result.value
            if not output.get("continue", True):
                return result
        return r[t.Quality.HookOutput].ok({"continue": True})

    def get_config(self) -> t.JsonMapping:
        """Get hooks configuration as dict."""
        config: dict[str, t.JsonValue] = {}
        for event, hooks in self._hooks.items():
            hook_entries: list[t.JsonValue] = []
            for hook in hooks:
                matcher = hook.matcher
                matcher_value: t.JsonValue
                if isinstance(matcher, Sequence) and not isinstance(matcher, str):
                    matcher_value = [str(item) for item in matcher]
                else:
                    matcher_value = matcher
                hook_entries.append({"matcher": matcher_value})
            config[event.value] = hook_entries
        return config

    def get_config_json(self) -> str:
        """Get hooks configuration as JSON."""
        return str(
            t.CONTAINER_MAPPING_ADAPTER.dump_json(
                dict(self.get_config()),
                indent=c.Quality.Defaults.JSON_INDENT,
            ).decode("utf-8")
        )

    def register(self, hook: FlextQualityBaseHook) -> p.Result[bool]:
        """Register a hook."""
        event = hook.event
        if event not in self._hooks:
            self._hooks[event] = list[FlextQualityBaseHook]()
        self._hooks[event].append(hook)
        return r[bool].ok(value=True)
