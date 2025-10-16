"""Configuration manager helpers for quality tooling.

Migrated from ``flext_tools.config_manager`` with additional conveniences such
as JSON serialisation and FlextResult based error handling.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes


class ConfigurationManager(FlextService[FlextTypes.StringDict]):
    """Provide lightweight configuration storage for automation scripts."""

    def __init__(self: Self, config_path: str | Path | None = None) -> None:
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._config_path = Path(config_path).expanduser() if config_path else None
        self._config: FlextTypes.StringDict = {}

    def execute(self: Self) -> FlextResult[FlextTypes.StringDict]:
        """Return the current configuration snapshot."""
        return FlextResult[FlextTypes.StringDict].ok(self._config)

    def load_config(self) -> FlextResult[FlextTypes.StringDict]:
        """Load configuration from disk if a path is configured."""
        if not self._config_path:
            return FlextResult[FlextTypes.StringDict].ok(self._config)

        try:
            if self._config_path.exists():
                with self._config_path.open(encoding="utf-8") as handle:
                    raw_data = json.load(handle)
                    self._config = {key: str(value) for key, value in raw_data.items()}
            return FlextResult[FlextTypes.StringDict].ok(self._config)
        except (OSError, json.JSONDecodeError) as error:
            self._logger.exception("Failed to load configuration")
            return FlextResult[FlextTypes.StringDict].fail(
                f"Failed to load configuration: {error}"
            )

    def save_config(self) -> FlextResult[None]:
        """Persist the configuration to disk if a path has been provided."""
        if not self._config_path:
            return FlextResult[None].ok(None)

        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with self._config_path.open("w", encoding="utf-8") as handle:
                json.dump(self._config, handle, indent=2, ensure_ascii=False)
            return FlextResult[None].ok(None)
        except OSError as error:
            self._logger.exception("Failed to save configuration")
            return FlextResult[None].fail(f"Failed to save configuration: {error}")

    def get(self, key: str, default: str | None = None) -> FlextResult[str | None]:
        """Retrieve a configuration value."""
        return FlextResult[str | None].ok(self._config.get(key, default))

    def set(self, key: str, value: str) -> FlextResult[None]:
        """Set a configuration value."""
        self._config[key] = value
        return FlextResult[None].ok(None)

    def delete(self, key: str) -> FlextResult[None]:
        """Delete a configuration value if present."""
        self._config.pop(key, None)
        return FlextResult[None].ok(None)

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration structure (placeholder for compatibility)."""
        return FlextResult[None].ok(None)


__all__ = ["ConfigurationManager"]
