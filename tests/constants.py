"""Constants for flext-quality tests.

Provides TestsFlextQualityConstants extending FlextQualityConstants with test-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_quality.constants import FlextQualityConstants


class TestsFlextQualityConstants(FlextQualityConstants):
    """Constants for flext-quality tests.

    Access patterns:
    - c.Quality.* (domain constants from production)
    - c.Quality.Literals.* (type literals from production)
    - c.Paths.* (test path constants)
    - c.TestQuality.* (project-specific test data)
    """

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_quality_test_"

    class TestQuality:
        """Quality test constants."""

        TEST_PROJECT_PATH: Final[str] = "tests/fixtures/projects/test_project"
        TEST_ANALYSIS_TIMEOUT: Final[int] = 60
        TEST_WORKERS: Final[int] = 2


# Short aliases per FLEXT convention
c = TestsFlextQualityConstants
c = TestsFlextQualityConstants

__all__ = [
    "TestsFlextQualityConstants",
    "c",
]
