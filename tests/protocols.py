"""Test protocol definitions for flext-quality.

Provides TestsFlextQualityProtocols, combining FlextTestsProtocols with
FlextQualityProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_quality import FlextQualityProtocols


class TestsFlextQualityProtocols(FlextTestsProtocols, FlextQualityProtocols):
    """Test protocols combining FlextTestsProtocols and FlextQualityProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Quality.* (from FlextQualityProtocols)
    """


p = TestsFlextQualityProtocols
__all__ = ["TestsFlextQualityProtocols", "p"]
