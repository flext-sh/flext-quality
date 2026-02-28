"""Test constants for flext-quality.

Provides test-specific constants extending FlextQualityConstants
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import FlextQualityConstants


class TestsConstants(FlextQualityConstants):
    """Test-specific constants extending FlextQualityConstants.

    Provides test-specific constant values that extend production
    constants with test-specific definitions. Uses real inheritance to
    expose the full hierarchy without duplication.
    """

    # Test-specific constants can be added here as nested classes
    # All parent constants are accessible via inheritance


# Standardized short name for use in tests (same pattern as flext-core)
c = TestsConstants

__all__ = ["TestsConstants", "c"]
