"""Test type aliases for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_quality import FlextQualityTypes


class FlextQualityTestTypes(FlextTestsTypes, FlextQualityTypes):
    """Test type aliases for flext-quality."""

    class Quality(FlextQualityTypes.Quality):
        """Quality domain test type aliases."""

        class Tests:
            """Test-specific type aliases."""


t = FlextQualityTestTypes
__all__ = ["FlextQualityTestTypes", "t"]
