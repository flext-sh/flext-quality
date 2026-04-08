"""Test constants for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_tests import FlextTestsConstants

from flext_quality import FlextQualityConstants


class TestsFlextQualityConstants(FlextTestsConstants, FlextQualityConstants):
    """Test constants for flext-quality."""

    class Quality(FlextQualityConstants.Quality):
        """Quality domain test constants."""

        class Tests:
            """Test-specific constants."""

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


c = TestsFlextQualityConstants
__all__ = ["TestsFlextQualityConstants", "c"]
