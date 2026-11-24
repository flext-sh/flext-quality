"""Test type aliases for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from tests import FlextQualityTypes


class TestsFlextQualityTypes(FlextTestsTypes, FlextQualityTypes):
    """Test type aliases for flext-quality."""

    class Tests(FlextTestsTypes.Tests):
        """Test-specific type aliases."""


t = TestsFlextQualityTypes
__all__: list[str] = ["TestsFlextQualityTypes", "t"]
