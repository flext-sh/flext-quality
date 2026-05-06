"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
    Sequence,
)
from pathlib import Path

from flext_quality import c, m, t, u

type ConfigValue = t.Primitives | t.StrSequence
type ConfigSection = MutableMapping[str, t.Primitives | t.StrSequence]
type ConfigData = MutableMapping[
    str,
    MutableMapping[str, t.Primitives | t.StrSequence],
]
type RawSectionValue = t.Primitives | t.SequenceOf[t.Primitives]
type RawSectionMap = t.MappingKV[
    str,
    t.Primitives | t.SequenceOf[t.Primitives],
]
type RawConfigMap = t.MappingKV[
    str,
    t.MappingKV[str, t.Primitives | t.SequenceOf[t.Primitives]],
]


class FlextQualityAuditRules:
    """Configuration for audit rules and thresholds."""

    def __init__(self, data: ConfigData) -> None:
        """Initialize audit rules configuration."""
        self.quality_thresholds: ConfigSection = data.get("quality_thresholds", {})
        self.content_checks: ConfigSection = data.get("content_checks", {})
        self.link_checks: ConfigSection = data.get("link_checks", {})
        self.style_checks: ConfigSection = data.get("style_checks", {})
        self.accessibility_checks: ConfigSection = data.get("accessibility_checks", {})

    def get_threshold(
        self,
        key: str,
        *,
        default: t.Primitives | None = None,
    ) -> t.Primitives | None:
        """Get a quality threshold value."""
        threshold = self.quality_thresholds.get(key, default)
        return threshold if isinstance(threshold, (str, int, float, bool)) else default

    def is_check_enabled(self, check_type: str, check_name: str) -> bool:
        """Check if a specific audit check is enabled."""
        checks = getattr(self, f"{check_type}_checks", {})
        return bool(checks.get(check_name, False))


class FlextQualityStyleGuide:
    """Configuration for style and formatting guidelines."""

    def __init__(self, data: ConfigData) -> None:
        """Initialize style guidelines configuration."""
        self.markdown: ConfigSection = data.get("markdown", {})
        self.accessibility: ConfigSection = data.get("accessibility", {})
        self.formatting: ConfigSection = data.get("formatting", {})

    def get_markdown_rule(
        self,
        rule: str,
        *,
        default: t.Primitives | None = None,
    ) -> t.Primitives | None:
        """Get a markdown formatting rule."""
        value = self.markdown.get(rule, default)
        return value if isinstance(value, (str, int, float, bool)) else default

    def get_accessibility_rule(
        self,
        rule: str,
        *,
        default: t.Primitives | None = None,
    ) -> t.Primitives | None:
        """Get an accessibility rule."""
        value = self.accessibility.get(rule, default)
        return value if isinstance(value, (str, int, float, bool)) else default


class FlextQualityValidationSettings:
    """Configuration for validation operations."""

    def __init__(self, data: ConfigData) -> None:
        """Initialize validation configuration."""
        self.link_validation: ConfigSection = data.get("link_validation", {})
        self.content_validation: ConfigSection = data.get("content_validation", {})
        self.image_validation: ConfigSection = data.get("image_validation", {})
        self.accessibility_validation: ConfigSection = data.get(
            "accessibility_validation",
            {},
        )
        self.security_validation: ConfigSection = data.get("security_validation", {})
        self.performance_validation: ConfigSection = data.get(
            "performance_validation",
            {},
        )

    def get_link_setting(
        self,
        setting: str,
        *,
        default: t.Primitives | None = None,
    ) -> t.Primitives | None:
        """Get a link validation setting."""
        value = self.link_validation.get(setting, default)
        return value if isinstance(value, (str, int, float, bool)) else default

    def get_content_setting(
        self,
        setting: str,
        *,
        default: t.Primitives | None = None,
    ) -> t.Primitives | None:
        """Get a content validation setting."""
        value = self.content_validation.get(setting, default)
        return value if isinstance(value, (str, int, float, bool)) else default


