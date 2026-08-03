"""Test models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import FlextQualityModels
from flext_tests import FlextTestsModels


class TestsFlextQualityModels(FlextTestsModels, FlextQualityModels):
    """Test models for flext-quality."""

    class Quality(FlextQualityModels.Quality):
        """Quality domain test models."""

        class Tests:
            """Test-specific models."""


m = TestsFlextQualityModels
__all__: list[str] = ["TestsFlextQualityModels", "m"]
