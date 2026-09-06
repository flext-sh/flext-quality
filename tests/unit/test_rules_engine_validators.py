"""Behavioral tests for the YAML rules engine and the built-in validators.

Exercises ``FlextQualityRulesEngine`` and ``FlextQualityValidators`` against
real files on ``tmp_path`` — no mocks, no patched collaborators.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_quality import (
    FlextQualityRulesEngine,
    FlextQualityRulesLoader,
    FlextQualityValidators,
)
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path

# Built as a concatenation so this fixture literal is never mistaken by
# static scanners for a real suppression directive in this test module.
_IGNORE_MARKER_CONTENT = "value = 1  # type:" + " ignore" + "\n"


class TestsFlextQualityRulesEngine:
    """Contract tests for ``FlextQualityRulesEngine``."""

    @staticmethod
    def _write_rules(tmp_path: Path) -> Path:
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text(
            "rules:\n"
            "  - name: no-todo\n"
            "    type: warning\n"
            "    description: TODO markers are discouraged\n"
            "    pattern: TODO\n"
            "    enabled: true\n"
            "  - name: no-fixme\n"
            "    type: blocking\n"
            "    description: FIXME markers block merge\n"
            "    pattern: FIXME\n"
            "    enabled: true\n",
            encoding="utf-8",
        )
        return rules_path

    def test_get_rules_starts_empty(self) -> None:
        """A freshly constructed engine has no loaded rules."""
        engine = FlextQualityRulesEngine()
        tm.that(engine.get_rules(), eq=[])

    def test_load_rules_populates_engine(self, tmp_path: Path) -> None:
        """Loading rules from YAML makes them retrievable via ``get_rules``."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        result = engine.load_rules()
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=2)
        tm.that(len(engine.get_rules()), eq=2)

    def test_load_rules_explicit_path_overrides_constructor_path(
        self, tmp_path: Path
    ) -> None:
        """An explicit path argument to ``load_rules`` wins over the default."""
        other_path = tmp_path / "other.yaml"
        other_path.write_text(
            "rules:\n"
            "  - name: solo\n"
            "    type: info\n"
            "    description: only rule\n"
            "    pattern: x\n"
            "    enabled: true\n",
            encoding="utf-8",
        )
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        result = engine.load_rules(other_path)
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=1)

    def test_validate_fails_for_missing_path(self, tmp_path: Path) -> None:
        """Validating a nonexistent path reports a descriptive failure."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        result = engine.validate(str(tmp_path / "nowhere.py"))
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="does not exist")

    def test_validate_finds_violations_in_a_single_file(self, tmp_path: Path) -> None:
        """Validating a single Python file surfaces matching-pattern violations."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        target = tmp_path / "module.py"
        target.write_text("# TODO: fix this\nvalue = 1\n", encoding="utf-8")
        result = engine.validate(str(target))
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=1)
        tm.that(result.value[0]["rule"], eq="no-todo")
        tm.that(result.value[0]["severity"], eq="warning")

    def test_validate_ignores_non_python_single_file(self, tmp_path: Path) -> None:
        """A non-``.py`` single file target yields no violations."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        target = tmp_path / "notes.txt"
        target.write_text("TODO: whatever\n", encoding="utf-8")
        result = engine.validate(str(target))
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=[])

    def test_validate_walks_directory_for_python_files(self, tmp_path: Path) -> None:
        """Validating a directory scans every Python file beneath it."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        (tmp_path / "a.py").write_text("# FIXME later\n", encoding="utf-8")
        (tmp_path / "b.py").write_text("clean = True\n", encoding="utf-8")
        result = engine.validate(str(tmp_path))
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=1)
        tm.that(result.value[0]["rule"], eq="no-fixme")

    def test_validate_passes_context_through_to_violations(
        self, tmp_path: Path
    ) -> None:
        """A context mapping is attached to every violation produced."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        target = tmp_path / "module.py"
        target.write_text("# TODO: ctx\n", encoding="utf-8")
        result = engine.validate(str(target), context={"stage": "ci"})
        violation_context = result.value[0].get("context")
        assert isinstance(violation_context, dict)
        tm.that(violation_context.get("stage"), eq="ci")

    def test_validate_content_checks_disabled_rule_is_skipped(
        self, tmp_path: Path
    ) -> None:
        """A disabled rule never contributes a violation via ``validate_content``."""
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text(
            "rules:\n"
            "  - name: disabled-rule\n"
            "    type: warning\n"
            "    description: never fires\n"
            "    pattern: TODO\n"
            "    enabled: false\n",
            encoding="utf-8",
        )
        engine = FlextQualityRulesEngine(rules_path)
        result = engine.validate_content("# TODO here")
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=[])

    def test_validate_content_lazy_loads_rules_on_first_use(
        self, tmp_path: Path
    ) -> None:
        """``validate_content`` triggers a lazy ``load_rules`` when unloaded."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        result = engine.validate_content("# TODO now", filename="in-memory.py")
        tm.that(result.success, eq=True)
        tm.that(result.value[0]["file"], eq="in-memory.py")

    def test_validate_content_fails_when_rules_missing(self, tmp_path: Path) -> None:
        """A missing rules file surfaces as a failure from ``validate_content``."""
        engine = FlextQualityRulesEngine(tmp_path / "absent.yaml")
        result = engine.validate_content("anything")
        tm.that(result.failure, eq=True)

    def test_validate_reports_read_error_for_invalid_utf8_file(
        self, tmp_path: Path
    ) -> None:
        """An undecodable target file surfaces as a file-read-error violation."""
        engine = FlextQualityRulesEngine(self._write_rules(tmp_path))
        bad_file = tmp_path / "invalid.py"
        bad_file.write_bytes(b"\xff\xfe# not valid utf-8\n")
        result = engine.validate(str(bad_file))
        tm.that(result.success, eq=True)
        tm.that(result.value[0]["rule"], eq="file-read-error")


