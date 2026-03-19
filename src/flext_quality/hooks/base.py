"""Base hook implementation."""

from __future__ import annotations

import fnmatch
from typing import ClassVar, Protocol, runtime_checkable

from flext_quality import c, r, t


@runtime_checkable
class BaseHookImpl(Protocol):
    """Abstract base for hook implementations."""

    event: ClassVar[c.Quality.HookEvent]
    matcher: ClassVar[list[str] | None]

    def execute(self, input_data: t.Quality.HookInput) -> r[t.Quality.HookOutput]:
        """Execute the hook logic."""
        ...

    def should_run(self, input_data: t.Quality.HookInput) -> bool:
        """Check if hook should run for this input."""
        if self.matcher is None:
            return True
        tool_name = str(input_data.get("tool_name", ""))
        return any(self._match_pattern(pattern, tool_name) for pattern in self.matcher)

    def _match_pattern(self, pattern: str, value: str) -> bool:
        """Match pattern against value (supports wildcards)."""
        return fnmatch.fnmatch(value, pattern)
