"""FLEXT Quality Documentation Maintenance - Configuration Management.

Single loader for the documentation maintenance configuration. Every file is
read from the declared configuration directory and validated into its canonical
``m.Quality`` model; a missing, unreadable, or invalid file fails loudly.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

from flext_quality import c, m, t, u

_DEFAULT_AUDIT_RULES: t.JsonMapping = MappingProxyType({
    "quality_thresholds": {
        "max_age_days": 90,
        "min_word_count": 100,
        "max_broken_links": 0,
        "min_completeness_score": 0.8,
        "max_file_size_mb": 10,
    },
    "content_checks": {
        "check_freshness": True,
        "check_completeness": True,
        "check_consistency": True,
        "check_links": True,
        "check_structure": True,
        "check_accessibility": True,
    },
    "severity_levels": {
        "critical": ["broken_external_link", "missing_section"],
        "high": ["outdated_content", "broken_internal_link"],
        "medium": ["style_inconsistency", "missing_alt_text"],
        "low": ["formatting_issue", "readability_warning"],
    },
})

_DEFAULT_STYLE_GUIDE: t.JsonMapping = MappingProxyType({
    "markdown": {
        "heading_style": "atx",
        "list_style": "dash",
        "emphasis_style": "*",
        "code_block_style": "fenced",
        "link_style": "inline",
    },
    "accessibility": {
        "require_alt_text": True,
        "descriptive_link_text": True,
        "proper_heading_hierarchy": True,
        "min_alt_text_length": 5,
        "max_alt_text_length": 100,
        "check_color_contrast": False,
        "minimum_contrast_ratio": 4.5,
    },
    "formatting": {
        "max_line_length": 88,
        "soft_line_limit": 80,
        "consistent_indentation": True,
        "trailing_spaces": False,
        "trailing_newlines": True,
        "indentation_type": "spaces",
        "indentation_size": 4,
        "blank_lines_before_headings": True,
        "blank_lines_after_headings": False,
        "blank_lines_around_lists": True,
        "blank_lines_around_code_blocks": True,
    },
    "headings": {
        "enforce_hierarchy": True,
        "max_heading_level": 4,
        "require_space_after_hash": True,
        "allow_closing_hashes": False,
        "first_heading_level": 1,
        "toc_heading_level": 2,
    },
    "code": {
        "require_language_specifier": False,
        "preferred_languages": [
            "python",
            "bash",
            "json",
            "yaml",
            "sql",
            "javascript",
            "html",
        ],
        "inline_code_style": "backticks",
        "consistent_fencing": True,
        "fence_style": "backticks",
    },
})

_DEFAULT_VALIDATION_CONFIG: t.JsonMapping = MappingProxyType({
    "validation": {
        "enabled": True,
        "fail_on_errors": False,
        "verbose_output": False,
        "save_results": True,
        "max_concurrent_requests": 5,
        "request_timeout": 10,
        "requests_per_second": 10,
        "burst_limit": 20,
    },
    "link_validation": {
        "timeout": 10,
        "user_agent": "FLEXT-Quality-Doc-Validator/1.0",
        "check_external": True,
        "check_internal": True,
        "check_images": True,
        "follow_redirects": True,
        "max_redirects": 5,
        "acceptable_status_codes": [200, 201, 202, 206, 301, 302, 303, 307, 308],
        "validate_content_type": False,
        "expected_content_types": ["text/html", "text/plain", "application/json"],
        "allowed_domains": [],
        "blocked_domains": [],
        "github_links": {"validate_existence": True, "check_rate_limits": False},
        "documentation_links": {"validate_structure": False, "check_anchors": False},
    },
    "content_analysis": {
        "check_structure": True,
        "min_section_depth": 2,
        "required_sections": [
            "Overview|Introduction|Purpose",
            "Installation|Setup|Getting Started",
            "Usage|Examples",
        ],
        "min_word_count": 100,
        "check_readability": False,
        "readability_target_score": 60,
        "check_todos": True,
        "check_fixmes": True,
    },
})


def _merged_over_defaults(
    defaults: t.JsonMapping, overrides: t.JsonMapping
) -> t.JsonMapping:
    """Merge YAML overrides over the built-in default payload."""
    merged: dict[str, t.JsonValue] = dict(defaults)
    for key, value in overrides.items():
        current = merged.get(key)
        if isinstance(value, Mapping) and isinstance(current, Mapping):
            merged[key] = dict(_merged_over_defaults(current, value))
        else:
            merged[key] = dict(value) if isinstance(value, Mapping) else value
    return merged


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

    class AuditRules(m.Quality.AuditRulesConfig):
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

    class StyleGuide(m.Quality.StyleGuideConfig):
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

    class ValidationSettings(m.Quality.ValidationConfig):
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
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = _merged_over_defaults(
                _DEFAULT_AUDIT_RULES, self._load_config_file("audit_rules.yaml")
            )
            self._audit_rules = m.Quality.AuditRulesConfig.model_validate(data)
        return self._audit_rules

    def resolve_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = _merged_over_defaults(
                _DEFAULT_STYLE_GUIDE, self._load_config_file("style_guide.yaml")
            )
            self._style_guide = m.Quality.StyleGuideConfig.model_validate(data)
        return self._style_guide

    def resolve_validation_config(self) -> m.Quality.ValidationConfig:
        """Get validation configuration."""
        if self._validation_config is None:
            data = _merged_over_defaults(
                _DEFAULT_VALIDATION_CONFIG,
                self._load_config_file("validation_config.yaml"),
            )
            self._validation_config = m.Quality.ValidationConfig.model_validate(data)
        return self._validation_config

    def _load_config_file(self, filename: str) -> t.JsonMapping:
        """Load a YAML configuration file, defaulting to an empty mapping.

        A missing or unreadable file yields ``{}`` so the canonical models
        validate against the built-in default payload; hard failures surface
        through the required-file checks in ``validate_configs``.
        """
        config_path = self.config_dir / filename
        loaded = u.Cli.yaml_safe_load(config_path)
        return {} if loaded.failure else loaded.value

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