class TestsFlextQualityValidators:
    """Contract tests for the built-in validator registry and validators."""

    def test_pattern_validator_reports_configured_name(self) -> None:
        """The pattern validator exposes its constructor-independent name."""
        validator = FlextQualityValidators.Pattern({"greeting": "hello"})
        tm.that(validator.name, eq="pattern")

    def test_pattern_validator_matches_configured_pattern(self) -> None:
        """Each configured named pattern produces a distinct violation."""
        validator = FlextQualityValidators.Pattern({"greeting": "hello"})
        result = validator.validate("hello world\ngoodbye", file_path="greet.py")
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=1)
        tm.that(result.value[0]["rule"], eq="pattern-greeting")
        tm.that(result.value[0]["file"], eq="greet.py")

    def test_pattern_validator_defaults_filename_for_string_content(self) -> None:
        """Content validated without a path is attributed to ``<string>``."""
        validator = FlextQualityValidators.Pattern({"greeting": "hello"})
        result = validator.validate("hello there")
        tm.that(result.value[0]["file"], eq="<string>")

    def test_forbidden_pattern_validator_has_dedicated_name(self) -> None:
        """The forbidden-pattern validator overrides the base validator name."""
        validator = FlextQualityValidators.ForbiddenPattern()
        tm.that(validator.name, eq="forbidden-patterns")

    def test_forbidden_pattern_validator_flags_a_forbidden_marker(self) -> None:
        """A forbidden suppression marker in content is flagged as a violation."""
        validator = FlextQualityValidators.ForbiddenPattern()
        result = validator.validate(_IGNORE_MARKER_CONTENT)
        tm.that(result.success, eq=True)
        tm.that(len(result.value) >= 1, eq=True)

    def test_tier_validator_has_dedicated_name(self) -> None:
        """The tier validator exposes the ``tier`` validator name."""
        validator = FlextQualityValidators.Tier()
        tm.that(validator.name, eq="tier")

    def test_tier_validator_skips_content_without_a_path(self) -> None:
        """Tier validation is a no-op when no file path is supplied."""
        validator = FlextQualityValidators.Tier()
        result = validator.validate("from flext_quality.api import FlextQuality")
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=[])

    def test_tier_validator_skips_files_outside_known_tiers(
        self, tmp_path: Path
    ) -> None:
        """A file whose name maps to no known tier yields no violations."""
        validator = FlextQualityValidators.Tier()
        target = tmp_path / "random_module.py"
        result = validator.validate(
            "from flext_quality.services import Something", file_path=target
        )
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=[])

    def test_tier_validator_flags_violation_in_constants_module(
        self, tmp_path: Path
    ) -> None:
        """A tier-0 ``constants.py`` importing from services is flagged."""
        validator = FlextQualityValidators.Tier()
        target = tmp_path / "constants.py"
        content = "from flext_quality.services import helper\n"
        result = validator.validate(content, file_path=str(target))
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=1)
        tm.that(result.value[0]["rule"], eq="tier-violation")

    def test_registry_registers_default_validators(self) -> None:
        """A fresh registry ships with the forbidden-pattern and tier validators."""
        registry = FlextQualityValidators.Registry()
        names = {validator.name for validator in registry.all()}
        tm.that(names, eq={"forbidden-patterns", "tier"})

    def test_registry_get_returns_none_for_unknown_validator(self) -> None:
        """Looking up an unregistered validator name returns ``None``."""
        registry = FlextQualityValidators.Registry()
        tm.that(registry.get("does-not-exist"), eq=None)

    def test_registry_get_returns_registered_validator(self) -> None:
        """A registered validator is retrievable by its own name."""
        registry = FlextQualityValidators.Registry()
        validator = registry.get("tier")
        tm.that(validator is not None, eq=True)

    def test_registry_register_adds_a_custom_validator(self) -> None:
        """Registering a validator makes it visible to ``all()`` and ``get()``."""
        registry = FlextQualityValidators.Registry()
        custom = FlextQualityValidators.Pattern({"marker": "XXX"})
        registry.register(custom)
        tm.that(registry.get("pattern") is custom, eq=True)
        tm.that(len(registry.all()), eq=3)

    def test_registry_validate_all_aggregates_every_validator(self) -> None:
        """``validate_all`` merges violations from every registered validator."""
        registry = FlextQualityValidators.Registry()
        result = registry.validate_all(_IGNORE_MARKER_CONTENT)
        tm.that(result.success, eq=True)
        tm.that(len(result.value) >= 1, eq=True)


