"""Utility functions for flext-quality."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import ClassVar

from flext_infra import u
from flext_web import u as web_u

from flext_quality import c, p, r, t


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
            flags = 0
            if ignorecase:
                flags |= re.IGNORECASE
            if multiline:
                flags |= re.MULTILINE
            if dotall:
                flags |= re.DOTALL
            return re.compile(pattern, flags=flags)

        @staticmethod
        def escape_pattern(text: str) -> str:
            """Escape literal text for safe regex interpolation."""
            return re.escape(text)

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
        def load_yaml_rules(
            path: Path,
        ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
            """Load rules from YAML file."""
            try:
                yaml_result = FlextQualityUtilities.Cli.yaml_safe_load(path)
                if yaml_result.failure:
                    return r[t.SequenceOf[t.JsonMapping]].fail(
                        f"Failed to load YAML: {yaml_result.error}",
                    )
                parsed = yaml_result.value
                if not isinstance(parsed, dict):
                    return r[t.SequenceOf[t.JsonMapping]].fail(
                        "Expected YAML dict",
                    )
                parsed_dict: t.JsonMapping = (
                    t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(parsed)
                )
                raw_rules_val = parsed_dict.get("rules", [])
                if not isinstance(raw_rules_val, list):
                    return r[t.SequenceOf[t.JsonMapping]].fail(
                        "Expected rules list",
                    )
                rules: t.SequenceOf[t.JsonMapping] = [
                    t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(item)
                    for item in raw_rules_val
                    if isinstance(item, dict)
                ]
                return r[t.SequenceOf[t.JsonMapping]].ok(rules)
            except c.EXC_BROAD_IO_TYPE as e:
                return r[t.SequenceOf[t.JsonMapping]].fail(
                    f"Failed to load rules: {e}",
                )

        @staticmethod
        def parse_hook_input(raw: str) -> p.Result[t.Quality.HookInput]:
            """Parse hook input JSON."""
            try:
                parsed: t.JsonMapping = (
                    t.Quality.CONTAINER_MAPPING_ADAPTER.validate_json(raw)
                )
                coerced_input: t.JsonMapping = parsed
                return r[t.Quality.HookInput].ok(coerced_input)
            except ValueError as e:
                return r[t.Quality.HookInput].fail(f"Invalid JSON: {e}")

        @staticmethod
        def read_stdin() -> p.Result[str]:
            """Read JSON from stdin (for hooks)."""
            return u.try_(
                sys.stdin.read,
                catch=Exception,
            ).map_error(lambda e: f"Failed to read stdin: {e}")

        @staticmethod
        def run_shell_command(
            cmd: t.StrSequence,
            timeout_ms: int = c.Quality.HOOK_TIMEOUT_MS,
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
