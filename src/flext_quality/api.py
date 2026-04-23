"""Public API facade for flext-quality.

Centralizes quality analysis, hook management, rule loading, and MCP
integration exposed as attributes of `FlextQuality`, maintaining
convenience wrappers that delegate to internal services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from collections.abc import (
    Sequence,
)
from pathlib import Path
from typing import ClassVar

from flext_core import FlextContainer

from flext_quality import (
    FlextQualityHookManager,
    FlextQualityRulesLoader,
    FlextQualitySettings,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextQuality:
    """Coordinate quality operations and expose domain services.

    Business Rules:
    ───────────────
    1. Singleton pattern ensures single instance per process (thread-safe)
    2. Service instances MUST be initialized before use (lazy initialization)
    3. All operations MUST return r[T] for error handling
    4. Configuration is auto-loaded via FlextSettings pattern
    5. Hook and rule management centralized through this facade

    Architecture Implications:
    ───────────────────────────
    - Singleton pattern with thread-safe locking prevents race conditions
    - Service instances are created on-demand (lazy initialization)
    - Railway-Oriented Programming via r for composable errors
    - FlextSettings provides auto self.settings and self.logger

    Usage:
        from flext_quality import FlextQuality

        quality = FlextQuality.get_instance()
        result = quality.load_rules(Path("rules.yaml"))
    """

    class Settings(FlextQualitySettings):
        """Quality settings extending FlextQualitySettings via inheritance."""

    class RulesLoader(FlextQualityRulesLoader):
        """Rules loader extending FlextQualityRulesLoader via inheritance."""

    _instance: ClassVar[FlextQuality | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _name: str
    _version: str
    _container: p.Container
    logger: p.Logger
    settings: FlextQualitySettings
    hooks: FlextQualityHookManager
    rules_loader: FlextQualityRulesLoader

    def __init__(self) -> None:
        """Initialize consolidated quality API with all functionality integrated."""
        self._name = c.Quality.Mcp.SERVER_NAME
        self._version = c.Quality.Mcp.SERVER_VERSION
        self.logger = u.fetch_logger(__name__)
        self.settings = FlextQualitySettings.get_instance()
        self._container = FlextContainer.shared()
        if not self._container.has("flext_quality"):
            _ = self._container.bind("flext_quality", "flext_quality")
        self.hooks = FlextQualityHookManager()
        self.rules_loader = FlextQualityRulesLoader()

    @classmethod
    def _reset_instance(cls) -> None:
        """Reset singleton instance (for testing)."""
        cls._instance = None

    @classmethod
    def get_instance(cls) -> FlextQuality:
        """Get singleton FlextQuality instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def execute_hook(
        self,
        event: str,
        input_data: t.Quality.HookInput,
    ) -> p.Result[t.Quality.HookOutput]:
        """Execute hooks for an event.

        Args:
            event: Hook event name (e.g., "PreToolUse")
            input_data: Hook input data

        Returns:
            r[t.Quality.HookOutput]: Hook execution result or error

        """
        return self.hooks.execute(event, input_data)

    def format_hook_output(
        self,
        *,
        continue_exec: bool = True,
        message: str | None = None,
        blocked_reason: str | None = None,
    ) -> str:
        """Format hook output for Claude Code.

        Args:
            continue_exec: Whether to continue execution
            message: Optional system message
            blocked_reason: Optional reason for blocking

        Returns:
            str: JSON-formatted hook output

        """
        return u.Quality.format_hook_output(
            continue_exec=continue_exec,
            message=message,
            blocked_reason=blocked_reason,
        )

    def get_hook_config_json(self) -> str:
        """Get hooks configuration as JSON string."""
        return self.hooks.get_config_json()

    def get_status(self) -> t.JsonMapping:
        """Get quality service status.

        Returns:
            t.JsonMapping: Status information

        """
        return {
            "name": self._name,
            "version": self._version,
            "settings": {
                "hook_timeout_ms": self.settings.hook_timeout_ms,
                "rule_timeout_seconds": self.settings.rule_timeout_seconds,
                "cache_enabled": self.settings.cache_enabled,
                "mcp_server_port": self.settings.mcp_server_port,
            },
            "hooks_registered": len(self.hooks.get_config()),
        }

    def load_rules(self, path: Path) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from a YAML file.

        Args:
            path: Path to rules YAML file

        Returns:
            r[Sequence[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        return self.rules_loader.load(path)

    def load_rules_from_config(self) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from configured rules directory.

        Returns:
            r[Sequence[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        rules_path = self.settings.get_rules_path()
        if not rules_path.exists():
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Rules directory not found: {rules_path}",
            )
        yaml_files = list(rules_path.glob("*.yaml")) + list(rules_path.glob("*.yml"))
        if not yaml_files:
            return r[Sequence[m.Quality.RuleDefinition]].ok([])
        return self.rules_loader.load_multiple(yaml_files)

    def process_stdin_hook(self) -> p.Result[t.Quality.HookOutput]:
        """Process hook input from stdin (for Claude Code hooks).

        Returns:
            r[t.Quality.HookOutput]: Hook execution result or error

        """
        stdin_result = u.Quality.read_stdin()
        if stdin_result.failure:
            return r[t.Quality.HookOutput].fail(
                stdin_result.error or "Failed to read stdin",
            )
        parse_result = u.Quality.parse_hook_input(stdin_result.value)
        if parse_result.failure:
            return r[t.Quality.HookOutput].fail(
                parse_result.error or "Failed to parse input",
            )
        input_data = parse_result.value
        event = str(input_data.get("event", ""))
        if not event:
            return r[t.Quality.HookOutput].ok({"continue": True})
        return self.execute_hook(event, input_data)

    def validate_configuration(self) -> p.Result[bool]:
        """Validate the current configuration.

        Returns:
            r[bool]: Success or validation error

        """
        threshold_result = self.settings.validate_thresholds()
        if threshold_result.failure:
            return r[bool].fail(threshold_result.error or "Threshold validation failed")
        return r[bool].ok(value=True)


quality = FlextQuality()

__all__: list[str] = ["FlextQuality", "quality"]
