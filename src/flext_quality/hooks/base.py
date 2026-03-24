"""Base hook implementation."""

from __future__ import annotations

import fnmatch
from typing import ClassVar

from flext_core import r

from flext_quality import c, t


class FlextQualityBaseHook:
    """Concrete base for hook implementations satisfying p.Quality.HookImpl."""

    event: ClassVar[c.Quality.HookEvent]
    matcher: ClassVar[t.StrSequence | None] = None

    def execute(self, input_data: t.Quality.HookInput) -> r[t.Quality.HookOutput]:
        """Execute the hook logic."""
        raise NotImplementedError

    def should_run(self, input_data: t.Quality.HookInput) -> bool:
        """Check if hook should run for this input."""
        if self.matcher is None:
            return True
        tool_name = str(input_data.get("tool_name", ""))
        return any(self._match_pattern(pattern, tool_name) for pattern in self.matcher)

    def _match_pattern(self, pattern: str, value: str) -> bool:
        """Match pattern against value (supports wildcards)."""
        return fnmatch.fnmatch(value, pattern)
