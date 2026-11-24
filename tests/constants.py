"""Test constants for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from tests import FlextQualityConstants


class TestsFlextQualityConstants(FlextTestsConstants, FlextQualityConstants):
    """Test constants for flext-quality."""

    class Tests(FlextTestsConstants.Tests):
        """Test-specific constants."""


c = TestsFlextQualityConstants
__all__: list[str] = ["TestsFlextQualityConstants", "c"]
