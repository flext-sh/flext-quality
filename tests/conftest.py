"""FLEXT Quality Test Configuration - Comprehensive Testing Infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_quality import FlextQualitySettings
from tests import u

if TYPE_CHECKING:
    from collections.abc import Generator

# Why: `reset_settings` is auto-registered as a pytest fixture by the
# `flext_tests` pytest11 plugin (flext_tests.conftest_plugin ->
# flext_tests._fixtures.settings); flext_tests no longer re-exports it at
# its package root, so the previous local re-import/reassignment was dead
# and broke pyrefly (flext-1wjg1.16.32). No local declaration is needed.


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
