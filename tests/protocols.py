"""Test protocols for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_quality import FlextQualityProtocols


class FlextQualityTestProtocols(FlextTestsProtocols, FlextQualityProtocols):
    """Test protocols for flext-quality."""

    class Quality(FlextQualityProtocols.Quality):
        """Quality domain test protocols."""

        class Tests:
            """Test-specific protocols."""


p = FlextQualityTestProtocols
__all__ = ["FlextQualityTestProtocols", "p"]
