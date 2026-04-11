"""Protocols for flext-quality."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Protocol, runtime_checkable

from flext_cli import p
from flext_web import FlextWebProtocols

from flext_core import r

from .typings import t


class FlextQualityProtocols(FlextWebProtocols, p):
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
            ) -> r[Sequence[t.ContainerMapping]]:
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
            ) -> r[t.Quality.HookOutput]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.Quality.HookInput) -> bool:
                """Check if hook should run for this input."""
                ...

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

        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: t.StrSequence | None

            def execute(
                self,
                input_data: t.Quality.HookInput,
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
                self,
                settings: t.Quality.RuleConfig,
                context: t.ContainerMapping,
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

            def health_check(self) -> r[t.StrMapping]:
                """Check integration health."""
                ...

        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(
                self,
                params: t.ContainerMapping,
            ) -> r[t.ContainerMapping]:
                """Execute MCP tool."""
                ...


p = FlextQualityProtocols
__all__ = ["FlextQualityProtocols", "p"]
