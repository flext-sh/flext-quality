# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import p

from flext_quality._protocols import FlextQualityProtocolsQuality


class FlextQualityProtocols(p):
    """Namespace for flext-quality protocols."""

    class Quality(FlextQualityProtocolsQuality):
        """Quality-specific protocols namespace."""


p = FlextQualityProtocols
__all__: list[str] = ["FlextQualityProtocols", "p"]
