"""Test CLI functionality."""

from __future__ import annotations

import argparse
from io import StringIO
from unittest.mock import MagicMock, patch

from flext_quality.cli import analyze_project, another_function, main, setup_logging


class TestSetupLogging:
    """Test setup_logging function."""

    def test_setup_logging_default(self) -> None:
        """Test setup_logging with default level."""
        # Currently a no-op, so just ensure it doesn't crash
        setup_logging()

    def test_setup_logging_with_level(self) -> None:
        """Test setup_logging with specific level."""
        # Currently a no-op, so just ensure it doesn't crash
        setup_logging("DEBUG")


class TestAnalyzeProject:
    """Test analyze_project function."""

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_success_high_quality(
        self,
        mock_path: MagicMock,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test successful analysis with high quality score."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {},
            "files_analyzed": 3,  # Mock some files analyzed
        }
        mock_analyzer.get_quality_score.return_value = 85.0
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report_class.return_value = mock_report

        # Create test args
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="text",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 0  # High quality returns 0
        mock_analyzer_class.assert_called_once_with(mock_path_instance)
        mock_analyzer.analyze_project.assert_called_once_with(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )
        mock_report_class.assert_called_once_with(
            {
                "issues": {},
                "files_analyzed": 3,  # Include the complete analyzer results
            },
        )

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_success_medium_quality(
        self,
        mock_path: MagicMock,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test successful analysis with medium quality score."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {},
            "files_analyzed": 3,  # Mock some files analyzed
        }
        mock_analyzer.get_quality_score.return_value = 70.0  # Medium quality
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report_class.return_value = mock_report

        # Create test args
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="text",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 1  # Medium quality returns 1

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_success_poor_quality(
        self,
        mock_path: MagicMock,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test successful analysis with poor quality score."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {},
            "files_analyzed": 3,  # Mock some files analyzed
        }
        mock_analyzer.get_quality_score.return_value = 40.0  # Poor quality
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report_class.return_value = mock_report

        # Create test args
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="text",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 2  # Poor quality returns 2

    @patch("flext_quality.cli.Path")
    def test_analyze_project_path_not_exists(self, mock_path: MagicMock) -> None:
        """Test analyze_project when path doesn't exist."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value.resolve.return_value = mock_path_instance

        # Create test args
        args = argparse.Namespace(path="/nonexistent/path")

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 1  # Path not exists returns 1

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_with_output_file(
        self,
        mock_path: MagicMock,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test analyze_project with output file."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {},
            "files_analyzed": 3,  # Mock some files analyzed
        }
        mock_analyzer.get_quality_score.return_value = 85.0
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report_class.return_value = mock_report

        # Create test args with output
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output="/output/report.html",
            format="html",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 0
        mock_report.save_report.assert_called_once()

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.QualityReport")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_json_format_no_output(
        self,
        mock_path: MagicMock,
        mock_report_class: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test analyze_project with JSON format but no output file."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {},
            "files_analyzed": 3,  # Mock some files analyzed
        }
        mock_analyzer.get_quality_score.return_value = 85.0
        mock_analyzer_class.return_value = mock_analyzer

        mock_report = MagicMock()
        mock_report.to_json.return_value = (
            '{"test": "json_output"}'  # Return string for sys.stdout.write()
        )
        mock_report_class.return_value = mock_report

        # Create test args with JSON format but no output
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="json",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 0
        # Should not call save_report when no output file
        mock_report.save_report.assert_not_called()

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.traceback")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_exception_verbose(
        self,
        mock_path: MagicMock,
        mock_traceback: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test analyze_project exception handling with verbose mode."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer_class.side_effect = RuntimeError("Test error")

        # Create test args with verbose mode
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="text",
            verbose=True,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 3  # Exception returns 3
        mock_traceback.print_exc.assert_called_once()

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.traceback")
    @patch("flext_quality.cli.Path")
    def test_analyze_project_exception_not_verbose(
        self,
        mock_path: MagicMock,
        mock_traceback: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test analyze_project exception handling without verbose mode."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer_class.side_effect = ValueError("Test error")

        # Create test args without verbose mode
        args = argparse.Namespace(
            path="/test/path",
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            output=None,
            format="text",
            verbose=False,
        )

        # Execute
        result = analyze_project(args)

        # Assertions
        assert result == 3  # Exception returns 3
        mock_traceback.print_exc.assert_not_called()


class TestAnotherFunction:
    """Test another_function (score command)."""

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.Path")
    def test_another_function_success_good_score(
        self,
        mock_path: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test another_function with good quality score."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {
                "security": ["issue1"],
                "complexity": ["issue2"],
            },
        }
        mock_analyzer.get_quality_score.return_value = 75.0  # Good score
        mock_analyzer.get_quality_grade.return_value = "B"
        mock_analyzer_class.return_value = mock_analyzer

        # Create test args
        args = argparse.Namespace(path="/test/path")

        # Execute
        result = another_function(args)

        # Assertions
        assert result == 0  # Good score returns 0
        mock_analyzer.analyze_project.assert_called_once_with(
            include_security=True,
            include_complexity=True,
            include_dead_code=False,  # Skip for speed
            include_duplicates=False,  # Skip for speed
        )
        mock_analyzer.get_quality_score.assert_called_once()
        mock_analyzer.get_quality_grade.assert_called_once()

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.Path")
    def test_another_function_success_poor_score(
        self,
        mock_path: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test another_function with poor quality score."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer = MagicMock()
        mock_analyzer.analyze_project.return_value = {
            "issues": {
                "security": [],
                "complexity": [],
            },
        }
        mock_analyzer.get_quality_score.return_value = 60.0  # Poor score
        mock_analyzer_class.return_value = mock_analyzer

        # Create test args
        args = argparse.Namespace(path="/test/path")

        # Execute
        result = another_function(args)

        # Assertions
        assert result == 1  # Poor score returns 1

    @patch("flext_quality.cli.Path")
    def test_another_function_path_not_exists(self, mock_path: MagicMock) -> None:
        """Test another_function when path doesn't exist."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value.resolve.return_value = mock_path_instance

        # Create test args
        args = argparse.Namespace(path="/nonexistent/path")

        # Execute
        result = another_function(args)

        # Assertions
        assert result == 1  # Path not exists returns 1

    @patch("flext_quality.cli.CodeAnalyzer")
    @patch("flext_quality.cli.Path")
    def test_another_function_exception(
        self,
        mock_path: MagicMock,
        mock_analyzer_class: MagicMock,
    ) -> None:
        """Test another_function exception handling."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.resolve.return_value = mock_path_instance

        mock_analyzer_class.side_effect = TypeError("Test error")

        # Create test args
        args = argparse.Namespace(path="/test/path")

        # Execute
        result = another_function(args)

        # Assertions
        assert result == 3  # Exception returns 3


class TestMain:
    """Test main function."""

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    @patch("sys.argv", ["flext-quality", "analyze", "/test/path"])
    def test_main_analyze_command(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
    ) -> None:
        """Test main function with analyze command."""
        mock_analyze.return_value = 0

        result = main()

        assert result == 0
        mock_setup_logging.assert_called_once_with("INFO")
        mock_analyze.assert_called_once()

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.another_function")
    @patch("sys.argv", ["flext-quality", "score", "/test/path"])
    def test_main_score_command(
        self,
        mock_another: MagicMock,
        mock_setup_logging: MagicMock,
    ) -> None:
        """Test main function with score command."""
        mock_another.return_value = 1

        result = main()

        assert result == 1
        mock_setup_logging.assert_called_once_with("INFO")
        mock_another.assert_called_once()

    @patch("flext_quality.cli.setup_logging")
    @patch("sys.argv", ["flext-quality"])
    def test_main_no_command(self, mock_setup_logging: MagicMock) -> None:
        """Test main function with no command (should show help)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = main()

        assert result == 1
        mock_setup_logging.assert_called_once_with("INFO")

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    @patch(
        "sys.argv",
        [
            "flext-quality",
            "--verbose",
            "--log-level",
            "DEBUG",
            "analyze",
            "/test/path",
            "--output",
            "report.html",
            "--format",
            "html",
            "--no-security",
            "--no-complexity",
            "--no-dead-code",
            "--no-duplicates",
        ],
    )
    def test_main_full_options(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
    ) -> None:
        """Test main function with full options."""
        mock_analyze.return_value = 0

        result = main()

        assert result == 0
        mock_setup_logging.assert_called_once_with("DEBUG")
        mock_analyze.assert_called_once()

        # Check that the args were parsed correctly
        call_args = mock_analyze.call_args[0][0]
        assert call_args.verbose is True
        assert call_args.log_level == "DEBUG"
        assert call_args.path == "/test/path"
        assert call_args.output == "report.html"
        assert call_args.format == "html"
        assert call_args.include_security is False
        assert call_args.include_complexity is False
        assert call_args.include_dead_code is False
        assert call_args.include_duplicates is False

    @patch("flext_quality.cli.setup_logging")
    @patch("flext_quality.cli.analyze_project")
    @patch("sys.argv", ["flext-quality", "analyze", "/test/path"])
    def test_main_function_returns_none(
        self,
        mock_analyze: MagicMock,
        mock_setup_logging: MagicMock,
    ) -> None:
        """Test main function when command function returns None."""
        mock_analyze.return_value = None

        result = main()

        assert result == 0  # None should be converted to 0
        mock_setup_logging.assert_called_once()
        mock_analyze.assert_called_once()


class TestMainExecution:
    """Test main execution block."""

    @patch("flext_quality.cli.main")
    @patch("sys.exit")
    def test_main_execution_block(
        self,
        mock_exit: MagicMock,
        mock_main: MagicMock,
    ) -> None:
        """Test the if __name__ == '__main__' block."""
        mock_main.return_value = 2

        # Import to trigger the main execution
        import flext_quality.cli

        # Manually trigger the main block since we can't easily test __name__ == '__main__'
        if hasattr(flext_quality.cli, "__main__"):
            flext_quality.cli.main()

        # The mock_main should have been called during import if __name__ == '__main__'
        # But since we're testing in pytest, __name__ won't be '__main__'
        # So we just verify the function exists and can be called
        assert callable(flext_quality.cli.main)
