"""FLEXT Quality Test Configuration - Comprehensive Testing Infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import reset_settings as _shared_reset_settings

from flext_quality.settings import FlextQualitySettings
from tests.utilities import u

if TYPE_CHECKING:
    from collections.abc import Generator

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
