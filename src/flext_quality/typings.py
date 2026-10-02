"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping

from flext_web import FlextWebTypes, m, t


class FlextQualityTypes(FlextWebTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace (project slot)."""

        type RuleResult = tuple[bool, str | None]
        type GenericItem = t.JsonValue | t.MappingKV[str, t.Primitives | None]
        type DocumentationReportValue = (
            str
            | int
            | float
            | bool
            | t.StrSequence
            | t.SequenceOf[Mapping[str, t.Primitives]]
            | t.MappingKV[str, t.Primitives]
            | None
        )


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
