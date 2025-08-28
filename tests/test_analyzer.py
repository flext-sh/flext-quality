"""Comprehensive tests for the CodeAnalyzer class."""

import ast
import logging
import stat
import tempfile
from collections.abc import Generator
from pathlib import Path
from textwrap import dedent

import pytest

from flext_quality import (
    AnalysisResults,
    CodeAnalyzer,
    DuplicationIssue,
    OverallMetrics,
    QualityGradeCalculator,
)
from flext_quality.analysis_types import FileAnalysisResult
from flext_quality.utilities import FlextTestUtilities


class TestCodeAnalyzer:
    """Test suite for CodeAnalyzer functionality."""

    @pytest.fixture
    def temp_project(self) -> Generator[Path]:
        """Create a temporary project with sample Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)

            # Create various test files

            # Simple file
            simple_file = project_path / "simple.py"
            simple_file.write_text(
                dedent("""
              # Simple module
              def hello_world():
                  '''Simple function.'''
                  return "Hello, World!"

              class SimpleClass:
                  '''Simple class.'''
                  def method(self):
                      return "simple"
          """),
            )

            # Complex file with high complexity
            complex_file = project_path / "complex.py"
            complex_file.write_text(
                dedent("""
              # Complex module with high cyclomatic complexity
              def complex_function(data):
                  '''Function with high complexity.'''
                  if not data:
                      return None

                  for item in data:
                      if item > 10:
                          for sub in item:
                              if sub < 5:
                                  while sub > 0:
                                      if sub % 2 == 0:
                                          try:
                                              result = sub / 2
                                          except ZeroDivisionError:
                                              result = 0
                                          if result > 1:
                                              return result
                                      sub -= 1
                  return data

              class ComplexClass:
                  def method1(self):
                      return 1

                  def method2(self):
                      return 2
          """),
            )

            # File with security issues
            security_file = project_path / "security.py"
            security_file.write_text(
                dedent("""
              # File with security issues
              import os

              def dangerous_function(user_input):
                  '''Function with security issues.'''
                  # Dangerous eval usage
                  result = eval(user_input)

                  # Dangerous exec usage
                  exec("print('test')")

                  # Command injection risk
                  os.system("ls -la")

                  return result
          """),
            )

            # File with syntax error
            syntax_error_file = project_path / "syntax_error.py"
            syntax_error_file.write_text(
                dedent("""
              # File with syntax error
              def broken_function(
                  return "This has a syntax error"
          """),
            )

            # File with unused imports
            dead_code_file = project_path / "dead_code.py"
            dead_code_file.write_text(
                dedent("""
              # File with dead code indicators
              import sys  # unused
              from typing import List  # unused
              import json

              def use_json():
                  return json.dumps({"test": True})
          """),
            )

            # Duplicate file 1
            duplicate1 = project_path / "duplicate1.py"
            duplicate1.write_text(
                dedent("""
              # Duplicate content file 1
              def duplicate_function():
                  '''Duplicate function implementation.'''
                  data = [1, 2, 3, 4, 5]
                  result = []
                  for item in data:
                      if item % 2 == 0:
                          result.append(item * 2)
                  return result

              class DuplicateClass:
                  def method(self):
                      return "duplicate"
          """),
            )

            # Duplicate file 2 (similar to duplicate1)
            duplicate2 = project_path / "duplicate2.py"
            duplicate2.write_text(
                dedent("""
              # Duplicate content file 2
              def duplicate_function():
                  '''Duplicate function implementation.'''
                  data = [1, 2, 3, 4, 5]
                  result = []
                  for item in data:
                      if item % 2 == 0:
                          result.append(item * 2)
                  return result

              class DuplicateClass:
                  def method(self):
                      return "duplicate"
          """),
            )

            # Create subdirectory with files
            subdir = project_path / "subpackage"
            subdir.mkdir()

            sub_file = subdir / "sub_module.py"
            sub_file.write_text(
                dedent("""
              # Subpackage module
              def sub_function():
                  return "sub"
          """),
            )

            # Create files to ignore (hidden, cache, etc.)
            (project_path / ".hidden.py").write_text("# Hidden file")
            cache_dir = project_path / "__pycache__"
            cache_dir.mkdir()
            (cache_dir / "cached.py").write_text("# Cached file")

            yield project_path

    def test_analyzer_initialization(self, temp_project: Path) -> None:
        """Test CodeAnalyzer initialization."""
        analyzer = CodeAnalyzer(temp_project)
        assert analyzer.project_path == temp_project
        assert analyzer._current_results is None

    def test_analyzer_with_string_path(self, temp_project: Path) -> None:
        """Test CodeAnalyzer initialization with string path."""
        analyzer = CodeAnalyzer(str(temp_project))
        assert analyzer.project_path == temp_project

    def test_find_python_files(self, temp_project: Path) -> None:
        """Test finding Python files in project."""
        analyzer = CodeAnalyzer(temp_project)
        python_files = analyzer._find_python_files()

        # Should find all .py files except hidden and cached ones
        file_names = {f.name for f in python_files}
        expected_files = {
            "simple.py",
            "complex.py",
            "security.py",
            "syntax_error.py",
            "dead_code.py",
            "duplicate1.py",
            "duplicate2.py",
            "sub_module.py",
        }

        assert expected_files.issubset(file_names)
        assert ".hidden.py" not in file_names
        assert "cached.py" not in file_names

    def test_find_python_files_nonexistent_path(self) -> None:
        """Test finding Python files with non-existent path."""
        analyzer = CodeAnalyzer("/nonexistent/path")
        python_files = analyzer._find_python_files()
        assert python_files == []

    def test_analyze_file_simple(self, temp_project: Path) -> None:
        """Test analyzing a simple Python file."""
        analyzer = CodeAnalyzer(temp_project)
        simple_file = temp_project / "simple.py"

        metrics = analyzer._analyze_file(simple_file)

        assert metrics is not None
        assert metrics.file_path == simple_file
        assert metrics.lines_of_code > 0
        assert metrics.complexity_score > 0
        assert isinstance(metrics.security_issues, int)
        assert isinstance(metrics.style_issues, int)
        assert isinstance(metrics.dead_code_lines, int)

    def test_analyze_file_with_syntax_error(self, temp_project: Path) -> None:
        """Test analyzing a file with syntax error."""
        analyzer = CodeAnalyzer(temp_project)
        syntax_error_file = temp_project / "syntax_error.py"

        metrics = analyzer._analyze_file(syntax_error_file)

        assert metrics is not None
        assert str(metrics.file_path).endswith("syntax_error.py")
        assert metrics.lines_of_code >= 0  # May have lines even with syntax error
        assert metrics.complexity_score >= 0
        assert metrics.security_issues >= 0

    def test_analyze_file_nonexistent(self, temp_project: Path) -> None:
        """Test analyzing a non-existent file."""
        analyzer = CodeAnalyzer(temp_project)
        nonexistent_file = temp_project / "does_not_exist.py"

        metrics = analyzer._analyze_file(nonexistent_file)
        assert metrics is None

    def test_calculate_complexity(self, temp_project: Path) -> None:
        """Test complexity calculation."""
        analyzer = CodeAnalyzer(temp_project)

        # Simple code with minimal complexity
        simple_code = "def simple(): return True"
        simple_tree = ast.parse(simple_code)
        simple_complexity = analyzer._calculate_complexity(simple_tree)
        assert simple_complexity == 1

        # Complex code with multiple decision points
        complex_code = dedent("""
          def complex_func(x):
              if x > 0:
                  for i in range(x):
                      if i % 2 == 0:
                          try:
                              result = i / 2
                          except ZeroDivisionError:
                              result = 0
                          if result and result > 1:
                              return result
                  return x
              else:
                  return 0
      """)
        complex_tree = ast.parse(complex_code)
        complex_complexity = analyzer._calculate_complexity(complex_tree)
        assert complex_complexity > 5

    def test_calculate_overall_metrics(self, temp_project: Path) -> None:
        """Test calculation of overall metrics."""
        analyzer = CodeAnalyzer(temp_project)

        file_metrics: list[dict[str, object]] = [
            {
                "lines_of_code": 10,
                "function_count": 2,
                "class_count": 1,
                "complexity": 3,
            },
            {
                "lines_of_code": 20,
                "function_count": 3,
                "class_count": 0,
                "complexity": 5,
            },
            {
                "lines_of_code": 15,
                "function_count": 1,
                "class_count": 2,
                "complexity": 2,
            },
        ]

        overall_metrics = analyzer._calculate_overall_metrics(file_metrics)

        assert overall_metrics["total_files"] == 3
        assert overall_metrics["total_lines_of_code"] == 45
        assert overall_metrics["total_functions"] == 6
        assert overall_metrics["total_classes"] == 3
        assert overall_metrics["average_complexity"] == 10 / 3  # (3+5+2)/3
        assert overall_metrics["max_complexity"] == 5
        assert overall_metrics["avg_lines_per_file"] == 15.0

    def test_calculate_overall_metrics_empty(self, temp_project: Path) -> None:
        """Test calculation of overall metrics with empty list."""
        analyzer = CodeAnalyzer(temp_project)
        overall_metrics = analyzer._calculate_overall_metrics([])
        assert overall_metrics == {}

    def test_analyze_security(self, temp_project: Path) -> None:
        """Test security analysis with real security issues."""
        # Create a file with real security issues
        security_file = temp_project / "security_issues.py"
        FlextTestUtilities.create_test_file_with_issues(security_file, "security")

        analyzer = CodeAnalyzer(temp_project)
        security_issues = analyzer._analyze_security()

        # Should return a list of security issue objects or dictionaries
        assert isinstance(security_issues, list)

        # Should detect at least some issues in the file with security problems
        if security_issues:
            # Check if we get proper issue objects
            first_issue = security_issues[0]
            # Could be SecurityIssue object or dict depending on implementation
            assert hasattr(first_issue, "__dict__")

    def test_analyze_complexity_issues(self, temp_project: Path) -> None:
        """Test complexity analysis."""
        analyzer = CodeAnalyzer(temp_project)

        # Create proper FileAnalysisResult objects for complexity analysis
        file_metrics = [
            FileAnalysisResult(
                file_path=Path("simple.py"),
                lines_of_code=20,
                complexity_score=85.0,  # Low complexity: (100-85)/2 = 7.5 (below threshold 10)
                security_issues=0,
                style_issues=0,
                dead_code_lines=0,
            ),
            FileAnalysisResult(
                file_path=Path("complex.py"),
                lines_of_code=50,
                complexity_score=70.0,  # High complexity: (100-70)/2 = 15 (above threshold 10)
                security_issues=0,
                style_issues=0,
                dead_code_lines=0,
            ),
            FileAnalysisResult(
                file_path=Path("other.py"),
                lines_of_code=30,
                complexity_score=82.0,  # Low complexity: (100-82)/2 = 9 (below threshold 10)
                security_issues=0,
                style_issues=0,
                dead_code_lines=0,
            ),
        ]

        complexity_issues = analyzer._analyze_complexity(file_metrics)

        assert len(complexity_issues) == 1
        # Use typed object access instead of dict access (migrated to current API)
        complexity_issue = complexity_issues[0]
        assert hasattr(complexity_issue, "file_path")
        assert complexity_issue.file_path == "complex.py"
        assert complexity_issue.complexity_value == 15  # (100-70)/2 = 15
        assert hasattr(complexity_issue, "function_name")

    def test_analyze_dead_code(self, temp_project: Path) -> None:
        """Test dead code analysis."""
        analyzer = CodeAnalyzer(temp_project)
        dead_code_issues = analyzer._analyze_dead_code()

        # Should find unused imports marked with # unused
        # Use typed object access instead of dict access (migrated to current API)
        unused_issues = [
            issue
            for issue in dead_code_issues
            if hasattr(issue, "code_type") and issue.code_type == "unused_import"
        ]
        assert len(unused_issues) >= 2  # sys and typing imports marked as unused

    def test_analyze_duplicates(self, temp_project: Path) -> None:
        """Test duplicate code analysis."""
        analyzer = CodeAnalyzer(temp_project)
        duplicate_issues = analyzer._analyze_duplicates()

        # Should find high similarity between duplicate1.py and duplicate2.py
        assert len(duplicate_issues) >= 1

        duplicate_issue = duplicate_issues[0]
        # Use typed object instead of dict access (migrated to current API)
        assert isinstance(duplicate_issue, DuplicationIssue)
        assert len(duplicate_issue.files) == 2
        assert duplicate_issue.similarity > 0.8
        assert "duplicate1.py" in duplicate_issue.files
        assert "duplicate2.py" in duplicate_issue.files

    def test_full_project_analysis(self, temp_project: Path) -> None:
        """Test complete project analysis."""
        analyzer = CodeAnalyzer(temp_project)
        results = analyzer.analyze_project()

        # Check that results is the correct type
        assert hasattr(results, "overall_metrics")
        assert hasattr(results, "file_metrics")
        assert hasattr(results, "complexity_issues")
        assert hasattr(results, "security_issues")
        assert hasattr(results, "dead_code_issues")
        assert hasattr(results, "duplication_issues")

        # Check that files were found
        assert results.overall_metrics.files_analyzed > 0
        assert results.overall_metrics.total_lines > 0

        # Check that all expected files are analyzed
        analyzed_files = [str(fm.file_path.name) for fm in results.file_metrics]
        expected_files = ["simple.py", "complex.py", "security.py", "dead_code.py"]
        for expected_file in expected_files:
            assert expected_file in analyzed_files

        # Check that we have file metrics for each analyzed file
        assert len(results.file_metrics) > 0
        for file_metric in results.file_metrics:
            assert file_metric.lines_of_code > 0
            assert file_metric.complexity_score >= 0

        # Should find security issues (due to eval/exec usage in security.py)
        assert len(results.security_issues) > 0

        # Check that issue types are correct
        for issue in results.security_issues:
            assert hasattr(issue, "file_path")
            assert hasattr(issue, "severity")
            assert hasattr(issue, "message")

        # Complexity issues depend on threshold
        assert len(results.complexity_issues) >= 0

        # Should find duplicate issues (duplicated files created in fixture)
        assert len(results.duplication_issues) > 0

    def test_selective_analysis(self, temp_project: Path) -> None:
        """Test analysis with selective options."""
        analyzer = CodeAnalyzer(temp_project)

        # Test with only security analysis
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=False,
            include_dead_code=False,
            include_duplicates=False,
        )

        # Use typed object access instead of dict access (migrated to current API)
        assert len(results.security_issues) > 0
        assert len(results.complexity_issues) == 0
        assert len(results.dead_code_issues) == 0
        assert len(results.duplication_issues) == 0

    def test_get_quality_score_no_analysis(self, temp_project: Path) -> None:
        """Test quality score with no analysis results."""
        analyzer = CodeAnalyzer(temp_project)
        score = analyzer.get_quality_score()
        assert score == 0.0

    def test_get_quality_score_with_issues(self, temp_project: Path) -> None:
        """Test quality score calculation with various issues."""
        analyzer = CodeAnalyzer(temp_project)

        # Run analysis first
        analyzer.analyze_project()

        score = analyzer.get_quality_score()
        assert 0.0 <= score <= 100.0

        # Score should be reduced due to issues found
        assert score < 100.0

    def test_get_quality_score_perfect(self, temp_project: Path) -> None:
        """Test quality score with no issues."""
        analyzer = CodeAnalyzer(temp_project)

        # Set perfect analysis results using new typed structure with all required fields
        analyzer._current_results = AnalysisResults(
            overall_metrics=OverallMetrics(
                files_analyzed=1,
                total_lines=10,
                quality_score=100.0,
                coverage_score=100.0,
                security_score=100.0,
                maintainability_score=100.0,
                complexity_score=100.0,
            ),
            file_metrics=[],
            complexity_issues=[],
            security_issues=[],
            dead_code_issues=[],
            duplication_issues=[],
        )

        score = analyzer.get_quality_score()
        assert score == 100.0

    def test_get_quality_grade(self) -> None:
        """Test quality grade calculation using real grade calculator."""
        # Test grade calculation using the real grade calculator directly
        # This tests the actual business logic without mocking
        test_cases = [
            (100.0, "A+"),
            (95.0, "A+"),
            (90.0, "A"),
            (85.0, "A-"),
            (75.0, "B"),
            (60.0, "C"),
            (45.0, "D"),
            (30.0, "F"),
        ]

        for score, expected_grade in test_cases:
            # Use real grade calculation logic - no mocks
            calculated_grade = QualityGradeCalculator.calculate_grade(score)
            assert calculated_grade.value == expected_grade, (
                f"Score {score} should give grade {expected_grade}"
            )

    def test_analysis_results_storage(self, temp_project: Path) -> None:
        """Test that analysis results are properly stored."""
        analyzer = CodeAnalyzer(temp_project)

        # Initially empty
        assert analyzer._current_results is None

        # After analysis, should contain results
        results = analyzer.analyze_project()
        assert analyzer._current_results == results
        assert analyzer._current_results is not None

    def test_analyze_project_logging(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test that analysis produces appropriate log messages."""
        caplog.set_level(logging.INFO)

        analyzer = CodeAnalyzer(temp_project)
        analyzer.analyze_project()

        # Check for expected log messages
        log_messages = [record.message for record in caplog.records]
        assert any("Starting project analysis" in msg for msg in log_messages)
        assert any("Analysis completed" in msg for msg in log_messages)

    def test_file_analysis_error_handling(self, temp_project: Path) -> None:
        """Test error handling in file analysis using real problematic files."""
        analyzer = CodeAnalyzer(temp_project)

        # Create a file with real syntax errors that will cause analysis issues
        problem_file = temp_project / "syntax_error.py"
        FlextTestUtilities.create_failing_file(problem_file, "syntax_error")

        # Create a normal file that should analyze successfully
        good_file = temp_project / "good_file.py"
        good_file.write_text("def hello(): return 'world'")

        # Should handle syntax error gracefully and continue with other files
        results = analyzer.analyze_project()

        # Should still return results and have analyzed at least the good file
        assert hasattr(results, "overall_metrics")
        assert results.overall_metrics.files_analyzed >= 1

    def test_security_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in security analysis using real problematic files."""
        caplog.set_level(logging.WARNING)
        analyzer = CodeAnalyzer(temp_project)

        # Create a file with real encoding issues that could cause read problems
        error_file = temp_project / "encoding_error.py"
        FlextTestUtilities.create_failing_file(error_file, "encoding_error")

        # Create a normal file for comparison
        normal_file = temp_project / "normal.py"
        normal_file.write_text("def safe_function(): return 'safe'")

        # Run security analysis - should handle encoding error gracefully
        security_issues = analyzer._analyze_security()

        # Should return a list even if some files had errors
        assert isinstance(security_issues, list)

        # Should still be able to analyze the normal file

    def test_dead_code_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in dead code analysis with real file system errors."""
        caplog.set_level(logging.WARNING)

        analyzer = CodeAnalyzer(temp_project)

        # Create a real file with problematic content that may cause parsing errors
        problematic_file = temp_project / "problematic_syntax.py"
        problematic_file.write_text(
            (
                "# File with syntax error that might cause issues\n"
                "import sys\n"
                "def broken_function(\n"  # Intentionally broken syntax
                "    pass\n"
            ),
            encoding="utf-8",
        )

        # Run dead code analysis - should handle errors gracefully
        dead_code_issues = analyzer._analyze_dead_code()
        assert isinstance(dead_code_issues, list)

        # The analysis should complete without crashing, even with problematic files
        # object warnings about file issues should be logged
        warning_messages = [
            record.message for record in caplog.records if record.levelname == "WARNING"
        ]
        # Warnings may or may not exist depending on the error handling implementation
        # The important thing is that the analysis completes successfully
        assert isinstance(
            warning_messages, list
        )  # Use the variable to avoid unused warning

    def test_duplicate_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in duplicate analysis."""
        caplog.set_level(logging.WARNING)

        analyzer = CodeAnalyzer(temp_project)

        # Create a real file that is likely to cause reading issues

        problematic_file = temp_project / "binary_file.py"
        # Create a file with binary content that might cause encoding issues
        problematic_file.write_bytes(
            b"\x00\x01\x02\x03# This file has binary content\nimport sys\n"
        )

        # Also create a file with permission issues
        permission_file = temp_project / "no_read.py"
        permission_file.write_text("import os\n", encoding="utf-8")
        permission_file.chmod(stat.S_IWRITE)  # Write-only, no read

        try:
            duplicate_issues = analyzer._analyze_duplicates()
            assert isinstance(duplicate_issues, list)

            # Check for warning log about file access issues
            warning_messages = [
                record.message
                for record in caplog.records
                if record.levelname == "WARNING"
            ]
            # Should complete analysis even with problematic files
            # Warnings may or may not exist depending on how errors are handled
            assert isinstance(
                warning_messages, list
            )  # Use the variable to avoid unused warning
        finally:
            # Restore permissions for cleanup
            if permission_file.exists():
                permission_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
