"""Test models for flext-quality.

Provides test-specific models extending FlextTestsModels and FlextQualityModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.models import FlextTestsModels

from flext_quality.models import FlextQualityModels


class TestsFlextQualityModels(FlextTestsModels, FlextQualityModels):
    """Test models - composition of FlextTestsModels + FlextQualityModels.

    Hierarchy:
    - FlextTestsModels: Generic test utilities from flext-tests
    - FlextQualityModels: Domain models from flext-quality
    - TestsFlextQualityModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Quality.* - Production domain models (inherited)
    - FlextTestsModels.Tests.* - Generic test utilities
    """

    class Tests:
        """Test fixtures namespace for flext-quality.

        Contains test-specific models and fixtures that should not
        be part of production code.
        """


# Short aliases for tests
tm = TestsFlextQualityModels
m = TestsFlextQualityModels

__all__ = ["TestsFlextQualityModels", "m", "tm"]
