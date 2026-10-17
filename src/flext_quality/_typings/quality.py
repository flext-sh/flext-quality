"""Quality domain type aliases for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import t as web_t


class FlextQualityTypingsQuality:
    """Quality domain type aliases composed into ``t.Quality``."""

    type RuleResult = tuple[bool, str | None]
    type GenericItem = web_t.JsonValue | web_t.MappingKV[str, web_t.Primitives | None]
    type DocumentationReportValue = web_t.JsonMapping


__all__: list[str] = ["FlextQualityTypingsQuality"]
