"""FLEXT Quality Command Strategies - Execution thresholds and strategy constants.

Command execution strategy thresholds for quality operations.
Follows FLEXT standards for constants organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class CommandStrategies:
    """Command execution strategy thresholds."""

    ANALYZE_SUCCESS_THRESHOLD: float = 80.0
    ANALYZE_WARNING_THRESHOLD: float = 60.0
    VALIDATE_SUCCESS_THRESHOLD: float = 70.0
    SCORE_SUCCESS_THRESHOLD: float = 80.0
    SCORE_WARNING_THRESHOLD: float = 60.0
    CHECK_SUCCESS_THRESHOLD: float = 70.0
    TEST_ANTIPATTERNS_THRESHOLD: float = 80.0
    TEST_INHERITANCE_THRESHOLD: float = 80.0
    TEST_STRUCTURE_THRESHOLD: float = 80.0
    TEST_FIXTURES_THRESHOLD: float = 80.0
