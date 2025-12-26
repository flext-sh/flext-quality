"""Constants for flext-quality tests.

Provides TestsFlextQualityConstants, extending FlextTestsConstants with flext-quality-specific
constants using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides .Tests.* namespace
- FlextQualityConstants (production) - Provides .Quality.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_tests.constants import FlextTestsConstants

from flext_quality.constants import FlextQualityConstants


class TestsFlextQualityConstants(FlextTestsConstants, FlextQualityConstants):
    """Constants for flext-quality tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsConstants - for test infrastructure (.Tests.*)
    2. FlextQualityConstants - for domain constants (.Quality.*)

    Access patterns:
    - tc.Tests.Docker.* (container testing)
    - tc.Tests.Matcher.* (assertion messages)
    - tc.Tests.Factory.* (test data generation)
    - tc.Quality.* (domain constants from production)
    - tc.TestQuality.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or FlextQualityConstants
    - Only flext-quality-specific test constants allowed
    - All generic constants come from FlextTestsConstants
    - All production constants come from FlextQualityConstants
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

    class Literals:
        """Literal type aliases for test constants (Python 3.13 pattern)."""

        AnalysisStatusLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.AnalysisStatusLiteral
        )
        IssueSeverityLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.IssueSeverityLiteral
        )
        IssueTypeLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.IssueTypeLiteral
        )
        ReportFormatLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.ReportFormatLiteral
        )
        BackendTypeLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.BackendTypeLiteral
        )
        LanguageLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.LanguageLiteral
        )
        CheckStatusLiteral: TypeAlias = (
            FlextQualityConstants.Quality.Literals.CheckStatusLiteral
        )
        LogLevelLiteral: TypeAlias = FlextQualityConstants.Settings.LogLevel


# Short aliases per FLEXT convention
tc = TestsFlextQualityConstants  # Primary test constants alias
c = TestsFlextQualityConstants  # Alternative alias for compatibility

__all__ = [
    "TestsFlextQualityConstants",
    "c",
    "tc",
]
