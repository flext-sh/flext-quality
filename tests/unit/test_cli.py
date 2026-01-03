"""Tests for CLI entry point."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from flext_quality.services.cli import (
    _run_lint,
    _run_security,
    _run_tests,
    _run_type_check,
    main,
)


class TestCLIMain:
    """Tests for main CLI entry point."""

    def test_main_no_args_shows_usage(self) -> None:
        """Test main with no arguments shows usage."""
        with patch.object(sys, "argv", ["flext-quality"]):
            stdout = StringIO()
            with patch.object(sys, "stdout", stdout):
                result = main()
            assert result == 0
            output = stdout.getvalue()
            assert "flext-quality v0.9.0" in output
            assert "Usage:" in output

    def test_main_unknown_command_returns_error(self) -> None:
        """Test main with unknown command returns error."""
        with patch.object(sys, "argv", ["flext-quality", "unknown"]):
            stderr = StringIO()
            with patch.object(sys, "stderr", stderr):
                result = main()
            assert result == 1
            assert "Unknown command" in stderr.getvalue()

    def test_main_check_command_success(self) -> None:
        """Test main check command with successful tools."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create src dir
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "check", tmpdir]):
                stdout = StringIO()
                # Mock subprocess.run to return success
                mock_result = subprocess.CompletedProcess([], 0, "", "")
                with patch("subprocess.run", return_value=mock_result):
                    with patch.object(sys, "stdout", stdout):
                        result = main()
                assert result == 0
                assert "All checks passed" in stdout.getvalue()

    def test_main_check_command_lint_fails(self) -> None:
        """Test main check command when lint fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(sys, "argv", ["flext-quality", "check", tmpdir]):
                stderr = StringIO()
                # Mock subprocess.run to return failure
                mock_result = subprocess.CompletedProcess([], 1, "", "lint error")
                with patch("subprocess.run", return_value=mock_result):
                    with patch.object(sys, "stderr", stderr):
                        result = main()
                assert result == 1
                assert "Lint check failed" in stderr.getvalue()

    def test_main_check_command_type_check_fails(self) -> None:
        """Test main check command when type check fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "check", tmpdir]):
                stderr = StringIO()

                call_count = [0]

                def mock_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
                    call_count[0] += 1
                    if call_count[0] == 1:  # lint succeeds
                        return subprocess.CompletedProcess([], 0, "", "")
                    return subprocess.CompletedProcess([], 1, "", "type error")  # type check fails

                with patch("subprocess.run", side_effect=mock_run):
                    with patch.object(sys, "stderr", stderr):
                        result = main()
                assert result == 1
                assert "Type check failed" in stderr.getvalue()

    def test_main_validate_command_success(self) -> None:
        """Test main validate command with all tools succeeding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "validate", tmpdir]):
                stdout = StringIO()
                mock_result = subprocess.CompletedProcess([], 0, "", "")
                with patch("subprocess.run", return_value=mock_result):
                    with patch.object(sys, "stdout", stdout):
                        result = main()
                assert result == 0
                assert "All validations passed" in stdout.getvalue()

    def test_main_validate_with_min_coverage(self) -> None:
        """Test main validate command with --min-coverage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()

            with patch.object(
                sys, "argv",
                ["flext-quality", "validate", tmpdir, "--min-coverage", "95"]
            ):
                stdout = StringIO()
                mock_result = subprocess.CompletedProcess([], 0, "", "")
                with patch("subprocess.run", return_value=mock_result):
                    with patch.object(sys, "stdout", stdout):
                        result = main()
                assert result == 0

    def test_main_validate_lint_fails(self) -> None:
        """Test main validate command when lint fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(sys, "argv", ["flext-quality", "validate", tmpdir]):
                mock_result = subprocess.CompletedProcess([], 1, "", "lint error")
                with patch("subprocess.run", return_value=mock_result):
                    result = main()
                assert result == 1

    def test_main_validate_type_check_fails(self) -> None:
        """Test main validate command when type check fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "validate", tmpdir]):
                call_count = [0]

                def mock_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
                    call_count[0] += 1
                    if call_count[0] == 1:
                        return subprocess.CompletedProcess([], 0, "", "")
                    return subprocess.CompletedProcess([], 1, "", "")

                with patch("subprocess.run", side_effect=mock_run):
                    result = main()
                assert result == 1

    def test_main_validate_security_fails(self) -> None:
        """Test main validate command when security scan fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "validate", tmpdir]):
                call_count = [0]

                def mock_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
                    call_count[0] += 1
                    if call_count[0] <= 2:  # lint and type succeed
                        return subprocess.CompletedProcess([], 0, "", "")
                    return subprocess.CompletedProcess([], 1, "", "")  # security fails

                with patch("subprocess.run", side_effect=mock_run):
                    result = main()
                assert result == 1

    def test_main_validate_tests_fail(self) -> None:
        """Test main validate command when tests fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()

            with patch.object(sys, "argv", ["flext-quality", "validate", tmpdir]):
                call_count = [0]

                def mock_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
                    call_count[0] += 1
                    if call_count[0] <= 3:  # lint, type, security succeed
                        return subprocess.CompletedProcess([], 0, "", "")
                    return subprocess.CompletedProcess([], 1, "", "")  # tests fail

                with patch("subprocess.run", side_effect=mock_run):
                    result = main()
                assert result == 1

    def test_main_check_uses_current_dir(self) -> None:
        """Test check command uses current dir when path not provided."""
        with patch.object(sys, "argv", ["flext-quality", "check"]):
            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                stdout = StringIO()
                with patch.object(sys, "stdout", stdout):
                    main()
            # Check that run was called (twice: lint + type)
            assert mock_run.call_count == 2


