"""FlextQualitySettings - Configuration for flext-quality.

Extends FlextSettings with quality-specific configuration for hooks,
rules, MCP integration, and quality thresholds.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from flext_core import FlextSettingsBase
from flext_quality import c, m, p, r, u


class FlextQualitySettings(FlextSettingsBase):
    """Runtime configuration for flext-quality services."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_",
        extra="ignore",
    )

    hook_timeout_ms: Annotated[int, u.Field(ge=100, le=60000)] = (
        c.Quality.HOOK_TIMEOUT_MS
    )
    rule_timeout_seconds: Annotated[int, u.Field(ge=1, le=3600)] = (
        c.Quality.RULE_TIMEOUT_SECONDS
    )
    cache_enabled: Annotated[bool, u.Field(default=True)]
    mcp_server_port: Annotated[int, u.Field(ge=1, le=65535)] = (
        c.Quality.MCP_DEFAULT_PORT
    )
    rules_dir: Annotated[str, u.Field(default=c.Quality.PATHS_RULES_DIR)]
    max_function_length: Annotated[int, u.Field(default=50)]
    max_class_length: Annotated[int, u.Field(default=200)]

    def resolve_rules_path(self) -> Path:
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
