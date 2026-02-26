"""Utility functions for flext-quality."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import yaml
from flext_core import FlextUtilities, r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.typings import HookInput


class FlextQualityUtilities(FlextUtilities):
    """Namespace for flext-quality utilities."""

    class Quality:
        """Quality-specific utilities namespace."""

        @staticmethod
        def read_stdin() -> r[str]:
            """Read JSON from stdin (for hooks)."""
            try:
                data = sys.stdin.read()
                return r[str].ok(data)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[str].fail(f"Failed to read stdin: {e}")

        @staticmethod
        def parse_hook_input(raw: str) -> r[HookInput]:
            """Parse hook input JSON."""
            try:
                parsed: object = json.loads(raw)
                match parsed:
                    case dict() as hook_input:
                        return r[HookInput].ok(hook_input)
                    case _:
                        return r[HookInput].fail("Expected JSON object")
            except json.JSONDecodeError as e:
                return r[HookInput].fail(f"Invalid JSON: {e}")

        @staticmethod
        def format_hook_output(
            *,
            continue_exec: bool = True,
            message: str | None = None,
            blocked_reason: str | None = None,
        ) -> str:
            """Format hook output JSON."""
            output: dict[str, object] = {"continue": continue_exec}
            if message:
                output["systemMessage"] = message
            if blocked_reason:
                output["blockedReason"] = blocked_reason
            return json.dumps(output)

        @staticmethod
        def load_yaml_rules(path: Path) -> r[list[Mapping[str, object]]]:
            """Load rules from YAML file."""
            try:
                with path.open(encoding="utf-8") as f:
                    parsed: object = yaml.safe_load(f)
                match parsed:
                    case dict() as parsed_dict:
                        raw_rules = parsed_dict.get("rules", [])
                    case _:
                        return r[list[Mapping[str, object]]].fail("Expected YAML dict")
                match raw_rules:
                    case list() as rules_list:
                        rules: list[Mapping[str, object]] = [
                            item for item in rules_list if isinstance(item, dict)
                        ]
                    case _:
                        return r[list[Mapping[str, object]]].fail("Expected rules list")
                return r[list[Mapping[str, object]]].ok(rules)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[list[Mapping[str, object]]].fail(f"Failed to load rules: {e}")

        @staticmethod
        def run_shell_command(
            cmd: list[str],
            timeout_ms: int = c.Quality.Defaults.HOOK_TIMEOUT_MS,
        ) -> r[str]:
            """Run a shell command with timeout."""
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout_ms / 1000,
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


# Short alias for imports
u = FlextQualityUtilities