class TestRunLint:
    """Tests for _run_lint function."""

    def test_run_lint_success(self) -> None:
        """Test _run_lint with successful lint."""
        mock_result = subprocess.CompletedProcess([], 0, "", "")
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            result = _run_lint(Path("/test/path"))
        assert result == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "ruff" in call_args
        assert "check" in call_args

    def test_run_lint_failure(self) -> None:
        """Test _run_lint with failed lint."""
        mock_result = subprocess.CompletedProcess([], 1, "", "error")
        with patch("subprocess.run", return_value=mock_result):
            result = _run_lint(Path("/test/path"))
        assert result == 1


class TestRunTypeCheck:
    """Tests for _run_type_check function."""

    def test_run_type_check_with_src_dir(self) -> None:
        """Test _run_type_check when src dir exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_type_check(Path(tmpdir))
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert "pyrefly" in call_args
            assert str(src_dir) in call_args

    def test_run_type_check_without_src_dir(self) -> None:
        """Test _run_type_check when src dir doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_type_check(Path(tmpdir))
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert tmpdir in call_args


class TestRunTests:
    """Tests for _run_tests function."""

    def test_run_tests_success(self) -> None:
        """Test _run_tests with passing tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_tests(Path(tmpdir))
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert "pytest" in call_args
            assert "--cov-fail-under=80" in call_args

    def test_run_tests_with_custom_coverage(self) -> None:
        """Test _run_tests with custom min coverage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_tests(Path(tmpdir), min_coverage=95)
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert "--cov-fail-under=95" in call_args

    def test_run_tests_failure(self) -> None:
        """Test _run_tests with failing tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 1, "", "test failure")
            with patch("subprocess.run", return_value=mock_result):
                result = _run_tests(Path(tmpdir))
            assert result == 1


class TestRunSecurity:
    """Tests for _run_security function."""

    def test_run_security_with_src_dir(self) -> None:
        """Test _run_security when src dir exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_security(Path(tmpdir))
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert "bandit" in call_args
            assert str(src_dir) in call_args

    def test_run_security_without_src_dir(self) -> None:
        """Test _run_security when src dir doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 0, "", "")
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                result = _run_security(Path(tmpdir))
            assert result == 0
            call_args = mock_run.call_args[0][0]
            assert tmpdir in call_args

    def test_run_security_failure(self) -> None:
        """Test _run_security with security issues."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = subprocess.CompletedProcess([], 1, "", "security issue")
            with patch("subprocess.run", return_value=mock_result):
                result = _run_security(Path(tmpdir))
            assert result == 1


class TestCLIMainBlock:
    """Tests for if __name__ == '__main__' block (cli.py:136)."""

    def test_main_block_execution_via_subprocess(self) -> None:
        """Test that main block executes via subprocess (cli.py:136)."""
        import os

        # Run the CLI module as __main__ via python -m
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"

        result = subprocess.run(
            [sys.executable, "-m", "flext_quality.services.cli"],
            capture_output=True,
            text=True,
            env=env,
        )

        # Should show usage (exit code 0) when called without args
        assert result.returncode == 0
        assert "flext-quality" in result.stdout.lower() or "usage" in result.stdout.lower()
