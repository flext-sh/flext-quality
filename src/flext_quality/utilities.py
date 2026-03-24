"""Utility functions for flext-quality."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path

import yaml
from flext_cli import FlextCliUtilities
from flext_core import r
from flext_web import FlextWebUtilities
from pydantic import TypeAdapter

from flext_quality import c, t


class FlextQualityUtilities(FlextWebUtilities, FlextCliUtilities):
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
            output: MutableMapping[str, str | bool | None] = {"continue": continue_exec}
            if message:
                output["systemMessage"] = message
            if blocked_reason:
                output["blockedReason"] = blocked_reason
            return (
                TypeAdapter(MutableMapping[str, str | bool | None])
                .dump_json(output)
                .decode("utf-8")
            )

        @staticmethod
        def load_yaml_rules(path: Path) -> r[Sequence[t.ContainerMapping]]:
            """Load rules from YAML file."""
            try:
                with path.open(encoding="utf-8") as f:
                    parsed = yaml.safe_load(f)
                if not isinstance(parsed, dict):
                    return r[Sequence[t.ContainerMapping]].fail(
                        "Expected YAML dict",
                    )
                parsed_dict: Mapping[str, t.NormalizedValue] = TypeAdapter(
                    Mapping[str, t.NormalizedValue],
                ).validate_python(parsed)
                raw_rules_val = parsed_dict.get("rules", [])
                if not isinstance(raw_rules_val, list):
                    return r[Sequence[t.ContainerMapping]].fail(
                        "Expected rules list",
                    )
                item_adapter: TypeAdapter[Mapping[str, t.NormalizedValue]] = (
                    TypeAdapter(
                        Mapping[str, t.NormalizedValue],
                    )
                )
                rules: list[Mapping[str, t.NormalizedValue]] = [
                    item_adapter.validate_python(item)
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
                parsed: Mapping[str, t.NormalizedValue] = TypeAdapter(
                    Mapping[str, t.NormalizedValue],
                ).validate_json(raw)
                coerced_input: Mapping[str, t.NormalizedValue] = parsed
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
            try:
                # Intentional subprocess usage: Quality validation command execution
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout_ms / c.Quality.Defaults.MS_TO_SECONDS_DIVISOR,
                    check=False,
                )
                if result.returncode != 0:
                    return r[str].fail(f"Command failed: {result.stderr}")
                return r[str].ok(result.stdout)
            except subprocess.TimeoutExpired:
                return r[str].fail(f"Command timed out after {timeout_ms}ms")
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[str].fail(f"Command error: {e}")


u = FlextQualityUtilities
