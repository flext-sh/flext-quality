"""Test models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_quality import FlextQualityModels


class FlextQualityTestModels(FlextTestsModels, FlextQualityModels):
    """Test models for flext-quality."""

    class Quality(FlextQualityModels.Quality):
        """Quality domain test models."""

        class Tests:
            """Test-specific models."""


m = FlextQualityTestModels
__all__ = ["FlextQualityTestModels", "m"]
