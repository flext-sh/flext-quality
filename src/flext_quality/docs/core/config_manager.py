"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files. Missing or
partial configuration files resolve through the canonical model defaults,
so an empty configuration directory still yields a fully typed, valid
configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from flext_quality import m, t, u

_REQUIRED_CONFIG_FILES: Final[t.StrSequence] = (
    "audit_rules.yaml",
    "style_guide.yaml",
    "validation_config.yaml",
)


class FlextQualityConfigManager:
    """Centralized configuration management for the documentation maintenance system."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory containing configuration files. If None,
                       uses the package's declared config directory.

        """
        if config_dir is None:
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        self._audit_rules: m.Quality.AuditRulesConfig | None = None
        self._style_guide: m.Quality.StyleGuideConfig | None = None
        self._validation_config: m.Quality.ValidationConfig | None = None

    def resolve_audit_rules(self) -> m.Quality.AuditRulesConfig:
        """Resolve the audit rules configuration, applying model defaults."""
        if self._audit_rules is None:
            self._audit_rules = m.Quality.AuditRulesConfig.model_validate(
                self._load_config_file("audit_rules.yaml")
            )
        return self._audit_rules

    def resolve_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Resolve the style guide configuration, applying model defaults."""
        if self._style_guide is None:
            self._style_guide = m.Quality.StyleGuideConfig.model_validate(
                self._load_config_file("style_guide.yaml")
            )
        return self._style_guide

    def resolve_validation_config(self) -> m.Quality.ValidationConfig:
        """Resolve the validation configuration, applying model defaults."""
        if self._validation_config is None:
            self._validation_config = m.Quality.ValidationConfig.model_validate(
                self._load_config_file("validation_config.yaml")
            )
        return self._validation_config

    def _load_config_file(self, filename: str) -> t.JsonMapping:
        """Load a YAML configuration file; a missing file yields empty data."""
        config_path = self.config_dir / filename
        if not config_path.is_file():
            return {}
        loaded: t.JsonMapping = u.Cli.yaml_safe_load(config_path).value
        return loaded or {}

    def reload_configs(self) -> None:
        """Reload all configurations from disk."""
        self._audit_rules = None
        self._style_guide = None
        self._validation_config = None

    def validate_configs(self) -> t.StrSequence:
        """Validate declared configuration and report every required file that is absent."""
        return [
            f"Missing required settings file: {name}"
            for name in _REQUIRED_CONFIG_FILES
            if not (self.config_dir / name).is_file()
        ]


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityConfigManager"]
