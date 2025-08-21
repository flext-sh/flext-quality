"""Quality grade calculation centralized module.

DRY REFACTOR: Centralizes grade calculation logic used across analyzer.py,
metrics.py, and reports.py to eliminate code duplication.

SOLID: Single Responsibility Principle - one place for grade logic.
"""

from __future__ import annotations

from typing import ClassVar

from flext_quality.domain.value_objects import QualityGrade


class QualityGradeCalculator:
    """Centralized quality grade calculation following DRY principle."""

    # Grade thresholds - single source of truth
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, QualityGrade]]] = [
        (95, QualityGrade.A_PLUS),
        (90, QualityGrade.A),
        (85, QualityGrade.A_MINUS),
        (80, QualityGrade.B_PLUS),
        (75, QualityGrade.B),
        (70, QualityGrade.B_MINUS),
        (65, QualityGrade.C_PLUS),
        (60, QualityGrade.C),
        (55, QualityGrade.C_MINUS),
        (50, QualityGrade.D_PLUS),
        (45, QualityGrade.D),
    ]

    @classmethod
    def calculate_grade(cls, score: float) -> QualityGrade:
        """Calculate grade from score - DRY implementation.

        Args:
            score: Quality score (0-100)

        Returns:
            QualityGrade enum value

        """
        for threshold, grade in cls._GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return QualityGrade.F

    @classmethod
    def get_grade_threshold(cls, grade: QualityGrade) -> int:
        """Get minimum threshold for a grade.

        Args:
            grade: QualityGrade enum value

        Returns:
            Minimum score threshold for the grade

        """
        for threshold, g in cls._GRADE_THRESHOLDS:
            if g == grade:
                return threshold
        return 0  # F grade


__all__ = ["QualityGrade", "QualityGradeCalculator"]
