"""FLEXT Quality Documentation Maintenance - Configuration Management.

Single loader for the documentation maintenance configuration. Every file is
read from the declared configuration directory and validated into its canonical
``m.Quality`` model; a missing, unreadable, or invalid file fails loudly.
"""

from __future__ import annotations

from pathlib import Path

from flext_quality import m, t, u


class FlextQualityConfigManager:
    """Load and cache the validated documentation maintenance configuration."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory containing the configuration files. ``None``
                selects the package's declared ``docs/config`` directory.

        """
        self.config_dir = (
            Path(__file__).parent.parent / "config"
            if config_dir is None
            else Path(config_dir)
        )
        self._audit_rules: m.Quality.AuditRulesConfig | None = None
        self._style_guide: m.Quality.StyleGuideConfig | None = None
        self._validation_config: m.Quality.ValidationConfig | None = None

    def resolve_audit_rules(self) -> m.Quality.AuditRulesConfig:
        """Return the validated ``audit_rules.yaml`` configuration."""
        if self._audit_rules is None:
            self._audit_rules = m.Quality.AuditRulesConfig.model_validate(
                self._load_config_file("audit_rules.yaml")
            )
        return self._audit_rules

    def resolve_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Return the validated ``style_guide.yaml`` configuration."""
        if self._style_guide is None:
            self._style_guide = m.Quality.StyleGuideConfig.model_validate(
                self._load_config_file("style_guide.yaml")
            )
        return self._style_guide

    def resolve_validation_config(self) -> m.Quality.ValidationConfig:
        """Return the validated ``validation_config.yaml`` configuration."""
        if self._validation_config is None:
            self._validation_config = m.Quality.ValidationConfig.model_validate(
                self._load_config_file("validation_config.yaml")
            )
        return self._validation_config

    def _load_config_file(self, filename: str) -> t.JsonMapping:
        """Load one YAML configuration file and propagate its failure."""
        return u.Cli.yaml_safe_load(self.config_dir / filename).unwrap()


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityConfigManager"]
