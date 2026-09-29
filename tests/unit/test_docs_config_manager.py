"""Behavioral tests for ``FlextQualityConfigManager`` and its consumers.

Exercises real YAML loading from the packaged configuration directory and from
``tmp_path`` — no mocks, no patched collaborators. Expected values are read from
the same YAML files the manager validates, never frozen in the test.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from flext_tests import tm

from flext_quality import (
    FlextQualityConfigManager,
    FlextQualityDocumentationAuditor,
    FlextQualityLinkChecker,
    FlextQualityStyleValidator,
    t,
    u,
)


class TestsFlextQualityConfigManager:
    """Contract tests for the documentation configuration manager."""

    @staticmethod
    def _declared(manager: FlextQualityConfigManager, filename: str) -> t.JsonMapping:
        return u.Cli.yaml_safe_load(manager.config_dir / filename).unwrap()

    def test_default_config_dir_holds_every_declared_file(self) -> None:
        """Omitting ``config_dir`` selects the packaged configuration directory."""
        manager = FlextQualityConfigManager()
        for filename in (
            "audit_rules.yaml",
            "style_guide.yaml",
            "validation_config.yaml",
        ):
            tm.that((manager.config_dir / filename).is_file(), eq=True)

    def test_audit_rules_match_the_declared_yaml(self) -> None:
        """Audit rules are the validated sections of ``audit_rules.yaml``."""
        manager = FlextQualityConfigManager()
        declared = self._declared(manager, "audit_rules.yaml")
        rules = manager.resolve_audit_rules()
        for section in ("quality_thresholds", "content_checks", "severity_levels"):
            tm.that(getattr(rules, section).model_dump(), eq=declared[section])

    def test_style_guide_matches_the_declared_yaml(self) -> None:
        """The style guide is the validated sections of ``style_guide.yaml``."""
        manager = FlextQualityConfigManager()
        declared = self._declared(manager, "style_guide.yaml")
        guide = manager.resolve_style_guide()
        for section in ("markdown", "accessibility", "formatting", "headings"):
            tm.that(getattr(guide, section).model_dump(), eq=declared[section])

    def test_validation_config_matches_the_declared_yaml(self) -> None:
        """Link and content settings come from ``validation_config.yaml``."""
        manager = FlextQualityConfigManager()
        declared = self._declared(manager, "validation_config.yaml")
        validation = manager.resolve_validation_config()
        adapter = t.json_mapping_adapter()
        link = validation.link_validation.model_dump()
        declared_link = adapter.validate_python(declared["link_validation"])
        tm.that(link, eq={key: declared_link[key] for key in link})
        content = validation.content_analysis.model_dump()
        declared_content = adapter.validate_python(declared["content_analysis"])
        tm.that(content, eq={key: declared_content[key] for key in content})

    def test_declared_configuration_carries_no_retry_policy(self) -> None:
        """Neither the YAML nor the model declares a retry policy."""
        manager = FlextQualityConfigManager()
        for filename in ("audit_rules.yaml", "validation_config.yaml"):
            text = (manager.config_dir / filename).read_text(encoding="utf-8")
            tm.that("retry_" in text, eq=False)
        link = manager.resolve_validation_config().link_validation.model_dump()
        tm.that(any(key.startswith("retry_") for key in link), eq=False)

    def test_resolved_configuration_is_cached(self) -> None:
        """Repeated lookups return the identical validated configuration."""
        manager = FlextQualityConfigManager()
        tm.that(manager.resolve_audit_rules() is manager.resolve_audit_rules(), eq=True)

    def test_config_dir_accepts_a_string_path(self, tmp_path: Path) -> None:
        """A string ``config_dir`` is normalized into a ``Path``."""
        manager = FlextQualityConfigManager(str(tmp_path))
        tm.that(manager.config_dir, eq=tmp_path)

    def test_missing_file_fails_loudly(self, tmp_path: Path) -> None:
        """An absent configuration file raises instead of loading defaults."""
        manager = FlextQualityConfigManager(tmp_path)
        with pytest.raises(RuntimeError, match=r"audit_rules\.yaml"):
            manager.resolve_audit_rules()

    def test_incomplete_section_fails_loudly(self, tmp_path: Path) -> None:
        """A section missing a declared key is rejected, never defaulted."""
        packaged = FlextQualityConfigManager().config_dir
        shutil.copy(packaged / "style_guide.yaml", tmp_path / "style_guide.yaml")
        manager = FlextQualityConfigManager(tmp_path)
        tm.that(
            manager.resolve_style_guide(),
            eq=FlextQualityConfigManager(packaged).resolve_style_guide(),
        )
        (tmp_path / "audit_rules.yaml").write_text(
            "quality_thresholds: {}\n", encoding="utf-8"
        )
        with pytest.raises(ValueError, match="quality_thresholds"):
            manager.resolve_audit_rules()


class TestsFlextQualityConfigConsumers:
    """The documentation tools consume the manager's validated configuration."""

    def test_consumers_fail_loudly_without_configuration(self, tmp_path: Path) -> None:
        """Every tool raises on a directory without configuration files."""
        for tool in (
            FlextQualityDocumentationAuditor,
            FlextQualityStyleValidator,
            FlextQualityLinkChecker,
        ):
            with pytest.raises(RuntimeError):
                tool(tmp_path)

    def test_auditor_uses_the_declared_configuration(self) -> None:
        """The auditor exposes the manager's validated configuration."""
        manager = FlextQualityConfigManager()
        auditor = FlextQualityDocumentationAuditor()
        tm.that(auditor.audit_rules, eq=manager.resolve_audit_rules())
        tm.that(auditor.style_guide, eq=manager.resolve_style_guide())
        tm.that(auditor.validation_config, eq=manager.resolve_validation_config())

    def test_style_validator_uses_the_declared_style_guide(
        self, tmp_path: Path
    ) -> None:
        """Line-length findings follow the declared formatting limit."""
        limit = FlextQualityConfigManager().resolve_style_guide().formatting
        document = tmp_path / "a" / "b" / "doc.md"
        document.parent.mkdir(parents=True)
        document.write_text(
            "# Title\n\n" + "x" * (limit.max_line_length + 1) + "\n", encoding="utf-8"
        )
        validator = FlextQualityStyleValidator()
        results = validator.validate_file(document)
        tm.that(
            [v.type for v in results.violations if v.type == "line_too_long"],
            eq=["line_too_long"],
        )
        tm.that(validator.results.files_checked, eq=1)

    def test_link_checker_records_links_with_their_origin(self, tmp_path: Path) -> None:
        """Inline and reference links become canonical link records."""
        document = tmp_path / "doc.md"
        document.write_text(
            "# Links\n\n[inline](https://example.org)\n\n[ref][one]\n\n"
            "[one]: https://example.com\n",
            encoding="utf-8",
        )
        checker = FlextQualityLinkChecker()
        tm.that(
            checker.settings,
            eq=FlextQualityConfigManager().resolve_validation_config().link_validation,
        )
        records = checker.find_all_links([document])
        tm.that(
            [(r.url, r.line_number, r.reference) for r in records],
            eq=[("https://example.org", 3, None), ("https://example.com", None, "one")],
        )

    def test_unsupported_report_formats_fail_loudly(self) -> None:
        """Only the declared report formats render; anything else raises."""
        for tool in (FlextQualityStyleValidator(), FlextQualityLinkChecker()):
            with pytest.raises(ValueError, match="Unsupported report format"):
                tool.generate_report("xml")
