"""Test models for flext-quality helpers.

Provides test-specific models extending FlextQualityModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.models import FlextQualityModels


class TestsModels(FlextQualityModels):
    """Test-specific models extending FlextQualityModels.

    Provides test-specific model definitions that extend production
    models with test-specific fixtures. Uses real inheritance to
    expose the full hierarchy without duplication.
    """

    # Test-specific models can be added here as nested classes
    # All parent models are accessible via inheritance


# Standardized short name for use in tests (same pattern as flext-core)
m = TestsModels

__all__ = ["TestsModels", "m"]
