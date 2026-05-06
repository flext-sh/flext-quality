"""Protocols for flext-quality."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Protocol, runtime_checkable

from flext_infra import p
from flext_web import p as web_p

from flext_quality import c, t


class FlextQualityProtocols(p, web_p):
    """Namespace for flext-quality protocols."""

    @runtime_checkable
    class Quality(Protocol):
        """Quality-specific protocols namespace."""

        @runtime_checkable
        class ArgumentOptionSpec(Protocol):
            """Structural contract for quality argparse option specs."""

            flags: t.StrSequence
            help: str
            action: c.Quality.ArgumentAction | None
            default: t.JsonValue | None
            value_type: c.Quality.ArgumentValueType | None
            nargs: int | str | None
            choices: t.StrSequence | None
            dest: str | None

        @runtime_checkable
        class ArgumentParserSpec(Protocol):
            """Structural contract for quality argparse parser specs."""

            description: str
            options: t.SequenceOf[FlextQualityProtocols.Quality.ArgumentOptionSpec]

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
            ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
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
                context: t.JsonMapping,
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
                params: t.JsonMapping,
            ) -> p.Result[t.JsonMapping]:
                """Execute MCP tool."""
                ...


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
