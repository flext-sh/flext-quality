"""Type definitions for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebTypes, t as web_t


class FlextQualityTypes(FlextWebTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace (project slot)."""

        type RuleResult = tuple[bool, str | None]
        type GenericItem = (
            web_t.JsonValue | web_t.MappingKV[str, web_t.Primitives | None]
        )
        type DocumentationReportValue = web_t.JsonMapping


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
