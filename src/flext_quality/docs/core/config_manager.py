"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
)
from pathlib import Path

from flext_quality import c, m, t, u


class FlextQualityConfigManager:
    """Centralized configuration management for the documentation maintenance system."""

    type ConfigValue = t.Primitives | t.StrSequence
    type ConfigSection = MutableMapping[str, t.Primitives | t.StrSequence]
    type ConfigData = MutableMapping[
        str,
        MutableMapping[str, t.Primitives | t.StrSequence],
    ]
    type RawSectionMap = t.MappingKV[
        str,
        t.Primitives | t.SequenceOf[t.Primitives],
    ]
    type RawConfigMap = t.MappingKV[
        str,
        t.MappingKV[str, t.Primitives | t.SequenceOf[t.Primitives]],
    ]

    class AuditRules(m.Quality.AuditRulesConfig):
        """Configuration for audit rules and thresholds."""

        link_checks: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        style_checks: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict
        )
        accessibility_checks: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(
                default_factory=dict,
            )
        )

        def get_threshold(
            self,
            key: str,
            *,
            default: t.Primitives | None = None,
        ) -> t.Primitives | None:
            """Get a quality threshold value."""
            threshold = getattr(self.quality_thresholds, key, default)
            return threshold if isinstance(threshold, t.PRIMITIVES_TYPES) else default

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

    class StyleGuide(m.Quality.StyleGuideConfig):
        """Configuration for style and formatting guidelines."""

        def get_markdown_rule(
            self,
            rule: str,
            *,
            default: t.Primitives | None = None,
        ) -> t.Primitives | None:
            """Get a markdown formatting rule."""
            value = getattr(self.markdown, rule, default)
            return value if isinstance(value, t.PRIMITIVES_TYPES) else default

        def get_accessibility_rule(
            self,
            rule: str,
            *,
            default: t.Primitives | None = None,
        ) -> t.Primitives | None:
            """Get an accessibility rule."""
            value = getattr(self.accessibility, rule, default)
            return value if isinstance(value, t.PRIMITIVES_TYPES) else default

    class ValidationSettings(m.Quality.ValidationConfig):
        """Configuration for validation operations."""

        content_validation: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict,
        )
        image_validation: MutableMapping[str, t.Primitives | t.StrSequence] = u.Field(
            default_factory=dict,
        )
        accessibility_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(
                default_factory=dict,
            )
        )
        security_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(
                default_factory=dict,
            )
        )
        performance_validation: MutableMapping[str, t.Primitives | t.StrSequence] = (
            u.Field(
                default_factory=dict,
            )
        )

        def get_link_setting(
            self,
            setting: str,
            *,
            default: t.Primitives | None = None,
        ) -> t.Primitives | None:
            """Get a link validation setting."""
            value = getattr(self.link_validation, setting, default)
            return value if isinstance(value, t.PRIMITIVES_TYPES) else default

        def get_content_setting(
            self,
            setting: str,
            *,
            default: t.Primitives | None = None,
        ) -> t.Primitives | None:
            """Get a content validation setting."""
            value = self.content_validation.get(setting, default)
            return value if isinstance(value, t.PRIMITIVES_TYPES) else default

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
            if isinstance(item, t.PRIMITIVES_TYPES):
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
            config_dir: Directory containing configuration files. If None,
                       uses the default settings directory.

        """
        if config_dir is None:
            # Find settings directory relative to this file
            self.config_dir = Path(__file__).parent.parent / "settings"
        else:
            self.config_dir = Path(config_dir)

        self._cache: MutableMapping[str, FlextQualityConfigManager.ConfigData] = {}
        self._audit_rules: FlextQualityConfigManager.AuditRules | None = None
        self._style_guide: FlextQualityConfigManager.StyleGuide | None = None
        self._validation_config: FlextQualityConfigManager.ValidationSettings | None = (
            None
        )

    def get_audit_rules(self) -> FlextQualityConfigManager.AuditRules:
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = self._load_config_file("audit_rules.yaml")
            self._audit_rules = FlextQualityConfigManager.AuditRules.model_validate(
                data
            )
        return self._audit_rules

    def get_style_guide(self) -> FlextQualityConfigManager.StyleGuide:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = self._load_config_file("style_guide.yaml")
            self._style_guide = FlextQualityConfigManager.StyleGuide.model_validate(
                data
            )
        return self._style_guide

    def get_validation_config(self) -> FlextQualityConfigManager.ValidationSettings:
        """Get validation configuration."""
        if self._validation_config is None:
            data = self._load_config_file("validation_config.yaml")
            self._validation_config = (
                FlextQualityConfigManager.ValidationSettings.model_validate(data)
            )
        return self._validation_config

    def get_config(self, name: str) -> FlextQualityConfigManager.ConfigData:
        """Get a configuration file by name."""
        if name not in self._cache:
            self._cache[name] = self._load_config_file(f"{name}.yaml")
        return self._cache[name]

    def _load_config_file(self, filename: str) -> FlextQualityConfigManager.ConfigData:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename

        try:
            raw = u.Cli.yaml_load_mapping(config_path)
            return (
                self._as_config_data(raw) if raw else self._get_default_config(filename)
            )
        except FileNotFoundError:
            return self._get_default_config(filename)
        except (OSError, PermissionError, UnicodeDecodeError) as exc:
            _ = exc
            return self._get_default_config(filename)

    def _get_default_config(
        self, filename: str
    ) -> FlextQualityConfigManager.ConfigData:
        """Get default configuration for a file."""
        defaults: t.MappingKV[str, FlextQualityConfigManager.RawConfigMap] = {
            "audit_rules.yaml": {
                "quality_thresholds": {
                    "max_age_days": 90,
                    "min_word_count": 100,
                    "max_broken_links": 0,
                    "min_completeness_score": 0.8,
                },
                "content_checks": {
                    "check_freshness": True,
                    "check_completeness": True,
                    "check_readability": False,
                },
                "link_checks": {
                    "check_external": True,
                    "check_internal": True,
                    "check_images": True,
                },
                "style_checks": {"check_formatting": True, "check_consistency": True},
                "accessibility_checks": {
                    "check_alt_text": True,
                    "check_headings": True,
                    "check_links": True,
                },
            },
            "style_guide.yaml": {
                "markdown": {
                    "heading_style": "atx",
                    "list_style": "dash",
                    "emphasis_style": "*",
                    "max_line_length": 88,
                },
                "accessibility": {
                    "require_alt_text": True,
                    "descriptive_links": True,
                    "heading_structure": True,
                },
                "formatting": {
                    "max_line_length": 88,
                    "consistent_indentation": True,
                    "trailing_spaces": False,
                },
            },
            "validation_config.yaml": {
                **m.Quality.ValidationConfig().model_dump(),
            },
        }

        default_value = defaults.get(filename)
        return self._as_config_data(default_value)

    def reload_configs(self) -> None:
        """Reload all configurations from disk."""
        self._cache.clear()
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
                self.get_audit_rules,
                "quality_thresholds",
                "Audit rules missing quality_thresholds section",
                "audit_rules.yaml",
            ),
            (
                self.get_style_guide,
                "markdown",
                "Style guide missing markdown section",
                "style_guide.yaml",
            ),
            (
                self.get_validation_config,
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

    def get_all_configs(
        self,
    ) -> t.JsonMapping:
        """Get all configurations as a single dictionary."""
        return t.json_mapping_adapter().validate_python(
            {
                "audit_rules": self.get_audit_rules().model_dump(mode="json"),
                "style_guide": self.get_style_guide().model_dump(mode="json"),
                "validation_config": self.get_validation_config().model_dump(
                    mode="json",
                ),
                "raw_configs": {
                    name: self.get_config(name)
                    for name in ["audit_rules", "style_guide", "validation_config"]
                },
            },
        )


FlextQualityConfigManager.AuditRules.model_rebuild(
    _types_namespace={"FlextQualityModels": m}
)
FlextQualityConfigManager.StyleGuide.model_rebuild(
    _types_namespace={"FlextQualityModels": m}
)
FlextQualityConfigManager.ValidationSettings.model_rebuild(
    _types_namespace={"FlextQualityModels": m}
)
