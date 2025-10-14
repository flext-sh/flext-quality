"""Test domain value objects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_quality import (
    ComplexityMetric,
    CoverageMetric,
    DuplicationMetric,
    IssueLocation,
    IssueSeverity,
    IssueType,
    QualityGrade,
    QualityScore,
)

# NOTE: FilePath was not included in consolidation - these tests will be skipped
# FilePath = FlextQualityValueObjects.FilePath


class TestIssueSeverity:
    """Test IssueSeverity enum."""

    def test_severity_values(self) -> None:
        """Test severity enum values."""
        assert IssueSeverity.LOW.value == "low"
        assert IssueSeverity.MEDIUM.value == "medium"
        assert IssueSeverity.HIGH.value == "high"
        assert IssueSeverity.CRITICAL.value == "critical"

    def test_severity_enum_membership(self) -> None:
        """Test severity enum membership."""
        assert "low" in IssueSeverity
        assert "medium" in IssueSeverity
        assert "high" in IssueSeverity
        assert "critical" in IssueSeverity
        assert "unknown" not in IssueSeverity


class TestIssueType:
    """Test IssueType enum."""

    def test_syntax_issues(self) -> None:
        """Test syntax issue types."""
        assert IssueType.SYNTAX_ERROR.value == "syntax_error"
        assert IssueType.STYLE_VIOLATION.value == "style_violation"
        assert IssueType.NAMING_CONVENTION.value == "naming_convention"

    def test_complexity_issues(self) -> None:
        """Test complexity issue types."""
        assert IssueType.HIGH_COMPLEXITY.value == "high_complexity"
        assert IssueType.HIGH_COGNITIVE_COMPLEXITY.value == "high_cognitive_complexity"
        assert IssueType.LONG_METHOD.value == "long_method"
        assert IssueType.LONG_PARAMETER_LIST.value == "long_parameter_list"

    def test_security_issues(self) -> None:
        """Test security issue types."""
        assert IssueType.SECURITY_VULNERABILITY.value == "security_vulnerability"
        assert IssueType.HARDCODED_CREDENTIAL.value == "hardcoded_credential"
        assert IssueType.SQL_INJECTION.value == "sql_injection"
        assert IssueType.XSS_VULNERABILITY.value == "xss_vulnerability"

    def test_dead_code_issues(self) -> None:
        """Test dead code issue types."""
        assert IssueType.UNUSED_IMPORT.value == "unused_import"
        assert IssueType.UNUSED_VARIABLE.value == "unused_variable"
        assert IssueType.UNUSED_FUNCTION.value == "unused_function"
        assert IssueType.UNREACHABLE_CODE.value == "unreachable_code"

    def test_duplication_issues(self) -> None:
        """Test duplication issue types."""
        assert IssueType.DUPLICATE_CODE.value == "duplicate_code"
        assert IssueType.SIMILAR_CODE.value == "similar_code"

    def test_type_issues(self) -> None:
        """Test type issue types."""
        assert IssueType.TYPE_ERROR.value == "type_error"
        assert IssueType.MISSING_TYPE_ANNOTATION.value == "missing_type_annotation"

    def test_documentation_issues(self) -> None:
        """Test documentation issue types."""
        assert IssueType.MISSING_DOCSTRING.value == "missing_docstring"
        assert IssueType.INVALID_DOCSTRING.value == "invalid_docstring"


class TestQualityGrade:
    """Test QualityGrade enum."""

    def test_grade_values(self) -> None:
        """Test quality grade values."""
        assert QualityGrade.A_PLUS.value == "A+"
        assert QualityGrade.A == "A"
        assert QualityGrade.B == "B"
        assert QualityGrade.C == "C"
        assert QualityGrade.D == "D"
        assert QualityGrade.F == "F"

    def test_all_grades_exist(self) -> None:
        """Test all expected grades exist."""
        expected_grades = [
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
        ]

        for grade in expected_grades:
            assert grade in QualityGrade


# COMMENTED: FilePath not implemented in consolidation
# class TestFilePath:
#     """Test FilePath value object."""

#
#     def test_file_path_creation(self) -> None:
#         """Test file path creation."""

#         file_path = FilePath(value="/path/to/file.py")
#         assert file_path.value == "/path/to/file.py"
#         assert not file_path.is_absolute
#
#     def test_file_path_with_absolute_flag(self) -> None:
#         """Test file path with absolute flag."""

#         file_path = FilePath(value="/path/to/file.py", is_absolute=True)
#         assert file_path.is_absolute
#
#     def test_empty_path_validation(self) -> None:
#         """Test empty path validation fails."""

#         with pytest.raises(ValidationError):
#             FilePath(value="")
#
#     def test_path_property(self) -> None:
#         """Test path property returns Path object."""

#         file_path = FilePath(value="src/test.py")
#         assert isinstance(file_path.path, Path)
#         assert str(file_path.path) == "src/test.py"
#
#     def test_filename_property(self) -> None:
#         """Test filename property."""

#         file_path = FilePath(value="src/test.py")
#         assert file_path.filename == "test.py"
#
#     def test_extension_property(self) -> None:
#         """Test extension property."""

#         file_path = FilePath(value="src/test.py")
#         assert file_path.extension == ".py"
#
#     def test_parent_dir_property(self) -> None:
#         """Test parent directory property."""

#         file_path = FilePath(value="src/test.py")
#         assert file_path.parent_dir == "src"
#
#     def test_path_normalization(self) -> None:
#         """Test path normalization uses posix format."""

#         file_path = FilePath(value="src/test.py")
#         # Verify the path property works correctly with normalized paths
#         assert file_path.path.name == "test.py"
#         assert file_path.filename == "test.py"


class TestIssueLocation:
    """Test IssueLocation value object."""

    def test_location_creation(self) -> None:
        """Test issue location creation."""
        location = IssueLocation(line=10, column=5)
        assert location.line == 10
        assert location.column == 5

    def test_location_with_defaults(self) -> None:
        """Test location with default column."""
        location = IssueLocation(line=10)
        assert location.line == 10
        assert location.column == 1

    def test_location_with_range(self) -> None:
        """Test location with line range."""
        location = IssueLocation(line=10, column=5, end_line=12, end_column=8)
        assert location.line == 10
        assert location.end_line == 12
        assert location.end_column == 8

    def test_invalid_line_validation(self) -> None:
        """Test invalid line number validation."""
        with pytest.raises(ValidationError):
            IssueLocation(line=0)

    def test_invalid_end_line_validation(self) -> None:
        """Test invalid end line validation."""
        with pytest.raises(ValidationError):
            IssueLocation(line=10, end_line=0)

    def test_range_text_single_line(self) -> None:
        """Test range text for single line."""
        location = IssueLocation(line=10, column=5)
        assert location.range_text == "line 10, column 5"

    def test_range_text_same_line_range(self) -> None:
        """Test range text for same line range."""
        location = IssueLocation(line=10, column=5, end_line=10, end_column=8)
        assert location.range_text == "line 10, columns 5-8"

    def test_range_text_multi_line(self) -> None:
        """Test range text for multi-line range."""
        location = IssueLocation(line=10, column=5, end_line=12, end_column=8)
        assert location.range_text == "lines 10-12"

    def test_range_text_no_end_column(self) -> None:
        """Test range text without end column."""
        location = IssueLocation(line=10, column=5, end_line=10)
        assert location.range_text == "line 10, columns 5-end"


class TestQualityScore:
    """Test QualityScore value object."""

    def test_quality_score_creation(self) -> None:
        """Test quality score creation."""
        score = QualityScore(value=85.5)
        assert score.value == 85.5

    def test_score_bounds_validation(self) -> None:
        """Test score bounds validation."""
        with pytest.raises(ValidationError):
            QualityScore(value=-1.0)

        with pytest.raises(ValidationError):
            QualityScore(value=101.0)

    def test_percentage_property(self) -> None:
        """Test percentage property formatting."""
        score = QualityScore(value=85.567)
        assert score.percentage == "85.6%"

    def test_grade_property_a_plus(self) -> None:
        """Test A+ grade assignment."""
        score = QualityScore(value=95.0)
        assert score.grade == QualityGrade.A_PLUS

    def test_grade_property_a(self) -> None:
        """Test A grade assignment."""
        score = QualityScore(value=90.0)
        assert score.grade == QualityGrade.A

    def test_grade_property_b(self) -> None:
        """Test B grade assignment."""
        score = QualityScore(value=75.0)
        assert score.grade == QualityGrade.B

    def test_grade_property_f(self) -> None:
        """Test F grade assignment."""
        score = QualityScore(value=30.0)
        assert score.grade == QualityGrade.F

    def test_all_grade_ranges(self) -> None:
        """Test all grade ranges are correctly assigned."""
        test_cases = [
            (96.0, QualityGrade.A_PLUS),
            (91.0, QualityGrade.A),
            (86.0, QualityGrade.A_MINUS),
            (81.0, QualityGrade.B_PLUS),
            (76.0, QualityGrade.B),
            (71.0, QualityGrade.B_MINUS),
            (66.0, QualityGrade.C_PLUS),
            (61.0, QualityGrade.C),
            (56.0, QualityGrade.C_MINUS),
            (51.0, QualityGrade.D_PLUS),
            (46.0, QualityGrade.D),
            (41.0, QualityGrade.D_MINUS),
            (30.0, QualityGrade.F),
        ]

        for score_value, expected_grade in test_cases:
            score = QualityScore(value=score_value)
            assert score.grade == expected_grade


class TestComplexityMetric:
    """Test ComplexityMetric value object."""

    def test_complexity_creation(self) -> None:
        """Test complexity metric creation."""
        complexity = ComplexityMetric(cyclomatic=5, cognitive=3, max_depth=2)
        assert complexity.cyclomatic == 5
        assert complexity.cognitive == 3
        assert complexity.max_depth == 2

    def test_complexity_defaults(self) -> None:
        """Test complexity metric defaults."""
        complexity = ComplexityMetric()
        assert complexity.cyclomatic == 1
        assert complexity.cognitive == 0
        assert complexity.max_depth == 0

    def test_is_complex_false(self) -> None:
        """Test is_complex returns False for simple code."""
        complexity = ComplexityMetric(cyclomatic=5, cognitive=10, max_depth=2)
        assert not complexity.is_complex

    def test_is_complex_high_cyclomatic(self) -> None:
        """Test is_complex returns True for high cyclomatic complexity."""
        complexity = ComplexityMetric(cyclomatic=15)
        assert complexity.is_complex

    def test_is_complex_high_cognitive(self) -> None:
        """Test is_complex returns True for high cognitive complexity."""
        complexity = ComplexityMetric(cognitive=20)
        assert complexity.is_complex

    def test_is_complex_high_depth(self) -> None:
        """Test is_complex returns True for high max depth."""
        complexity = ComplexityMetric(max_depth=6)
        assert complexity.is_complex

    def test_complexity_level_simple(self) -> None:
        """Test complexity level for simple code."""
        complexity = ComplexityMetric(cyclomatic=3)
        assert complexity.complexity_level == "simple"

    def test_complexity_level_moderate(self) -> None:
        """Test complexity level for moderate code."""
        complexity = ComplexityMetric(cyclomatic=8)
        assert complexity.complexity_level == "moderate"

    def test_complexity_level_complex(self) -> None:
        """Test complexity level for complex code."""
        complexity = ComplexityMetric(cyclomatic=15)
        assert complexity.complexity_level == "complex"

    def test_complexity_level_very_complex(self) -> None:
        """Test complexity level for very complex code."""
        complexity = ComplexityMetric(cyclomatic=25)
        assert complexity.complexity_level == "very complex"


class TestCoverageMetric:
    """Test CoverageMetric value object."""

    def test_coverage_creation(self) -> None:
        """Test coverage metric creation."""
        coverage = CoverageMetric(
            line_coverage=85.0,
            branch_coverage=75.0,
            function_coverage=90.0,
        )
        assert coverage.line_coverage == 85.0
        assert coverage.branch_coverage == 75.0
        assert coverage.function_coverage == 90.0

    def test_coverage_defaults(self) -> None:
        """Test coverage metric defaults."""
        coverage = CoverageMetric()
        assert coverage.line_coverage == 0.0
        assert coverage.branch_coverage == 0.0
        assert coverage.function_coverage == 0.0

    def test_coverage_bounds_validation(self) -> None:
        """Test coverage bounds validation."""
        with pytest.raises(ValidationError):
            CoverageMetric(line_coverage=-1.0)

        with pytest.raises(ValidationError):
            CoverageMetric(line_coverage=101.0)

    def test_overall_coverage_calculation(self) -> None:
        """Test overall coverage calculation with weights."""
        coverage = CoverageMetric(
            line_coverage=80.0,  # 50% weight = 40.0
            branch_coverage=70.0,  # 30% weight = 21.0
            function_coverage=90.0,  # 20% weight = 18.0
        )
        # Total: 40.0 + 21.0 + 18.0 = 79.0
        expected = 79.0
        assert coverage.overall_coverage == expected

    def test_is_sufficient_true(self) -> None:
        """Test is_sufficient returns True for high coverage."""
        coverage = CoverageMetric(
            line_coverage=95.0,
            branch_coverage=95.0,
            function_coverage=95.0,
        )
        assert coverage.is_sufficient

    def test_is_sufficient_false(self) -> None:
        """Test is_sufficient returns False for low coverage."""
        coverage = CoverageMetric(
            line_coverage=80.0,
            branch_coverage=70.0,
            function_coverage=90.0,
        )
        assert not coverage.is_sufficient


class TestDuplicationMetric:
    """Test DuplicationMetric value object."""

    def test_duplication_creation(self) -> None:
        """Test duplication metric creation."""
        duplication = DuplicationMetric(
            duplicate_lines=50,
            total_lines=1000,
            duplicate_blocks=5,
        )
        assert duplication.duplicate_lines == 50
        assert duplication.total_lines == 1000
        assert duplication.duplicate_blocks == 5

    def test_duplication_defaults(self) -> None:
        """Test duplication metric defaults."""
        duplication = DuplicationMetric()
        assert duplication.duplicate_lines == 0
        assert duplication.total_lines == 0
        assert duplication.duplicate_blocks == 0

    def test_duplication_validation(self) -> None:
        """Test duplication metric validation."""
        with pytest.raises(ValidationError):
            DuplicationMetric(duplicate_lines=-1)

    def test_duplication_percentage_calculation(self) -> None:
        """Test duplication percentage calculation."""
        duplication = DuplicationMetric(duplicate_lines=50, total_lines=1000)
        assert duplication.duplication_percentage == 5.0

    def test_duplication_percentage_zero_lines(self) -> None:
        """Test duplication percentage with zero total lines."""
        duplication = DuplicationMetric(duplicate_lines=10, total_lines=0)
        assert duplication.duplication_percentage == 0.0

    def test_is_acceptable_true(self) -> None:
        """Test is_acceptable returns True for low duplication."""
        duplication = DuplicationMetric(duplicate_lines=30, total_lines=1000)  # 3%
        assert duplication.is_acceptable

    def test_is_acceptable_false(self) -> None:
        """Test is_acceptable returns False for high duplication."""
        duplication = DuplicationMetric(duplicate_lines=60, total_lines=1000)  # 6%
        assert not duplication.is_acceptable

    def test_is_acceptable_edge_case(self) -> None:
        """Test is_acceptable at exactly 5% threshold."""
        duplication = DuplicationMetric(duplicate_lines=50, total_lines=1000)  # 5%
        assert not duplication.is_acceptable  # Should be False since >= 5%
