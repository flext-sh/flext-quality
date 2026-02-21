"""Base hook implementation."""

from __future__ import annotations

import fnmatch
from abc import ABC, abstractmethod
from typing import ClassVar

from flext_core import r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.typings import HookInput, HookOutput


class BaseHookImpl(ABC):
    """Abstract base for hook implementations."""

    event: ClassVar[c.Quality.HookEvent]
    matcher: ClassVar[list[str] | None]

    def should_run(self, input_data: HookInput) -> bool:
        """Check if hook should run for this input."""
        if self.matcher is None:
            return True
        tool_name = str(input_data.get("tool_name", ""))
        return any(self._match_pattern(pattern, tool_name) for pattern in self.matcher)

    def _match_pattern(self, pattern: str, value: str) -> bool:
        """Match pattern against value (supports wildcards)."""
        return fnmatch.fnmatch(value, pattern)

    @abstractmethod
    def execute(self, input_data: HookInput) -> r[HookOutput]:
        """Execute the hook logic."""
        ...
