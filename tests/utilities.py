"""Test utilities for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_quality import FlextQualityUtilities


class FlextQualityTestUtilities(FlextTestsUtilities, FlextQualityUtilities):
    """Test utilities for flext-quality."""

    class Quality(FlextQualityUtilities.Quality):
        """Quality domain test utilities."""

        class Tests:
            """Test-specific utilities."""


u = FlextQualityTestUtilities
__all__ = ["FlextQualityTestUtilities", "u"]
