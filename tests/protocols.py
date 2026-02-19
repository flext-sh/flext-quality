"""Test protocol definitions for flext-quality.

Provides TestsFlextQualityProtocols, combining FlextTestsProtocols with
FlextQualityProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.protocols import FlextQualityProtocols
from flext_tests.protocols import FlextTestsProtocols


class TestsFlextQualityProtocols(FlextTestsProtocols, FlextQualityProtocols):
    """Test protocols combining FlextTestsProtocols and FlextQualityProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.Quality.* (from FlextQualityProtocols)
    """

    # class Tests:
    #     """Project-specific test protocols.
    #
    #     Extends FlextTestsProtocols.Tests with Quality-specific protocols.
    #     """

    # class Quality:
    #     """Quality-specific test protocols."""


# Runtime aliases
p = TestsFlextQualityProtocols
tp = TestsFlextQualityProtocols

__all__ = ["TestsFlextQualityProtocols", "p", "tp"]
