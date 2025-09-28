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

        # Enterprise-ready threshold (combination requirement)
        ENTERPRISE_READY_THRESHOLD = 85.0

        # Poor quality (anything below BELOW_AVERAGE_THRESHOLD)

    class Coverage:
        """Coverage thresholds and limits."""

        # Coverage requirements
        MINIMUM_COVERAGE = 90.0
        PRODUCTION_COVERAGE = 75.0  # Minimum for production-ready configs
        TARGET_COVERAGE = 95.0
        EXCELLENT_COVERAGE = 98.0
        MAXIMUM_COVERAGE = 100.0  # Maximum possible coverage percentage

    class Complexity:
        """Complexity thresholds."""

        # Cyclomatic complexity limits
        MAX_COMPLEXITY = 10
        WARNING_COMPLEXITY = 7
        IDEAL_COMPLEXITY = 5
        STRICT_COMPLEXITY = 8  # Strict threshold for enterprise configurations
        HIGH_COMPLEXITY_WARNING_THRESHOLD = (
            50  # Warning threshold for very high complexity
        )

    class Security:
        """Security scoring thresholds."""

        MINIMUM_SECURITY_SCORE = 90.0
        TARGET_SECURITY_SCORE = 95.0
        HIGH_SECURITY_SCORE_THRESHOLD = 95.0  # Threshold requiring enhanced validation

    class Maintainability:
        """Maintainability scoring thresholds."""

        MINIMUM_MAINTAINABILITY = 80.0
        TARGET_MAINTAINABILITY = 90.0

    class Performance:
        """Performance and timeout limits."""

        # Analysis timeouts in seconds
        MINIMUM_ANALYSIS_TIMEOUT = 30  # Minimum timeout for analysis operations
        MAXIMUM_ANALYSIS_TIMEOUT = 3600  # Maximum timeout to prevent system impact
        DEFAULT_ANALYSIS_TIMEOUT = 300  # Default timeout for most operations

        # Worker limits
        MINIMUM_WORKERS = 1  # Minimum number of worker processes
        MAXIMUM_WORKERS = 16  # Maximum workers to prevent system overload
        DEFAULT_WORKERS = 4  # Default number of worker processes

    class Validation:
        """Validation ranges and limits."""

        # Percentage validation
        MINIMUM_PERCENTAGE = 0.0
        MAXIMUM_PERCENTAGE = 100.0

        # Score thresholds requiring specific tools
        COVERAGE_EXTERNAL_TOOLS_THRESHOLD = 100.0  # Coverage requiring external tools
        SECURITY_BANDIT_THRESHOLD = 90.0  # Security score requiring Bandit
        SECURITY_DEPENDENCY_SCAN_THRESHOLD = 95.0  # Security requiring dependency scan

    class Reporting:
        """Reporting constants and limits."""

        # Report size thresholds
        LARGE_REPORT_SIZE_BYTES = 100000  # 100KB threshold for large reports

        # Path display limits
        PATH_SEGMENTS_TO_KEEP = 4  # Number of path segments to keep in display

    class Project:
        """Project lifecycle constants."""

        # Time-based thresholds
        RECENT_UPDATE_DAYS = 7  # Days threshold for "recently updated" status
