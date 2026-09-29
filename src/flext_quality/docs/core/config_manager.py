"""FLEXT Quality Documentation Maintenance - Configuration Management.

Single loader for the documentation maintenance configuration. Every file is
read from the declared configuration directory and validated into its canonical
``m.Quality`` model; a missing, unreadable, or invalid file fails loudly.
"""

from __future__ import annotations

from pathlib import Path

from flext_quality import m, t, u


class FlextQualityConfigManager:
    """Centralized configuration management for the documentation maintenance system."""

    type ConfigValue = t.Primitives | t.StrSequence
    type ConfigSection = MutableMapping[str, t.Primitives | t.StrSequence]
    type ConfigData = MutableMapping[
        str, MutableMapping[str, t.Primitives | t.StrSequence]
    ]
    type RawSectionMap = t.MappingKV[str, t.Primitives | t.SequenceOf[t.Primitives]]
    type RawConfigMap = t.MappingKV[
        str, t.MappingKV[str, t.Primitives | t.SequenceOf[t.Primitives]]
    ]

    class AuditRules(FlextQualityModels.Quality.AuditRulesConfig):
        """Configuration for audit rules and thresholds."""

        link_checks: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        style_checks: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        accessibility_checks: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(default_factory=dict)
        )

        def get_threshold(
            self, key: str, *, default: t.Primitives | None = None
        ) -> t.Primitives | None:
            """Get a quality threshold value."""
            threshold = getattr(self.quality_thresholds, key, default)
            return threshold if isinstance(threshold, c.PRIMITIVES_TYPES) else default

        def is_check_enabled(self, check_type: str, check_name: str) -> bool:
            """Check if a specific audit check is enabled."""
            check_value = False
            match check_type:
                case "content":
                    check_value = bool(getattr(self.content_checks, check_name, False))
                case "link":
                    check_value = bool(self.link_checks.get(check_name, False))
                case "style":
                    check_value = bool(self.style_checks.get(check_name, False))
                case "accessibility":
                    check_value = bool(self.accessibility_checks.get(check_name, False))
                case _:
                    pass
            return check_value

    class StyleGuide(FlextQualityModels.Quality.StyleGuideConfig):
        """Configuration for style and formatting guidelines."""

        def get_markdown_rule(
            self, rule: str, *, default: t.Primitives | None = None
        ) -> t.Primitives | None:
            """Get a markdown formatting rule."""
            value = getattr(self.markdown, rule, default)
            return value if isinstance(value, c.PRIMITIVES_TYPES) else default

        def get_accessibility_rule(
            self, rule: str, *, default: t.Primitives | None = None
        ) -> t.Primitives | None:
            """Get an accessibility rule."""
            value = getattr(self.accessibility, rule, default)
            return value if isinstance(value, c.PRIMITIVES_TYPES) else default

    class ValidationSettings(FlextQualityModels.Quality.ValidationConfig):
        """Configuration for validation operations."""

        content_validation: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        image_validation: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        accessibility_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(default_factory=dict)
        )
        security_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(default_factory=dict)
        )
        performance_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(default_factory=dict)
        )

        def get_link_setting(
            self, setting: str, *, default: t.Primitives | None = None
        ) -> t.Primitives | None:
            """Get a link validation setting."""
            value = getattr(self.link_validation, setting, default)
            return value if isinstance(value, c.PRIMITIVES_TYPES) else default

        def get_content_setting(
            self, setting: str, *, default: t.Primitives | None = None
        ) -> t.Primitives | None:
            """Get a content validation setting."""
            value = self.content_validation.get(setting, default)
            return value if isinstance(value, c.PRIMITIVES_TYPES) else default

    @staticmethod
    def _as_section(
        value: FlextQualityConfigManager.RawSectionMap | t.JsonValue,
    ) -> FlextQualityConfigManager.ConfigSection:
        """Normalize any value into a configuration section mapping."""
        if not isinstance(value, Mapping):
            return {}
        section: FlextQualityConfigManager.ConfigSection = {}
        for key, item in value.items():
            key_str = key
            if isinstance(item, c.PRIMITIVES_TYPES):
                section[key_str] = item
            elif isinstance(item, list):
                section[key_str] = [str(entry) for entry in item]
        return section

    @staticmethod
    def _as_config_data(
        value: FlextQualityConfigManager.RawConfigMap | t.JsonMapping | None,
    ) -> FlextQualityConfigManager.ConfigData:
        """Normalize loaded YAML content into typed settings data."""
        if not isinstance(value, Mapping):
            return {}
        settings: FlextQualityConfigManager.ConfigData = {}
        for key, item in value.items():
            section = FlextQualityConfigManager._as_section(item)
            if section:
                settings[key] = section
        return settings

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
