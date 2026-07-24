"""Utility functions for flext-quality."""

from __future__ import annotations

import re
import sys
from typing import TYPE_CHECKING, ClassVar

from flext_cli import cli
from flext_core import FlextResult as r
from flext_infra import FlextInfraUtilities as u
from flext_quality import (
    FlextQualityConstants as c,
    FlextQualityProtocols as p,
    FlextQualityTypes as t,
)
from flext_web import FlextWebUtilities as web_u

if TYPE_CHECKING:
    from pathlib import Path


class FlextQualityUtilities(u, web_u):
    """Namespace for flext-quality utilities.

    Marked as Pattern-B: this facade legitimately composes multiple parent
    utilities namespaces and references ``u`` in nested methods. The flext-core
    beartype self-reference check honours this marker via
    ``getattr(target, "__flext_pattern_b__", False)`` instead of a hand-curated
    package whitelist.
    """

    __flext_pattern_b__: ClassVar[bool] = True

    class Quality:
        """Quality-specific utilities namespace."""

        @staticmethod
        def compile_pattern(
            pattern: str,
            *,
            ignorecase: bool = False,
            multiline: bool = False,
            dotall: bool = False,
        ) -> t.RegexPattern:
            """Compile a runtime-supplied regex pattern for quality tooling."""
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
            """Escape literal text for safe regex interpolation."""
            return re.escape(text)

        @staticmethod
        def execute_result_command(
            *,
            args: t.StrSequence | None,
            app_name: str,
            app_help: str,
            route: p.Cli.ResultCommandRoute,
        ) -> int:
            """Execute a single result-command Typer application."""
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
            """Format hook output JSON."""
            output: t.MutableOptionalFeatureFlagMapping = {"continue": continue_exec}
            if message:
                output["systemMessage"] = message
            if blocked_reason:
                output["blockedReason"] = blocked_reason
            serialized_output: bytes = (
                t.Quality.MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER.dump_json(
                    output
                )
            )
            decoded_output: str = serialized_output.decode(c.DEFAULT_ENCODING)
            return decoded_output

        @staticmethod
        def extract_rules_from_yaml(
            parsed: t.JsonMapping,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Validate and extract the rules list from parsed YAML."""
            if not isinstance(parsed, dict):
                return r[t.SequenceOf[t.JsonMapping]].fail("Expected YAML dict")
            parsed_dict: t.JsonMapping = t.json_mapping_adapter().validate_python(
                parsed
            )
            raw_rules_val = parsed_dict.get("rules", [])
            if not isinstance(raw_rules_val, list):
                return r[t.SequenceOf[t.JsonMapping]].fail("Expected rules list")
            rules: t.SequenceOf[t.JsonMapping] = [
                t.json_mapping_adapter().validate_python(item)
                for item in raw_rules_val
                if isinstance(item, dict)
            ]
            return r[t.SequenceOf[t.JsonMapping]].ok(rules)

        @staticmethod
        def load_yaml_rules(path: Path) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Load rules from YAML file."""
            try:
                yaml_result = FlextQualityUtilities.Cli.yaml_safe_load(path)
                if yaml_result.failure:
                    return r[t.SequenceOf[t.JsonMapping]].fail(
                        f"Failed to load YAML: {yaml_result.error}"
                    )
                return FlextQualityUtilities.Quality.extract_rules_from_yaml(
                    yaml_result.value
                )
            except c.EXC_BROAD_IO_TYPE as e:
                return r[t.SequenceOf[t.JsonMapping]].fail(f"Failed to load rules: {e}")

        @staticmethod
        def parse_hook_input(raw: str) -> p.Result[t.JsonMapping]:
            """Parse hook input JSON."""
            try:
                parsed: t.JsonMapping = t.json_mapping_adapter().validate_json(raw)
                coerced_input: t.JsonMapping = parsed
                return r[t.JsonMapping].ok(coerced_input)
            except ValueError as e:
                return r[t.JsonMapping].fail(f"Invalid JSON: {e}")

        @staticmethod
        def read_stdin() -> p.Result[str]:
            """Read JSON from stdin (for hooks)."""
            return u.try_(sys.stdin.read, catch=Exception).map_error(
                lambda e: f"Failed to read stdin: {e}"
            )

        @staticmethod
        def run_shell_command(
            cmd: t.StrSequence, timeout_ms: int = c.Quality.HOOK_TIMEOUT_MS
        ) -> p.Result[str]:
            """Run a shell command with timeout."""
            timeout_secs = int(timeout_ms / c.Quality.MS_TO_SECONDS_DIVISOR)
            cmd_result = u.Cli.run_raw(list(cmd), timeout=timeout_secs)
            if cmd_result.failure:
                return r[str].fail(str(cmd_result.error))
            out = cmd_result.value
            if out.exit_code != 0:
                return r[str].fail_op("Command", out.stderr)
            return r[str].ok(out.stdout)


u = FlextQualityUtilities

__all__: list[str] = ["FlextQualityUtilities", "u"]
