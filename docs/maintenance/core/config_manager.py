"""FLEXT Quality Documentation Maintenance - Configuration Management.

Centralized configuration management system for all maintenance components.
Handles loading, validation, and access to configuration files.
"""

from pathlib import Path
from typing import Any

import yaml
from flext_core import FlextCore


class AuditRules:
    """Configuration for audit rules and thresholds."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize audit rules configuration."""
        self.quality_thresholds = data.get("quality_thresholds", {})
        self.content_checks = data.get("content_checks", {})
        self.link_checks = data.get("link_checks", {})
        self.style_checks = data.get("style_checks", {})
        self.accessibility_checks = data.get("accessibility_checks", {})

    def get_threshold(self, key: str, default: object = None) -> object:
        """Get a quality threshold value."""
        return self.quality_thresholds.get(key, default)

    def is_check_enabled(self, check_type: str, check_name: str) -> bool:
        """Check if a specific audit check is enabled."""
        checks = getattr(self, f"{check_type}_checks", {})
        return checks.get(check_name, False)


class StyleGuide:
    """Configuration for style and formatting guidelines."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize style guidelines configuration."""
        self.markdown = data.get("markdown", {})
        self.accessibility = data.get("accessibility", {})
        self.formatting = data.get("formatting", {})

    def get_markdown_rule(self, rule: str, default: object = None) -> object:
        """Get a markdown formatting rule."""
        return self.markdown.get(rule, default)

    def get_accessibility_rule(self, rule: str, default: object = None) -> object:
        """Get an accessibility rule."""
        return self.accessibility.get(rule, default)


class ValidationConfig:
    """Configuration for validation operations."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize validation configuration."""
        self.link_validation = data.get("link_validation", {})
        self.content_validation = data.get("content_validation", {})
        self.image_validation = data.get("image_validation", {})
        self.accessibility_validation = data.get("accessibility_validation", {})
        self.security_validation = data.get("security_validation", {})
        self.performance_validation = data.get("performance_validation", {})

    def get_link_setting(self, setting: str, default: object = None) -> object:
        """Get a link validation setting."""
        return self.link_validation.get(setting, default)

    def get_content_setting(self, setting: str, default: object = None) -> object:
        """Get a content validation setting."""
        return self.content_validation.get(setting, default)


class ConfigManager:
    """Centralized configuration management for the documentation maintenance system."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory containing configuration files. If None,
                       uses the default config directory.

        """
        if config_dir is None:
            # Find config directory relative to this file
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        self._cache: dict[str, Any] = {}
        self._audit_rules: AuditRules | None = None
        self._style_guide: StyleGuide | None = None
        self._validation_config: ValidationConfig | None = None

    def get_audit_rules(self) -> AuditRules:
        """Get audit rules configuration."""
        if self._audit_rules is None:
            data = self._load_config_file("audit_rules.yaml")
            self._audit_rules = AuditRules(data)
        return self._audit_rules

    def get_style_guide(self) -> StyleGuide:
        """Get style guide configuration."""
        if self._style_guide is None:
            data = self._load_config_file("style_guide.yaml")
            self._style_guide = StyleGuide(data)
        return self._style_guide

    def get_validation_config(self) -> ValidationConfig:
        """Get validation configuration."""
        if self._validation_config is None:
            data = self._load_config_file("validation_config.yaml")
            self._validation_config = ValidationConfig(data)
        return self._validation_config

    def get_config(self, name: str) -> dict[str, Any]:
        """Get a configuration file by name."""
        if name not in self._cache:
            self._cache[name] = self._load_config_file(f"{name}.yaml")
        return self._cache[name]

    def _load_config_file(self, filename: str) -> dict[str, Any]:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename

        try:
            with config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return self._get_default_config(filename)
        except yaml.YAMLError:
            return self._get_default_config(filename)
        except Exception:
            return self._get_default_config(filename)

    def _get_default_config(self, filename: str) -> dict[str, Any]:
        """Get default configuration for a file."""
        defaults = {
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
                "link_validation": {
                    "timeout": 10,
                    "retry_attempts": 3,
                    "user_agent": "FLEXT-Quality-Doc-Validator/1.0",
                    "check_external": True,
                    "check_internal": True,
                    "check_images": True,
                },
                "content_analysis": {
                    "min_section_depth": 2,
                    "required_sections": ["Overview", "Installation", "Usage"],
                    "check_todos": True,
                    "check_fixmes": True,
                },
            },
        }

        return defaults.get(filename, {})

    def reload_configs(self) -> None:
        """Reload all configurations from disk."""
        self._cache.clear()
        self._audit_rules = None
        self._style_guide = None
        self._validation_config = None

    def validate_configs(self) -> FlextCore.Types.StringList:
        """Validate all configuration files and return any issues."""
        # Check required config files exist
        required_files = [
            "audit_rules.yaml",
            "style_guide.yaml",
            "validation_config.yaml",
        ]
        issues = [
            f"Missing required config file: {filename}"
            for filename in required_files
            if not (self.config_dir / filename).exists()
        ]

        # Validate audit rules structure
        try:
            audit_rules = self.get_audit_rules()
            if not audit_rules.quality_thresholds:
                issues.append("Audit rules missing quality_thresholds section")
        except Exception as e:
            issues.append(f"Invalid audit_rules.yaml: {e}")

        # Validate style guide structure
        try:
            style_guide = self.get_style_guide()
            if not style_guide.markdown:
                issues.append("Style guide missing markdown section")
        except Exception as e:
            issues.append(f"Invalid style_guide.yaml: {e}")

        # Validate validation config structure
        try:
            validation_config = self.get_validation_config()
            if not validation_config.link_validation:
                issues.append("Validation config missing link_validation section")
        except Exception as e:
            issues.append(f"Invalid validation_config.yaml: {e}")

        return issues

    def get_all_configs(self) -> dict[str, Any]:
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

    def save_config(self, name: str, data: dict[str, Any]) -> bool:
        """Save a configuration to file."""
        try:
            config_path = self.config_dir / f"{name}.yaml"
            self.config_dir.mkdir(parents=True, exist_ok=True)

            with config_path.open("w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)

            # Clear cache for this config
            if name in self._cache:
                del self._cache[name]

            # Reset specific config objects
            if name == "audit_rules":
                self._audit_rules = None
            elif name == "style_guide":
                self._style_guide = None
            elif name == "validation_config":
                self._validation_config = None

            return True
        except Exception:
            return False
