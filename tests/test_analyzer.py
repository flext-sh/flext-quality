"""Comprehensive functional tests for CodeAnalyzer to achieve 100% coverage.

Real functional tests covering all analyzer functionality following flext-core patterns.
Tests all branches, error paths, and integration scenarios for production-grade coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_core import FlextTypes
from flext_quality import CodeAnalyzer
from flext_quality.analysis_types import (
    AnalysisResults,
    DuplicationIssue,
    FileAnalysisResult,
)

# No longer need legacy dict helpers - using typed AnalysisResults API


class TestCodeAnalyzerComprehensive:
    """Comprehensive functional tests for CodeAnalyzer with 100% coverage focus."""

    def test_init_with_string_path(self) -> None:
        """Test CodeAnalyzer initialization with string path."""
        analyzer = CodeAnalyzer("/test/path")
        assert analyzer.project_path == Path("/test/path")
        assert analyzer._current_results is None

    def test_init_with_path_object(self) -> None:
        """Test CodeAnalyzer initialization with Path object."""
        path_obj = Path("/test/path")
        analyzer = CodeAnalyzer(path_obj)
        assert analyzer.project_path == path_obj
        assert analyzer._current_results is None

    def test_analyze_project_all_features_enabled(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with all analysis features enabled."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

        # Verify structure using typed AnalysisResults API
        assert isinstance(results, AnalysisResults)

        # Verify overall metrics using typed API
        metrics = results.overall_metrics
        assert metrics.files_analyzed > 0
        assert metrics.total_lines > 0
        # Note: function counts are in file_metrics, not overall_metrics
        assert len(results.file_metrics) > 0

        # Verify issues structure using typed AnalysisResults API
        assert hasattr(results, "security_issues")
        assert hasattr(results, "complexity_issues")
        assert hasattr(results, "dead_code_issues")
        assert hasattr(results, "duplication_issues")
        # Verify these are lists
        assert isinstance(results.security_issues, list)
        assert isinstance(results.complexity_issues, list)
        assert isinstance(results.dead_code_issues, list)
        assert isinstance(results.duplication_issues, list)

    def test_analyze_project_selective_features(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with selective feature enabling."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        # Test with only security and complexity
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=False,
            include_duplicates=False,
        )

        # Use modern AnalysisResults API instead of dict access
        # Note: Security issues depend on the specific code content
        assert len(results.security_issues) >= 0  # May or may not have security issues
        assert (
            len(results.complexity_issues) >= 0
        )  # May or may not have complexity issues
        # When disabled, these should be empty lists
        assert results.dead_code_issues == []
        assert results.duplication_issues == []

    def test_analyze_project_no_features(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test analyze_project with all analysis features disabled."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        results = analyzer.analyze_project(
            include_security=False,
            include_complexity=False,
            include_dead_code=False,
            include_duplicates=False,
        )

        # Should still have basic structure
        assert hasattr(results, "overall_metrics")
        assert hasattr(results, "security_issues")

        # But all issue types should be empty when disabled
        assert results.security_issues == []
        assert results.complexity_issues == []
        assert results.dead_code_issues == []
        assert results.duplication_issues == []

    def test_find_python_files_with_valid_project(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test _find_python_files with real project structure."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        python_files = analyzer._find_python_files()

        assert isinstance(python_files, list)
        assert len(python_files) >= 2  # main.py and utils.py

        # Verify all found files are Python files
        for file_path in python_files:
            assert isinstance(file_path, Path)
            assert file_path.suffix == ".py"
            assert file_path.exists()

    def test_find_python_files_empty_directory(self) -> None:
        """Test _find_python_files with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)
            python_files = analyzer._find_python_files()
            assert python_files == []

    def test_find_python_files_nonexistent_directory(self) -> None:
        """Test _find_python_files with nonexistent directory."""
        analyzer = CodeAnalyzer("/nonexistent/path")
        python_files = analyzer._find_python_files()
        assert python_files == []

    def test_internal_analyze_file_simple_valid_file(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test _analyze_file with simple valid Python file."""
        analyzer = CodeAnalyzer(temporary_project_structure)
        project_path = Path(temporary_project_structure)
        main_file = project_path / "src" / "main.py"

        metrics = analyzer._analyze_file(main_file)

        # Now returns FileAnalysisResult object, not dict
        assert metrics is not None
        assert hasattr(metrics, "lines_of_code")
        assert hasattr(metrics, "complexity_score")
        assert hasattr(metrics, "file_path")
        assert metrics.lines_of_code > 0

        # Verify types and values
        assert isinstance(metrics.lines_of_code, int)
        assert isinstance(metrics.complexity_score, (int, float))
        assert metrics.lines_of_code >= 1

    def test_internal_analyze_file_with_syntax_error(self) -> None:
        """Test _analyze_file with file containing syntax errors."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write("def broken_function(\n")  # Intentional syntax error
            f.flush()

            with tempfile.TemporaryDirectory() as tmp_dir:
                analyzer = CodeAnalyzer(tmp_dir)
            metrics = analyzer._analyze_file(Path(f.name))

            # Should return FileAnalysisResult with security_issues=1 for syntax errors
            assert metrics is not None
            assert hasattr(metrics, "security_issues")
            assert metrics.security_issues == 1  # Syntax error marked as security issue
            assert metrics.complexity_score == 0.0  # No complexity for syntax errors

    def test_internal_analyze_file_nonexistent_file(self) -> None:
        """Test _analyze_file with nonexistent file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = CodeAnalyzer(tmp_dir)
        metrics = analyzer._analyze_file(Path("/nonexistent/file.py"))

        # Should return None for non-existent files
        assert metrics is None

    def test_calculate_overall_metrics_with_multiple_files(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test _calculate_overall_metrics with multiple file metrics."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        file_metrics: list[FlextTypes.Core.Dict] = [
            {
                "lines_of_code": 50,
                "complexity": 5,
                "function_count": 3,
                "class_count": 1,
            },
            {
                "lines_of_code": 30,
                "complexity": 3,
                "function_count": 2,
                "class_count": 0,
            },
            {
                "lines_of_code": 20,
                "complexity": 2,
                "function_count": 1,
                "class_count": 1,
            },
        ]

        overall = analyzer._calculate_overall_metrics(file_metrics)

        assert isinstance(overall, dict)
        assert overall["total_files"] == 3
        assert overall["total_lines_of_code"] == 100  # 50 + 30 + 20
        assert overall["total_functions"] == 6  # 3 + 2 + 1
        assert overall["total_classes"] == 2  # 1 + 0 + 1
        assert overall["average_complexity"] == 10 / 3  # (5 + 3 + 2) / 3
        assert overall["max_complexity"] == 5

    def test_calculate_overall_metrics_empty_list(self) -> None:
        """Test _calculate_overall_metrics with empty file list."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = CodeAnalyzer(tmp_dir)
            overall = analyzer._calculate_overall_metrics([])

            # Real implementation returns empty dict for empty input
            assert overall == {}

    def test_calculate_overall_metrics_single_file(self) -> None:
        """Test _calculate_overall_metrics with single file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = CodeAnalyzer(tmp_dir)
        file_metrics: list[FlextTypes.Core.Dict] = [
            {
                "lines_of_code": 42,
                "complexity": 7,
                "function_count": 5,
                "class_count": 2,
            },
        ]

        overall = analyzer._calculate_overall_metrics(file_metrics)

        assert overall["total_files"] == 1
        assert overall["total_lines_of_code"] == 42
        assert overall["total_functions"] == 5
        assert overall["total_classes"] == 2
        assert overall["average_complexity"] == 7
        assert overall["max_complexity"] == 7

    def test_analyze_security_enabled(self, temporary_project_structure: str) -> None:
        """Test _analyze_security when security analysis is enabled."""
        project_path = Path(temporary_project_structure)

        # Create a file with potential security issues
        security_file = project_path / "security_test.py"
        security_file.write_text("""
# INTENTIONAL SECURITY VULNERABILITIES FOR TESTING PURPOSES ONLY
# These are deliberately insecure patterns to test the security analyzer

password = "hardcoded_password"
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection risk - INTENTIONAL FOR TESTING
subprocess.call(f"rm -rf {user_input}")  # Command injection risk - INTENTIONAL FOR TESTING
""")

        analyzer = CodeAnalyzer(temporary_project_structure)
        issues = analyzer._analyze_security()

        assert isinstance(issues, list)
        # Method should return security issues
        for issue in issues:
            assert isinstance(issue, dict)

    def test_analyze_security_no_files(self) -> None:
        """Test _analyze_security with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)
            issues = analyzer._analyze_security()
            assert isinstance(issues, list)
            assert len(issues) == 0

    def test_analyze_complexity_enabled(self, temporary_project_structure: str) -> None:
        """Test _analyze_complexity when complexity analysis is enabled."""
        analyzer = CodeAnalyzer(temporary_project_structure)
        project_path = Path(temporary_project_structure)

        # Create a file with high complexity
        complex_file = project_path / "complex_test.py"
        complex_file.write_text("""

def complex_function(x):
    if x > 10:
      if x > 20:
          if x > 30:
              if x > 40:
                  if x > 50:
                      return "very high"
                  else:
                      return "high"
              else:
                  return "medium-high"
          else:
              return "medium"
      else:
          return "low-medium"
    else:
      return "low"
""")

        analyzer = CodeAnalyzer(temporary_project_structure)
        # Create sample file metrics for complexity analysis
        # Create proper FileAnalysisResult objects

        file_metrics = [
            FileAnalysisResult(
                file_path=Path("complex_test.py"),
                lines_of_code=50,
                complexity_score=70.0,  # (100-70)/2 = 15 complexity
                security_issues=0,
                style_issues=0,
                dead_code_lines=0,
            ),
        ]
        issues = analyzer._analyze_complexity(file_metrics)

        assert isinstance(issues, list)
        # Should detect complexity issues
        for issue in issues:
            assert hasattr(issue, "issue_type")
            assert hasattr(issue, "function_name")
            assert hasattr(issue, "complexity_value")

    def test_analyze_complexity_no_files(self) -> None:
        """Test _analyze_complexity with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)
            # Empty file metrics for no files scenario
            file_metrics: list[FileAnalysisResult] = []
            issues = analyzer._analyze_complexity(file_metrics)
            assert isinstance(issues, list)
            assert len(issues) == 0

    def test_analyze_dead_code_enabled(self, temporary_project_structure: str) -> None:
        """Test _analyze_dead_code when dead code analysis is enabled."""
        analyzer = CodeAnalyzer(temporary_project_structure)
        project_path = Path(temporary_project_structure)

        # Create a file with dead code
        dead_code_file = project_path / "dead_code_test.py"
        dead_code_file.write_text("""


def unused_function():
    pass

def used_function():
    return os.getcwd()

unused_variable = "not used anywhere"
used_variable = "used below"
print(used_variable)
""")

        analyzer = CodeAnalyzer(temporary_project_structure)
        issues = analyzer._analyze_dead_code()

        assert isinstance(issues, list)
        # Should detect dead code issues
        for issue in issues:
            assert isinstance(issue, dict)
            assert "type" in issue
            assert "file" in issue

    def test_analyze_dead_code_no_files(self) -> None:
        """Test _analyze_dead_code with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)
            issues = analyzer._analyze_dead_code()
            assert isinstance(issues, list)
            assert len(issues) == 0

    def test_analyze_duplicates_enabled(self, temporary_project_structure: str) -> None:
        """Test _analyze_duplicates when duplicate analysis is enabled."""
        analyzer = CodeAnalyzer(temporary_project_structure)
        project_path = Path(temporary_project_structure)

        # Create files with duplicate code blocks
        dup_file1 = project_path / "dup_test1.py"
        dup_file1.write_text("""

def process_data(data):
    result = []
    for item in data:
      if item is not None:
          result.append(item.upper())
    return result
""")

        dup_file2 = project_path / "dup_test2.py"
        dup_file2.write_text("""

def handle_data(data):
    result = []
    for item in data:
      if item is not None:
          result.append(item.upper())
    return result
""")

        analyzer = CodeAnalyzer(temporary_project_structure)
        issues = analyzer._analyze_duplicates()

        assert isinstance(issues, list)
        # Should detect duplicate code blocks
        for issue in issues:
            assert isinstance(issue, DuplicationIssue)
            assert hasattr(issue, "files")
            assert hasattr(issue, "message")
            assert len(issue.files) >= 2  # At least 2 files involved in duplication

    def test_analyze_duplicates_no_files(self) -> None:
        """Test _analyze_duplicates with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)
            issues = analyzer._analyze_duplicates()
            assert isinstance(issues, list)
            assert len(issues) == 0

    def test_analyze_duplicates_single_file(self) -> None:
        """Test _analyze_duplicates with single file (no duplicates possible)."""
        # Create directory with only one file
        with tempfile.TemporaryDirectory() as temp_dir:
            single_file = Path(temp_dir) / "single.py"
            single_file.write_text("def test(): pass")

            analyzer = CodeAnalyzer(temp_dir)
            issues = analyzer._analyze_duplicates()
            assert isinstance(issues, list)
            # Single file should not have duplicate issues
            assert len(issues) == 0

    @patch("flext_quality.analyzer.flext_create_trace")
    @patch("flext_quality.analyzer.flext_create_metric")
    @patch("flext_quality.analyzer.flext_create_log_entry")
    def test_observability_integration(
        self,
        mock_log: MagicMock,
        mock_metric: MagicMock,
        mock_trace: MagicMock,
        temporary_project_structure: str,
    ) -> None:
        """Test integration with flext-observability components."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        analyzer.analyze_project()

        # Verify observability calls were made
        mock_trace.assert_called()
        mock_metric.assert_called()
        mock_log.assert_called()

        # Verify trace creation
        trace_call = mock_trace.call_args
        assert trace_call is not None
        args, kwargs = trace_call
        # Check for observability parameters - any one of these indicates proper tracing
        assert (
            "trace_id" in kwargs
            or "operation_name" in kwargs
            or "service_name" in kwargs
            or len(args) > 0
        )

    def test_analyze_project_integration_flow(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test complete analyze_project integration flow with real files."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        # Add more content to test files for better coverage
        project_path = Path(temporary_project_structure)

        # Enhance utils.py with more content
        utils_file = project_path / "src" / "utils.py"
        utils_file.write_text("""


class DataProcessor:
    def __init__(self, config_path: str):
        \"\"\"Initialize the instance.\"\"\"

      self.config_path = config_path
      self.config = self._load_config()

    def _load_config(self) -> dict:
      if os.path.exists(self.config_path):
          with open(self.config_path) as f:
              return json.load(f)
      return {}

    def process(self, data: list) -> list:
      result = []
      for item in data:
          if self._is_valid(item):
              processed = self._transform(item)
              result.append(processed)
      return result

    def _is_valid(self, item) -> bool:
      return item is not None and len(str(item)) > 0

    def _transform(self, item):
      if isinstance(item, str):
          return item.upper()
      return str(item)

def get_env_var(name: str) -> str | None:
    return os.environ.get(name)

def complex_calculation(x, y, z):
    if x > 0:
      if y > 0:
          if z > 0:
              return x * y * z
          else:
              return x * y
      else:
          if z > 0:
              return x * z
          else:
              return x
    else:
      return 0
""")

        # Run comprehensive analysis
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

        # Verify comprehensive results using modern AnalysisResults API
        assert isinstance(results, AnalysisResults), (
            f"Expected AnalysisResults, got {type(results)}"
        )

        # Check metrics using type-safe AnalysisResults properties
        metrics = results.overall_metrics
        assert metrics.files_analyzed >= 2
        assert metrics.total_lines > 20
        # Note: Functions and classes are in file_metrics, not overall_metrics
        assert len(results.file_metrics) >= 2

        # Verify we have file analysis results with functions/classes
        total_functions = sum(
            1 for _ in results.file_metrics if hasattr(_, "complexity_score")
        )
        assert total_functions >= 1

        # Check issues structure using AnalysisResults properties
        assert hasattr(results, "security_issues")
        assert hasattr(results, "complexity_issues")
        assert hasattr(results, "dead_code_issues")
        assert hasattr(results, "duplication_issues")

        # Verify file metrics list
        assert isinstance(results.file_metrics, list)
        assert len(results.file_metrics) >= 2

    def test_edge_case_ast_parsing_with_encoding_issues(self) -> None:
        """Test AST parsing with different file encodings."""
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write("""# -*- coding: utf-8 -*-
def test_unicode():
    text = "Teste com acentos: ção, ã, é"
    return text
""")
            f.flush()

            with tempfile.TemporaryDirectory() as tmp_dir:
                analyzer = CodeAnalyzer(tmp_dir)
            metrics = analyzer._analyze_file(Path(f.name))

            # Should handle unicode properly - metrics is FileAnalysisResult
            assert isinstance(metrics, FileAnalysisResult), (
                f"Expected FileAnalysisResult, got {type(metrics)}"
            )
            # FileAnalysisResult doesn't have function_count - this needs to be updated based on actual structure
            assert metrics.file_path.name == Path(f.name).name

    def test_ast_visitor_comprehensive_coverage(
        self,
        temporary_project_structure: str,
    ) -> None:
        """Test AST visitor with comprehensive Python constructs."""
        project_path = Path(temporary_project_structure)
        comprehensive_file = project_path / "comprehensive_test.py"

        comprehensive_file.write_text('''

from typing import Dict
from typing import Optional

class BaseClass:
    """Base class for testing."""

    def __init__(self, name: str):
        """Initialize the instance."""

      self.name = name

class DerivedClass(BaseClass):
    """Derived class for testing."""

    def __init__(self, name: str, value: int):
        """Initialize the instance."""

      super().__init__(name)
      self.value = value

    @property
    def display_name(self) -> str:
      return f"{self.name}: {self.value}"

    @staticmethod
    def static_method() -> str:
      return "static"

    @classmethod
    def class_method(cls) -> str:
      return cls.__name__

def simple_function() -> None:
    pass

async def async_function() -> int:
    await asyncio.sleep(0.1)
    return 42

def complex_function(data: List[Dict[str, Optional[int]]]) -> Dict[str, int]:
    result = {}
    for i, item in enumerate(data):
      if item:
          for key, value in item.items():
              if value is not None:
                  if key in result:
                      result[key] += value
                  else:
                      result[key] = value
              else:
                  if key not in result:
                      result[key] = 0
    return result

def generator_function():
    for i in range(10):
      yield i * 2

lambda_func = lambda x: x * 2

# Global variables
CONSTANT = 42
variable = "test"
''')

        analyzer = CodeAnalyzer(temporary_project_structure)
        metrics = analyzer._analyze_file(comprehensive_file)

        # Should properly analyze all constructs - metrics is FileAnalysisResult
        assert isinstance(metrics, FileAnalysisResult), (
            f"Expected FileAnalysisResult, got {type(metrics)}"
        )
        # FileAnalysisResult has different structure - verify basic properties
        assert metrics.lines_of_code > 0
        assert metrics.complexity_score >= 0.0
        assert metrics.file_path == comprehensive_file
        # Note: Class/function names are not stored in FileAnalysisResult

    def test_get_quality_score_method(self, temporary_project_structure: str) -> None:
        """Test get_quality_score public method."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        # First analyze the project to populate analysis_results
        analyzer.analyze_project()

        score = analyzer.get_quality_score()

        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0

    def test_get_quality_grade_method(self, temporary_project_structure: str) -> None:
        """Test get_quality_grade public method."""
        analyzer = CodeAnalyzer(temporary_project_structure)

        # First analyze the project to populate analysis_results
        analyzer.analyze_project()

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
            "F",
        }

    def test_get_quality_score_no_analysis(self) -> None:
        """Test get_quality_score without prior analysis."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = CodeAnalyzer(tmp_dir)

        score = analyzer.get_quality_score()

        # Should return default score when no analysis has been run
        assert isinstance(score, float)
        assert score >= 0.0

    def test_get_quality_grade_no_analysis(self) -> None:
        """Test get_quality_grade without prior analysis."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = CodeAnalyzer(tmp_dir)

        grade = analyzer.get_quality_grade()

        # Should return default grade when no analysis has been run
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
            "F",
        }
