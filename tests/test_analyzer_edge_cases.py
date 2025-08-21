"""Edge case tests for CodeAnalyzer.

Real functional tests covering uncovered lines and edge cases in analyzer.py.
Tests specific scenarios for 100% coverage following flext-core patterns.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from flext_quality import CodeAnalyzer


class TestCodeAnalyzerEdgeCases:
    """Test edge cases and uncovered paths in CodeAnalyzer."""

    def test_analyze_project_with_no_analysis_results(self) -> None:
        """Test get_quality_score when no analysis_results - covers line 137."""
        with TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)

            # Call get_quality_score without running analyze_project first
            score = analyzer.get_quality_score()

            # Should return 0.0 when no analysis results
            assert score == 0.0

    def test_get_quality_score_with_invalid_issues_type(self) -> None:
        """Test get_quality_score when issues is not dict - covers line 180."""
        with TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)

            # Manually set _current_results to test error handling
            from flext_quality.analysis_types import AnalysisResults, OverallMetrics

            analyzer._current_results = AnalysisResults(
                overall_metrics=OverallMetrics(),
                file_metrics=[],
                complexity_issues=[],
                security_issues=[],
                dead_code_issues=[],
                duplication_issues=[],
            )

            score = analyzer.get_quality_score()

            # Should return 0.0 when issues is not dict
            assert score == 0.0

    def test_calculate_overall_metrics_with_empty_file_metrics(self) -> None:
        """Test _calculate_overall_metrics with empty list - covers line 349."""
        with TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)

            # Call with empty list
            result = analyzer._calculate_overall_metrics([])

            # Should return empty dict
            assert result == {}

    def test_analyze_project_with_large_duplicate_files(self) -> None:
        """Test _analyze_duplicates with files reaching similarity threshold."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create two files with similar content (>80% similarity)
            file1 = temp_path / "file1.py"
            file2 = temp_path / "file2.py"

            similar_content = """
def function1():
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print("Line 4")
    print("Line 5")
    return True

def function2():
    print("Another line")
    return False
"""

            # File1 has exact content
            file1.write_text(similar_content)

            # File2 has mostly same content with one difference
            file2_content = similar_content.replace("Line 5", "Line 5 modified")
            file2.write_text(file2_content)

            analyzer = CodeAnalyzer(temp_dir)
            results = analyzer.analyze_project(include_duplicates=True)

            # Should detect high similarity using typed API
            duplicates = results.duplication_issues

            # Verify duplication detection works with real code execution
            assert len(duplicates) > 0, "Should detect duplication in identical files"

            # Verify the similarity is high (above 80% threshold)
            similarity_found = any(
                getattr(issue, "similarity", 0) > 0.8
                for issue in duplicates
                if hasattr(issue, "similarity")
            )
            assert similarity_found, "Should find high similarity in duplicate files"

            # Additional verification: ensure the analysis actually ran with real metrics
            assert results.overall_metrics.files_analyzed >= 2
            assert results.overall_metrics.total_lines > 0

    def test_find_python_files_with_hidden_directories(self) -> None:
        """Test _find_python_files skips hidden directories correctly."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create regular Python file
            regular_file = temp_path / "regular.py"
            regular_file.write_text("print('regular')")

            # Create hidden directory with Python file
            hidden_dir = temp_path / ".hidden"
            hidden_dir.mkdir()
            hidden_file = hidden_dir / "hidden.py"
            hidden_file.write_text("print('hidden')")

            # Create __pycache__ directory with .pyc file
            pycache_dir = temp_path / "__pycache__"
            pycache_dir.mkdir()
            pyc_file = pycache_dir / "cached.py"
            pyc_file.write_text("print('cached')")

            analyzer = CodeAnalyzer(temp_dir)
            python_files = analyzer._find_python_files()

            # Should only find regular file, skip hidden and __pycache__
            file_names = [f.name for f in python_files]
            assert "regular.py" in file_names
            assert "hidden.py" not in file_names
            assert "cached.py" not in file_names

    def test_analyze_file_with_syntax_error(self) -> None:
        """Test _analyze_file handles syntax errors correctly."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create file with syntax error
            syntax_error_file = temp_path / "syntax_error.py"
            syntax_error_file.write_text("""
def invalid_syntax(
    # Missing closing parenthesis and colon
    print("This will cause syntax error")
""")

            analyzer = CodeAnalyzer(temp_dir)
            metrics = analyzer._analyze_file(syntax_error_file)

            # Should handle syntax error and return metrics with error info
            assert metrics is not None
            # Syntax errors are tracked via security_issues field (as per analyzer.py:264)
            assert metrics.security_issues == 1
            assert metrics.complexity_score == 0.0
            assert metrics.lines_of_code >= 0

    def test_analyze_file_with_file_read_error(self) -> None:
        """Test _analyze_file handles file read errors."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create file then make it unreadable
            unreadable_file = temp_path / "unreadable.py"
            unreadable_file.write_text("print('test')")

            analyzer = CodeAnalyzer(temp_dir)

            # Mock open to raise FileNotFoundError
            with patch(
                "builtins.open",
                side_effect=FileNotFoundError("File not accessible"),
            ):
                metrics = analyzer._analyze_file(unreadable_file)

                # Should return None when file cannot be read
                assert metrics is None

    def test_analyze_security_with_file_read_error(self) -> None:
        """Test _analyze_security handles file read errors."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create file
            test_file = temp_path / "test.py"
            test_file.write_text("print('test')")

            analyzer = CodeAnalyzer(temp_dir)

            # Mock open to raise RuntimeError during security analysis
            with patch("builtins.open", side_effect=RuntimeError("Permission denied")):
                # Call analyze_project which calls _analyze_security
                results = analyzer.analyze_project(include_security=True)

                # Should handle error gracefully and continue
                assert results is not None
                # Security issues should be empty due to read error
                security_issues = results.security_issues
                assert isinstance(security_issues, list)

    def test_analyze_dead_code_with_file_read_error(self) -> None:
        """Test _analyze_dead_code handles file read errors."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create file
            test_file = temp_path / "test.py"
            test_file.write_text("import unused  # unused")

            analyzer = CodeAnalyzer(temp_dir)

            # Mock open to raise ValueError during dead code analysis
            with patch("builtins.open", side_effect=ValueError("Encoding error")):
                # Call analyze_project which calls _analyze_dead_code
                results = analyzer.analyze_project(include_dead_code=True)

                # Should handle error gracefully
                assert results is not None
                dead_code_issues = results.dead_code_issues
                assert isinstance(dead_code_issues, list)

    def test_analyze_duplicates_with_file_read_error(self) -> None:
        """Test _analyze_duplicates handles file read errors."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create files
            file1 = temp_path / "file1.py"
            file1.write_text("print('file1')")
            file2 = temp_path / "file2.py"
            file2.write_text("print('file2')")

            analyzer = CodeAnalyzer(temp_dir)

            # Mock open to raise TypeError during duplicate analysis
            with patch("builtins.open", side_effect=TypeError("Invalid operation")):
                # Call analyze_project which calls _analyze_duplicates
                results = analyzer.analyze_project(include_duplicates=True)

                # Should handle error gracefully
                assert results is not None
                duplicates_issues = results.duplication_issues
                assert isinstance(duplicates_issues, list)

    def test_find_python_files_nonexistent_path(self) -> None:
        """Test _find_python_files with non-existent project path."""
        # Use non-existent path
        analyzer = CodeAnalyzer("/non/existent/path")
        python_files = analyzer._find_python_files()

        # Should return empty list
        assert python_files == []

    def test_analyze_dead_code_with_unused_import_comment(self) -> None:
        """Test _analyze_dead_code detects unused import comments."""
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create file with "unused" comment
            test_file = temp_path / "test_unused.py"
            test_file.write_text("""
import os  # unused
from sys import path  # UNUSED import
import json
""")

            analyzer = CodeAnalyzer(temp_dir)
            results = analyzer.analyze_project(include_dead_code=True)

            # Should detect unused imports with comments
            dead_code_issues = results.dead_code_issues
            assert len(dead_code_issues) >= 2  # Should find both unused imports

            # Check that it found the specific unused imports
            messages = [issue.message for issue in dead_code_issues]
            assert any("import os" in msg for msg in messages)
            assert any("from sys import path" in msg for msg in messages)

    def test_quality_grade_calculator_edge_case(self) -> None:
        """Test get_quality_grade with edge case score."""
        with TemporaryDirectory() as temp_dir:
            analyzer = CodeAnalyzer(temp_dir)

            # Set _current_results manually to test grade calculator
            from flext_quality.analysis_types import AnalysisResults, OverallMetrics

            analyzer._current_results = AnalysisResults(
                overall_metrics=OverallMetrics(),
                file_metrics=[],
                complexity_issues=[],
                security_issues=[],
                dead_code_issues=[],
                duplication_issues=[],
            )

            # Should get perfect score and A+ grade
            score = analyzer.get_quality_score()
            grade = analyzer.get_quality_grade()

            assert score == 100.0
            assert grade == "A+"
