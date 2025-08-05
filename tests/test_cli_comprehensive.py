"""Comprehensive functional tests for CLI module to achieve high coverage.

Real functional tests covering all CLI functionality following flext-core patterns.
Tests all command-line scenarios, argument handling, and integration flows.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from flext_quality.cli import (
    analyze_project,
    another_function,
    main,
    setup_logging,
)


class TestAnalyzeProjectComprehensive:
    """Comprehensive functional tests for analyze_project CLI function."""

    def _create_analyze_args(
        self,
        path: str,
        output: str | None = None,
        format_type: str = "text",
        verbose: bool = False,
    ) -> argparse.Namespace:
        """DRY helper: Create analyze_project arguments."""
        return argparse.Namespace(
            path=path,
            output=output,
            format=format_type,
            verbose=verbose,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

    def test_analyze_project_valid_path_default_params(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with valid path and default parameters."""
        args = argparse.Namespace(
            path=temporary_project_structure,
            output=None,
            format="text",
            verbose=False,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        result = analyze_project(args)

        # Should return success code
        assert result == 0

    def test_analyze_project_valid_path_with_output_file(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with output file specified."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".json",
            delete=False,
        ) as f:
            output_file = f.name

        args = argparse.Namespace(
            path=temporary_project_structure,
            output=output_file,
            format="json",
            verbose=False,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        result = analyze_project(args)

        # Should return success code
        assert result == 0

        # Output file should exist
        output_path = Path(output_file)
        assert output_path.exists()

    def test_analyze_project_with_format_json(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with JSON format."""
        args = self._create_analyze_args(
            temporary_project_structure,
            format_type="json",
        )
        result = analyze_project(args)

        # Should return success code
        assert result == 0

    def test_analyze_project_with_format_text(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with text format."""
        args = argparse.Namespace(
            path=temporary_project_structure,
            output=None,
            format="text",
            verbose=False,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        result = analyze_project(args)

        # Should return success code
        assert result == 0

    def test_analyze_project_with_verbose_true(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with verbose output enabled."""
        args = self._create_analyze_args(temporary_project_structure, verbose=True)
        result = analyze_project(args)

        # Should return success code
        assert result == 0

    def test_analyze_project_with_verbose_false(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with verbose output disabled."""
        args = self._create_analyze_args(temporary_project_structure, verbose=False)
        result = analyze_project(args)

        # Should return success code
        assert result == 0

    def test_analyze_project_nonexistent_path(self) -> None:
        """Test analyze_project with nonexistent path."""
        args = self._create_analyze_args("/nonexistent/path")
        result = analyze_project(args)

        # Should return error code
        assert result != 0

    def test_analyze_project_invalid_path_type(self) -> None:
        """Test analyze_project with invalid path type."""
        # Path that exists but is not a directory
        with tempfile.NamedTemporaryFile() as f:
            args = self._create_analyze_args(f.name)
            result = analyze_project(args)

            # Should handle gracefully and return error code
            assert result != 0

    @patch("flext_quality.cli.CodeAnalyzer")
    def test_analyze_project_analyzer_exception(
        self,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project when analyzer raises exception."""
        # Make analyzer raise exception
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.side_effect = RuntimeError("Analysis failed")
        mock_analyzer_class.return_value = mock_analyzer

        args = self._create_analyze_args(temporary_project_structure, verbose=True)
        result = analyze_project(args)

        # Should return error code
        assert result != 0

    @patch("flext_quality.cli.CodeAnalyzer")
    def test_analyze_project_analyzer_exception_non_verbose(
        self,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project when analyzer raises exception with verbose=False."""
        # Make analyzer raise exception
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.side_effect = RuntimeError("Analysis failed")
        mock_analyzer_class.return_value = mock_analyzer

        args = self._create_analyze_args(temporary_project_structure, verbose=False)
        result = analyze_project(args)

        # Should return error code
        assert result != 0

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    def test_analyze_project_with_json_output_and_file(
        self,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with JSON output to file."""
        # Setup mocks
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "test": "data",
            "files_analyzed": 5,  # Mock at least 1 file analyzed
        }
        mock_analyzer.get_quality_score.return_value = 85.0
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report.to_json.return_value = '{"report": "data"}'
        mock_report_class.return_value = mock_report

        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".json",
            delete=False,
        ) as f:
            output_file = f.name

        args = self._create_analyze_args(
            temporary_project_structure,
            output=output_file,
            format_type="json",
        )
        result = analyze_project(args)

        # Should return success code
        assert result == 0

        # Verify file was written
        assert Path(output_file).exists()

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    def test_analyze_project_json_format_no_output_file(
        self,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with JSON format but no output file."""
        # Setup mocks
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "test": "data",
            "files_analyzed": 3,  # Mock at least 1 file analyzed
        }
        mock_analyzer.get_quality_score.return_value = 85.0
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report.to_json.return_value = '{"report": "data"}'
        mock_report_class.return_value = mock_report

        # Capture stdout to verify JSON output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            args = self._create_analyze_args(
                temporary_project_structure,
                format_type="json",
            )
            result = analyze_project(args)

        # Should return success code
        assert result == 0

        # Should have printed JSON to stdout
        output = captured_output.getvalue()
        assert '{"report": "data"}' in output


class TestAnotherFunctionComprehensive:
    """Comprehensive functional tests for another_function CLI function."""

    def _create_score_args(self, path: str) -> argparse.Namespace:
        """DRY helper: Create another_function arguments."""
        return argparse.Namespace(path=path)

    def test_another_function_valid_path_good_score(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test another_function with valid path resulting in good score."""
        args = self._create_score_args(temporary_project_structure)
        result = another_function(args)

        # Should return success code
        assert result == 0

    def test_another_function_nonexistent_path(self) -> None:
        """Test another_function with nonexistent path."""
        args = self._create_score_args("/nonexistent/path")
        result = another_function(args)

        # Should return error code
        assert result != 0

    @patch("flext_quality.cli.CodeAnalyzer")
    def test_another_function_low_quality_score(
        self,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test another_function with low quality score."""
        # Setup mock analyzer to return low score
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {"test": "data"}
        mock_analyzer.get_quality_score.return_value = 45.0  # Below 75 threshold
        mock_analyzer_class.return_value = mock_analyzer

        args = self._create_score_args(temporary_project_structure)
        result = another_function(args)

        # Should return error code for low score
        assert result != 0

    @patch("flext_quality.cli.CodeAnalyzer")
    def test_another_function_high_quality_score(
        self,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test another_function with high quality score."""
        # Setup mock analyzer to return high score
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {"test": "data"}
        mock_analyzer.get_quality_score.return_value = 85.0  # Above 75 threshold
        mock_analyzer_class.return_value = mock_analyzer

        args = self._create_score_args(temporary_project_structure)
        result = another_function(args)

        # Should return success code for high score
        assert result == 0

    @patch("flext_quality.cli.CodeAnalyzer")
    def test_another_function_analyzer_exception(
        self,
        mock_analyzer_class: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test another_function when analyzer raises exception."""
        # Make analyzer raise exception
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.side_effect = RuntimeError("Analysis failed")
        mock_analyzer_class.return_value = mock_analyzer

        args = self._create_score_args(temporary_project_structure)
        result = another_function(args)

        # Should return error code
        assert result != 0


class TestSetupLogging:
    """Comprehensive tests for setup_logging function."""

    def test_setup_logging_debug_level(self) -> None:
        """Test setup_logging with debug level."""
        setup_logging("debug")
        # Function should complete without error
        # Actual logging verification would require checking logger state

    def test_setup_logging_info_level(self) -> None:
        """Test setup_logging with info level."""
        setup_logging("info")
        # Function should complete without error

    def test_setup_logging_warning_level(self) -> None:
        """Test setup_logging with warning level."""
        setup_logging("warning")
        # Function should complete without error

    def test_setup_logging_error_level(self) -> None:
        """Test setup_logging with error level."""
        setup_logging("error")
        # Function should complete without error

    def test_setup_logging_invalid_level(self) -> None:
        """Test setup_logging with invalid level."""
        # Should handle gracefully
        setup_logging("invalid_level")

    def test_setup_logging_default_level(self) -> None:
        """Test setup_logging with default level."""
        setup_logging()
        # Function should complete without error


class TestMainFunctionComprehensive:
    """Comprehensive tests for main function with argument parsing."""

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_analyze_command_success(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with analyze command."""
        mock_analyze.return_value = 0

        # Simulate command line arguments
        test_args = ["flext-quality", "analyze", temporary_project_structure]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_setup_logging.assert_called_once()
        mock_analyze.assert_called_once()
        assert result == 0

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_analyze_command_with_verbose(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with analyze command and verbose flag."""
        mock_analyze.return_value = 0

        test_args = [
            "flext-quality",
            "--verbose",
            "analyze",
            temporary_project_structure,
        ]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_setup_logging.assert_called_once()
        mock_analyze.assert_called_once()
        args = mock_analyze.call_args[0][0]
        assert args.path == temporary_project_structure
        assert args.output is None
        assert args.format == "text"
        assert args.verbose is True
        assert result == 0

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_analyze_command_with_output_file(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with analyze command and output file."""
        mock_analyze.return_value = 0

        test_args = [
            "flext-quality",
            "analyze",
            temporary_project_structure,
            "-o",
            "output.json",
        ]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_analyze.assert_called_once()
        args = mock_analyze.call_args[0][0]
        assert args.path == temporary_project_structure
        assert args.output == "output.json"
        assert args.format == "text"
        assert args.verbose is False
        assert result == 0

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_analyze_command_with_format(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with analyze command and format option."""
        mock_analyze.return_value = 0

        test_args = [
            "flext-quality",
            "analyze",
            temporary_project_structure,
            "-f",
            "json",
        ]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_analyze.assert_called_once()
        args = mock_analyze.call_args[0][0]
        assert args.path == temporary_project_structure
        assert args.output is None
        assert args.format == "json"
        assert args.verbose is False
        assert result == 0

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.another_function")
    def test_main_score_command(
        self,
        mock_another: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with score command."""
        mock_another.return_value = 0

        test_args = ["flext-quality", "score", temporary_project_structure]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_setup_logging.assert_called_once()
        # Check that another_function was called with the right arguments
        mock_another.assert_called_once()
        args = mock_another.call_args[0][0]
        assert args.path == temporary_project_structure
        assert result == 0

    @patch("flext_quality.cli.setup_logging")
    def test_main_no_command(self, mock_setup_logging: MagicMock) -> None:
        """Test main function with no command provided."""
        test_args = ["flext-quality"]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_setup_logging.assert_called_once()
        # Should print help and return error code
        assert result != 0

    @patch("flext_quality.cli.setup_logging")
    def test_main_invalid_command(self, mock_setup_logging: MagicMock) -> None:
        """Test main function with invalid command."""
        test_args = ["flext-quality", "invalid-command"]
        with (
            patch.object(sys, "argv", test_args),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        # Should exit with error code
        assert exc_info.value.code != 0

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_analyze_command_failure(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function when analyze command fails."""
        mock_analyze.return_value = 1  # Error code

        test_args = ["flext-quality", "analyze", temporary_project_structure]
        with patch.object(sys, "argv", test_args):
            result = main()

        assert result == 1

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.another_function")
    def test_main_score_command_failure(
        self,
        mock_another: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function when score command fails."""
        mock_another.return_value = 1  # Error code

        test_args = ["flext-quality", "score", temporary_project_structure]
        with patch.object(sys, "argv", test_args):
            result = main()

        assert result == 1

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    def test_main_all_options_combined(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test main function with all options combined."""
        mock_analyze.return_value = 0

        test_args = [
            "flext-quality",
            "--verbose",
            "analyze",
            temporary_project_structure,
            "-o",
            "report.json",
            "-f",
            "json",
        ]
        with patch.object(sys, "argv", test_args):
            result = main()

        mock_analyze.assert_called_once()
        args = mock_analyze.call_args[0][0]
        assert args.path == temporary_project_structure
        assert args.output == "report.json"
        assert args.format == "json"
        assert args.verbose is True
        assert result == 0


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def _create_score_args(self, path: str) -> argparse.Namespace:
        """DRY helper: Create another_function arguments."""
        return argparse.Namespace(path=path)

    def test_end_to_end_analyze_flow(self, temporary_project_structure: str) -> None:
        """Test complete end-to-end analyze flow."""
        # This test uses real implementations without mocking
        args = argparse.Namespace(
            path=temporary_project_structure,
            output=None,
            format="text",
            verbose=True,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        result = analyze_project(args)

        # Should complete successfully
        assert result == 0

    def test_end_to_end_score_flow(self, temporary_project_structure: str) -> None:
        """Test complete end-to-end score flow."""
        # This test uses real implementations without mocking
        args = self._create_score_args(temporary_project_structure)
        result = another_function(args)

        # Should complete (result depends on actual code quality)
        assert isinstance(result, int)
        assert result in {0, 1}  # Valid return codes

    def test_main_function_integration(self, temporary_project_structure: str) -> None:
        """Test main function integration without mocking."""
        test_args = ["flext-quality", "analyze", temporary_project_structure]
        with patch.object(sys, "argv", test_args):
            result = main()

        # Should complete successfully
        assert result == 0

    def test_logging_integration(self) -> None:
        """Test logging setup integration."""
        # Test that logging can be set up without errors
        setup_logging("info")
        setup_logging("debug")
        setup_logging("warning")
        setup_logging("error")

        # Should complete without raising exceptions
        assert True

    def test_error_handling_integration(self) -> None:
        """Test error handling in CLI functions."""
        # Test with invalid paths
        args1 = argparse.Namespace(
            path="/nonexistent/path/that/does/not/exist",
            output=None,
            format="text",
            verbose=False,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        result1 = analyze_project(args1)
        assert result1 != 0

        args2 = argparse.Namespace(path="/nonexistent/path/that/does/not/exist")
        result2 = another_function(args2)
        assert result2 != 0