class TestsFlextQualityRulesLoader:
    """Contract tests for ``FlextQualityRulesLoader``."""

    def test_load_fails_for_missing_file(self, tmp_path: Path) -> None:
        """Loading a nonexistent rules file reports a descriptive failure."""
        loader = FlextQualityRulesLoader()
        result = loader.load(tmp_path / "missing.yaml")
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="not found")

    def test_load_fails_for_non_mapping_root(self, tmp_path: Path) -> None:
        """A YAML document whose root is not a mapping is rejected.

        The underlying YAML round-trip loader itself enforces a mapping
        root before this loader's own dict check ever runs.
        """
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text("- just\n- a\n- list\n", encoding="utf-8")
        loader = FlextQualityRulesLoader()
        result = loader.load(rules_path)
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="must be a mapping")

    def test_load_fails_when_rules_key_is_not_a_list(self, tmp_path: Path) -> None:
        """A ``rules`` key that is not a list is rejected."""
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text("rules: not-a-list\n", encoding="utf-8")
        loader = FlextQualityRulesLoader()
        result = loader.load(rules_path)
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="must be a list")

    def test_load_fails_for_rule_missing_name(self, tmp_path: Path) -> None:
        """A rule entry without a ``name`` is rejected with its index."""
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text(
            "rules:\n  - type: warning\n    description: no name\n",
            encoding="utf-8",
        )
        loader = FlextQualityRulesLoader()
        result = loader.load(rules_path)
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="missing 'name'")

    def test_load_fails_for_invalid_rule_type(self, tmp_path: Path) -> None:
        """A rule declaring an unknown ``type`` is rejected."""
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text(
            "rules:\n  - name: bad-type\n    type: not-a-real-type\n",
            encoding="utf-8",
        )
        loader = FlextQualityRulesLoader()
        result = loader.load(rules_path)
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="invalid type")

    def test_load_defaults_optional_fields(self, tmp_path: Path) -> None:
        """A minimal rule entry gets safe defaults for optional fields."""
        rules_path = tmp_path / "rules.yaml"
        rules_path.write_text(
            "rules:\n  - name: minimal\n    type: info\n", encoding="utf-8"
        )
        loader = FlextQualityRulesLoader()
        result = loader.load(rules_path)
        tm.that(result.success, eq=True)
        rule = result.value[0]
        tm.that(rule.description, eq="")
        tm.that(rule.action, eq="warn")
        tm.that(rule.pattern, eq=None)
        tm.that(rule.enabled, eq=True)

    def test_load_multiple_aggregates_rules_across_files(
        self, tmp_path: Path
    ) -> None:
        """``load_multiple`` concatenates rules loaded from every given file."""
        first = tmp_path / "first.yaml"
        first.write_text(
            "rules:\n  - name: one\n    type: info\n", encoding="utf-8"
        )
        second = tmp_path / "second.yaml"
        second.write_text(
            "rules:\n  - name: two\n    type: warning\n", encoding="utf-8"
        )
        loader = FlextQualityRulesLoader()
        result = loader.load_multiple([first, second])
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=2)

    def test_load_multiple_fails_fast_and_names_the_offending_file(
        self, tmp_path: Path
    ) -> None:
        """``load_multiple`` reports which file failed to load."""
        good = tmp_path / "good.yaml"
        good.write_text("rules:\n  - name: ok\n    type: info\n", encoding="utf-8")
        missing = tmp_path / "missing.yaml"
        loader = FlextQualityRulesLoader()
        result = loader.load_multiple([good, missing])
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has=str(missing))


__all__: list[str] = [
    "TestsFlextQualityRulesEngine",
    "TestsFlextQualityRulesLoader",
    "TestsFlextQualityValidators",
]
