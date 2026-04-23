"""Rule validators for specific validation types."""

from __future__ import annotations

import re
from collections.abc import (
    MutableMapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import override

from flext_quality import c, p, r, t


class FlextQualityValidators:
    """Namespace for flext-quality validators (one class per module pattern)."""

    Base = p.Quality.ValidatorBase

    class Pattern(p.Quality.ValidatorBase):
        """Validates content against regex patterns."""

        def __init__(self, patterns: t.StrMapping) -> None:
            """Initialize with patterns."""
            self._patterns = patterns
            self._compiled: MutableMapping[str, re.Pattern[str]] = {}
            for pname, pattern in patterns.items():
                self._compiled[pname] = re.compile(pattern)

        @property
        @override
        def name(self) -> str:
            """Return validator name."""
            return "pattern"

        @override
        def validate(
            self,
            content: str,
            file_path: Path | None = None,
        ) -> p.Result[Sequence[t.JsonMapping]]:
            """Validate content against patterns."""
            violations: MutableSequence[t.JsonMapping] = []
            filename = str(file_path) if file_path else "<string>"
            lines = content.splitlines()
            for line_num, line in enumerate(lines, start=1):
                for pattern_name, compiled in self._compiled.items():
                    if compiled.search(line):
                        violations.append({
                            "rule": f"pattern-{pattern_name}",
                            "file": filename,
                            "line": line_num,
                            "message": f"Pattern violation: {pattern_name}",
                            "severity": c.Quality.Severity.ERROR,
                        })
            return r[Sequence[t.JsonMapping]].ok(violations)

    class ForbiddenPattern(Pattern):
        """Validates against FLEXT forbidden patterns."""

        def __init__(self) -> None:
            """Initialize with FLEXT forbidden patterns."""
            patterns = {
                "type-ignore": c.Quality.Patterns.TYPE_IGNORE,
                "cast-usage": c.Quality.Patterns.CAST_USAGE,
                "any-type": c.Quality.Patterns.ANY_TYPE,
                "type-checking": c.Quality.Patterns.TYPE_CHECKING,
                "optional-pattern": c.Quality.Patterns.OPTIONAL_PATTERN,
                "union-pattern": c.Quality.Patterns.UNION_PATTERN,
            }
            super().__init__(patterns)

        @property
        @override
        def name(self) -> str:
            """Return validator name."""
            return "forbidden-patterns"

    class Tier(p.Quality.ValidatorBase):
        """Validates architecture tier violations."""

        @property
        @override
        def name(self) -> str:
            """Return validator name."""
            return "tier"

        @override
        def validate(
            self,
            content: str,
            file_path: Path | None = None,
        ) -> p.Result[Sequence[t.JsonMapping]]:
            """Validate tier violations."""
            violations: MutableSequence[t.JsonMapping] = []
            filename = str(file_path) if file_path else "<string>"
            if file_path is None:
                return r[Sequence[t.JsonMapping]].ok(violations)
            file_tier = self._get_file_tier(file_path)
            if file_tier is None:
                return r[Sequence[t.JsonMapping]].ok(violations)
            tier_pattern = re.compile(c.Quality.Patterns.TIER_VIOLATION)
            lines = content.splitlines()
            for line_num, line in enumerate(lines, start=1):
                if tier_pattern.search(line):
                    violations.append({
                        "rule": "tier-violation",
                        "file": filename,
                        "line": line_num,
                        "message": "Tier 0/1 modules cannot import from services/api",
                        "severity": c.Quality.Severity.ERROR,
                    })
            return r[Sequence[t.JsonMapping]].ok(violations)

        def _get_file_tier(self, path: Path) -> int | None:
            """Determine file tier from path."""
            name = path.name
            if name in {"constants.py", "typings.py", "protocols.py"}:
                return 0
            if name in {"models.py", "utilities.py"}:
                return 1
            if "servers" in path.parts:
                return 2
            if "services" in path.parts or name == "api.py":
                return 3
            return None

    class Registry:
        """Registry of available validators."""

        def __init__(self) -> None:
            """Initialize with default validators."""
            self._validators: MutableMapping[str, p.Quality.ValidatorBase] = {}
            self._register_defaults()

        def all(self) -> Sequence[p.Quality.ValidatorBase]:
            """Get all registered validators."""
            return list(self._validators.values())

        def get(self, name: str) -> p.Quality.ValidatorBase | None:
            """Get validator by name."""
            return self._validators.get(name)

        def register(self, validator: p.Quality.ValidatorBase) -> None:
            """Register a validator."""
            self._validators[validator.name] = validator

        def validate_all(
            self,
            content: str,
            file_path: Path | None = None,
        ) -> p.Result[Sequence[t.JsonMapping]]:
            """Run all validators."""
            all_violations: MutableSequence[t.JsonMapping] = []
            for validator in self._validators.values():
                result = validator.validate(content, file_path)
                if result.success:
                    all_violations.extend(result.value)
            return r[Sequence[t.JsonMapping]].ok(all_violations)

        def _register_defaults(self) -> None:
            """Register default validators."""
            self.register(FlextQualityValidators.ForbiddenPattern())
            self.register(FlextQualityValidators.Tier())
