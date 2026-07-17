"""FLEXT Quality Test Configuration - Comprehensive Testing Infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from flext_tests._fixtures.settings import reset_settings as _shared_reset_settings

from flext_quality import FlextQualitySettings
from tests import u

reset_settings = _shared_reset_settings


@pytest.fixture
def set_test_environment(reset_settings: None) -> Generator[None]:
    """Configure isolated test environment variables."""
    _ = reset_settings
    FlextQualitySettings.reset_for_testing()
    try:
        with u.Tests.env_vars_context({
            "FLEXT_ENV": "test",
            "FLEXT_LOG_LEVEL": "DEBUG",
        }):
            yield
    finally:
        FlextQualitySettings.reset_for_testing()
