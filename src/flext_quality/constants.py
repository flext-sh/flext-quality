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

from typing import TYPE_CHECKING

from flext_web import FlextWebConstants

from flext_quality._constants import FlextQualityConstantsValues
from flext_quality._constants.enums import FlextQualityConstantsEnums

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

    class Quality(
        FlextQualityConstantsEnums,
        FlextQualityConstantsValues.Quality,
        FlextQualityConstantsValues,
    ):
        """Quality-specific constants namespace."""

        class LinkCheckerDemo(FlextQualityConstantsValues.LinkCheckerDemo):
            """Demo link fixtures for the documentation link checker."""


c = FlextQualityConstants
__all__: t.StrSequence = ("FlextQualityConstants", "c")
