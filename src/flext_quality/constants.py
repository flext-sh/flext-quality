"""FLEXT Quality Constants.

Centralized, immutable constants for the flext-quality project providing
hook events, rule types, validation thresholds, and runtime enumerations.
Every fixed compiled ``re.Pattern`` for the Quality domain is declared on
the ``FlextQualityConstantsValues`` SSOT and inherited through this
namespace; runtime-supplied regex construction lives in ``u.Quality``
instead of this constants surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

from flext_web import FlextWebConstants

from ._constants.values import FlextQualityConstantsValues

if TYPE_CHECKING:
    from flext_quality import t


class FlextQualityConstants(FlextWebConstants):
    """Centralized constants for flext-quality (Layer 0).

    Provides immutable, namespace-organized constants for hook processing,
    rule engines, validation, and quality enforcement.

    Usage:
        from flext_core import c

        event = c.Quality.HookEvent.PRE_TOOL_USE
        threshold = c.Quality.THRESHOLD_DEFAULT_LINES
    """

    class Quality(FlextQualityConstantsValues.Quality):
        """Quality-specific constants namespace."""

        class LinkCheckerDemo(FlextQualityConstantsValues.LinkCheckerDemo):
            """Demo link fixtures for the documentation link checker."""

        @unique
        class HookEvent(StrEnum):
            """Claude Code hook events."""

            PRE_TOOL_USE = "PreToolUse"
            STOP = "Stop"

        @unique
        class RuleType(StrEnum):
            """Rule types for validation."""

            BLOCKING = "blocking"
            WARNING = "warning"
            INFO = "info"

        @unique
        class Severity(StrEnum):
            """Rule severity levels."""

            ERROR = "error"
            WARNING = "warning"
            INFO = "info"

        @unique
        class RuleResult(StrEnum):
            """Rule evaluation results."""

            PASS = auto()
            FAIL = "fail"
            SKIP = "skip"

        @unique
        class IntegrationStatus(StrEnum):
            """External integration status."""

            CONNECTED = "connected"
            DISCONNECTED = "disconnected"
            ERROR = "error"

        @unique
        class NotificationPriority(StrEnum):
            """Notification priority levels for quality alerts."""

            CRITICAL = "critical"
            WARNING = "warning"
            INFO = "info"

        @unique
        class ArgumentAction(StrEnum):
            """Supported argparse actions for quality tooling."""

            STORE_TRUE = "store_true"
            STORE_FALSE = "store_false"

        @unique
        class ArgumentValueType(StrEnum):
            """Supported argparse value coercions for quality tooling."""

            STRING = "str"
            INTEGER = "int"


c = FlextQualityConstants
__all__: t.StrSequence = ("FlextQualityConstants", "c")
