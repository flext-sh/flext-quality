"""Utility functions for flext-quality."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from flext_cli import u as _cli_u
from flext_web import FlextWebUtilities

from flext_core import r
from flext_quality import c, t


class FlextQualityUtilities(FlextWebUtilities, _cli_u):
    """Namespace for flext-quality utilities."""

    class Quality:
        """Quality-specific utilities namespace."""

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
            return t.MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER.dump_json(
                output
            ).decode("utf-8")

        @staticmethod
        def load_yaml_rules(path: Path) -> r[Sequence[t.ContainerMapping]]:
            """Load rules from YAML file."""
            try:
                yaml_result = FlextQualityUtilities.Cli.yaml_safe_load(path)
                if yaml_result.is_failure:
                    return r[Sequence[t.ContainerMapping]].fail(
                        f"Failed to load YAML: {yaml_result.error}",
                    )
                parsed = yaml_result.value
                if not isinstance(parsed, dict):
                    return r[Sequence[t.ContainerMapping]].fail(
                        "Expected YAML dict",
                    )
                parsed_dict: t.ContainerMapping = (
                    t.CONTAINER_MAPPING_ADAPTER.validate_python(parsed)
                )
                raw_rules_val = parsed_dict.get("rules", [])
                if not isinstance(raw_rules_val, list):
                    return r[Sequence[t.ContainerMapping]].fail(
                        "Expected rules list",
                    )
                rules: Sequence[t.ContainerMapping] = [
                    t.CONTAINER_MAPPING_ADAPTER.validate_python(item)
                    for item in raw_rules_val
                    if isinstance(item, dict)
                ]
                return r[Sequence[t.ContainerMapping]].ok(rules)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[Sequence[t.ContainerMapping]].fail(
                    f"Failed to load rules: {e}",
                )

        @staticmethod
        def parse_hook_input(raw: str) -> r[t.Quality.HookInput]:
            """Parse hook input JSON."""
            try:
                parsed: t.ContainerMapping = t.CONTAINER_MAPPING_ADAPTER.validate_json(
                    raw
                )
                coerced_input: t.ContainerMapping = parsed
                return r[t.Quality.HookInput].ok(coerced_input)
            except ValueError as e:
                return r[t.Quality.HookInput].fail(f"Invalid JSON: {e}")

        @staticmethod
        def read_stdin() -> r[str]:
            """Read JSON from stdin (for hooks)."""
            return u.try_(
                sys.stdin.read,
                catch=Exception,
            ).map_error(lambda e: f"Failed to read stdin: {e}")

        @staticmethod
        def run_shell_command(
            cmd: t.StrSequence,
            timeout_ms: int = c.Quality.Defaults.HOOK_TIMEOUT_MS,
        ) -> r[str]:
            """Run a shell command with timeout."""
            timeout_secs = int(timeout_ms / c.Quality.Defaults.MS_TO_SECONDS_DIVISOR)
            cmd_result = u.Cli.run_raw(list(cmd), timeout=timeout_secs)
            if cmd_result.is_failure:
                return r[str].fail(str(cmd_result.error))
            out = cmd_result.value
            if out.exit_code != 0:
                return r[str].fail(f"Command failed: {out.stderr}")
            return r[str].ok(out.stdout)


u = FlextQualityUtilities
