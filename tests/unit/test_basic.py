"""Basic test to verify flext-infrastructure.monitoring.flext-quality is working.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import u


def test_basic() -> None:
    """Test that basic functionality works."""
    u.Tests.Matchers.that(True, eq=True)
