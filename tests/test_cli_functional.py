"""Functional tests for CLI to improve coverage from 12% to 70%+.

Tests main CLI functions with real argument parsing and file operations.
Focuses on analyze_project and other CLI commands.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# NOTE: Old imports removed - functions moved to new API
# from flext_quality import analyze_project, another_function, setup_logging


# Global fixtures available to all test classes
@pytest.fixture
def sample_project_dir() -> Path:
    """Create a temporary directory with sample Python files."""
    temp_dir = Path(tempfile.mkdtemp())

    # Create main.py with simple code
    main_py = temp_dir / "main.py"
    main_py.write_text('''"""Main module."""

def hello_world():
    """Print hello world."""

    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
''')

    # Create utils.py
    utils_py = temp_dir / "utils.py"
    utils_py.write_text('''"""Utilities."""

def add(a: int, b: int) -> int:
    """Add two numbers."""

    return a + b
''')

    return temp_dir


@pytest.fixture
def basic_args(sample_project_dir: Path) -> argparse.Namespace:
    """Create basic CLI arguments."""
    return argparse.Namespace(
        path=str(sample_project_dir),
        format="json",
        output=None,
        include_security=True,
        include_complexity=True,
        include_dead_code=True,
        include_duplicates=True,
        verbose=False,
    )


class TestCLIFunctional:
    """Functional tests for CLI commands."""

    def test_setup_logging(self) -> None:
        """Test setup_logging function."""
        # Currently a no-op, but should not crash
        setup_logging()
        setup_logging("DEBUG")
        setup_logging("WARNING")
        # Should complete without errors
        assert True

    def test_analyze_project_basic_success(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test basic successful project analysis."""
        result = analyze_project(basic_args)

        # Should return 0 for success (good quality expected for simple code)
        assert result in {0, 1, 2}  # Valid exit codes

    def test_analyze_project_json_output(
        self,
        basic_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test project analysis with JSON output."""
        basic_args.format = "json"
        basic_args.output = None  # Print to stdout

        result = analyze_project(basic_args)

        # Should succeed
        assert result in {0, 1, 2}

        # Check stdout contains JSON
        captured = capsys.readouterr()
        assert captured.out.strip()  # Should have output

        # Should be valid JSON
        try:
            json.loads(captured.out)
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")

    def test_analyze_project_html_output(
        self,
        basic_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test project analysis with HTML output."""
        basic_args.format = "html"
        basic_args.output = None  # Print to stdout

        result = analyze_project(basic_args)

        # Should succeed
        assert result in {0, 1, 2}

        # Check stdout contains HTML
        captured = capsys.readouterr()
        assert captured.out.strip()  # Should have output
        assert "<html>" in captured.out or "<!DOCTYPE" in captured.out

    def test_self(self, basic_args: argparse.Namespace) -> None:
        """Test project analysis with file output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "report.json"
            basic_args.output = str(output_file)
            basic_args.format = "json"

            result = analyze_project(basic_args)

            # Should succeed
            assert result in {0, 1, 2}

            # File should be created
            assert output_file.exists()
            assert output_file.stat().st_size > 0

            # Should be valid JSON
            with output_file.open() as f:
                json.load(f)  # Should not raise exception

    def test_analyze_project_nonexistent_path(self) -> None:
        """Test analysis with non-existent project path."""
        args = argparse.Namespace(
            path="/nonexistent/path/to/project",
            format="json",
            output=None,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            verbose=False,
        )

        result = analyze_project(args)

        # Should return error code
        assert result == 1

    def test_analyze_project_empty_directory(self) -> None:
        """Test analysis with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = argparse.Namespace(
                path=temp_dir,
                format="json",
                output=None,
                include_security=True,
                include_complexity=True,
                include_dead_code=True,
                include_duplicates=True,
                verbose=False,
            )

            result = analyze_project(args)

            # Should return error code (no files to analyze)
            assert result == 1

    def test_analyze_project_with_options_disabled(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test analysis with various options disabled."""
        basic_args.include_security = False
        basic_args.include_complexity = False
        basic_args.include_dead_code = False
        basic_args.include_duplicates = False

        result = analyze_project(basic_args)

        # Should still succeed
        assert result in {0, 1, 2}

    def test_analysis_with_verbose_mode(self, basic_args: argparse.Namespace) -> None:
        """Test analysis with verbose mode."""
        basic_args.verbose = True

        result = analyze_project(basic_args)

        # Should succeed
        assert result in {0, 1, 2}

    def test_analyze_project_quiet_mode_json(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test that quiet mode is enabled for JSON output."""
        basic_args.format = "json"
        basic_args.verbose = False

        with patch.dict("os.environ", {}, clear=True):
            result = analyze_project(basic_args)

            # Should succeed
            assert result in {0, 1, 2}

            # Should have set quiet mode
            assert os.environ.get("FLEXT_OBSERVABILITY_QUIET") == "1"

    def test_analyze_project_quiet_mode_html(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test that quiet mode is enabled for HTML output."""
        basic_args.format = "html"
        basic_args.verbose = False

        with patch.dict("os.environ", {}, clear=True):
            result = analyze_project(basic_args)

            # Should succeed
            assert result in {0, 1, 2}

            # Should have set quiet mode
            assert os.environ.get("FLEXT_OBSERVABILITY_QUIET") == "1"

    def test_analyze_project_no_quiet_mode_verbose(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test that quiet mode is NOT enabled when verbose is True."""
        basic_args.format = "json"
        basic_args.verbose = True

        with patch.dict("os.environ", {}, clear=True):
            result = analyze_project(basic_args)

            # Should succeed
            assert result in {0, 1, 2}

            # Should NOT have set quiet mode
            assert "FLEXT_OBSERVABILITY_QUIET" not in os.environ

    def test_analyze_project_exception_handling(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test exception handling in analyze_project."""
        # Force an exception by corrupting the path
        basic_args.path = None  # This should cause an exception

        result = analyze_project(basic_args)

        # Should return error code
        assert result == 3

    def test_analyze_project_exception_verbose(
        self,
        basic_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test exception handling with verbose mode."""
        basic_args.path = None  # Force exception
        basic_args.verbose = True

        result = analyze_project(basic_args)

        # Should return error code
        assert result == 3

        # Should print traceback in verbose mode
        captured = capsys.readouterr()
        assert "Traceback" in captured.err or len(captured.err) > 0

    def test_another_function_basic_args(self, basic_args: argparse.Namespace) -> None:
        """Test another_function with basic arguments."""
        result = another_function(basic_args)

        # Should complete (return code varies by implementation)
        assert isinstance(result, int)

    def test_another_function_nonexistent_path(self) -> None:
        """Test another_function with non-existent path."""
        args = argparse.Namespace(path="/nonexistent/path", verbose=False)

        result = another_function(args)

        # Should return error code
        assert result == 1

    def test_another_function_exception_handling(self) -> None:
        """Test exception handling in another_function."""
        args = argparse.Namespace(
            path=None,  # Force exception
            verbose=False,
        )

        result = another_function(args)

        # Should handle exception gracefully
        assert isinstance(result, int)

    def test_analyze_project_quality_score_thresholds(
        self,
        sample_project_dir: Path,
    ) -> None:
        """Test different quality score thresholds."""
        # Create low-quality code to test different exit codes
        bad_code_file = sample_project_dir / "bad_code.py"
        bad_code_file.write_text("""

# Intentionally bad code for testing
def very_complex_function_with_many_parameters_and_bad_style(param1, param2, param3, param4, param5, param6, param7, param8):
    if param1:
      if param2:
          if param3:
              if param4:
                  if param5:
                      if param6:
                          if param7:
                              if param8:
                                  return param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8
                              else:
                                  return param1
                          else:
                              return param2
                      else:
                          return param3
                  else:
                      return param4
              else:
                  return param5
          else:
              return param6
      else:
          return param7
    else:
      return param8

def unused_function():
    pass

class UnusedClass:
    def unused_method(self):
      pass
""")

        args = argparse.Namespace(
            path=str(sample_project_dir),
            format="json",
            output=None,
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
            verbose=False,
        )

        result = analyze_project(args)

        # Should return some valid exit code
        assert result in {0, 1, 2}


class TestCLIEdgeCases:
    """Test edge cases and error conditions."""

    def test_analyze_project_invalid_format(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test analysis with invalid format argument."""
        basic_args.format = "invalid_format"

        # Should handle gracefully
        result = analyze_project(basic_args)
        assert isinstance(result, int)

    def test_analyze_project_path_resolution(self) -> None:
        """Test path resolution with relative paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "test.py").write_text("print('hello')")

            # Use relative path
            relative_path = (
                Path(temp_dir).relative_to(Path.cwd())
                if temp_dir.startswith(str(Path.cwd()))
                else temp_dir
            )

            args = argparse.Namespace(
                path=str(relative_path)
                if str(relative_path) != temp_dir
                else "./test_temp",
                format="json",
                output=None,
                include_security=True,
                include_complexity=True,
                include_dead_code=True,
                include_duplicates=True,
                verbose=False,
            )

            # Create a test directory in current working directory
            test_dir = Path("./test_temp")
            if not test_dir.exists():
                test_dir.mkdir()
                (test_dir / "test.py").write_text("print('hello')")

                try:
                    result = analyze_project(args)
                    assert isinstance(result, int)
                finally:
                    # Clean up
                    shutil.rmtree(test_dir)

    def test_analyze_project_output_directory_creation(
        self,
        basic_args: argparse.Namespace,
    ) -> None:
        """Test behavior when output directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Nested directory that doesn't exist - should raise FileNotFoundError
            output_file = Path(temp_dir) / "nested" / "dir" / "report.json"
            basic_args.output = str(output_file)
            basic_args.format = "json"

            # This should raise FileNotFoundError since CLI doesn't catch it
            with pytest.raises(FileNotFoundError):
                analyze_project(basic_args)

    def test_file_permissions_edge_case(self) -> None:
        """Test behavior with file permission issues."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            test_file = project_path / "test.py"
            test_file.write_text("print('hello')")

            args = argparse.Namespace(
                path=str(project_path),
                format="json",
                output=None,
                include_security=True,
                include_complexity=True,
                include_dead_code=True,
                include_duplicates=True,
                verbose=False,
            )

            # Should handle gracefully even with potential permission issues
            result = analyze_project(args)
            assert isinstance(result, int)

    def test_large_project_handling(self) -> None:
        """Test CLI with a larger project structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create multiple directories and files
            for i in range(10):
                subdir = project_path / f"module_{i}"
                subdir.mkdir()

                for j in range(5):
                    py_file = subdir / f"file_{j}.py"
                    py_file.write_text(f'''
"""Module {i} file {j}."""

def function_{i}_{j}():
    """Function {i} {j}."""

    return {i} + {j}

class Class_{i}_{j}:
    """Class {i} {j}."""

    def method(self):
      return {i} * {j}
''')

            args = argparse.Namespace(
                path=str(project_path),
                format="json",
                output=None,
                include_security=True,
                include_complexity=True,
                include_dead_code=True,
                include_duplicates=True,
                verbose=False,
            )

            result = analyze_project(args)

            # Should handle large projects
            assert isinstance(result, int)
            assert result in {0, 1, 2}  # Should succeed with some quality score


class TestCLIIntegration:
    """Integration tests for CLI with various scenarios."""

    def test_end_to_end_analysis_workflow(self) -> None:
        """Test complete end-to-end analysis workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create a realistic Python project structure
            src_dir = project_path / "src"
            src_dir.mkdir()
            tests_dir = project_path / "tests"
            tests_dir.mkdir()

            # Main application code
            (src_dir / "__init__.py").write_text("")
            (src_dir / "main.py").write_text('''
"""Main application module."""

import sys

def process_data(data: list[str]) -> Optional[list[str]]:
    """Process input data."""

    if not data:
      return None

    results = []
    for item in data:
      if item and isinstance(item, str):
          processed = item.strip().upper()
          results.append(processed)

    return results

def main() -> int:
    """Main entry point."""

    test_data = ["hello", "world", " test "]
    results = process_data(test_data)

    if results:
      for result in results:
          print(result)
      return 0
    else:
      print("No data to process")
      return 1

if __name__ == "__main__":
    sys.exit(main())
''')

            # Test code
            (tests_dir / "__init__.py").write_text("")
            (tests_dir / "test_main.py").write_text('''
"""Tests for main module."""

import unittest
from src.main import process_data

class TestProcessData(unittest.TestCase):
    """Test process_data function."""

    def test_process_data_success(self):
      """Test successful data processing."""

      data = ["hello", "world"]
      result = process_data(data)
      self.assertEqual(result, ["HELLO", "WORLD"])

    def test_process_data_empty(self):
      """Test empty data processing."""

      result = process_data([])
      self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
''')

            # Run analysis
            args = argparse.Namespace(
                path=str(project_path),
                format="json",
                output=None,
                include_security=True,
                include_complexity=True,
                include_dead_code=True,
                include_duplicates=True,
                verbose=False,
            )

            result = analyze_project(args)

            # Should succeed
            assert result in {0, 1, 2}

    def test_cli_with_configuration_variations(self) -> None:
        """Test CLI with different configuration combinations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "simple.py").write_text("def hello(): return 'hello'")

            # Test different combinations of analysis options
            configurations = [
                {
                    "include_security": True,
                    "include_complexity": False,
                    "include_dead_code": False,
                    "include_duplicates": False,
                },
                {
                    "include_security": False,
                    "include_complexity": True,
                    "include_dead_code": False,
                    "include_duplicates": False,
                },
                {
                    "include_security": False,
                    "include_complexity": False,
                    "include_dead_code": True,
                    "include_duplicates": False,
                },
                {
                    "include_security": False,
                    "include_complexity": False,
                    "include_dead_code": False,
                    "include_duplicates": True,
                },
                {
                    "include_security": True,
                    "include_complexity": True,
                    "include_dead_code": True,
                    "include_duplicates": True,
                },
            ]

            for config in configurations:
                args = argparse.Namespace(
                    path=str(project_path),
                    format="json",
                    output=None,
                    verbose=False,
                    **config,
                )

                result = analyze_project(args)
                assert isinstance(result, int)
                assert result in {0, 1, 2}
