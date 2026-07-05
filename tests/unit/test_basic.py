"""Behavioral contract for the flext-quality package surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_quality import FlextQuality, c, quality


class TestsFlextQualityBasic:
    """Public contract of the flext-quality package facade and constants."""

    def test_facade_constructs_without_arguments(self) -> None:
        """FlextQuality() is constructible with no arguments."""
        tm.that(FlextQuality(), is_=FlextQuality)

    def test_global_alias_is_facade_instance(self) -> None:
        """The module-level ``quality`` alias is a FlextQuality facade."""
        tm.that(quality, is_=FlextQuality)

    def test_execute_reports_success(self) -> None:
        """execute() yields a successful result carrying the status snapshot."""
        result = FlextQuality().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    @pytest.mark.parametrize(
        "key",
        ["name", "version", "settings", "hooks_registered"],
    )
    def test_execute_status_exposes_public_keys(self, key: str) -> None:
        """The status snapshot from execute() carries every documented key."""
        tm.that(FlextQuality().execute().value, has=key)

    def test_execute_reports_canonical_identity(self) -> None:
        """execute() surfaces the canonical server name and version constants."""
        status = FlextQuality().execute().value
        tm.that(status["name"], eq=c.Quality.MCP_SERVER_NAME)
        tm.that(status["version"], eq=c.Quality.MCP_SERVER_VERSION)

    def test_execute_is_idempotent_in_shape(self) -> None:
        """Repeated execute() calls return the same observable identity."""
        facade = FlextQuality()
        first = facade.execute().value
        second = facade.execute().value
        tm.that(first["name"], eq=second["name"])
        tm.that(first["version"], eq=second["version"])

    def test_hooks_registered_count_is_non_negative(self) -> None:
        """The reported hook-registration count is a valid non-negative total."""
        count = FlextQuality().execute().value["hooks_registered"]
        tm.that(count, is_=int)
        tm.that(isinstance(count, int) and count >= 0, eq=True)
