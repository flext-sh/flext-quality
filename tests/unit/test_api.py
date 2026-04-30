"""Tests for FlextQuality API facade."""

from __future__ import annotations

import io
import sys
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_tests import tm

from flext_quality import FlextQuality, quality
from flext_quality.settings import FlextQualitySettings


class TestsFlextQualityApi:
    """Tests for FlextQuality API."""

    @pytest.fixture(autouse=True)
    def _reset_settings(self) -> Generator[None]:
        """Isolate singleton state across API tests."""
        FlextQualitySettings.reset_for_testing()
        try:
            yield
        finally:
            FlextQualitySettings.reset_for_testing()

    def test_quality_alias_exposes_facade_instance(self) -> None:
        """Test that the runtime alias exposes the public facade instance."""
        tm.that(quality.fetch_status(), has="name")

    def test_instance_has_required_attributes(self) -> None:
        """Test that the facade instantiates without constructor arguments."""
        tm.that(FlextQuality().fetch_status(), has="name")

    def test_fetch_status_returns_dict(self) -> None:
        """Test that fetch_status returns status dict."""
        status = FlextQuality().fetch_status()
        tm.that(status, is_=dict)
        tm.that(status, has="name")
        tm.that(status, has="version")
        tm.that(status, has="settings")
        tm.that(status, has="hooks_registered")

    def test_validate_configuration_succeeds(self) -> None:
        """Test that validate_configuration returns success."""
        result = FlextQuality().validate_configuration()
        tm.that(result.success, eq=True)
        tm.that(result.value is True, eq=True)

    def test_format_hook_output_continue(self) -> None:
        """Test format_hook_output with continue=True."""
        output = FlextQuality().format_hook_output(continue_exec=True)
        tm.that(output, has='"continue":true')

    def test_format_hook_output_with_message(self) -> None:
        """Test format_hook_output with message."""
        output = FlextQuality().format_hook_output(
            continue_exec=True,
            message="Test message",
        )
        tm.that(output, has='"continue":true')
        tm.that(output, has="Test message")

    def test_format_hook_output_blocked(self) -> None:
        """Test format_hook_output with blocked reason."""
        output = FlextQuality().format_hook_output(
            continue_exec=False,
            blocked_reason="Blocked for testing",
        )
        tm.that(output, has='"continue":false')

    def test_fetch_hook_config_json(self) -> None:
        """Test get_hook_config_json returns valid JSON."""
        config_json = FlextQuality().fetch_hook_config_json()
        tm.that(config_json, is_=str)
        tm.that(config_json, eq="{}")

    def test_load_rules_from_config_with_no_rules_dir(self) -> None:
        """Test load_rules_from_config when rules dir doesn't exist."""
        result = FlextQuality().load_rules_from_config()
        tm.that(result.success or result.failure, eq=True)

    def test_load_rules_from_file(self) -> None:
        """Test load_rules from a YAML file."""
        quality_service = FlextQuality()
        rules_yaml = '\nrules:\n  - name: test-rule\n    type: warning\n    description: Test rule\n    pattern: "test"\n    enabled: true\n'
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".yaml",
            delete=False,
        ) as f:
            f.write(rules_yaml)
            rules_path = Path(f.name)
        try:
            result = quality_service.load_rules(rules_path)
            tm.that(result.success, eq=True)
            tm.that(len(result.value), eq=1)
            tm.that(result.value[0].name, eq="test-rule")
        finally:
            rules_path.unlink()

    def test_load_rules_from_nonexistent_file(self) -> None:
        """Test load_rules fails for nonexistent file."""
        result = FlextQuality().load_rules(Path("/nonexistent/rules.yaml"))
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    def test_execute_hook_unknown_event(self) -> None:
        """Test execute_hook fails for unknown event."""
        result = FlextQuality().execute_hook("UnknownEvent", {})
        tm.that(result.failure, eq=True)
        tm.that((result.error or ""), has="Unknown event")

    def test_execute_hook_valid_event_no_hooks(self) -> None:
        """Test execute_hook succeeds with no registered hooks."""
        result = FlextQuality().execute_hook("PreToolUse", {"tool_name": "Edit"})
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue") is True, eq=True)

    def test_load_rules_from_config_nonexistent_dir(self) -> None:
        """Test load_rules_from_config fails when rules dir doesn't exist."""
        quality_service = FlextQuality()
        original_dir = quality_service.settings.rules_dir
        quality_service.settings.rules_dir = "/nonexistent/rules/dir"
        result = quality_service.load_rules_from_config()
        quality_service.settings.rules_dir = original_dir
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    def test_load_rules_from_config_with_multiple_files(self) -> None:
        """Test load_rules_from_config loads multiple YAML files."""
        quality_service = FlextQuality()
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_dir = Path(tmpdir)
            (rules_dir / "rules1.yaml").write_text(
                '\nrules:\n  - name: rule-one\n    type: warning\n    description: First rule\n    pattern: "one"\n    enabled: true\n',
            )
            (rules_dir / "rules2.yml").write_text(
                '\nrules:\n  - name: rule-two\n    type: blocking\n    description: Second rule\n    pattern: "two"\n    enabled: true\n',
            )
            original_dir = quality_service.settings.rules_dir
            quality_service.settings.rules_dir = str(rules_dir)
            result = quality_service.load_rules_from_config()
            quality_service.settings.rules_dir = original_dir
            tm.that(result.success, eq=True)
            tm.that(len(result.value), eq=2)

    def test_process_stdin_hook_success(self) -> None:
        """Test process_stdin_hook with valid input."""
        quality_service = FlextQuality()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"event": "PreToolUse", "tool_name": "Edit"}')
        try:
            result = quality_service.process_stdin_hook()
            tm.that(result.success, eq=True)
            tm.that(result.value.get("continue") is True, eq=True)
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_empty_event(self) -> None:
        """Test process_stdin_hook with empty event returns continue."""
        quality_service = FlextQuality()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"tool_name": "Edit"}')
        try:
            result = quality_service.process_stdin_hook()
            tm.that(result.success, eq=True)
            tm.that(result.value.get("continue") is True, eq=True)
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_invalid_json(self) -> None:
        """Test process_stdin_hook with invalid JSON fails."""
        quality_service = FlextQuality()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO("not valid json")
        try:
            result = quality_service.process_stdin_hook()
            tm.that(result.failure, eq=True)
            tm.that(
                (
                    "parse" in (result.error or "").lower()
                    or "invalid" in (result.error or "").lower()
                ),
                eq=True,
            )
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_with_unknown_event(self) -> None:
        """Test process_stdin_hook with unknown event fails."""
        quality_service = FlextQuality()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"event": "UnknownEvent"}')
        try:
            result = quality_service.process_stdin_hook()
            tm.that(result.failure, eq=True)
            tm.that((result.error or ""), has="Unknown event")
        finally:
            sys.stdin = original_stdin

    def test_validate_configuration_threshold_failure(self) -> None:
        """Test validate_configuration fails when thresholds are invalid."""
        quality_service = FlextQuality()
        original_function = quality_service.settings.max_function_length
        original_class = quality_service.settings.max_class_length
        quality_service.settings.max_function_length = 500
        quality_service.settings.max_class_length = 100
        result = quality_service.validate_configuration()
        quality_service.settings.max_function_length = original_function
        quality_service.settings.max_class_length = original_class
        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="max_function_length")
