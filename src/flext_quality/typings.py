"""Type definitions for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_web import FlextWebTypes, t as web_t


class FlextQualityTypes(FlextWebTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace (project slot)."""

        type RuleResult = tuple[bool, str | None]
        type GenericItem = (
            web_t.JsonValue | web_t.MappingKV[str, web_t.Primitives | None]
        )
        type DocumentationReportValue = (
            str
            | int
            | float
            | bool
            | web_t.StrSequence
            | web_t.SequenceOf[Mapping[str, web_t.Primitives]]
            | web_t.MappingKV[str, web_t.Primitives]
            | None
        )


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
