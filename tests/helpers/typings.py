"""Test typings extending flext_quality.typings for test-specific type definitions.

This module provides test-specific type definitions that extend the production
types from src/flext_quality/typings.py. All test types use real inheritance
to expose the full hierarchy and avoid duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality import FlextQualityTypes


class TestsTypings(FlextQualityTypes):
    """Test-specific type definitions extending FlextQualityTypes.

    Provides test-specific type aliases that extend production types
    with test-specific type definitions. Uses real inheritance to expose
    the full hierarchy without duplication.
    """


t = TestsTypings
__all__ = ["TestsTypings", "t"]
