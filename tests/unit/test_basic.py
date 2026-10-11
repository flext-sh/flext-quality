"""Behavioral contract for the flext-quality package surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_quality import FlextQuality, FlextQualityConfig, c, config, quality
from tests import tm


class TestsFlextQualityBasic:
    """Public contract of the flext-quality package facade and constants."""

    @staticmethod
    def test_facade_constructs_without_arguments() -> None:
        """FlextQuality() is constructible with no arguments and executes."""
        tm.that(FlextQuality().execute().success, eq=True)

    @staticmethod
    def test_global_alias_is_facade_instance() -> None:
        """The module-level ``quality`` alias is a FlextQuality facade."""
        tm.that(quality, is_=FlextQuality)

    @staticmethod
    def test_execute_reports_success() -> None:
        """execute() yields a successful result carrying the status snapshot."""
        result = FlextQuality().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    @staticmethod
    @pytest.mark.parametrize("key", ["name", "version", "settings", "hooks_registered"])
    def test_execute_status_exposes_public_keys(key: str) -> None:
        """The status snapshot from execute() carries every documented key."""
        tm.that(FlextQuality().execute().value, has=key)

    @staticmethod
    def test_execute_reports_canonical_identity() -> None:
        """execute() surfaces the canonical server name and version constants."""
        status = FlextQuality().execute().value
        tm.that(status["name"], eq=c.Quality.MCP_SERVER_NAME)
        tm.that(status["version"], eq=c.Quality.MCP_SERVER_VERSION)

    @staticmethod
    def test_execute_is_idempotent_in_shape() -> None:
        """Repeated execute() calls return the same observable identity."""
        facade = FlextQuality()
        first = facade.execute().value
        second = facade.execute().value
        tm.that(first["name"], eq=second["name"])
        tm.that(first["version"], eq=second["version"])

    @staticmethod
    def test_hooks_registered_count_is_non_negative() -> None:
        """The reported hook-registration count is a valid non-negative total."""
        count = FlextQuality().execute().value["hooks_registered"]
        tm.that(count, is_=int)
        tm.that(isinstance(count, int) and count >= 0, eq=True)

    @staticmethod
    def test_config_singleton_is_a_frozen_quality_config() -> None:
        """The module-level ``config`` singleton is a frozen ``FlextQualityConfig``."""
        tm.that(config, is_=FlextQualityConfig)
        tm.that(config.model_config.get("frozen"), eq=True)

    @staticmethod
    def test_config_quality_namespace_allows_open_extra_fields() -> None:
        """``config.Quality`` is an open namespace exposing config/*.yaml data."""
        tm.that(config.Quality, is_=object)
        tm.that(type(config.Quality).model_config.get("extra"), eq="allow")
