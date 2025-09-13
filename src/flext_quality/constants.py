"""Quality assessment constants extending flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants


class FlextQualityConstants(FlextConstants):
    """Central container for quality assessment constants.

    Follows the same pattern as FlextConstants from flext-core,
    organizing constants into logical categories with type safety.
    """

    class QualityThresholds:
        """Quality score thresholds for assessment levels."""

        # Industry-leading quality
        OUTSTANDING_THRESHOLD = 95.0

        # Production-ready quality
        EXCELLENT_THRESHOLD = 90.0

        # Good quality with minor improvements
        GOOD_THRESHOLD = 80.0

        # Acceptable quality with moderate improvements
        ACCEPTABLE_THRESHOLD = 70.0

        # Below average quality
        BELOW_AVERAGE_THRESHOLD = 60.0

        # Poor quality (anything below BELOW_AVERAGE_THRESHOLD)

    class Coverage:
        """Coverage thresholds and limits."""

        # Coverage requirements
        MINIMUM_COVERAGE = 90.0
        TARGET_COVERAGE = 95.0
        EXCELLENT_COVERAGE = 98.0

    class Complexity:
        """Complexity thresholds."""

        # Cyclomatic complexity limits
        MAX_COMPLEXITY = 10
        WARNING_COMPLEXITY = 7
        IDEAL_COMPLEXITY = 5

    class Security:
        """Security scoring thresholds."""

        MINIMUM_SECURITY_SCORE = 90.0
        TARGET_SECURITY_SCORE = 95.0

    class Maintainability:
        """Maintainability scoring thresholds."""

        MINIMUM_MAINTAINABILITY = 80.0
        TARGET_MAINTAINABILITY = 90.0