class FlextQualityConfigManager:
    """Centralized configuration management for the documentation maintenance system."""

    @staticmethod
    def _as_section(value: RawSectionMap | t.JsonValue) -> ConfigSection:
        """Normalize any value into a configuration section mapping."""
        if not isinstance(value, Mapping):
            return {}
        section: ConfigSection = {}
        for key, item in value.items():
            key_str = key
            if isinstance(item, (str, int, float, bool)):
                section[key_str] = item
            elif isinstance(item, list):
                section[key_str] = [str(entry) for entry in item]
        return section

    @staticmethod
    def _as_config_data(
        value: RawConfigMap | t.JsonMapping | None,
    ) -> ConfigData:
        """Normalize loaded YAML content into typed settings data."""
        if not isinstance(value, Mapping):
            return {}
        settings: ConfigData = {}
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

        self._cache: MutableMapping[str, ConfigData] = {}
        self._audit_rules: FlextQualityAuditRules | None = None
        self._style_guide: FlextQualityStyleGuide | None = None
        self._validation_config: FlextQualityValidationSettings | None = None

    def get_audit_rules(self) -> FlextQualityAuditRules:
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = self._load_config_file("audit_rules.yaml")
            self._audit_rules = FlextQualityAuditRules(data)
        return self._audit_rules

    def get_style_guide(self) -> FlextQualityStyleGuide:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = self._load_config_file("style_guide.yaml")
            self._style_guide = FlextQualityStyleGuide(data)
        return self._style_guide

    def get_validation_config(self) -> FlextQualityValidationSettings:
        """Get validation configuration."""
        if self._validation_config is None:
            data = self._load_config_file("validation_config.yaml")
            self._validation_config = FlextQualityValidationSettings(data)
        return self._validation_config

    def get_config(self, name: str) -> ConfigData:
        """Get a configuration file by name."""
        if name not in self._cache:
            self._cache[name] = self._load_config_file(f"{name}.yaml")
        return self._cache[name]

    def _load_config_file(self, filename: str) -> ConfigData:
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

    def _get_default_config(self, filename: str) -> ConfigData:
        """Get default configuration for a file."""
        defaults: t.MappingKV[str, RawConfigMap] = {
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
    ) -> t.MappingKV[str, ConfigData | t.MappingKV[str, ConfigData]]:
        """Get all configurations as a single dictionary."""
        return {
            "audit_rules": self.get_audit_rules().__dict__,
            "style_guide": self.get_style_guide().__dict__,
            "validation_config": self.get_validation_config().__dict__,
            "raw_configs": {
                name: self.get_config(name)
                for name in ["audit_rules", "style_guide", "validation_config"]
            },
        }

    def save_config(self, name: str, data: ConfigData) -> bool:
        """Save a configuration to file."""
        try:
            config_path = self.config_dir / f"{name}.yaml"
            self.config_dir.mkdir(parents=True, exist_ok=True)

            normalized_data: t.JsonDict = {}
            for section_name, section in data.items():
                normalized_section: t.JsonDict = {}
                for key, value in section.items():
                    normalized_value: t.JsonValue
                    if isinstance(value, Sequence) and not isinstance(
                        value, (str, bytes)
                    ):
                        normalized_value = t.json_value_adapter().validate_python(
                            list(value),
                        )
                    else:
                        normalized_value = t.json_value_adapter().validate_python(
                            value,
                        )
                    normalized_section[key] = normalized_value
                normalized_data[section_name] = t.json_value_adapter().validate_python(
                    normalized_section,
                )

            result = u.Cli.yaml_dump(config_path, normalized_data)
            if result.failure:
                return False

            # Clear cache for this settings
            if name in self._cache:
                del self._cache[name]

            # Reset specific settings objects
            if name == "audit_rules":
                self._audit_rules = None
            elif name == "style_guide":
                self._style_guide = None
            elif name == "validation_config":
                self._validation_config = None

            return True
        except (FileNotFoundError, PermissionError, ValueError, OSError):
            return False
