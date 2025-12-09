"""SOLID: Single Responsibility Principle - one place for grade logic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import warnings
from typing import ClassVar

from .models import FlextQualityModels


class FlextQualityGradeCalculator:
    """Centralized quality grade calculation following DRY principle."""

    # Grade thresholds - single source of truth
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, FlextQualityModels.QualityGrade]]] = [
        (95, FlextQualityModels.QualityGrade.A_PLUS),
        (90, FlextQualityModels.QualityGrade.A),
        (85, FlextQualityModels.QualityGrade.A_MINUS),
        (80, FlextQualityModels.QualityGrade.B_PLUS),
        (75, FlextQualityModels.QualityGrade.B),
        (70, FlextQualityModels.QualityGrade.B_MINUS),
        (65, FlextQualityModels.QualityGrade.C_PLUS),
        (60, FlextQualityModels.QualityGrade.C),
        (55, FlextQualityModels.QualityGrade.C_MINUS),
        (50, FlextQualityModels.QualityGrade.D_PLUS),
        (45, FlextQualityModels.QualityGrade.D),
    ]

    @classmethod
    def calculate_grade(cls, score: float) -> FlextQualityModels.QualityGrade:
        """Calculate grade from score - DRY implementation.

        Args:
        score: Quality score (0-100)

        Returns:
        FlextQualityGrade enum value

        """
        for threshold, grade in cls._GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return FlextQualityModels.QualityGrade.F

    @classmethod
    def get_grade_threshold(cls, grade: FlextQualityModels.QualityGrade) -> int:
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
