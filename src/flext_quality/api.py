"""Public API facade for flext-quality.

Centralizes quality analysis, hook management, rule loading, and MCP
integration exposed as attributes of `FlextQuality`, maintaining
convenience wrappers that delegate to internal services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import ClassVar

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult as r,
)
from flext_core.protocols import p

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.hooks.manager import HookManager
from flext_quality.models import RuleDefinition
from flext_quality.rules.loader import FlextQualityRulesLoader
from flext_quality.settings import FlextQualitySettings
from flext_quality.typings import HookInput, HookOutput
from flext_quality.utilities import FlextQualityUtilities as u


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
    - Railway-Oriented Programming via FlextResult for composable errors
    - FlextSettings provides auto self.config and self.logger

    Usage:
        from flext_quality import FlextQuality

        quality = FlextQuality.get_instance()
        result = quality.load_rules(Path("rules.yaml"))
    """

    # Nested classes - FLEXT pattern with real inheritance
    class Settings(FlextQualitySettings):
        """Quality settings extending FlextQualitySettings via inheritance."""

    class RulesLoader(FlextQualityRulesLoader):
        """Rules loader extending FlextQualityRulesLoader via inheritance."""

    # Singleton management
    _instance: ClassVar[FlextQuality | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    # Private instance variables
    _name: str
    _version: str
    _container: FlextContainer

    # Public service instances (typed at class level for documentation)
    logger: p.Log.StructlogLogger
    config: FlextQualitySettings
    hooks: HookManager
    rules_loader: FlextQualityRulesLoader

    def __init__(self) -> None:
        """Initialize consolidated quality API with all functionality integrated."""
        self._name = c.Quality.Mcp.SERVER_NAME
        self._version = c.Quality.Mcp.SERVER_VERSION

        # Auto self.logger and self.config via FlextSettings pattern
        self.logger = FlextLogger.create_module_logger(__name__)
        self.config = FlextQualitySettings.get_instance()

        # Container registration (singleton via __new__)
        self._container = FlextContainer.get_global()
        if not self._container.has_service("flext_quality"):
            register_result = self._container.register(
                "flext_quality",
                "flext_quality",
            )
            if register_result.is_failure:
                self.logger.warning(
                    f"Failed to register quality service: {register_result.error}",
                )

        # Domain services
        self.hooks = HookManager()
        self.rules_loader = FlextQualityRulesLoader()

    @classmethod
    def get_instance(cls) -> FlextQuality:
        """Get singleton FlextQuality instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # pragma: no branch
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def _reset_instance(cls) -> None:
        """Reset singleton instance (for testing)."""
        cls._instance = None

    # =========================================================================
    # RULES OPERATIONS
    # =========================================================================

    def load_rules(self, path: Path) -> r[list[RuleDefinition]]:
        """Load rules from a YAML file.

        Args:
            path: Path to rules YAML file

        Returns:
            r[list[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        return self.rules_loader.load(path)

    def load_rules_from_config(self) -> r[list[RuleDefinition]]:
        """Load rules from configured rules directory.

        Returns:
            r[list[m.Quality.RuleDefinition]]: List of rule definitions or error

        """
        rules_path = self.config.get_rules_path()
        if not rules_path.exists():
            return r[list[RuleDefinition]].fail(
                f"Rules directory not found: {rules_path}"
            )

        yaml_files = list(rules_path.glob("*.yaml")) + list(rules_path.glob("*.yml"))
        if not yaml_files:
            return r[list[RuleDefinition]].ok([])

        return self.rules_loader.load_multiple(yaml_files)

    # =========================================================================
    # HOOK OPERATIONS
    # =========================================================================

    def execute_hook(
        self,
        event: str,
        input_data: HookInput,
    ) -> r[HookOutput]:
        """Execute hooks for an event.

        Args:
            event: Hook event name (e.g., "PreToolUse")
            input_data: Hook input data

        Returns:
            r[HookOutput]: Hook execution result or error

        """
        return self.hooks.execute(event, input_data)

    def process_stdin_hook(self) -> r[HookOutput]:
        """Process hook input from stdin (for Claude Code hooks).

        Returns:
            r[HookOutput]: Hook execution result or error

        """
        stdin_result = u.Quality.read_stdin()
        if stdin_result.is_failure:
            return r[HookOutput].fail(stdin_result.error or "Failed to read stdin")

        parse_result = u.Quality.parse_hook_input(stdin_result.value)
        if parse_result.is_failure:
            return r[HookOutput].fail(parse_result.error or "Failed to parse input")

        input_data = parse_result.value
        event = str(input_data.get("event", ""))
        if not event:
            return r[HookOutput].ok({"continue": True})

        return self.execute_hook(event, input_data)

    def get_hook_config_json(self) -> str:
        """Get hooks configuration as JSON string."""
        return self.hooks.get_config_json()

    # =========================================================================
    # UTILITY OPERATIONS
    # =========================================================================

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

    # =========================================================================
    # VALIDATION OPERATIONS
    # =========================================================================

    def validate_configuration(self) -> r[bool]:
        """Validate the current configuration.

        Returns:
            r[bool]: Success or validation error

        """
        threshold_result = self.config.validate_thresholds()
        if threshold_result.is_failure:
            return r[bool].fail(threshold_result.error or "Threshold validation failed")
        return r[bool].ok(value=True)

    def get_status(self) -> dict[str, object]:
        """Get quality service status.

        Returns:
            dict[str, object]: Status information

        """
        return {
            "name": self._name,
            "version": self._version,
            "config": {
                "hook_timeout_ms": self.config.hook_timeout_ms,
                "rule_timeout_seconds": self.config.rule_timeout_seconds,
                "cache_enabled": self.config.cache_enabled,
                "mcp_server_port": self.config.mcp_server_port,
            },
            "hooks_registered": len(self.hooks.get_config()),
        }


__all__ = ["FlextQuality"]
