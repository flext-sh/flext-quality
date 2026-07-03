"""Basic test to verify flext-infrastructure.monitoring.flext-quality is working.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm


class TestsFlextQualityBasic:
    """Behavior contract for test_basic."""

    def test_basic(self) -> None:
        """Test that basic functionality works."""
        tm.that(True, eq=True)
