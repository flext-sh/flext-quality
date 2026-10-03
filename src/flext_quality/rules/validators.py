"""Rule validators for specific validation types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, override

from flext_quality import c, p, r, t, u

if TYPE_CHECKING:
    from collections.abc import MutableMapping, MutableSequence


class FlextQualityValidators:
    """Namespace for flext-quality validators (one class per module pattern)."""

    Base = p.Quality.ValidatorBase

    class Pattern(p.Quality.ValidatorBase):
        """Validates content against regex patterns."""

        def __init__(self, patterns: t.StrMapping) -> None:
            """Initialize with patterns."""
            self._patterns = patterns
            self._compiled: MutableMapping[str, t.RegexPattern] = {
                pname: u.Quality.compile_pattern(pattern)
                for pname, pattern in patterns.items()
            }

        @property
        @override
        def name(self) -> str:
            """The validator name."""
            return "pattern"

        @override
        def validate(
            self, content: str, file_path: t.Cli.TextPath | None = None,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Validate content against patterns.

            Returns:
                The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
            """
            path_value = Path(file_path) if isinstance(file_path, str) else file_path
            violations: MutableSequence[t.JsonMapping] = []
            filename = str(path_value) if path_value else "<string>"
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
            return r[t.SequenceOf[t.JsonMapping]].ok(violations)

    class ForbiddenPattern(Pattern):
        """Validates against FLEXT forbidden patterns."""

        def __init__(self) -> None:
            """Initialize with FLEXT forbidden patterns."""
            patterns = {
                "type-ignore": c.Quality.PATTERNS_TYPE_IGNORE,
                "cast-usage": c.Quality.PATTERNS_CAST_USAGE,
                "any-type": c.Quality.PATTERNS_ANY_TYPE,
                "type-checking": c.Quality.PATTERNS_TYPE_CHECKING,
                "optional-pattern": c.Quality.PATTERNS_OPTIONAL_PATTERN,
                "union-pattern": c.Quality.PATTERNS_UNION_PATTERN,
            }
            super().__init__(patterns)

        @property
        @override
        def name(self) -> str:
            """The validator name."""
            return "forbidden-patterns"

    class Tier(p.Quality.ValidatorBase):
        """Validates architecture tier violations."""

        @property
        @override
        def name(self) -> str:
            """The validator name."""
            return "tier"

        @override
        def validate(
            self, content: str, file_path: t.Cli.TextPath | None = None,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Validate tier violations.

            Returns:
                The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
            """
            path_value = Path(file_path) if isinstance(file_path, str) else file_path
            violations: MutableSequence[t.JsonMapping] = []
            filename = str(path_value) if path_value else "<string>"
            if path_value is None:
                return r[t.SequenceOf[t.JsonMapping]].ok(violations)
            file_tier = self._get_file_tier(path_value)
            if file_tier is None:
                return r[t.SequenceOf[t.JsonMapping]].ok(violations)
            lines = content.splitlines()
            for line_num, line in enumerate(lines, start=1):
                if c.Quality.PATTERNS_TIER_VIOLATION_RE.search(line):
                    violations.append({
                        "rule": "tier-violation",
                        "file": filename,
                        "line": line_num,
                        "message": "Tier 0/1 modules cannot import from services/api",
                        "severity": c.Quality.Severity.ERROR,
                    })
            return r[t.SequenceOf[t.JsonMapping]].ok(violations)

        @staticmethod
        def _get_file_tier(path: Path) -> int | None:
            """Determine file tier from path.

            Returns:
                The resulting ``int | None``.
            """
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

        def all(self) -> t.SequenceOf[p.Quality.ValidatorBase]:
            """Get all registered validators.

            Returns:
                The resulting ``t.SequenceOf[p.Quality.ValidatorBase]``.
            """
            return list(self._validators.values())

        def get(self, name: str) -> p.Quality.ValidatorBase | None:
            """Get validator by name.

            Returns:
                The resulting ``p.Quality.ValidatorBase | None``.
            """
            return self._validators.get(name)

        def register(self, validator: p.Quality.ValidatorBase) -> None:
            """Register a validator."""
            self._validators[validator.name] = validator

        def validate_all(
            self, content: str, file_path: Path | None = None,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Run all validators.

            Returns:
                The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
            """
            all_violations: MutableSequence[t.JsonMapping] = []
            for validator in self._validators.values():
                result = validator.validate(content, file_path)
                if result.success:
                    all_violations.extend(result.value)
            return r[t.SequenceOf[t.JsonMapping]].ok(all_violations)

        def _register_defaults(self) -> None:
            """Register default validators."""
            self.register(FlextQualityValidators.ForbiddenPattern())
            self.register(FlextQualityValidators.Tier())


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityValidators"]
