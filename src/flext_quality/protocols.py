"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol, runtime_checkable

from flext_web import FlextWebProtocols

if TYPE_CHECKING:
    from flext_quality import c, t


class FlextQualityProtocols(FlextWebProtocols):
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
                """The validator name."""
                ...

            def validate(
                self,
                content: str,
                file_path: t.Cli.TextPath | None = None,
            ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
                """Validate content and return violations.

                Args:
                    content: Text content checked by the validator.
                    file_path: Optional source path recorded in violations.

                """
                ...

        @runtime_checkable
        class HookImpl(Protocol):
            """Abstract base protocol for hook implementations."""

            event: ClassVar[type]
            matcher: ClassVar[t.StrSequence | None]

            def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute the hook logic.

                Args:
                    input_data: Hook input payload carrying the event data.

                """
                ...

            def should_run(self, input_data: t.JsonMapping) -> bool:
                """Check if the hook should run for this input.

                Args:
                    input_data: Hook input payload evaluated by the hook.

                """
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
                """Return a configuration value.

                Args:
                    key: Configuration key to look up.
                    default: Value returned when the key is absent.

                """
                ...

            def __getitem__(self, key: str) -> None:
                """Return a configuration value with bracket notation.

                Args:
                    key: Configuration key to look up.

                """
                ...

        @runtime_checkable
        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: t.StrSequence | None

            def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute the hook logic.

                Args:
                    input_data: Hook input payload carrying the event data.

                """
                ...

            def should_run(self, input_data: t.JsonMapping) -> bool:
                """Check if the hook should run for this input.

                Args:
                    input_data: Hook input payload evaluated by the hook.

                """
                ...

        @runtime_checkable
        class RuleValidator(Protocol):
            """Protocol for rule validators."""

            rule_type: str

            def validate(
                self,
                settings: t.JsonMapping,
                context: t.JsonMapping,
            ) -> p.Result[t.Quality.RuleResult]:
                """Validate according to the rule type.

                Args:
                    settings: Rule settings configuring the validation.
                    context: Validation context for the rule.

                """
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

            def execute(self, params: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute the MCP tool.

                Args:
                    params: Parameters passed to the tool.

                """
                ...


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
