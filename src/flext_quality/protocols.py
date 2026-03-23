"""Protocols for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols
from flext_core import r
from flext_web import FlextWebProtocols

from .typings import t


class FlextQualityProtocols(FlextWebProtocols, FlextCliProtocols):
    """Namespace for flext-quality protocols."""

    class Quality:
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
            ) -> r[list[Mapping[str, t.NormalizedValue]]]:
                """Validate content and return violations."""
                ...

        @runtime_checkable
        class HookImpl(Protocol):
            """Abstract base protocol for hook implementations."""

            event: ClassVar[type]
            matcher: ClassVar[list[str] | None]

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
            matcher: list[str] | None

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
                config: t.Quality.RuleConfig,
                context: Mapping[str, t.NormalizedValue],
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

            def health_check(self) -> r[Mapping[str, str]]:
                """Check integration health."""
                ...

        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(
                self,
                params: Mapping[str, t.NormalizedValue],
            ) -> r[Mapping[str, t.NormalizedValue]]:
                """Execute MCP tool."""
                ...


p = FlextQualityProtocols
__all__ = ["FlextQualityProtocols", "p"]
