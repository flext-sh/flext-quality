"""Settings for flext-quality — namespaced under ``settings.Quality``.

Layer-0: imports only stdlib + pydantic + ``FlextSettings``. Universal runtime
fields come from ``FlextSettings`` by MRO. All project fields live in the
``Quality`` namespace group with simple scalar types (env-settable).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings


class FlextQualitySettings(FlextSettings):
    """Runtime configuration for flext-quality; fields under ``settings.Quality.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_", env_nested_delimiter="__", extra="ignore"
    )

    class _Quality(BaseModel):
        """Namespaced quality settings (hooks, rules, MCP, thresholds)."""

        hook_timeout_ms: Annotated[int, Field(default=5000, ge=100, le=60000)]
        rule_timeout_seconds: Annotated[int, Field(default=30, ge=1, le=3600)]
        cache_enabled: Annotated[bool, Field(default=True)]
        mcp_server_port: Annotated[int, Field(default=3100, ge=1, le=65535)]
        rules_dir: Annotated[str, Field(default="rules")]
        max_function_length: Annotated[int, Field(default=50)]
        max_class_length: Annotated[int, Field(default=200)]

        @model_validator(mode="after")
        def _validate_thresholds(self) -> FlextQualitySettings._Quality:
            """Ensure function length ceiling does not exceed class length ceiling."""
            if self.max_function_length > self.max_class_length:
                msg = (
                    f"max_function_length ({self.max_function_length}) must be <= "
                    f"max_class_length ({self.max_class_length})"
                )
                raise ValueError(msg)
            return self

    if TYPE_CHECKING:
        Quality: _Quality
    else:
        Quality: _Quality = Field(
            default_factory=_Quality, description="Namespaced quality settings."
        )


settings: FlextQualitySettings = FlextQualitySettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_quality import settings``."""

__all__: list[str] = ["FlextQualitySettings", "settings"]
