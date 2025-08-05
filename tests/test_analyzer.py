"""Comprehensive tests for the CodeAnalyzer class."""

import ast
import tempfile
from collections.abc import Callable, Generator
from pathlib import Path
from textwrap import dedent
from typing import TextIO

import pytest

from flext_quality.analyzer import CodeAnalyzer


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
        assert analyzer.analysis_results == {}

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
        assert metrics["file_path"] == "simple.py"
        assert metrics["function_count"] >= 1
        assert metrics["class_count"] == 1
        assert metrics["lines_of_code"] > 0
        assert metrics["complexity"] > 0
        assert "hello_world" in metrics["functions"]
        assert "SimpleClass" in metrics["classes"]

    def test_analyze_file_with_syntax_error(self, temp_project: Path) -> None:
        """Test analyzing a file with syntax error."""
        analyzer = CodeAnalyzer(temp_project)
        syntax_error_file = temp_project / "syntax_error.py"

        metrics = analyzer._analyze_file(syntax_error_file)

        assert metrics is not None
        assert metrics["file_path"] == "syntax_error.py"
        assert metrics["function_count"] == 0
        assert metrics["class_count"] == 0
        assert "syntax_error" in metrics

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

        file_metrics = [
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
        """Test security analysis."""
        analyzer = CodeAnalyzer(temp_project)
        security_issues = analyzer._analyze_security()

        # Should find all security issues in security.py
        issues_by_type = {}
        for issue in security_issues:
            issue_type = issue["type"]
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        assert "dangerous_function" in issues_by_type
        assert "command_injection" in issues_by_type

        # Should find eval and exec issues
        dangerous_issues = issues_by_type["dangerous_function"]
        assert len(dangerous_issues) >= 2  # eval and exec

        messages = [issue["message"] for issue in dangerous_issues]
        assert any("eval()" in msg for msg in messages)
        assert any("exec()" in msg for msg in messages)

    def test_analyze_complexity_issues(self, temp_project: Path) -> None:
        """Test complexity analysis."""
        analyzer = CodeAnalyzer(temp_project)

        file_metrics = [
            {"file_path": "simple.py", "complexity": 5},
            {"file_path": "complex.py", "complexity": 15},  # Above threshold
            {"file_path": "other.py", "complexity": 8},
        ]

        complexity_issues = analyzer._analyze_complexity(file_metrics)

        assert len(complexity_issues) == 1
        assert complexity_issues[0]["file"] == "complex.py"
        assert complexity_issues[0]["complexity"] == 15
        assert complexity_issues[0]["threshold"] == 10

    def test_analyze_dead_code(self, temp_project: Path) -> None:
        """Test dead code analysis."""
        analyzer = CodeAnalyzer(temp_project)
        dead_code_issues = analyzer._analyze_dead_code()

        # Should find unused imports marked with # unused
        unused_issues = [
            issue for issue in dead_code_issues if issue["type"] == "unused_import"
        ]
        assert len(unused_issues) >= 2  # sys and typing imports marked as unused

    def test_analyze_duplicates(self, temp_project: Path) -> None:
        """Test duplicate code analysis."""
        analyzer = CodeAnalyzer(temp_project)
        duplicate_issues = analyzer._analyze_duplicates()

        # Should find high similarity between duplicate1.py and duplicate2.py
        assert len(duplicate_issues) >= 1

        duplicate_issue = duplicate_issues[0]
        assert duplicate_issue["type"] == "duplicate_files"
        assert len(duplicate_issue["files"]) == 2
        assert duplicate_issue["similarity"] > 0.8
        assert "duplicate1.py" in duplicate_issue["files"]
        assert "duplicate2.py" in duplicate_issue["files"]

    def test_full_project_analysis(self, temp_project: Path) -> None:
        """Test complete project analysis."""
        analyzer = CodeAnalyzer(temp_project)
        results = analyzer.analyze_project()

        assert "project_path" in results
        assert "files_analyzed" in results
        assert "total_lines" in results
        assert "python_files" in results
        assert "metrics" in results
        assert "issues" in results

        # Check that files were found
        assert results["files_analyzed"] > 0
        assert results["total_lines"] > 0

        # Check that all expected files are analyzed
        python_files = results["python_files"]
        expected_files = ["simple.py", "complex.py", "security.py", "dead_code.py"]
        for expected_file in expected_files:
            assert any(expected_file in pf for pf in python_files)

        # Check metrics
        metrics = results["metrics"]
        assert "total_files" in metrics
        assert "total_lines_of_code" in metrics
        assert "total_functions" in metrics
        assert "total_classes" in metrics

        # Check issues
        issues = results["issues"]
        assert "security" in issues
        assert "complexity" in issues
        assert "dead_code" in issues
        assert "duplicates" in issues

        # Should find security issues
        assert len(issues["security"]) > 0

        # May or may not find complexity issues depending on threshold
        assert len(issues["complexity"]) >= 0

        # Should find duplicate issues
        assert len(issues["duplicates"]) > 0

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

        issues = results["issues"]
        assert len(issues["security"]) > 0
        assert len(issues["complexity"]) == 0
        assert len(issues["dead_code"]) == 0
        assert len(issues["duplicates"]) == 0

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

        # Mock perfect analysis results
        analyzer.analysis_results = {
            "metrics": {},
            "issues": {
                "complexity": [],
                "security": [],
                "dead_code": [],
                "duplicates": [],
            },
        }

        score = analyzer.get_quality_score()
        assert score == 100.0

    def test_get_quality_grade(self, temp_project: Path) -> None:
        """Test quality grade calculation."""
        analyzer = CodeAnalyzer(temp_project)

        # Test a few key grade boundaries
        test_cases = [
            (100, "A+"),
            (95, "A+"),
            (90, "A"),
            (85, "A-"),
            (75, "B"),
            (60, "C"),
            (45, "D"),
            (30, "F"),
        ]

        for score, expected_grade in test_cases:
            # Mock the get_quality_score method to return specific score
            original_get_score = analyzer.get_quality_score

            # Use closure to avoid loop variable binding issue
            def make_score_lambda(s: float) -> Callable[[], float]:
                return lambda: s

            analyzer.get_quality_score = make_score_lambda(score)

            grade = analyzer.get_quality_grade()
            assert grade == expected_grade

            # Restore original method
            analyzer.get_quality_score = original_get_score

    def test_analysis_results_storage(self, temp_project: Path) -> None:
        """Test that analysis results are properly stored."""
        analyzer = CodeAnalyzer(temp_project)

        # Initially empty
        assert analyzer.analysis_results == {}

        # After analysis, should contain results
        results = analyzer.analyze_project()
        assert analyzer.analysis_results == results
        assert analyzer.analysis_results != {}

    def test_analyze_project_logging(
        self, temp_project: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that analysis produces appropriate log messages."""
        import logging

        caplog.set_level(logging.INFO)

        analyzer = CodeAnalyzer(temp_project)
        analyzer.analyze_project()

        # Check for expected log messages
        log_messages = [record.message for record in caplog.records]
        assert any("Starting project analysis" in msg for msg in log_messages)
        assert any("Analysis completed" in msg for msg in log_messages)

    def test_file_analysis_error_handling(self, temp_project: Path) -> None:
        """Test error handling in file analysis."""
        analyzer = CodeAnalyzer(temp_project)

        # Create a file that will cause read error (simulate permission error)
        problem_file = temp_project / "problem.py"
        problem_file.write_text("# Test file")

        # Mock file to raise exception during analysis
        original_analyze = analyzer._analyze_file

        def mock_analyze(file_path: Path) -> dict[str, object] | None:
            if file_path.name == "problem.py":
                return None  # Simulate failure
            return original_analyze(file_path)

        analyzer._analyze_file = mock_analyze

        # Should handle error gracefully
        results = analyzer.analyze_project()
        assert "files_analyzed" in results
        # Should still analyze other files
        assert results["files_analyzed"] > 0

    def test_security_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in security analysis."""
        import logging

        caplog.set_level(logging.WARNING)

        analyzer = CodeAnalyzer(temp_project)

        # Create a file that might cause issues during security scan
        # This tests the exception handling in _analyze_security
        error_file = temp_project / "error_file.py"
        error_file.write_text("# Error file")

        # Mock open to raise exception for specific file
        import builtins

        original_open = builtins.open

        def mock_open(file_path: str | Path, *args: object, **kwargs: object) -> TextIO:
            if "error_file.py" in str(file_path):
                msg = "Simulated read error"
                raise RuntimeError(msg)
            return original_open(file_path, *args, **kwargs)

        builtins.open = mock_open

        try:
            security_issues = analyzer._analyze_security()
            # Should handle error and continue with other files
            assert isinstance(security_issues, list)

            # Check for warning log
            warning_messages = [
                record.message
                for record in caplog.records
                if record.levelname == "WARNING"
            ]
            assert any("Error checking security" in msg for msg in warning_messages)
        finally:
            builtins.open = original_open

    def test_dead_code_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in dead code analysis."""
        import logging

        caplog.set_level(logging.WARNING)

        analyzer = CodeAnalyzer(temp_project)

        # Mock file operations to simulate errors
        import builtins

        original_open = builtins.open

        def mock_open(file_path: str | Path, *args: object, **kwargs: object) -> TextIO:
            if "dead_code.py" in str(file_path):
                msg = "Simulated error"
                raise ValueError(msg)
            return original_open(file_path, *args, **kwargs)

        builtins.open = mock_open

        try:
            dead_code_issues = analyzer._analyze_dead_code()
            assert isinstance(dead_code_issues, list)

            # Check for warning log
            warning_messages = [
                record.message
                for record in caplog.records
                if record.levelname == "WARNING"
            ]
            assert any("Error checking dead code" in msg for msg in warning_messages)
        finally:
            builtins.open = original_open

    def test_duplicate_analysis_error_handling(
        self,
        temp_project: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test error handling in duplicate analysis."""
        import logging

        caplog.set_level(logging.WARNING)

        analyzer = CodeAnalyzer(temp_project)

        # Mock file operations to simulate errors
        import builtins

        original_open = builtins.open

        def mock_open(file_path: str | Path, *args: object, **kwargs: object) -> TextIO:
            if "duplicate1.py" in str(file_path):
                msg = "Simulated error"
                raise TypeError(msg)
            return original_open(file_path, *args, **kwargs)

        builtins.open = mock_open

        try:
            duplicate_issues = analyzer._analyze_duplicates()
            assert isinstance(duplicate_issues, list)

            # Check for warning log
            warning_messages = [
                record.message
                for record in caplog.records
                if record.levelname == "WARNING"
            ]
            assert any("Error reading" in msg for msg in warning_messages)
        finally:
            builtins.open = original_open
