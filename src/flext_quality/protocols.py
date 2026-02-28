"""Protocols for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from flext_cli import FlextCliProtocols
from flext_core import FlextResult
from flext_web import FlextWebProtocols

from .typings import t


class FlextQualityProtocols(FlextWebProtocols, FlextCliProtocols):
    """Namespace for flext-quality protocols."""

    class Quality:
        """Quality-specific protocols namespace."""

        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: list[str] | None

            def execute(
                self, input_data: t.Quality.HookInput
            ) -> FlextResult[t.Quality.HookOutput]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.Quality.HookInput) -> bool:
                """Check if hook should run for this input."""
                ...

        class RuleValidator(Protocol):
            """Protocol for rule validators."""

            rule_type: str

            def validate(
                self,
                config: t.Quality.RuleConfig,
                context: Mapping[str, object],
            ) -> FlextResult[t.Quality.RuleResult]:
                """Validate according to rule."""
                ...

        class IntegrationClient(Protocol):
            """Protocol for external integrations."""

            def connect(self) -> FlextResult[bool]:
                """Connect to external service."""
                ...

            def disconnect(self) -> FlextResult[bool]:
                """Disconnect from external service."""
                ...

            def health_check(self) -> FlextResult[Mapping[str, str]]:
                """Check integration health."""
                ...

        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(
                self,
                params: Mapping[str, object],
            ) -> FlextResult[Mapping[str, object]]:
                """Execute MCP tool."""
                ...


# Short alias for imports
p = FlextQualityProtocols

__all__ = [
    "FlextQualityProtocols",
    "p",
]
