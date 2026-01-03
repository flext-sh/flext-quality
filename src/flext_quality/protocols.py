"""Protocols for flext-quality."""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextProtocols, FlextResult as r

from .typings import FlextQualityTypes as t


class FlextQualityProtocols(FlextProtocols):
    """Namespace for flext-quality protocols."""

    class Quality:
        """Quality-specific protocols namespace."""

        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: list[str] | None

            def execute(
                self, input_data: t.Quality.HookInput
            ) -> r[t.Quality.HookOutput]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.Quality.HookInput) -> bool:
                """Check if hook should run for this input."""
                ...

        class RuleValidator(Protocol):
            """Protocol for rule validators."""

            rule_type: str

            def validate(
                self, config: t.Quality.RuleConfig, context: dict[str, object]
            ) -> r[t.Quality.RuleResult]:
                """Validate according to rule."""
                ...

        class IntegrationClient(Protocol):
            """Protocol for external integrations."""

            def connect(self) -> r[bool]:
                """Connect to external service."""
                ...

            def disconnect(self) -> r[bool]:
                """Disconnect from external service."""
                ...

            def health_check(self) -> r[dict[str, str]]:
                """Check integration health."""
                ...

        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(self, params: dict[str, object]) -> r[dict[str, object]]:
                """Execute MCP tool."""
                ...


# Short alias for imports
p = FlextQualityProtocols
