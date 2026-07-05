"""Behavioral tests for the FlextQuality public API facade.

Every test exercises the observable public contract of ``FlextQuality`` and its
shared ``quality`` alias: the ``r[T]`` outcome of fallible operations, returned
values, and public configuration state. No private attributes, internal
collaborators, or implementation details are touched.
"""

from __future__ import annotations

import io
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest
from flext_tests import tm

from flext_quality import FlextQuality, p, quality, t


class TestsFlextQualityApi:
    """Behavioral contract for the FlextQuality facade."""

    @pytest.fixture(autouse=True)
    def _restore_settings(self) -> Iterator[None]:
        """Snapshot and restore shared settings mutated by behavioral tests."""
        settings = FlextQuality().settings
        rules_dir = settings.rules_dir
        max_function_length = settings.max_function_length
        max_class_length = settings.max_class_length
        yield
        settings.rules_dir = rules_dir
        settings.max_function_length = max_function_length
        settings.max_class_length = max_class_length

    # -- construction / status -------------------------------------------

    def test_facade_constructs_without_arguments(self) -> None:
        """FlextQuality() instantiates and reports a successful status."""
        result = FlextQuality().fetch_status()
        tm.that(result.success, eq=True)
        tm.that(result.value, has="name")

    def test_quality_alias_is_a_ready_facade(self) -> None:
        """The shared ``quality`` alias exposes the same status contract."""
        result = quality.fetch_status()
        tm.that(result.success, eq=True)
        tm.that(result.value, has="name")

    def test_fetch_status_exposes_full_snapshot_contract(self) -> None:
        """fetch_status returns a mapping with the promised public keys."""
        status = FlextQuality().fetch_status().value
        tm.that(status, is_=dict)
        tm.that(status, has="name")
        tm.that(status, has="version")
        tm.that(status, has="settings")
        tm.that(status, has="hooks_registered")

    def test_fetch_status_is_idempotent(self) -> None:
        """Repeated status snapshots report the same name and version."""
        service = FlextQuality()
        first = service.fetch_status().value
        second = service.fetch_status().value
        tm.that(first["name"], eq=second["name"])
        tm.that(first["version"], eq=second["version"])

    def test_execute_delegates_to_status(self) -> None:
        """The default execute() operation yields the status snapshot."""
        result = FlextQuality().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, has="name")

    # -- configuration validation ----------------------------------------

    def test_validate_configuration_succeeds_with_defaults(self) -> None:
        """Default thresholds validate successfully to True."""
        result = FlextQuality().validate_configuration()
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=True)

    def test_validate_configuration_fails_when_function_exceeds_class_limit(
        self,
    ) -> None:
        """max_function_length greater than max_class_length is rejected."""
        service = FlextQuality()
        service.settings.max_function_length = 500
        service.settings.max_class_length = 100
        result = service.validate_configuration()
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="max_function_length")

    # -- hook output formatting ------------------------------------------

    @pytest.mark.parametrize(
        ("continue_exec", "expected"),
        [
            (True, '"continue":true'),
            (False, '"continue":false'),
        ],
    )
    def test_format_hook_output_encodes_continue_flag(
        self,
        *,
        continue_exec: bool,
        expected: str,
    ) -> None:
        """The continue flag is serialized into the JSON output string."""
        output = FlextQuality().format_hook_output(continue_exec=continue_exec).value
        tm.that(output, is_=str)
        tm.that(output, has=expected)

    def test_format_hook_output_includes_message(self) -> None:
        """A provided message is embedded in the formatted output."""
        output = (
            FlextQuality()
            .format_hook_output(continue_exec=True, message="Test message")
            .value
        )
        tm.that(output, has='"continue":true')
        tm.that(output, has="Test message")

    def test_format_hook_output_includes_blocked_reason(self) -> None:
        """A blocked reason is emitted with continue disabled."""
        output = (
            FlextQuality()
            .format_hook_output(
                continue_exec=False,
                blocked_reason="Blocked for testing",
            )
            .value
        )
        tm.that(output, has='"continue":false')
        tm.that(output, has="Blocked for testing")

    def test_fetch_hook_config_json_returns_empty_object(self) -> None:
        """With no hooks configured the config JSON is an empty object."""
        result = FlextQuality().fetch_hook_config_json()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=str)
        tm.that(result.value, eq="{}")

    # -- hook execution ---------------------------------------------------

    def test_execute_hook_succeeds_for_known_event(self) -> None:
        """A known event with no registered hooks continues execution."""
        result = FlextQuality().execute_hook("PreToolUse", {"tool_name": "Edit"})
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue"), eq=True)

    def test_execute_hook_fails_for_unknown_event(self) -> None:
        """An unknown event name yields a failure describing the problem."""
        result = FlextQuality().execute_hook("UnknownEvent", {})
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="Unknown event")

    # -- rule loading -----------------------------------------------------

    def test_load_rules_parses_definitions_from_yaml_file(self) -> None:
        """load_rules returns the rule definitions declared in a YAML file."""
        rules_yaml = (
            "\nrules:\n  - name: test-rule\n    type: warning\n"
            '    description: Test rule\n    pattern: "test"\n    enabled: true\n'
        )
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".yaml",
            delete=False,
        ) as handle:
            handle.write(rules_yaml)
            rules_path = Path(handle.name)
        try:
            result = FlextQuality().load_rules(rules_path)
            tm.that(result.success, eq=True)
            tm.that(len(result.value), eq=1)
            tm.that(result.value[0].name, eq="test-rule")
        finally:
            rules_path.unlink()

    def test_load_rules_fails_for_missing_file(self) -> None:
        """load_rules reports a not-found failure for a nonexistent path."""
        result = FlextQuality().load_rules(Path("/nonexistent/rules.yaml"))
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    def test_load_rules_from_config_returns_empty_for_empty_directory(self) -> None:
        """A configured but empty rules directory yields an empty rule list."""
        service = FlextQuality()
        with tempfile.TemporaryDirectory() as tmpdir:
            service.settings.rules_dir = tmpdir
            result = service.load_rules_from_config()
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=0)

    def test_load_rules_from_config_loads_every_yaml_and_yml_file(self) -> None:
        """load_rules_from_config aggregates rules across .yaml and .yml files."""
        service = FlextQuality()
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_dir = Path(tmpdir)
            (rules_dir / "rules1.yaml").write_text(
                "\nrules:\n  - name: rule-one\n    type: warning\n"
                '    description: First rule\n    pattern: "one"\n    enabled: true\n',
            )
            (rules_dir / "rules2.yml").write_text(
                "\nrules:\n  - name: rule-two\n    type: blocking\n"
                '    description: Second rule\n    pattern: "two"\n    enabled: true\n',
            )
            service.settings.rules_dir = str(rules_dir)
            result = service.load_rules_from_config()
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=2)

    def test_load_rules_from_config_fails_for_missing_directory(self) -> None:
        """A configured rules directory that does not exist yields a failure."""
        service = FlextQuality()
        service.settings.rules_dir = "/nonexistent/rules/dir"
        result = service.load_rules_from_config()
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    # -- stdin hook processing (external boundary: sys.stdin) ------------

    def _run_with_stdin(self, payload: str) -> p.Result[t.JsonMapping]:
        service = FlextQuality()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO(payload)
        try:
            return service.process_stdin_hook()
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_executes_known_event(self) -> None:
        """A well-formed known event on stdin is executed successfully."""
        result = self._run_with_stdin(
            '{"event": "PreToolUse", "tool_name": "Edit"}',
        )
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue"), eq=True)

    def test_process_stdin_hook_continues_when_event_absent(self) -> None:
        """Input without an event continues execution by default."""
        result = self._run_with_stdin('{"tool_name": "Edit"}')
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue"), eq=True)

    def test_process_stdin_hook_fails_on_invalid_json(self) -> None:
        """Malformed JSON on stdin produces a parse/invalid failure."""
        result = self._run_with_stdin("not valid json")
        tm.that(result.failure, eq=True)
        error = (result.error or "").lower()
        tm.that("parse" in error or "invalid" in error, eq=True)

    def test_process_stdin_hook_fails_for_unknown_event(self) -> None:
        """An unknown event supplied via stdin fails with a clear error."""
        result = self._run_with_stdin('{"event": "UnknownEvent"}')
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="Unknown event")
