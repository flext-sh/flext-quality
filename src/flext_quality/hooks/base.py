"""Base hook implementation.

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

import fnmatch
from collections.abc import Sequence
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from flext_quality import c, p, t


class FlextQualityBaseHook:
    """Concrete base for hook implementations satisfying p.Quality.HookImpl."""

    event: ClassVar[c.Quality.HookEvent]
    matcher: ClassVar[Sequence[str] | None] = None

    def execute(self, _input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        """Execute the hook logic.

        Args:
            input_data: Hook input payload carrying the tool event data.

        """
        raise NotImplementedError

    def should_run(self, input_data: t.JsonMapping) -> bool:
        """Check if the hook should run for this input.

        Args:
            input_data: Hook input payload whose ``tool_name`` is matched
                against the hook's matcher patterns.

        Returns:
            ``True`` when the hook applies to the input.

        """
        if self.matcher is None:
            return True
        tool_name = str(input_data.get("tool_name", ""))
        return any(self._match_pattern(pattern, tool_name) for pattern in self.matcher)

    @staticmethod
    def _match_pattern(pattern: str, value: str) -> bool:
        """Match pattern against value (supports wildcards).

        Args:
            pattern: Glob pattern supporting ``*`` wildcards.
            value: Value matched against the pattern.

        Returns:
            ``True`` when the value matches the pattern.

        """
        return fnmatch.fnmatch(value, pattern)


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityBaseHook"]
