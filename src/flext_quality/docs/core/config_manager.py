"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path

from flext_quality import m, t, u


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

        self._cache: MutableMapping[str, t.JsonMapping] = {}
        self._audit_rules: m.Quality.AuditRulesConfig | None = None
        self._style_guide: m.Quality.StyleGuideConfig | None = None
        self._validation_config: m.Quality.ValidationConfig | None = None

    def get_audit_rules(self) -> m.Quality.AuditRulesConfig:
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = self._load_config_file("audit_rules.yaml")
            self._audit_rules = m.Quality.AuditRulesConfig.model_validate(data)
        return self._audit_rules

    def get_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = self._load_config_file("style_guide.yaml")
            self._style_guide = m.Quality.StyleGuideConfig.model_validate(data)
        return self._style_guide

    def get_validation_config(self) -> m.Quality.ValidationConfig:
        """Get validation configuration."""
        if self._validation_config is None:
            data = self._load_config_file("validation_config.yaml")
            self._validation_config = m.Quality.ValidationConfig.model_validate(data)
        return self._validation_config

    def get_config(self, name: str) -> t.JsonMapping:
        """Get a configuration file by name."""
        if name not in self._cache:
            self._cache[name] = self._load_config_file(f"{name}.yaml")
        return self._cache[name]

    def _load_config_file(self, filename: str) -> t.JsonMapping:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename
        return u.Cli.yaml_safe_load(config_path).value

    def reload_configs(self) -> None:
        """Reload all configurations from disk."""
        self._cache.clear()
        self._audit_rules = None
        self._style_guide = None
        self._validation_config = None

    def validate_configs(self) -> t.StrSequence:
        """Validate declared configuration and propagate the first failure."""
        self.get_audit_rules()
        self.get_style_guide()
        self.get_validation_config()
        return []

    def get_all_configs(self) -> t.JsonMapping:
        """Get all configurations as a single dictionary."""
        return t.json_mapping_adapter().validate_python({
            "audit_rules": self.get_audit_rules().model_dump(mode="json"),
            "style_guide": self.get_style_guide().model_dump(mode="json"),
            "validation_config": self.get_validation_config().model_dump(mode="json"),
            "raw_configs": {
                name: self.get_config(name)
                for name in ["audit_rules", "style_guide", "validation_config"]
            },
        })


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityConfigManager"]
