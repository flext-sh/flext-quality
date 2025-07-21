"""Persistence layer for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core persistence patterns - NO duplication.
"""

from __future__ import annotations

from flext_quality.infrastructure.persistence.repositories import (
    AnalysisResultRepository,
    QualityMetricsRepository,
    QualityRuleRepository,
)

__all__ = [
    "AnalysisResultRepository",
    "QualityMetricsRepository",
    "QualityRuleRepository",
]
