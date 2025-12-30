"""Domain models for flext-quality plugin system.

Consolidated FlextQualityPlugin class containing all plugin-related enums and dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class FlextQualityPlugin:
    """Domain models for flext-quality plugin system.

    Consolidates all plugin-related enums and dataclasses under a single namespace.
    This follows strict FLEXT naming conventions with FlextQuality prefix.
    """

    class Category(StrEnum):
        """Plugin capability categories."""

        LINT = "lint"
        TYPE_CHECK = "type_check"
        SECURITY = "security"
        QUALITY = "quality"
        LANGUAGE = "language"
        RULES = "rules"

    @dataclass(frozen=True, slots=True)
    class Metadata:
        """Metadata describing a plugin's capabilities and dependencies."""

        name: str
        plugin_class: type
        categories: frozenset[Category]
        priority: int = 50
        depends_on: tuple[str, ...] = field(default_factory=tuple)
        parallel_safe: bool = True
        languages: frozenset[str] | None = None

        def applies_to_language(self, language: str) -> bool:
            """Check if plugin applies to specific language."""
            if self.languages is None:
                return True
            return language in self.languages

    @dataclass(frozen=True, slots=True)
    class Violation:
        """Single rule/plugin violation."""

        code: str
        name: str
        severity: str
        blocking: bool
        guidance: str
        category: str
        source_plugin: str
        line: int | None = None
        column: int | None = None

        def to_dict(self) -> dict[str, Any]:
            """Convert to JSON-compatible dict."""
            return {
                "code": self.code,
                "name": self.name,
                "severity": self.severity,
                "blocking": self.blocking,
                "guidance": self.guidance,
                "category": self.category,
                "source_plugin": self.source_plugin,
                "line": self.line,
                "column": self.column,
            }

    @dataclass(frozen=True, slots=True)
    class ValidationResult:
        """Aggregated validation result from all plugins."""

        status: str
        file_path: str
        language: str
        violations: tuple[Violation, ...]
        warnings: tuple[Violation, ...]
        suggestions: tuple[Violation, ...]
        total_violations: int
        total_warnings: int
        has_blocking: bool
        plugin_results: dict[str, Any]

        def to_dict(self) -> dict[str, Any]:
            """Convert to JSON-compatible dict (bash hooks)."""
            return {
                "status": self.status,
                "file": self.file_path,
                "language": self.language,
                "violations": [v.to_dict() for v in self.violations],
                "warnings": [w.to_dict() for w in self.warnings],
                "suggestions": [s.to_dict() for s in self.suggestions],
                "total_violations": self.total_violations,
                "total_warnings": self.total_warnings,
                "has_blocking": self.has_blocking,
            }
