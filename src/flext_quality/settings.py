"""FlextQualitySettings - Configuration for flext-quality.

Extends FlextSettings with quality-specific configuration for hooks,
rules, MCP integration, and quality thresholds.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, r
from flext_quality import c


@FlextSettings.auto_register("quality")
class FlextQualitySettings(FlextSettings):
    """Runtime configuration for flext-quality services."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_", extra="ignore"
    )

    hook_timeout_ms: Annotated[
        int, Field(default=c.Quality.Defaults.HOOK_TIMEOUT_MS, ge=100, le=60000)
    ]
    rule_timeout_seconds: Annotated[
        int, Field(default=c.Quality.Defaults.RULE_TIMEOUT_SECONDS, ge=1, le=3600)
    ]
    cache_enabled: Annotated[bool, Field(default=True)]
    mcp_server_port: Annotated[
        int, Field(default=c.Quality.Mcp.DEFAULT_PORT, ge=1, le=65535)
    ]
    rules_dir: Annotated[str, Field(default=c.Quality.Paths.RULES_DIR)]
    max_function_length: Annotated[int, Field(default=50)]
    max_class_length: Annotated[int, Field(default=200)]

    @classmethod
    def get_instance(cls) -> FlextQualitySettings:
        """Create settings instance from current environment."""
        return cls.fetch_global()

    def get_rules_path(self) -> Path:
        """Resolve configured rules directory path."""
        return Path(self.rules_dir)

    def validate_thresholds(self) -> p.Result[bool]:
        """Validate numeric thresholds and feature toggles."""
        if self.max_function_length > self.max_class_length:
            return r[bool].fail(
                f"max_function_length ({self.max_function_length}) must be <= "
                f"max_class_length ({self.max_class_length})",
            )
        return r[bool].ok(True)


__all__: list[str] = ["FlextQualitySettings"]
