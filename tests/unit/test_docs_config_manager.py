"""Behavioral tests for ``FlextQualityConfigManager``.

Exercises real YAML loading, defaulting, caching and validation against
``tmp_path`` — no mocks, no patched collaborators.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_quality import FlextQualityConfigManager
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextQualityConfigManager:
    """Contract tests for the documentation configuration manager."""

    def test_get_audit_rules_falls_back_to_defaults_for_empty_dir(
        self, tmp_path: Path
    ) -> None:
        """An empty config directory yields the built-in audit-rule defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.quality_thresholds.max_age_days, eq=90)
        tm.that(rules.content_checks.check_freshness, eq=True)

    def test_get_audit_rules_is_cached_across_calls(self, tmp_path: Path) -> None:
        """Repeated lookups return the identical cached configuration object."""
        manager = FlextQualityConfigManager(tmp_path)
        first = manager.get_audit_rules()
        second = manager.get_audit_rules()
        tm.that(first is second, eq=True)

    def test_get_style_guide_falls_back_to_defaults(self, tmp_path: Path) -> None:
        """An empty config directory yields the built-in style-guide defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        guide = manager.get_style_guide()
        tm.that(guide.markdown.heading_style, eq="atx")
        tm.that(guide.accessibility.require_alt_text, eq=True)

    def test_get_validation_config_falls_back_to_defaults(
        self, tmp_path: Path
    ) -> None:
        """An empty config directory yields the built-in validation defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        validation = manager.get_validation_config()
        tm.that(validation.link_validation.timeout, eq=10)

    def test_get_audit_rules_reads_real_yaml_overrides(self, tmp_path: Path) -> None:
        """A real YAML file on disk overrides the built-in threshold defaults."""
        (tmp_path / "audit_rules.yaml").write_text(
            "quality_thresholds:\n"
            "  max_age_days: 30\n"
            "  min_word_count: 50\n"
            "content_checks:\n"
            "  check_freshness: false\n",
            encoding="utf-8",
        )
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.quality_thresholds.max_age_days, eq=30)
        tm.that(rules.content_checks.check_freshness, eq=False)

    def test_get_config_caches_raw_mapping_by_name(self, tmp_path: Path) -> None:
        """``get_config`` loads and caches the raw section mapping by name."""
        (tmp_path / "custom.yaml").write_text(
            "section:\n  flag: true\n  items:\n    - a\n    - b\n",
            encoding="utf-8",
        )
        manager = FlextQualityConfigManager(tmp_path)
        data = manager.get_config("custom")
        tm.that(data.get("section", {}).get("flag"), eq=True)
        tm.that(data.get("section", {}).get("items"), eq=["a", "b"])
        tm.that(manager.get_config("custom") is data, eq=True)

    def test_get_config_returns_default_for_missing_file(self, tmp_path: Path) -> None:
        """A configuration name with no matching file loads its safe default."""
        manager = FlextQualityConfigManager(tmp_path)
        tm.that(manager.get_config("audit_rules"), has="quality_thresholds")
        tm.that(manager.get_config("unknown_config"), eq={})

    def test_reload_configs_clears_cached_state(self, tmp_path: Path) -> None:
        """Reloading clears the memoized audit/style/validation/config caches."""
        manager = FlextQualityConfigManager(tmp_path)
        first_rules = manager.get_audit_rules()
        manager.get_config("audit_rules")
        manager.reload_configs()
        second_rules = manager.get_audit_rules()
        tm.that(first_rules is second_rules, eq=False)

    def test_validate_configs_reports_missing_required_files(
        self, tmp_path: Path
    ) -> None:
        """Validation reports every required settings file that is absent."""
        manager = FlextQualityConfigManager(tmp_path)
        issues = manager.validate_configs()
        tm.that(len(issues) >= 3, eq=True)
        tm.that(any("audit_rules.yaml" in issue for issue in issues), eq=True)

    def test_validate_configs_passes_when_files_present_with_defaults(
        self, tmp_path: Path
    ) -> None:
        """With every required file present, no missing-file issues remain."""
        (tmp_path / "audit_rules.yaml").write_text("{}\n", encoding="utf-8")
        (tmp_path / "style_guide.yaml").write_text("{}\n", encoding="utf-8")
        (tmp_path / "validation_config.yaml").write_text("{}\n", encoding="utf-8")
        manager = FlextQualityConfigManager(tmp_path)
        issues = manager.validate_configs()
        tm.that(
            any("Missing required settings file" in issue for issue in issues),
            eq=False,
        )

    def test_get_all_configs_returns_composite_mapping(self, tmp_path: Path) -> None:
        """``get_all_configs`` composes typed and raw sections for every file."""
        manager = FlextQualityConfigManager(tmp_path)
        composite = manager.get_all_configs()
        tm.that(composite, has=("audit_rules", "style_guide", "validation_config"))
        tm.that(composite, has="raw_configs")

    def test_default_config_dir_derives_from_package_location(self) -> None:
        """Omitting ``config_dir`` resolves a settings directory near the package."""
        manager = FlextQualityConfigManager()
        tm.that(str(manager.config_dir), has="settings")

    def test_config_dir_accepts_a_string_path(self, tmp_path: Path) -> None:
        """A string ``config_dir`` is normalized into a ``Path`` internally."""
        manager = FlextQualityConfigManager(str(tmp_path))
        tm.that(manager.config_dir, eq=tmp_path)

    def test_audit_rules_get_threshold_reads_a_known_field(
        self, tmp_path: Path
    ) -> None:
        """``get_threshold`` reads a real field from the quality thresholds."""
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.get_threshold("max_age_days"), eq=90)

    def test_audit_rules_get_threshold_falls_back_to_default(
        self, tmp_path: Path
    ) -> None:
        """An unknown threshold key returns the supplied default value."""
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.get_threshold("not_a_field", default=42), eq=42)

    def test_audit_rules_is_check_enabled_for_each_check_type(
        self, tmp_path: Path
    ) -> None:
        """``is_check_enabled`` dispatches across every supported check type.

        The built-in defaults (``_get_default_config``) enable every listed
        link/style/accessibility check, so each real default is ``True``;
        only an unrecognized check type falls through to ``False``.
        """
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.is_check_enabled("content", "check_freshness"), eq=True)
        tm.that(rules.is_check_enabled("link", "check_external"), eq=True)
        tm.that(rules.is_check_enabled("style", "check_formatting"), eq=True)
        tm.that(rules.is_check_enabled("accessibility", "check_alt_text"), eq=True)
        tm.that(rules.is_check_enabled("link", "no-such-check"), eq=False)
        tm.that(rules.is_check_enabled("unknown-type", "anything"), eq=False)

    def test_audit_rules_is_check_enabled_reads_real_link_check_yaml(
        self, tmp_path: Path
    ) -> None:
        """A real YAML-configured link check overrides the enabled default."""
        (tmp_path / "audit_rules.yaml").write_text(
            "link_checks:\n  check_external: false\n", encoding="utf-8"
        )
        manager = FlextQualityConfigManager(tmp_path)
        rules = manager.get_audit_rules()
        tm.that(rules.is_check_enabled("link", "check_external"), eq=False)

    def test_style_guide_get_markdown_rule(self, tmp_path: Path) -> None:
        """``get_markdown_rule`` reads a real field from the markdown config."""
        manager = FlextQualityConfigManager(tmp_path)
        guide = manager.get_style_guide()
        tm.that(guide.get_markdown_rule("heading_style"), eq="atx")
        tm.that(guide.get_markdown_rule("not_a_field", default="x"), eq="x")

    def test_style_guide_get_accessibility_rule(self, tmp_path: Path) -> None:
        """``get_accessibility_rule`` reads a real field from the accessibility config."""
        manager = FlextQualityConfigManager(tmp_path)
        guide = manager.get_style_guide()
        tm.that(guide.get_accessibility_rule("require_alt_text"), eq=True)
        tm.that(guide.get_accessibility_rule("not_a_field", default=False), eq=False)

    def test_validation_config_get_link_setting(self, tmp_path: Path) -> None:
        """``get_link_setting`` reads a real field from the link validation config."""
        manager = FlextQualityConfigManager(tmp_path)
        validation = manager.get_validation_config()
        tm.that(validation.get_link_setting("timeout"), eq=10)
        tm.that(validation.get_link_setting("not_a_field", default=1), eq=1)

    def test_validation_config_get_content_setting(self, tmp_path: Path) -> None:
        """``get_content_setting`` reads from the raw content-validation mapping."""
        manager = FlextQualityConfigManager(tmp_path)
        validation = manager.get_validation_config()
        tm.that(validation.get_content_setting("missing", default="fallback"), eq="fallback")

    def test_as_section_coerces_list_items_to_strings(self, tmp_path: Path) -> None:
        """A YAML list value is normalized into a list of strings."""
        (tmp_path / "custom.yaml").write_text(
            "section:\n  items:\n    - 1\n    - true\n    - text\n",
            encoding="utf-8",
        )
        manager = FlextQualityConfigManager(tmp_path)
        data = manager.get_config("custom")
        tm.that(data.get("section", {}).get("items"), eq=["1", "True", "text"])

    def test_validate_configs_reports_invalid_yaml_content(
        self, tmp_path: Path
    ) -> None:
        """Configuration missing a required attribute is reported as an issue."""
        (tmp_path / "audit_rules.yaml").write_text(
            "quality_thresholds: {}\n", encoding="utf-8"
        )
        (tmp_path / "style_guide.yaml").write_text("{}\n", encoding="utf-8")
        (tmp_path / "validation_config.yaml").write_text("{}\n", encoding="utf-8")
        manager = FlextQualityConfigManager(tmp_path)
        issues = manager.validate_configs()
        tm.that(issues, eq=[])


__all__: list[str] = ["TestsFlextQualityConfigManager"]
