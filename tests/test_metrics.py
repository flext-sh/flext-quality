"""Test quality metrics functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_core import FlextTypes
from pydantic import ValidationError

from flext_quality import QualityGradeCalculator, QualityMetrics
from flext_quality.analysis_types import (
    AnalysisResults,
    FileAnalysisResult,
    OverallMetrics,
)

# Import correct classes - now independent classes, not nested
FileMetrics = FileAnalysisResult  # Alias for backward compatibility


class TestQualityMetrics:
    """Test QualityMetrics class."""

    def test_metrics_creation_defaults(self) -> None:
        """Test quality metrics creation with defaults."""
        metrics = QualityMetrics.create_default()

        assert metrics.overall_score == 0.0
        assert metrics.quality_grade == "F"
        assert metrics.total_files == 0
        assert metrics.total_lines_of_code == 0
        assert metrics.total_functions == 0
        assert metrics.total_classes == 0

    def test_metrics_creation_with_values(self) -> None:
        """Test quality metrics creation with specific values."""
        metrics = QualityMetrics.create(
            overall_score=85.5,
            quality_grade="B+",
            total_files=10,
            total_lines_of_code=1000,
            total_functions=50,
            total_classes=15,
            average_complexity=8.2,
            max_complexity=15.0,
        )

        assert metrics.overall_score == 85.5
        assert metrics.quality_grade == "B+"
        assert metrics.total_files == 10
        assert metrics.total_lines_of_code == 1000
        assert metrics.total_functions == 50
        assert metrics.total_classes == 15
        assert metrics.average_complexity == 8.2
        assert metrics.max_complexity == 15.0

    def test_score_validation(self) -> None:
        """Test score validation bounds."""
        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(overall_score=-1.0)

        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(overall_score=101.0)

        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(complexity_score=-5.0)

        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(security_score=150.0)

    def test_count_validation(self) -> None:
        """Test count validation (non-negative)."""
        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(total_files=-1)

        with pytest.raises(ValidationError):
            QualityMetrics.create_for_validation_test(security_issues_count=-5)

    def test_from_analysis_results_empty(self) -> None:
        """Test creating metrics from empty analysis results using AnalysisResults."""
        results = AnalysisResults(
            overall_metrics=OverallMetrics(),
            file_metrics=[],
            complexity_issues=[],
            security_issues=[],
            dead_code_issues=[],
            duplication_issues=[],
        )

        metrics = QualityMetrics.from_analysis_results(results)

        assert metrics.total_files == 0
        assert metrics.total_lines_of_code == 0
        assert metrics.security_issues_count == 0
        assert metrics.overall_score > 0  # Should have some base score

    def test_from_analysis_results_with_metrics(self) -> None:
        """Test creating metrics from analysis results with data using AnalysisResults."""
        results = AnalysisResults(
            overall_metrics=OverallMetrics(
                files_analyzed=20,
                total_lines=2500,
                functions_count=100,
                classes_count=25,
                average_complexity=6.5,
                max_complexity=12.0,
            ),
            file_metrics=[
                FileMetrics(
                    file_path="test1.py", lines_of_code=1000, complexity_score=5.0
                ),
                FileMetrics(
                    file_path="test2.py", lines_of_code=1500, complexity_score=8.0
                ),
            ],
            complexity_issues=[{"type": "high_complexity"}],
            security_issues=[{"type": "hardcoded_secret"}, {"type": "sql_injection"}],
            dead_code_issues=[{"type": "unused_import"}],
            duplication_issues=[{"type": "duplicate_block"}],
        )

        metrics = QualityMetrics.from_analysis_results(results)

        assert metrics.total_files == 20
        assert metrics.total_lines_of_code == 2500
        assert metrics.total_functions == 100
        assert metrics.total_classes == 25
        assert metrics.average_complexity == 6.5
        assert metrics.max_complexity == 12.0

        # Issue counts
        assert metrics.security_issues_count == 2
        assert metrics.dead_code_items_count == 1
        assert metrics.duplicate_blocks_count == 1
        assert metrics.complexity_issues_count == 1

    def test_score_calculations(self) -> None:
        """Test score calculations in from_analysis_results using AnalysisResults."""
        results = AnalysisResults(
            overall_metrics=OverallMetrics(average_complexity=4.0),
            file_metrics=[],
            security_issues=[{"issue": 1}],  # 1 issue = -10 points
            complexity_issues=[{"issue": 1}, {"issue": 2}],  # 2 issues = -10 points
            duplication_issues=[{"issue": 1}],  # 1 issue = -10 points
            dead_code_issues=[],
        )

        metrics = QualityMetrics.from_analysis_results(results)

        # complexity_score = max(0, 100 - (4.0 * 5)) = 80
        assert metrics.complexity_score == 80.0

        # security_score = max(0, 100 - (1 * 10)) = 90
        assert metrics.security_score == 90.0

        # maintainability_score = max(0, 100 - (2 * 5)) = 90
        assert metrics.maintainability_score == 90.0

        # duplication_score = max(0, 100 - (1 * 10)) = 90
        assert metrics.duplication_score == 90.0

    def test_overall_score_calculation(self) -> None:
        """Test overall score weighted calculation using AnalysisResults."""
        results = AnalysisResults(
            overall_metrics=OverallMetrics(),  # Default values (no complexity)
            file_metrics=[],
            security_issues=[],
            dead_code_issues=[],
            duplication_issues=[],
            complexity_issues=[],
        )

        metrics = QualityMetrics.from_analysis_results(results)

        # All component scores should be 100 (no issues, no complexity)
        # documentation_score = 75 (placeholder value)
        # Overall = 100*0.25 + 100*0.25 + 100*0.2 + 100*0.15 + 75*0.15
        # Overall = 25 + 25 + 20 + 15 + 11.25 = 96.25
        expected_overall = 96.25
        assert abs(metrics.overall_score - expected_overall) < 0.01

    def test_scores_summary_computed_field(self) -> None:
        """Test scores_summary computed field."""
        metrics = QualityMetrics.create(
            complexity_score=85.0,
            security_score=90.0,
            maintainability_score=80.0,
            duplication_score=95.0,
            documentation_score=75.0,
        )

        summary = metrics.scores_summary

        assert summary["complexity"] == 85.0
        assert summary["security"] == 90.0
        assert summary["maintainability"] == 80.0
        assert summary["duplication"] == 95.0
        assert summary["documentation"] == 75.0

    def test_total_issues_computed_field(self) -> None:
        """Test total_issues computed field."""
        metrics = QualityMetrics.create(
            security_issues_count=5,
            dead_code_items_count=3,
            duplicate_blocks_count=2,
            complexity_issues_count=8,
        )

        assert metrics.total_issues == 18  # 5+3+2+8

    def test_to_dict(self) -> None:
        """Test to_dict method."""
        metrics = QualityMetrics.create(
            overall_score=87.5,
            quality_grade="B+",
            total_files=15,
            total_lines_of_code=1200,
            security_issues_count=2,
        )

        result = metrics.to_dict()

        assert result["overall_score"] == 87.5
        assert result["quality_grade"] == "B+"
        assert result["total_files"] == 15
        assert result["total_lines_of_code"] == 1200
        assert result["security_issues_count"] == 2
        assert "scores" in result
        assert "total_issues" in result
        assert isinstance(result["scores"], dict)

    def test_get_summary(self) -> None:
        """Test get_summary method."""
        metrics = QualityMetrics.create(
            overall_score=87.5,
            quality_grade="B+",
            total_files=15,
            total_lines_of_code=1200,
            total_functions=60,
            total_classes=12,
            security_issues_count=2,
            complexity_issues_count=3,
            dead_code_items_count=1,
            duplicate_blocks_count=0,
        )

        summary = metrics.get_summary()

        assert "B+ (87.5/100)" in summary
        assert "Files: 15" in summary
        assert "Lines: 1,200" in summary
        assert "Functions: 60" in summary
        assert "Classes: 12" in summary
        assert "Security(2)" in summary
        assert "Complexity(3)" in summary
        assert "DeadCode(1)" in summary
        assert "Duplicates(0)" in summary

    def test_calculate_grade_thresholds(self) -> None:
        """Test grade calculation for all thresholds."""
        test_cases = [
            (96.0, "A+"),
            (95.0, "A+"),
            (94.0, "A"),
            (90.0, "A"),
            (89.0, "A-"),
            (85.0, "A-"),
            (84.0, "B+"),
            (80.0, "B+"),
            (79.0, "B"),
            (75.0, "B"),
            (74.0, "B-"),
            (70.0, "B-"),
            (69.0, "C+"),
            (65.0, "C+"),
            (64.0, "C"),
            (60.0, "C"),
            (59.0, "C-"),
            (55.0, "C-"),
            (54.0, "D+"),
            (50.0, "D+"),
            (49.0, "D"),
            (45.0, "D"),
            (44.0, "F"),
            (0.0, "F"),
        ]

        for score, expected_grade in test_cases:
            grade = QualityGradeCalculator.calculate_grade(score)
            assert grade.value == expected_grade

    def test_from_analysis_results_missing_sections(self) -> None:
        """Test from_analysis_results with missing sections."""
        # Missing metrics section
        results_no_metrics: FlextTypes.Core.Dict = {"issues": {}}
        metrics = QualityMetrics.from_analysis_results(results_no_metrics)
        assert metrics.total_files == 0

        # Missing issues section
        results_no_issues: FlextTypes.Core.Dict = {"metrics": {"total_files": 5}}
        metrics = QualityMetrics.from_analysis_results(results_no_issues)
        assert metrics.security_issues_count == 0
        assert metrics.total_files == 5

    def test_from_analysis_results_missing_issue_categories(self) -> None:
        """Test from_analysis_results with missing issue categories."""
        results: FlextTypes.Core.Dict = {
            "metrics": {},
            "issues": {
                "security": [{"issue": 1}],
                # Missing dead_code, duplicates, complexity categories
            },
        }

        metrics = QualityMetrics.from_analysis_results(results)

        assert metrics.security_issues_count == 1
        assert metrics.dead_code_items_count == 0
        assert metrics.duplicate_blocks_count == 0
        assert metrics.complexity_issues_count == 0

    def test_edge_case_zero_complexity(self) -> None:
        """Test edge case with zero complexity."""
        results: FlextTypes.Core.Dict = {
            "metrics": {"average_complexity": 0.0},
            "issues": {},
        }

        metrics = QualityMetrics.from_analysis_results(results)

        # complexity_score = max(0, 100 - (0.0 * 5)) = 100
        assert metrics.complexity_score == 100.0

    def test_edge_case_high_issue_counts(self) -> None:
        """Test edge case with high issue counts."""
        many_issues = [{"issue": i} for i in range(50)]  # 50 issues

        results: FlextTypes.Core.Dict = {
            "metrics": {},
            "issues": {
                "security": many_issues,
                "complexity": many_issues,
                "duplicates": many_issues,
            },
        }

        metrics = QualityMetrics.from_analysis_results(results)

        # Scores should be clamped to 0 (max(0, 100 - penalty))
        assert metrics.security_score == 0.0
        assert metrics.duplication_score == 0.0

    def test_integration_realistic_project(self) -> None:
        """Test with realistic project data."""
        results = {
            "metrics": {
                "total_files": 45,
                "total_lines_of_code": 8500,
                "total_functions": 320,
                "total_classes": 45,
                "average_complexity": 7.2,
                "max_complexity": 18.5,
            },
            "issues": {
                "security": [{"type": "hardcoded_password"}],
                "dead_code": [{"type": "unused_import"}, {"type": "unused_variable"}],
                "duplicates": [{"type": "code_clone"}],
                "complexity": [
                    {"type": "high_complexity"},
                    {"type": "long_method"},
                    {"type": "deep_nesting"},
                ],
            },
        }

        metrics = QualityMetrics.from_analysis_results(results)

        # Verify all data is captured
        assert metrics.total_files == 45
        assert metrics.total_lines_of_code == 8500
        assert metrics.total_functions == 320
        assert metrics.total_classes == 45

        # Verify issue counts
        assert metrics.security_issues_count == 1
        assert metrics.dead_code_items_count == 2
        assert metrics.duplicate_blocks_count == 1
        assert metrics.complexity_issues_count == 3
        assert metrics.total_issues == 7

        # Verify scores are calculated
        assert 0 <= metrics.overall_score <= 100
        assert metrics.quality_grade in {
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

        # Verify computed fields work
        assert len(metrics.scores_summary) == 5
        assert all(0 <= score <= 100 for score in metrics.scores_summary.values())

        # Verify string representation
        summary = metrics.get_summary()
        assert "Files: 45" in summary
        assert "Lines: 8,500" in summary
