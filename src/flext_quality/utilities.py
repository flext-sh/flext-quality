"""Utility functions for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import TYPE_CHECKING

from flext_cli import cli
from flext_web import FlextWebUtilities, t as web_t, u

from flext_core import FlextResult as r
from flext_quality import (
    FlextQualityConstants as c,
    FlextQualityModels as m,
    FlextQualityProtocols as p,
    FlextQualityTypes as t,
)

if TYPE_CHECKING:
    from pathlib import Path


class FlextQualityUtilities(FlextWebUtilities):
    """Namespace for flext-quality utilities."""

    DocumentationReportValue = web_t.JsonMapping

    class Quality:
        """Quality-specific utilities namespace."""

        type DocumentationReportValue = web_t.JsonMapping

        # Resolved generics, not bare PEP 695 aliases: the adapter form must be
        # a checker-visible type expression (bare aliases evaluate to
        # TypeAliasType objects, which the adapter form rejects). Concrete
        # generics only; runtime objects identical to the unwrapped aliases.
        RELAXED_CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.JsonValue]] = (
            FlextWebUtilities.type_adapter(
                Mapping[str, t.JsonValue],
                config=m.ConfigDict(strict=False),
            )
        )
        RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
            Sequence[Mapping[str, t.JsonValue]]
        ] = FlextWebUtilities.type_adapter(
            Sequence[Mapping[str, t.JsonValue]],
            config=m.ConfigDict(strict=False),
        )
        MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER: m.TypeAdapter[
            MutableMapping[str, str | bool | None]
        ] = FlextWebUtilities.type_adapter(MutableMapping[str, str | bool | None])
        STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
            MutableSequence[Mapping[str, str]]
        ] = FlextWebUtilities.type_adapter(MutableSequence[Mapping[str, str]])
        REPORT_VALUE_MAPPING_ADAPTER: m.TypeAdapter[
            t.MappingKV[str, DocumentationReportValue]
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

            Returns:
                The resulting ``int``.
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
        def format_hook_output(
            *,
            continue_exec: bool = True,
            message: str | None = None,
            blocked_reason: str | None = None,
        ) -> str:
            """Format hook output JSON.

            Returns:
                The resulting ``str``.
            """
            output: t.MutableOptionalFeatureFlagMapping = {"continue": continue_exec}
            if message:
                output["systemMessage"] = message
            if blocked_reason:
                output["blockedReason"] = blocked_reason
            quality_utils = FlextQualityUtilities.Quality
            adapter = quality_utils.MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER
            serialized_output: bytes = adapter.dump_json(output)
            decoded_output: str = serialized_output.decode(c.DEFAULT_ENCODING)
            return decoded_output

        @staticmethod
        def extract_rules_from_yaml(
            parsed: t.JsonMapping,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Validate and extract the rules list from parsed YAML.

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
            """Load rules from YAML file.

            Returns:
                The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
            """
            try:
                yaml_result = FlextQualityUtilities.Cli.yaml_safe_load(path)
                if yaml_result.failure:
                    return r[t.SequenceOf[t.JsonMapping]].fail(
                        f"Failed to load YAML: {yaml_result.error}",
                    )
                return FlextQualityUtilities.Quality.extract_rules_from_yaml(
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


u = FlextQualityUtilities

__all__: list[str] = ["FlextQualityUtilities", "u"]
