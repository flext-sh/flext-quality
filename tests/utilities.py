"""Module skeleton for TestsFlextQualityUtilities.

Test utilities for flextquality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u as _base_u
from flext_tests._utilities.matchers import FlextTestsMatchersUtilities

from flext_quality.utilities import FlextQualityUtilities


class TestsFlextQualityUtilities(FlextQualityUtilities):
    """Test utilities for flextquality."""

    class Tests(FlextTestsMatchersUtilities.Tests, _base_u.Tests):
        """Merged Tests namespace with Matchers from FlextTestsMatchersUtilities."""


u = TestsFlextQualityUtilities
__all__ = ["TestsFlextQualityUtilities", "u"]
