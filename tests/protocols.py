"""Test protocol definitions for flext-quality.

Provides TestsFlextQualityProtocols, combining p with
FlextQualityProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_quality import FlextQualityProtocols


class TestsFlextQualityProtocols(p, FlextQualityProtocols):
    """Test protocols combining p and FlextQualityProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Quality.* (from FlextQualityProtocols)
    """


p = TestsFlextQualityProtocols
__all__ = ["TestsFlextQualityProtocols", "p"]
