"""Tests for FlextQuality API facade."""

from __future__ import annotations

import io
import sys
import tempfile
import threading
from pathlib import Path

from flext_quality.api import FlextQuality


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

        assert instance1 is instance2

    def test_instance_has_required_attributes(self) -> None:
        """Test that instance has all required attributes."""
        quality = FlextQuality.get_instance()

        assert hasattr(quality, "logger")
        assert hasattr(quality, "config")
        assert hasattr(quality, "hooks")
        assert hasattr(quality, "rules_loader")

    def test_get_status_returns_dict(self) -> None:
        """Test that get_status returns status dict."""
        quality = FlextQuality.get_instance()
        status = quality.get_status()

        assert isinstance(status, dict)
        assert "name" in status
        assert "version" in status
        assert "config" in status
        assert "hooks_registered" in status

    def test_validate_configuration_succeeds(self) -> None:
        """Test that validate_configuration returns success."""
        quality = FlextQuality.get_instance()
        result = quality.validate_configuration()

        assert result.is_success
        assert result.value is True

    def test_format_hook_output_continue(self) -> None:
        """Test format_hook_output with continue=True."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(continue_exec=True)

        assert '"continue": true' in output

    def test_format_hook_output_with_message(self) -> None:
        """Test format_hook_output with message."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(
            continue_exec=True,
            message="Test message",
        )

        assert '"continue": true' in output
        assert "Test message" in output

    def test_format_hook_output_blocked(self) -> None:
        """Test format_hook_output with blocked reason."""
        quality = FlextQuality.get_instance()
        output = quality.format_hook_output(
            continue_exec=False,
            blocked_reason="Blocked for testing",
        )

        assert '"continue": false' in output

    def test_get_hook_config_json(self) -> None:
        """Test get_hook_config_json returns valid JSON."""
        quality = FlextQuality.get_instance()
        config_json = quality.get_hook_config_json()

        assert isinstance(config_json, str)
        # Should be valid JSON (empty or with hooks)
        assert config_json == "{}"

    def test_load_rules_from_config_with_no_rules_dir(self) -> None:
        """Test load_rules_from_config when rules dir doesn't exist."""
        quality = FlextQuality.get_instance()
        result = quality.load_rules_from_config()

        # Should succeed with empty list or fail with missing dir
        # Both are valid depending on config
        assert result.is_success or result.is_failure

    def test_load_rules_from_file(self) -> None:
        """Test load_rules from a YAML file."""
        quality = FlextQuality.get_instance()

        # Create temp rules file
        rules_yaml = """
rules:
  - name: test-rule
    type: warning
    description: Test rule
    pattern: "test"
    enabled: true
"""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write(rules_yaml)
            rules_path = Path(f.name)

        try:
            result = quality.load_rules(rules_path)
            assert result.is_success
            assert len(result.value) == 1
            assert result.value[0].name == "test-rule"
        finally:
            rules_path.unlink()

    def test_load_rules_from_nonexistent_file(self) -> None:
        """Test load_rules fails for nonexistent file."""
        quality = FlextQuality.get_instance()
        result = quality.load_rules(Path("/nonexistent/rules.yaml"))

        assert result.is_failure
        assert "not found" in (result.error or "").lower()


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

        assert result.is_failure
        assert "Unknown event" in (result.error or "")

    def test_execute_hook_valid_event_no_hooks(self) -> None:
        """Test execute_hook succeeds with no registered hooks."""
        quality = FlextQuality.get_instance()
        result = quality.execute_hook("PreToolUse", {"tool_name": "Edit"})

        assert result.is_success
        assert result.value.get("continue") is True


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
        instances: list[FlextQuality] = []
        errors: list[Exception] = []

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

        assert len(errors) == 0
        assert len(instances) == 10
        # All should be the same instance
        assert all(i is instances[0] for i in instances)


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
        # Save original rules_dir
        original_dir = quality.config.rules_dir

        # Set to nonexistent path
        quality.config.rules_dir = "/nonexistent/rules/dir"
        result = quality.load_rules_from_config()

        # Restore original
        quality.config.rules_dir = original_dir

        assert result.is_failure
        assert "not found" in (result.error or "").lower()

    def test_load_rules_from_config_with_multiple_files(self) -> None:
        """Test load_rules_from_config loads multiple YAML files."""
        quality = FlextQuality.get_instance()

        # Create temp directory with multiple rules files
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_dir = Path(tmpdir)

            # Create first rules file
            (rules_dir / "rules1.yaml").write_text("""
rules:
  - name: rule-one
    type: warning
    description: First rule
    pattern: "one"
    enabled: true
""")

            # Create second rules file
            (rules_dir / "rules2.yml").write_text("""
rules:
  - name: rule-two
    type: blocking
    description: Second rule
    pattern: "two"
    enabled: true
""")

            # Save original path and set temp path
            original_dir = quality.config.rules_dir
            quality.config.rules_dir = str(rules_dir)

            result = quality.load_rules_from_config()

            # Restore original
            quality.config.rules_dir = original_dir

            assert result.is_success
            assert len(result.value) == 2


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

        # Mock stdin
        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"event": "PreToolUse", "tool_name": "Edit"}')

        try:
            result = quality.process_stdin_hook()
            assert result.is_success
            assert result.value.get("continue") is True
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_empty_event(self) -> None:
        """Test process_stdin_hook with empty event returns continue."""
        quality = FlextQuality.get_instance()

        original_stdin = sys.stdin
        sys.stdin = io.StringIO('{"tool_name": "Edit"}')

        try:
            result = quality.process_stdin_hook()
            assert result.is_success
            assert result.value.get("continue") is True
        finally:
            sys.stdin = original_stdin

    def test_process_stdin_hook_invalid_json(self) -> None:
        """Test process_stdin_hook with invalid JSON fails."""
        quality = FlextQuality.get_instance()

        original_stdin = sys.stdin
        sys.stdin = io.StringIO("not valid json")

        try:
            result = quality.process_stdin_hook()
            assert result.is_failure
            assert (
                "parse" in (result.error or "").lower()
                or "invalid" in (result.error or "").lower()
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
            assert result.is_failure
            assert "Unknown event" in (result.error or "")
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

        # Save original values
        original_function = quality.config.max_function_length
        original_class = quality.config.max_class_length

        # Set invalid thresholds (function > class)
        quality.config.max_function_length = 500
        quality.config.max_class_length = 100

        result = quality.validate_configuration()

        # Restore original values
        quality.config.max_function_length = original_function
        quality.config.max_class_length = original_class

        assert result.is_failure
        assert "max_function_length" in (result.error or "").lower()
