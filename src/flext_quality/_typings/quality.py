"""Quality domain type aliases for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping

from flext_cli import t


class FlextQualityTypingsQuality:
    """Quality domain type aliases composed into ``t.Quality``."""

    type RuleResult = tuple[bool, str | None]
    type GenericItem = t.JsonValue | Mapping[str, t.Primitives | None]
    type DocumentationReportValue = t.JsonMapping


__all__: list[str] = ["FlextQualityTypingsQuality"]
