"""Behavioral tests for ``FlextQualityConfigManager`` and its consumers.

Exercises real YAML loading from the packaged configuration directory and from
``tmp_path`` — no mocks, no patched collaborators. Expected values are read from
the same YAML files the manager validates, never frozen in the test.
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import tm

from flext_quality import FlextQualityConfigManager, t, u


class TestsFlextQualityConfigManager:
    """Contract tests for the documentation configuration manager."""

    @staticmethod
    def _declared(manager: FlextQualityConfigManager, filename: str) -> t.JsonMapping:
        return u.Cli.yaml_safe_load(manager.config_dir / filename).unwrap()

    def test_get_audit_rules_is_cached_across_calls(self, tmp_path: Path) -> None:
        """Repeated lookups return the identical cached configuration object."""
        manager = FlextQualityConfigManager(tmp_path)
        first = manager.resolve_audit_rules()
        second = manager.resolve_audit_rules()
        tm.that(first is second, eq=True)

    def test_get_style_guide_falls_back_to_defaults(self, tmp_path: Path) -> None:
        """An empty config directory yields the built-in style-guide defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        guide = manager.resolve_style_guide()
        tm.that(guide.markdown.heading_style, eq="atx")
        tm.that(guide.accessibility.require_alt_text, eq=True)

    def test_get_validation_config_falls_back_to_defaults(self, tmp_path: Path) -> None:
        """An empty config directory yields the built-in validation defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        validation = manager.resolve_validation_config()
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
        rules = manager.resolve_audit_rules()
        tm.that(rules.quality_thresholds.max_age_days, eq=30)
        tm.that(rules.content_checks.check_freshness, eq=False)

    def test_reload_configs_clears_cached_state(self, tmp_path: Path) -> None:
        """Reloading clears the memoized typed configuration models."""
        manager = FlextQualityConfigManager(tmp_path)
        first_rules = manager.resolve_audit_rules()
        manager.reload_configs()
        second_rules = manager.resolve_audit_rules()
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
            any("Missing required settings file" in issue for issue in issues), eq=False
        )

    def test_default_config_dir_derives_from_package_location(self) -> None:
        """Omitting ``config_dir`` resolves the declared config directory near the package."""
        manager = FlextQualityConfigManager()
        tm.that(str(manager.config_dir), has="config")

    def test_config_dir_accepts_a_string_path(self, tmp_path: Path) -> None:
        """A string ``config_dir`` is normalized into a ``Path``."""
        manager = FlextQualityConfigManager(str(tmp_path))
        tm.that(manager.config_dir, eq=tmp_path)

    def test_validate_configs_reports_invalid_yaml_content(
        self, tmp_path: Path
    ) -> None:
        """Partial YAML configuration validates through the canonical model defaults."""
        (tmp_path / "audit_rules.yaml").write_text(
            "quality_thresholds: {}\n", encoding="utf-8"
        )
        (tmp_path / "style_guide.yaml").write_text("{}\n", encoding="utf-8")
        (tmp_path / "validation_config.yaml").write_text("{}\n", encoding="utf-8")
        manager = FlextQualityConfigManager(tmp_path)
        issues = manager.validate_configs()
        tm.that(issues, eq=[])


__all__: list[str] = ["TestsFlextQualityConfigManager"]
