"""SOLID: Single Responsibility Principle - one place for grade logic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import ClassVar

from flext_quality.value_objects import FlextQualityGrade


class FlextQualityGradeCalculator:
    """Centralized quality grade calculation following DRY principle."""

    # Grade thresholds - single source of truth
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, FlextQualityGrade]]] = [
        (95, FlextQualityGrade.A_PLUS),
        (90, FlextQualityGrade.A),
        (85, FlextQualityGrade.A_MINUS),
        (80, FlextQualityGrade.B_PLUS),
        (75, FlextQualityGrade.B),
        (70, FlextQualityGrade.B_MINUS),
        (65, FlextQualityGrade.C_PLUS),
        (60, FlextQualityGrade.C),
        (55, FlextQualityGrade.C_MINUS),
        (50, FlextQualityGrade.D_PLUS),
        (45, FlextQualityGrade.D),
    ]

    @classmethod
    def calculate_grade(cls, score: float) -> FlextQualityGrade:
        """Calculate grade from score - DRY implementation.

        Args:
            score: Quality score (0-100)

        Returns:
            FlextQualityGrade enum value

        """
        for threshold, grade in cls._GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return FlextQualityGrade.F

    @classmethod
    def get_grade_threshold(cls, grade: FlextQualityGrade) -> int:
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
