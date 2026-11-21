"""Test protocols for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from tests import FlextQualityProtocols


class TestsFlextQualityProtocols(FlextTestsProtocols, FlextQualityProtocols):
    """Test protocols for flext-quality."""

    class Tests(FlextTestsProtocols.Tests):
        """Test-specific protocols."""


p = TestsFlextQualityProtocols
__all__: list[str] = ["TestsFlextQualityProtocols", "p"]
