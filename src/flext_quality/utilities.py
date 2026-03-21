"""Utility functions for flext-quality."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import yaml
from flext_cli import FlextCliUtilities
from flext_core.constants import c
from flext_core.result import r
from flext_core.typings import t
from flext_web import FlextWebUtilities
from pydantic import TypeAdapter


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
            output: dict[str, str | bool | None] = {"continue": continue_exec}
            if message:
                output["systemMessage"] = message
            if blocked_reason:
                output["blockedReason"] = blocked_reason
            return (
                TypeAdapter(dict[str, str | bool | None])
                .dump_json(output)
                .decode("utf-8")
            )

        @staticmethod
        def load_yaml_rules(path: Path) -> r[list[Mapping[str, t.NormalizedValue]]]:
            """Load rules from YAML file."""
            try:
                with path.open(encoding="utf-8") as f:
                    parsed = yaml.safe_load(f)
                match parsed:
                    case dict() as parsed_dict:
                        raw_rules = parsed_dict.get("rules", [])
                    case _:
                        return r[list[Mapping[str, t.NormalizedValue]]].fail(
                            "Expected YAML dict",
                        )
                match raw_rules:
                    case list() as rules_list:
                        rules: list[Mapping[str, t.NormalizedValue]] = [
                            item for item in rules_list if isinstance(item, dict)
                        ]
                    case _:
                        return r[list[Mapping[str, t.NormalizedValue]]].fail(
                            "Expected rules list",
                        )
                return r[list[Mapping[str, t.NormalizedValue]]].ok(rules)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[list[Mapping[str, t.NormalizedValue]]].fail(
                    f"Failed to load rules: {e}",
                )

        @staticmethod
        def parse_hook_input(raw: str) -> r[t.Quality.HookInput]:
            """Parse hook input JSON."""
            try:
                parsed = TypeAdapter(dict[str, t.NormalizedValue]).validate_json(raw)
                coerced_input: t.Quality.HookInput = parsed
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
            cmd: list[str],
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
