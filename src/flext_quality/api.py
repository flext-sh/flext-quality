"""Public API facade for flext-quality."""

from __future__ import annotations

from collections.abc import (
    Sequence,
)
from pathlib import Path
from typing import override

from flext_quality import (
    FlextQualityHookManager,
    FlextQualityRulesLoader,
    c,
    m,
    p,
    r,
    t,
    u,
)
from flext_quality._settings import FlextQualitySettings
from flext_quality.base import FlextQualityServiceBase


class FlextQuality(FlextQualityServiceBase):
    """Coordinate quality operations through the canonical facade instance."""

    _hooks: FlextQualityHookManager = u.PrivateAttr(
        default_factory=FlextQualityHookManager,
    )
    _rules_loader: FlextQualityRulesLoader = u.PrivateAttr(
        default_factory=FlextQualityRulesLoader,
    )

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute the default quality runtime operation."""
        return self.fetch_status()

    def execute_hook(
        self,
        event: str,
        input_data: t.JsonMapping,
    ) -> p.Result[t.JsonMapping]:
        """Execute hooks for an event.

        Args:
            event: Hook event name (e.g., "PreToolUse")
            input_data: Hook input data

        Returns:
            r[t.JsonMapping]: Hook execution result or error

        """
        return self._hooks.execute(event, input_data)

    def format_hook_output(
        self,
        *,
        continue_exec: bool = True,
        message: str | None = None,
        blocked_reason: str | None = None,
    ) -> p.Result[str]:
        """Format hook output for Claude Code as JSON string."""
        return r[str].ok(
            u.Quality.format_hook_output(
                continue_exec=continue_exec,
                message=message,
                blocked_reason=blocked_reason,
            ),
        )

    def fetch_hook_config_json(self) -> p.Result[str]:
        """Return hooks configuration as JSON string."""
        return r[str].ok(self._hooks.fetch_config_json())

    def fetch_status(self) -> p.Result[t.JsonMapping]:
        """Return quality service status snapshot."""
        settings = FlextQualitySettings.fetch_global()
        return r[t.JsonMapping].ok({
            "name": c.Quality.MCP_SERVER_NAME,
            "version": c.Quality.MCP_SERVER_VERSION,
            "settings": {
                "hook_timeout_ms": settings.Quality.hook_timeout_ms,
                "rule_timeout_seconds": settings.Quality.rule_timeout_seconds,
                "cache_enabled": settings.Quality.cache_enabled,
                "mcp_server_port": settings.Quality.mcp_server_port,
            },
            "hooks_registered": len(self._hooks.fetch_config()),
        })

    def load_rules(self, path: Path) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from a YAML file.

        Args:
            path: Path to rules YAML file

        Returns:
            r[Sequence[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        return self._rules_loader.load(path)

    def load_rules_from_config(self) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from configured rules directory.

        Returns:
            r[Sequence[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        settings = FlextQualitySettings.fetch_global()
        rules_path = Path(settings.Quality.rules_dir)
        if not rules_path.exists():
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Rules directory not found: {rules_path}",
            )
        yaml_files = list(rules_path.glob("*.yaml")) + list(rules_path.glob("*.yml"))
        if not yaml_files:
            return r[Sequence[m.Quality.RuleDefinition]].ok([])
        return self._rules_loader.load_multiple(yaml_files)

    def process_stdin_hook(self) -> p.Result[t.JsonMapping]:
        """Process hook input from stdin (for Claude Code hooks).

        Returns:
            r[t.JsonMapping]: Hook execution result or error

        """
        stdin_result = u.Quality.read_stdin()
        if stdin_result.failure:
            return r[t.JsonMapping].fail(
                stdin_result.error or "Failed to read stdin",
            )
        parse_result = u.Quality.parse_hook_input(stdin_result.value)
        if parse_result.failure:
            return r[t.JsonMapping].fail(
                parse_result.error or "Failed to parse input",
            )
        input_data = parse_result.value
        event = str(input_data.get("event", ""))
        if not event:
            return r[t.JsonMapping].ok({"continue": True})
        return self.execute_hook(event, input_data)

    def validate_configuration(self) -> p.Result[bool]:
        """Validate the current configuration.

        Threshold invariants are enforced at settings construction time, so a
        constructed settings instance is always valid.

        Returns:
            r[bool]: Success or validation error

        """
        return r[bool].ok(value=True)


quality: FlextQuality = FlextQuality.fetch_global()
"""Shared FlextQuality facade instance."""

__all__: list[str] = ["FlextQuality", "quality"]
