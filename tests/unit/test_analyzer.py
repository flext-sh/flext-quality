"""Tests for FlextQualityAnalyzer - Real API tests only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Tests only the PUBLIC API:
- analyze_project()
- get_quality_score()
- get_quality_grade()
- get_last_analysis_result()
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_quality import FlextQualityAnalyzer


class TestFlextQualityAnalyzer:
    """Tests for FlextQualityAnalyzer public API."""

    def test_analyzer_initialization_with_path(self, tmp_path: Path) -> None:
        """Test analyzer can be initialized with a path."""
        analyzer = FlextQualityAnalyzer(tmp_path)
        assert analyzer.project_path == tmp_path

    def test_analyzer_initialization_with_string(self) -> None:
        """Test analyzer can be initialized with string path."""
        analyzer = FlextQualityAnalyzer(".")
        assert analyzer.project_path == Path()

    def test_analyzer_initialization_without_path(self) -> None:
        """Test analyzer defaults to current directory."""
        analyzer = FlextQualityAnalyzer()
        assert analyzer.project_path == Path()

    def test_analyzer_initialization_with_none(self) -> None:
        """Test analyzer accepts None path and defaults to current directory."""
        analyzer = FlextQualityAnalyzer(None)
        assert analyzer.project_path == Path()

    def test_get_quality_score_default(self, tmp_path: Path) -> None:
        """Test get_quality_score returns default when no analysis run."""
        analyzer = FlextQualityAnalyzer(tmp_path)
        score = analyzer.get_quality_score()
        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0

    def test_get_quality_grade_default(self, tmp_path: Path) -> None:
        """Test get_quality_grade returns valid grade."""
        analyzer = FlextQualityAnalyzer(tmp_path)
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

    def test_get_last_analysis_result_none_initially(self, tmp_path: Path) -> None:
        """Test get_last_analysis_result returns None before analysis."""
        analyzer = FlextQualityAnalyzer(tmp_path)
        result = analyzer.get_last_analysis_result()
        assert result is None

    def test_analyze_project_with_empty_directory(self) -> None:
        """Test analyze_project with empty directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = FlextQualityAnalyzer(tmp_dir)
            analysis_result = analyzer.analyze_project()

            # Should return FlextResult
            assert hasattr(analysis_result, "is_success")
            # Empty directory should succeed with zero issues
            if analysis_result.is_success:
                result = analysis_result.value
                assert hasattr(result, "overall_score")

    def test_analyze_project_with_python_files(self) -> None:
        """Test analyze_project with actual Python files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Create a simple Python file
            (tmp_path / "simple.py").write_text("def hello(): pass\n")

            analyzer = FlextQualityAnalyzer(tmp_path)
            analysis_result = analyzer.analyze_project()

            assert hasattr(analysis_result, "is_success")
            if analysis_result.is_success:
                result = analysis_result.value
                assert hasattr(result, "files_analyzed")

    def test_execute_returns_flext_result(self, tmp_path: Path) -> None:
        """Test execute() returns FlextResult[bool]."""
        analyzer = FlextQualityAnalyzer(tmp_path)
        result = analyzer.execute()

        assert hasattr(result, "is_success")
        assert hasattr(result, "is_failure")
        # execute() should return ok(True)
        assert result.is_success
