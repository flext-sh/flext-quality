"""Quality domain enumerations for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, auto, unique


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


__all__: list[str] = [
    "ArgumentAction",
    "ArgumentValueType",
    "HookEvent",
    "IntegrationStatus",
    "NotificationPriority",
    "RuleResult",
    "RuleType",
    "Severity",
]
