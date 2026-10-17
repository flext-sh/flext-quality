"""Type definitions for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebTypes

from flext_quality._typings.quality import FlextQualityTypingsQuality


class FlextQualityTypes(FlextWebTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace (project slot)."""

        RuleResult = FlextQualityTypingsQuality.RuleResult
        GenericItem = FlextQualityTypingsQuality.GenericItem
        DocumentationReportValue = FlextQualityTypingsQuality.DocumentationReportValue


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
