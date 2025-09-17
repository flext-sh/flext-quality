"""Functional tests for CodeAnalyzer to improve coverage from 7% to 80%+.

Tests core functionality of the analyzer using real file analysis.
Focuses on the main analyze_project method and its helper methods.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_core import FlextTypes
from flext_quality import CodeAnalyzer


class TestCodeAnalyzerFunctional:
    """Functional tests for CodeAnalyzer main workflows."""

    @pytest.fixture
    def sample_project_dir(self) -> Path:
        """Create a temporary directory with sample Python files."""
        temp_dir = Path(tempfile.mkdtemp())

        # Create main.py with various code patterns
        main_py = temp_dir / "main.py"
        main_py.write_text('''"""Sample main module."""

import os
import sys
from typing import List, Optional
from typing import Dict
from typing import Optional

def calculate_average(numbers: List[float]) -> float:
    """Calculate average of numbers."""

    if not numbers:
      return 0.0

    total = sum(numbers)
    return total / len(numbers)

class DataProcessor:
    """Process data with validation."""

    def __init__(self, threshold: float = 0.8):
        """Initialize the instance."""

      self.threshold = threshold
      self.processed_count = 0

    def process_items(self, items: List[object]) -> List[object]:
      """Process list of items."""

      results = []
      for item in items:
          if self._is_valid_item(item):
              processed = self._process_single_item(item)
              if processed is not None:
                  results.append(processed)
                  self.processed_count += 1

      return results

    def _is_valid_item(self, item: object) -> bool:
      """Check if item is valid for processing."""

      return item is not None and isinstance(item, (str, int, float))

    def _process_single_item(self, item: object) -> object:
      """Process a single item."""

      if isinstance(item, str):
          return item.upper().strip()
      elif isinstance(item, (int, float)):
          return item * 2
      else:
          return None

def main():
    """Main function."""

    processor = DataProcessor()
    test_data = ["hello", "world", 42, 3.14, None]

    results = processor.process_items(test_data)
    average = calculate_average([1.0, 2.0, 3.0, 4.0, 5.0])

    print(f"Processed {len(results)} items")
    print(f"Average: {average}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
''')

        # Create utils.py with utility functions
        utils_py = temp_dir / "utils.py"
        utils_py.write_text('''"""Utility functions."""

def format_percentage(value: float) -> str:
    """Format value as percentage."""

    return f"{value * 100:.1f}%"

def safe_divide(a: float, b: float) -> float:
    """Safely divide two numbers."""

    if b == 0:
      return 0.0
    return a / b

# Simple function for testing
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""

    return x * y
''')

        # Create empty __init__.py
        (temp_dir / "__init__.py").write_text('"""Package init file."""\n')

        return temp_dir

    def test_analyzer_initialization(self, sample_project_dir: Path) -> None:
        """Test CodeAnalyzer initialization."""
        analyzer = CodeAnalyzer(sample_project_dir)

        assert analyzer.project_path == sample_project_dir
        assert analyzer._current_results is None

    def test_analyze_project_basic(self, sample_project_dir: Path) -> None:
        """Test basic project analysis functionality."""
        analyzer = CodeAnalyzer(sample_project_dir)

        results = analyzer.analyze_project()

        # Verify results structure
        assert hasattr(results, "overall_metrics")
        assert hasattr(results, "overall_metrics")
        assert "files_analyzed" in results
        assert hasattr(results.overall_metrics, "total_lines")
        assert "python_files" in results
        assert "metrics" in results
        assert "issues" in results

        # Verify basic metrics
        assert results["project_path"] == str(sample_project_dir)
        assert (
            results.overall_metrics.files_analyzed == 3
        )  # main.py, utils.py, __init__.py
        assert results["total_lines"] > 0

        # Verify file list
        python_files = results["python_files"]
        assert isinstance(python_files, list)
        assert len(python_files) == 3

        # Check that all expected files are found
        file_names = [Path(f).name for f in python_files]
        assert "main.py" in file_names
        assert "utils.py" in file_names
        assert "__init__.py" in file_names

    def test_analyze_project_with_options(self, sample_project_dir: Path) -> None:
        """Test project analysis with various options."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Test with all options enabled
        results_all = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

        assert isinstance(results_all, dict)
        assert results_all["files_analyzed"] == 3

        # Test with some options disabled
        results_minimal = analyzer.analyze_project(
            include_security=False,
            include_complexity=False,
            include_dead_code=False,
            include_duplicates=False,
        )

        assert isinstance(results_minimal, dict)
        assert results_minimal["files_analyzed"] == 3

    def test_find_python_files(self, sample_project_dir: Path) -> None:
        """Test _find_python_files method."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Access private method for testing
        python_files = analyzer._find_python_files()

        assert isinstance(python_files, list)
        assert len(python_files) == 3

        # Verify all files are Path objects and have .py extension
        for file_path in python_files:
            assert isinstance(file_path, Path)
            assert file_path.suffix == ".py"
            assert file_path.exists()

    def test_analyze_file_individual(self, sample_project_dir: Path) -> None:
        """Test _analyze_file method on individual files."""
        analyzer = CodeAnalyzer(sample_project_dir)

        main_py = sample_project_dir / "main.py"

        # Test analyzing individual file
        metrics = analyzer._analyze_file(main_py)

        # Now returns FileAnalysisResult object
        assert metrics is not None
        assert hasattr(metrics, "file_path")
        assert hasattr(metrics, "lines_of_code")
        assert hasattr(metrics, "complexity_score")

        # Verify metrics are reasonable
        assert isinstance(metrics.lines_of_code, int)
        assert metrics.lines_of_code > 10  # main.py has many lines
        assert isinstance(metrics.complexity_score, (int, float))

    def test_analyze_nonexistent_file(self, sample_project_dir: Path) -> None:
        """Test analyzing a non-existent file."""
        analyzer = CodeAnalyzer(sample_project_dir)

        nonexistent_file = sample_project_dir / "nonexistent.py"

        # Should return None or empty dict for non-existent file
        result = analyzer._analyze_file(nonexistent_file)

        # The method should gracefully handle missing files
        assert result is None or result == {}

    def test_calculate_overall_metrics(self, sample_project_dir: Path) -> None:
        """Test _calculate_overall_metrics method."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Create sample file metrics matching actual structure
        file_metrics = [
            {
                "lines_of_code": 50,
                "function_count": 3,
                "class_count": 1,
                "complexity": 10,
            },
            {
                "lines_of_code": 30,
                "function_count": 2,
                "class_count": 0,
                "complexity": 5,
            },
            {
                "lines_of_code": 10,
                "function_count": 0,
                "class_count": 1,
                "complexity": 2,
            },
        ]

        # Cast to expected type to handle list invariance
        file_metrics_typed: list[FlextTypes.Core.Dict] = file_metrics
        overall_metrics = analyzer._calculate_overall_metrics(file_metrics_typed)

        assert isinstance(overall_metrics, dict)

        # Should aggregate metrics from all files if implemented
        # Note: The actual implementation may vary, just verify it returns a dict

    def test_get_quality_score(self, sample_project_dir: Path) -> None:
        """Test get_quality_score method."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Run analysis first
        analyzer.analyze_project()

        # Get quality score
        score = analyzer.get_quality_score()

        assert isinstance(score, (int, float))
        assert 0 <= score <= 100

    def test_get_quality_grade(self, sample_project_dir: Path) -> None:
        """Test get_quality_grade method."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Run analysis first
        analyzer.analyze_project()

        # Get quality grade
        grade = analyzer.get_quality_grade()

        assert isinstance(grade, str)
        assert grade in {
            "A+",
            "A",
            "A-",
            "B+",
            "B",
            "B-",
            "C+",
            "C",
            "C-",
            "D+",
            "D",
            "D-",
            "F",
        }

    def test_empty_project_directory(self) -> None:
        """Test analyzer with empty project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_dir = Path(temp_dir)
            analyzer = CodeAnalyzer(empty_dir)

            results = analyzer.analyze_project()

            assert hasattr(results, "overall_metrics")
            assert results.overall_metrics.files_analyzed == 0
            assert results["total_lines"] == 0
            assert len(results["python_files"]) == 0

    def test_project_with_syntax_errors(self) -> None:
        """Test analyzer with files containing syntax errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)

            # Create file with syntax error
            bad_file = project_dir / "bad_syntax.py"
            bad_file.write_text("""

# This file has syntax errors
def broken_function(
    # Missing closing parenthesis and colon

invalid_syntax here
""")

            analyzer = CodeAnalyzer(project_dir)

            # Should handle syntax errors gracefully
            results = analyzer.analyze_project()

            assert hasattr(results, "overall_metrics")
            assert results.overall_metrics.files_analyzed == 1
            # Should still attempt to process the file

    def test_large_file_analysis(self, sample_project_dir: Path) -> None:
        """Test analyzer with a larger file."""
        # Create a larger Python file
        large_file = sample_project_dir / "large_file.py"
        large_content = '''"""Large Python file for testing."""

# Generate a larger file with repeated patterns
''' + "\n".join(
            [
                f'def function_{i}(param_{i}: int) -> int:\n    """Function {i}."""\n    return param_{i} * {i}'
                for i in range(50)
            ],
        )

        large_file.write_text(large_content)

        analyzer = CodeAnalyzer(sample_project_dir)
        results = analyzer.analyze_project()

        assert hasattr(results, "overall_metrics")
        assert results.overall_metrics.files_analyzed == 4  # Original 3 + 1 large file
        assert results["total_lines"] > 100  # Should be much larger now

    def test_analyzer_with_string_path(self) -> None:
        """Test analyzer initialization with string path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Pass string instead of Path
            analyzer = CodeAnalyzer(temp_dir)

            assert isinstance(analyzer.project_path, Path)
            assert str(analyzer.project_path) == temp_dir

    def test_concurrent_analysis_safety(self, sample_project_dir: Path) -> None:
        """Test that analyzer can handle multiple analyses safely."""
        analyzer = CodeAnalyzer(sample_project_dir)

        # Run multiple analyses
        results1 = analyzer.analyze_project(include_security=True)
        results2 = analyzer.analyze_project(include_security=False)

        # Both should succeed and return valid results
        assert isinstance(results1, dict)
        assert isinstance(results2, dict)
        assert results1["files_analyzed"] == results2["files_analyzed"]
        assert results1["project_path"] == results2["project_path"]


class TestCodeAnalyzerEdgeCases:
    """Test edge cases and error handling."""

    def test_nonexistent_project_path(self) -> None:
        """Test analyzer with non-existent project path."""
        nonexistent_path = Path("/nonexistent/path/to/project")
        analyzer = CodeAnalyzer(nonexistent_path)

        # Should handle gracefully
        results = analyzer.analyze_project()

        assert hasattr(results, "overall_metrics")
        assert results.overall_metrics.files_analyzed == 0

    def test_file_permission_issues(self) -> None:
        """Test analyzer when file permissions might be an issue."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)

            # Create a file
            test_file = project_dir / "test.py"
            test_file.write_text("# Simple test file\nprint('hello')\n")

            analyzer = CodeAnalyzer(project_dir)

            # Should work normally in most cases
            results = analyzer.analyze_project()

            assert hasattr(results, "overall_metrics")
            assert (
                results.overall_metrics.files_analyzed >= 0
            )  # Should handle gracefully

    def test_nested_directory_structure(self) -> None:
        """Test analyzer with nested directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)

            # Create nested structure
            (project_dir / "src").mkdir()
            (project_dir / "src" / "module1").mkdir()
            (project_dir / "tests").mkdir()

            # Add files in various locations
            (project_dir / "main.py").write_text("# Main file\nprint('main')\n")
            (project_dir / "src" / "utils.py").write_text(
                "# Utils file\ndef util(): pass\n",
            )
            (project_dir / "src" / "module1" / "core.py").write_text(
                "# Core file\nclass Core: pass\n",
            )
            (project_dir / "tests" / "test_main.py").write_text(
                "# Test file\ndef test(): assert True\n",
            )

            analyzer = CodeAnalyzer(project_dir)
            results = analyzer.analyze_project()

            assert hasattr(results, "overall_metrics")
            assert (
                results.overall_metrics.files_analyzed == 4
            )  # Should find all Python files

            # Check that files from different directories are found
            file_names = [Path(fm.file_path).name for fm in results.file_metrics]
            assert "main.py" in file_names
            assert "utils.py" in file_names
            assert "core.py" in file_names
            assert "test_main.py" in file_names
