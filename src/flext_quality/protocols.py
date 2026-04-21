"""Protocols for flext-quality."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path
from typing import ClassVar, Protocol, runtime_checkable

from flext_web import p

from flext_quality import t


class FlextQualityProtocols(p):
    """Namespace for flext-quality protocols."""

    @runtime_checkable
    class Quality(Protocol):
        """Quality-specific protocols namespace."""

        @runtime_checkable
        class ValidatorBase(Protocol):
            """Abstract base protocol for rule validators."""

            @property
            def name(self) -> str:
                """Return validator name."""
                ...

            def validate(
                self,
                content: str,
                file_path: Path | None = None,
            ) -> p.Result[Sequence[Mapping[str, t.Container]]]:
                """Validate content and return violations."""
                ...

        @runtime_checkable
        class HookImpl(Protocol):
            """Abstract base protocol for hook implementations."""

            event: ClassVar[type]
            matcher: ClassVar[t.StrSequence | None]

            def execute(
                self,
                input_data: t.Quality.HookInput,
            ) -> p.Result[t.Quality.HookOutput]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.Quality.HookInput) -> bool:
                """Check if hook should run for this input."""
                ...

        @runtime_checkable
        class DocsConfig(Protocol):
            """Protocol for documentation configuration objects."""

            def get(
                self,
                key: str,
                *,
                default: str | float | bool | None = None,
            ) -> t.Primitives | None:
                """Get a configuration value."""
                ...

            def __getitem__(self, key: str) -> None:
                """Get a configuration value with bracket notation."""
                ...

        @runtime_checkable
        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: t.StrSequence | None

            def execute(
                self,
                input_data: t.Quality.HookInput,
            ) -> p.Result[t.Quality.HookOutput]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.Quality.HookInput) -> bool:
                """Check if hook should run for this input."""
                ...

        @runtime_checkable
        class RuleValidator(Protocol):
            """Protocol for rule validators."""

            rule_type: str

            def validate(
                self,
                settings: t.Quality.RuleConfig,
                context: Mapping[str, t.Container],
            ) -> p.Result[t.Quality.RuleResult]:
                """Validate according to rule."""
                ...

        @runtime_checkable
        class IntegrationClient(Protocol):
            """Protocol for external integrations."""

            def connect(self) -> p.Result[bool]:
                """Connect to external service."""
                ...

            def disconnect(self) -> p.Result[bool]:
                """Disconnect from external service."""
                ...

            def health_check(self) -> p.Result[t.StrMapping]:
                """Check integration health."""
                ...

        @runtime_checkable
        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(
                self,
                params: Mapping[str, t.Container],
            ) -> p.Result[Mapping[str, t.Container]]:
                """Execute MCP tool."""
                ...


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
