"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files.
"""

from __future__ import annotations

from pathlib import Path

from flext_quality import c, m, t, u


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
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = self._load_config_file("audit_rules.yaml")
            self._audit_rules = m.Quality.AuditRulesConfig.model_validate(data)
        return self._audit_rules

    def resolve_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = self._load_config_file("style_guide.yaml")
            self._style_guide = m.Quality.StyleGuideConfig.model_validate(data)
        return self._style_guide

    def resolve_validation_config(self) -> m.Quality.ValidationConfig:
        """Get validation configuration."""
        if self._validation_config is None:
            data = self._load_config_file("validation_config.yaml")
            self._validation_config = m.Quality.ValidationConfig.model_validate(data)
        return self._validation_config

    def _load_config_file(self, filename: str) -> t.JsonMapping:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename
        return u.Cli.yaml_safe_load(config_path).value

    def reload_configs(self) -> None:
        """Reload all configurations from disk."""
        self._audit_rules = None
        self._style_guide = None
        self._validation_config = None

    def validate_configs(self) -> t.StrSequence:
        """Validate all configuration files and return any issues."""
        # Check required settings files exist
        required_files = [
            "audit_rules.yaml",
            "style_guide.yaml",
            "validation_config.yaml",
        ]
        issues = [
            f"Missing required settings file: {filename}"
            for filename in required_files
            if not (self.config_dir / filename).exists()
        ]

        validations = (
            (
                self.resolve_audit_rules,
                "quality_thresholds",
                "Audit rules missing quality_thresholds section",
                "audit_rules.yaml",
            ),
            (
                self.resolve_style_guide,
                "markdown",
                "Style guide missing markdown section",
                "style_guide.yaml",
            ),
            (
                self.resolve_validation_config,
                "link_validation",
                "Validation settings missing link_validation section",
                "validation_config.yaml",
            ),
        )
        for getter, required_attr, missing_message, filename in validations:
            try:
                config = getter()
                if not getattr(config, required_attr):
                    issues.append(missing_message)
            except c.EXC_FS_KEY_VALUE as exc:
                issues.append(f"Invalid {filename}: {exc}")

        return issues


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityConfigManager"]
