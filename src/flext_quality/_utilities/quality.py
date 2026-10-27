"""Quality domain utilities for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import TYPE_CHECKING, ClassVar

from flext_cli import cli, u
from flext_web import FlextWebUtilities

from flext_quality import c, m, r, t

if TYPE_CHECKING:
    from pathlib import Path

    from flext_quality import FlextQualityServiceBase, p


class FlextQualityUtilitiesQuality:
    """Quality domain utility behavior composed into ``u.Quality``."""

    # Resolved generics, not bare PEP 695 aliases: the adapter form must be
    # a checker-visible type expression (bare aliases evaluate to
    # TypeAliasType objects, which the adapter form rejects). Concrete
    # generics only; runtime objects identical to the unwrapped aliases.
    RELAXED_CONTAINER_MAPPING_ADAPTER: ClassVar[
        t.TypeAdapter[Mapping[str, t.JsonValue]]
    ] = FlextWebUtilities.type_adapter(
        Mapping[str, t.JsonValue],
        config=m.ConfigDict(strict=False),
    )
    RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER: ClassVar[
        t.TypeAdapter[Sequence[Mapping[str, t.JsonValue]]]
    ] = FlextWebUtilities.type_adapter(
        Sequence[Mapping[str, t.JsonValue]],
        config=m.ConfigDict(strict=False),
    )
    MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER: ClassVar[
        t.TypeAdapter[MutableMapping[str, str | bool | None]]
    ] = FlextWebUtilities.type_adapter(MutableMapping[str, str | bool | None])
    STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER: ClassVar[
        t.TypeAdapter[MutableSequence[Mapping[str, str]]]
    ] = FlextWebUtilities.type_adapter(MutableSequence[Mapping[str, str]])
    REPORT_VALUE_MAPPING_ADAPTER: ClassVar[
        t.TypeAdapter[t.MappingKV[str, t.JsonMapping]]
    ] = FlextWebUtilities.type_adapter(
        Mapping[str, Mapping[str, t.JsonValue]],
    )

    @staticmethod
    def compile_pattern(
        pattern: str,
        *,
        ignorecase: bool = False,
        multiline: bool = False,
        dotall: bool = False,
    ) -> t.RegexPattern:
        """Compile a runtime-supplied regex pattern for quality tooling.

        Args:
            pattern: Regular expression source to compile.
            ignorecase: Enable case-insensitive matching.
            multiline: Enable multi-line mode (``^``/``$`` match per line).
            dotall: Enable dot-all mode (``.`` matches newlines).

        Returns:
            The resulting ``t.RegexPattern``.

        """
        flags = re.NOFLAG
        for enabled, flag in (
            (ignorecase, re.IGNORECASE),
            (multiline, re.MULTILINE),
            (dotall, re.DOTALL),
        ):
            if enabled:
                flags |= flag
        return re.compile(pattern, flags=flags)

    @staticmethod
    def escape_pattern(text: str) -> str:
        """Escape literal text for safe regex interpolation.

        Returns:
            The resulting ``str``.

        """
        return re.escape(text)

    @staticmethod
    def execute_result_command(
        *,
        args: t.StrSequence | None,
        app_name: str,
        app_help: str,
        route: p.Cli.ResultCommandRoute,
    ) -> int:
        """Execute a single result-command Typer application.

        Args:
            args: Command-line arguments for the application; defaults to
                ``sys.argv[1:]`` when ``None``.
            app_name: Display name of the Typer application.
            app_help: Help text of the Typer application.
            route: Result-command route registered on the application.

        Returns:
            The process exit code.

        """
        app = cli.create_app_with_common_params(name=app_name, help_text=app_help)
        cli.register_result_routes(app, [route])
        outcome = cli.execute_app(
            app,
            prog_name=app_name,
            args=list(args) if args is not None else sys.argv[1:],
        )
        return 0 if outcome.success else 1

    @staticmethod
    def execute_run_command(
        *,
        args: t.StrSequence | None,
        app_name: str,
        app_help: str,
        route_help: str,
        model_cls: type[FlextQualityServiceBase[bool]],
    ) -> int:
        """Execute a single ``run`` result command for one self-executing model.

        Args:
            args: Command-line arguments for the application; defaults to
                ``sys.argv[1:]`` when ``None``.
            app_name: Display name of the Typer application.
            app_help: Help text of the Typer application.
            route_help: Help text of the registered ``run`` route.
            model_cls: Command model class whose ``execute`` runs the route.

        Returns:
            The process exit code.

        """
        return FlextQualityUtilitiesQuality.execute_result_command(
            args=args,
            app_name=app_name,
            app_help=app_help,
            route=m.Cli.ResultCommandRoute(
                name="run",
                help_text=route_help,
                model_cls=model_cls,
                handler=FlextQualityUtilitiesQuality.execute_run_route,
            ),
        )

    @staticmethod
    def execute_run_route(
        params: FlextQualityServiceBase[bool],
    ) -> p.Result[bool]:
        """Execute one self-executing ``run`` command model.

        Args:
            params: Command model instance carrying the parsed arguments.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        return params.execute()

    @staticmethod
    def format_hook_output(
        *,
        continue_exec: bool = True,
        message: str | None = None,
        blocked_reason: str | None = None,
    ) -> str:
        """Format hook output JSON.

        Args:
            continue_exec: Whether execution may continue after the hook.
            message: Optional message surfaced to the model.
            blocked_reason: Optional reason emitted when the hook blocks.

        Returns:
            The resulting ``str``.

        """
        output: t.MutableOptionalFeatureFlagMapping = {"continue": continue_exec}
        if message:
            output["systemMessage"] = message
        if blocked_reason:
            output["blockedReason"] = blocked_reason
        quality_utils = FlextQualityUtilitiesQuality
        adapter = quality_utils.MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER
        serialized_output: bytes = adapter.dump_json(output)
        decoded_output: str = serialized_output.decode(c.DEFAULT_ENCODING)
        return decoded_output

    @staticmethod
    def extract_rules_from_yaml(
        parsed: t.JsonMapping,
    ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
        """Validate and extract the rules list from parsed YAML.

        Args:
            parsed: Parsed YAML mapping expected to carry a ``rules`` list.

        Returns:
            The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.

        """
        if not isinstance(parsed, dict):
            return r[t.SequenceOf[t.JsonMapping]].fail("Expected YAML dict")
        parsed_dict: t.JsonMapping = u.json_mapping_adapter().validate_python(
            parsed,
        )
        raw_rules_val = parsed_dict.get("rules", [])
        if not isinstance(raw_rules_val, list):
            return r[t.SequenceOf[t.JsonMapping]].fail("Expected rules list")
        rules: t.SequenceOf[t.JsonMapping] = [
            u.json_mapping_adapter().validate_python(item)
            for item in raw_rules_val
            if isinstance(item, dict)
        ]
        return r[t.SequenceOf[t.JsonMapping]].ok(rules)

    @staticmethod
    def load_yaml_rules(path: Path) -> p.Result[t.SequenceOf[t.JsonMapping]]:
        """Load rules from a YAML file.

        Args:
            path: Path to the YAML file holding the rule definitions.

        Returns:
            The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.

        """
        try:
            yaml_result = u.Cli.yaml_safe_load(path)
            if yaml_result.failure:
                return r[t.SequenceOf[t.JsonMapping]].fail(
                    f"Failed to load YAML: {yaml_result.error}",
                )
            return FlextQualityUtilitiesQuality.extract_rules_from_yaml(
                yaml_result.value,
            )
        except c.EXC_BROAD_IO_TYPE as e:
            return r[t.SequenceOf[t.JsonMapping]].fail(
                f"Failed to load rules: {e}",
                exception=e,
            )

    @staticmethod
    def parse_hook_input(raw: str) -> p.Result[t.JsonMapping]:
        """Parse hook input JSON.

        Args:
            raw: Raw JSON text describing the hook event.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        try:
            parsed: t.JsonMapping = u.json_mapping_adapter().validate_json(raw)
            coerced_input: t.JsonMapping = parsed
            return r[t.JsonMapping].ok(coerced_input)
        except ValueError as e:
            return r[t.JsonMapping].fail(f"Invalid JSON: {e}", exception=e)

    @staticmethod
    def read_stdin() -> p.Result[str]:
        """Read JSON from stdin (for hooks).

        Returns:
            The resulting ``p.Result[str]``.

        """
        return u.try_(sys.stdin.read, catch=Exception).map_error(
            lambda e: f"Failed to read stdin: {e}",
        )

    @staticmethod
    def run_shell_command(
        cmd: t.StrSequence,
        timeout_ms: int = c.Quality.HOOK_TIMEOUT_MS,
    ) -> p.Result[str]:
        """Run a shell command with timeout.

        Args:
            cmd: Command and arguments to execute.
            timeout_ms: Maximum wall-clock time for the command in
                milliseconds.

        Returns:
            The resulting ``p.Result[str]``.

        """
        timeout_secs = int(timeout_ms / c.Quality.MS_TO_SECONDS_DIVISOR)
        cmd_result = u.Cli.run_raw(list(cmd), timeout=timeout_secs)
        if cmd_result.failure:
            return r[str].fail(str(cmd_result.error))
        out = cmd_result.value
        if out.outcome.raw_return_code != 0:
            return r[str].fail_op("Command", out.stderr)
        return r[str].ok(out.stdout)


__all__: list[str] = ["FlextQualityUtilitiesQuality"]
