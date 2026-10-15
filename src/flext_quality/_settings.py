"""Settings for flext-quality — namespaced under ``settings.Quality``.

Layer-0: imports only stdlib + pydantic + ``FlextSettings``. Universal runtime
fields come from ``FlextSettings`` by MRO. All project fields live in the
``Quality`` namespace group with simple scalar types (env-settable).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_core import FlextSettings, m, u


class FlextQualitySettings(FlextSettings):
    """Runtime configuration for flext-quality; fields under ``settings.Quality.*``."""

    model_config = m.SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _Quality(m.BaseModel):
        """Namespaced quality settings (hooks, rules, MCP, thresholds)."""

        hook_timeout_ms: Annotated[int, m.Field(ge=100, le=60000)] = 5000
        rule_timeout_seconds: Annotated[int, m.Field(ge=1, le=3600)] = 30
        cache_enabled: bool = True
        mcp_server_port: Annotated[int, m.Field(ge=1, le=65535)] = 3100
        rules_dir: str = "rules"
        max_function_length: int = 50
        max_class_length: int = 200

        @u.model_validator(mode="after")
        def _validate_thresholds(self) -> FlextQualitySettings._Quality:
            """Ensure function length ceiling does not exceed class length ceiling.

            Returns:
                The resulting ``FlextQualitySettings._Quality``.

            Raises:
                ValueError: If max_function_length.

            """
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
        Quality: _Quality = m.Field(
            default_factory=_Quality,
            description="Namespaced quality settings.",
        )


settings: FlextQualitySettings = FlextQualitySettings.fetch_global()
"""Pre-instantiated project settings singleton.

``from flext_quality import settings``.
"""

__all__: list[str] = ["FlextQualitySettings", "settings"]
