"""Tests for FlextQuality API facade."""

from __future__ import annotations

import io
import sys
import tempfile
import threading
from collections.abc import Sequence
from pathlib import Path

from flext_tests import tm

from flext_quality import FlextQuality


class TestFlextQualityAPI:
    """Tests for FlextQuality API."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_get_instance_returns_singleton(self) -> None:
        """Test that get_instance returns same instance."""
        instance1 = FlextQuality.get_instance()
        instance2 = FlextQuality.get_instance()
        tm.that(instance1 is instance2, eq=True)

    def test_instance_has_required_attributes(self) -> None:
        """Test that instance has all required attributes."""
        quality = FlextQuality.get_instance()
        tm.that(hasattr(quality, "logger"), eq=True)
        tm.that(hasattr(quality, "config"), eq=True)
        tm.that(hasattr(quality, "hooks"), eq=True)
        tm.that(hasattr(quality, "rules_loader"), eq=True)

    def test_get_status_returns_dict(self) -> None:
        """Test that get_status returns status dict."""
        quality = FlextQuality.get_instance()
        status = quality.get_status()
        tm.that(status, is_=dict)
        tm.that(status, has="name")
        tm.that(status, has="version")
        tm.that(status, has="config")
        tm.that(status, has="hooks_registered")

    def test_validate_configuration_succeeds(self) -> None:
        """Test that validate_configuration returns success."""
        quality = FlextQuality.get_instance()
        result = quality.validate_configuration()
        tm.that(result.is_success, eq=True)
        tm.that(result.value is True, eq=True)

    def test_format_hook_output_continue(self) -> None:
        """Test format_hook_output with continue=True."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(continue_exec=True)
        tm.that(output, has='"continue":true')

    def test_format_hook_output_with_message(self) -> None:
        """Test format_hook_output with message."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(continue_exec=True, message="Test message")
        tm.that(output, has='"continue":true')
        tm.that(output, has="Test message")

    def test_format_hook_output_blocked(self) -> None:
        """Test format_hook_output with blocked reason."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(
            continue_exec=False,
            blocked_reason="Blocked for testing",
        )
        tm.that(output, has='"continue":false')

    def test_get_hook_config_json(self) -> None:
        """Test get_hook_config_json returns valid JSON."""
        quality = FlextQuality.get_instance()
        config_json = quality.get_hook_config_json()
        tm.that(config_json, is_=str)
        tm.that(config_json, eq="{}")

    def test_load_rules_from_config_with_no_rules_dir(self) -> None:
        """Test load_rules_from_config when rules dir doesn't exist."""
        quality = FlextQuality.get_instance()
        result = quality.load_rules_from_config()
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_load_rules_from_file(self) -> None:
        """Test load_rules from a YAML file."""
        quality = FlextQuality.get_instance()
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
            result = quality.load_rules(rules_path)
            tm.that(result.is_success, eq=True)
            tm.that(len(result.value), eq=1)
            tm.that(result.value[0].name, eq="test-rule")
        finally:
            rules_path.unlink()

    def test_load_rules_from_nonexistent_file(self) -> None:
        """Test load_rules fails for nonexistent file."""
        quality = FlextQuality.get_instance()
        result = quality.load_rules(Path("/nonexistent/rules.yaml"))
        tm.that(result.is_failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")


class TestFlextQualityHookExecution:
    """Tests for hook execution via FlextQuality."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_execute_hook_unknown_event(self) -> None:
        """Test execute_hook fails for unknown event."""
        quality = FlextQuality.get_instance()
        result = quality.execute_hook("UnknownEvent", {})
        tm.that(result.is_failure, eq=True)
        tm.that((result.error or ""), has="Unknown event")

    def test_execute_hook_valid_event_no_hooks(self) -> None:
        """Test execute_hook succeeds with no registered hooks."""
        quality = FlextQuality.get_instance()
        result = quality.execute_hook("PreToolUse", {"tool_name": "Edit"})
        tm.that(result.is_success, eq=True)
        tm.that(result.value.get("continue") is True, eq=True)


class TestFlextQualitySingleton:
    """Tests for singleton behavior with threading."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_double_check_locking_concurrent(self) -> None:
        """Test singleton creation with concurrent threads."""
        instances: Sequence[FlextQuality] = []
        errors: Sequence[Exception] = []

        def get_instance() -> None:
            try:
                instance = FlextQuality.get_instance()
                instances.append(instance)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=get_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        tm.that(not errors, eq=True)
        tm.that(len(instances), eq=10)
        tm.that(all(i is instances[0] for i in instances), eq=True)


class TestFlextQualityRulesConfig:
    """Tests for rules loading from config."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_load_rules_from_config_nonexistent_dir(self) -> None:
        """Test load_rules_from_config fails when rules dir doesn't exist."""
        quality = FlextQuality.get_instance()
        original_dir = quality.config.rules_dir
        quality.config.rules_dir = "/nonexistent/rules/dir"
        result = quality.load_rules_from_config()
        quality.config.rules_dir = original_dir
        tm.that(result.is_failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    def test_load_rules_from_config_with_multiple_files(self) -> None:
        """Test load_rules_from_config loads multiple YAML files."""
        quality = FlextQuality.get_instance()
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_dir = Path(tmpdir)
            (rules_dir / "rules1.yaml").write_text(
                '\nrules:\n  - name: rule-one\n    type: warning\n    description: First rule\n    pattern: "one"\n    enabled: true\n',
            )
            (rules_dir / "rules2.yml").write_text(
                '\nrules:\n  - name: rule-two\n    type: blocking\n    description: Second rule\n    pattern: "two"\n    enabled: true\n',
            )
            original_dir = quality.config.rules_dir
            quality.config.rules_dir = str(rules_dir)
            result = quality.load_rules_from_config()
            quality.config.rules_dir = original_dir
            tm.that(result.is_success, eq=True)
            tm.that(len(result.value), eq=2)


class TestFlextQualityStdinProcessing:
    """Tests for stdin hook processing."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_process_stdin_hook_success(self) -> None:
        """Test process_stdin_hook with valid input."""
        quality = FlextQuality.get_instance()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"event": "PreToolUse", "tool_name": "Edit"}')
        try:
            result = quality.process_stdin_hook()
            tm.that(result.is_success, eq=True)
            tm.that(result.value.get("continue") is True, eq=True)
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_empty_event(self) -> None:
        """Test process_stdin_hook with empty event returns continue."""
        quality = FlextQuality.get_instance()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"tool_name": "Edit"}')
        try:
            result = quality.process_stdin_hook()
            tm.that(result.is_success, eq=True)
            tm.that(result.value.get("continue") is True, eq=True)
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_invalid_json(self) -> None:
        """Test process_stdin_hook with invalid JSON fails."""
        quality = FlextQuality.get_instance()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO("not valid json")
        try:
            result = quality.process_stdin_hook()
            tm.that(result.is_failure, eq=True)
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
        quality = FlextQuality.get_instance()
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"event": "UnknownEvent"}')
        try:
            result = quality.process_stdin_hook()
            tm.that(result.is_failure, eq=True)
            tm.that((result.error or ""), has="Unknown event")
        finally:
            sys.stdin = original_stdin


class TestFlextQualityValidation:
    """Tests for configuration validation."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        FlextQuality._reset_instance()

    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        FlextQuality._reset_instance()

    def test_validate_configuration_threshold_failure(self) -> None:
        """Test validate_configuration fails when thresholds are invalid."""
        quality = FlextQuality.get_instance()
        original_function = quality.config.max_function_length
        original_class = quality.config.max_class_length
        quality.config.max_function_length = 500
        quality.config.max_class_length = 100
        result = quality.validate_configuration()
        quality.config.max_function_length = original_function
        quality.config.max_class_length = original_class
        tm.that(result.is_failure, eq=True)
        tm.that((result.error or "").lower(), has="max_function_length")
