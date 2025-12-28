"""SOLID: Single Responsibility Principle - one place for grade logic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import warnings
from typing import ClassVar

from .constants import c


class FlextQualityGradeCalculator:
    """Centralized quality grade calculation following DRY principle."""

    # Grade thresholds - single source of truth
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, c.Quality.QualityGrade]]] = [
        (95, c.Quality.QualityGrade.A_PLUS),
        (90, c.Quality.QualityGrade.A),
        (85, c.Quality.QualityGrade.A_MINUS),
        (80, c.Quality.QualityGrade.B_PLUS),
        (75, c.Quality.QualityGrade.B),
        (70, c.Quality.QualityGrade.B_MINUS),
        (65, c.Quality.QualityGrade.C_PLUS),
        (60, c.Quality.QualityGrade.C),
        (55, c.Quality.QualityGrade.C_MINUS),
        (50, c.Quality.QualityGrade.D_PLUS),
        (45, c.Quality.QualityGrade.D),
    ]

    @classmethod
    def calculate_grade(cls, score: float) -> c.Quality.QualityGrade:
        """Calculate grade from score - DRY implementation.

        Args:
        score: Quality score (0-100)

        Returns:
        FlextQualityGrade enum value

        """
        for threshold, grade in cls._GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return c.Quality.QualityGrade.F

    @classmethod
    def get_grade_threshold(cls, grade: c.Quality.QualityGrade) -> int:
        """Get minimum threshold for a grade.

        Args:
        grade: FlextQualityGrade enum value

        Returns:
        Minimum score threshold for the grade

        """
        for threshold, g in cls._GRADE_THRESHOLDS:
            if g == grade:
                return threshold
        return 0  # F grade


# Legacy compatibility facade - DEPRECATED
QualityGradeCalculator = FlextQualityGradeCalculator
warnings.warn(
    "QualityGradeCalculator is deprecated; use FlextQualityGradeCalculator",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["FlextQualityGradeCalculator", "QualityGradeCalculator"]
