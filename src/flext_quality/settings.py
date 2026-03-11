"""FlextQualitySettings - Configuration for flext-quality.

Extends FlextSettings with quality-specific configuration for hooks,
rules, MCP integration, and quality thresholds.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextSettings, r
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class FlextQualitySettings(FlextSettings):
    """Runtime configuration for flext-quality services."""

    model_config = SettingsConfigDict(extra="ignore")

    hook_timeout_ms: int = Field(default=5000, ge=100, le=60000)
    rule_timeout_seconds: int = Field(default=30, ge=1, le=3600)
    cache_enabled: bool = Field(default=True)
    mcp_server_port: int = Field(default=8765, ge=1, le=65535)
    rules_dir: str = Field(default="rules")

    @classmethod
    def get_instance(cls) -> FlextQualitySettings:
        """Create settings instance from current environment."""
        return cls()

    def get_rules_path(self) -> Path:
        """Resolve configured rules directory path."""
        return Path(self.rules_dir)

    def validate_thresholds(self) -> r[bool]:
        """Validate numeric thresholds and feature toggles."""
        return r[bool].ok(True)


__all__ = ["FlextQualitySettings"]
