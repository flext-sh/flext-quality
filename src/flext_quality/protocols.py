# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebProtocols

from flext_quality._protocols import (
    FlextQualityProtocolsBase,
    FlextQualityProtocolsFlextqualitymodelsPart01,
    FlextQualityProtocolsFlextqualitymodelsPart02,
    FlextQualityProtocolsQuality,
)


class FlextQualityProtocols(
    FlextWebProtocols,
    FlextQualityProtocolsBase,
    FlextQualityProtocolsFlextqualitymodelsPart01,
    FlextQualityProtocolsFlextqualitymodelsPart02,
    FlextQualityProtocolsQuality,
):
    """Namespace for flext-quality protocols."""

    class Quality(
        FlextQualityProtocolsBase,
        FlextQualityProtocolsFlextqualitymodelsPart01,
        FlextQualityProtocolsFlextqualitymodelsPart02,
        FlextQualityProtocolsQuality,
    ):
        """Quality-specific protocols namespace."""


p = FlextQualityProtocols
__all__: list[str] = ["FlextQualityProtocols", "p"]
