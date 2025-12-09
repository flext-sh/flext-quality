"""Test constants for flext-quality tests.

Centralized constants for test fixtures, factories, and test data.
Does NOT duplicate src/flext_quality/constants.py - only test-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_quality.constants import FlextQualityConstants


class TestsConstants(FlextQualityConstants):
    """Centralized test constants following flext-core nested class pattern."""

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_quality_test_"

    class Quality:
        """Quality test constants."""

        TEST_PROJECT_PATH: Final[str] = "tests/fixtures/projects/test_project"
        TEST_ANALYSIS_TIMEOUT: Final[int] = 60
        TEST_WORKERS: Final[int] = 2

    class Literals:
        """Literal type aliases for test constants (Python 3.13 pattern).

        These type aliases reuse production Literals from FlextQualityConstants
        to ensure consistency between tests and production code.
        """

        # Reuse production Literals for consistency (Python 3.13+ best practices)
        # Analysis status literal (reusing production type)
        AnalysisStatusLiteral: TypeAlias = (
            FlextQualityConstants.Literals.AnalysisStatusLiteral
        )

        # Issue severity literal (reusing production type)
        IssueSeverityLiteral: TypeAlias = (
            FlextQualityConstants.Literals.IssueSeverityLiteral
        )

        # Issue type literal (reusing production type)
        IssueTypeLiteral: TypeAlias = FlextQualityConstants.Literals.IssueTypeLiteral

        # Report format literal (reusing production type)
        ReportFormatLiteral: TypeAlias = (
            FlextQualityConstants.Literals.ReportFormatLiteral
        )

        # Backend type literal (reusing production type)
        BackendTypeLiteral: TypeAlias = (
            FlextQualityConstants.Literals.BackendTypeLiteral
        )

        # Language literal (reusing production type)
        LanguageLiteral: TypeAlias = FlextQualityConstants.Literals.LanguageLiteral

        # Check status literal (reusing production type)
        CheckStatusLiteral: TypeAlias = (
            FlextQualityConstants.Literals.CheckStatusLiteral
        )

        # Log level literal (reusing production type)
        LogLevelLiteral: TypeAlias = FlextQualityConstants.Settings.LogLevel


# Standardized short name for use in tests (same pattern as flext-core)
c = TestsConstants

__all__ = ["TestsConstants", "c"]
