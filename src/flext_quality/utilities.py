"""Utility functions for flext-quality."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import TypeGuard

import yaml
from flext_core import FlextUtilities, r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.typings import HookInput


def _is_dict(value: object) -> TypeGuard[dict[str, object]]:
    """Type guard for dict validation."""
    return isinstance(value, dict)


def _is_hook_input(value: object) -> TypeGuard[HookInput]:
    """Type guard for HookInput validation (dict from JSON parsing)."""
    return isinstance(value, dict)


def _is_list(value: object) -> TypeGuard[list[object]]:
    """Type guard for list validation."""
    return isinstance(value, list)


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
            except Exception as e:
                return r[str].fail(f"Failed to read stdin: {e}")

        @staticmethod
        def parse_hook_input(raw: str) -> r[HookInput]:
            """Parse hook input JSON."""
            try:
                parsed: object = json.loads(raw)
                if not _is_hook_input(parsed):
                    return r[HookInput].fail("Expected JSON object")
                return r[HookInput].ok(parsed)
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
        def load_yaml_rules(path: Path) -> r[list[dict[str, object]]]:
            """Load rules from YAML file."""
            try:
                with path.open(encoding="utf-8") as f:
                    parsed: object = yaml.safe_load(f)
                if not _is_dict(parsed):
                    return r[list[dict[str, object]]].fail("Expected YAML dict")
                raw_rules = parsed.get("rules", [])
                if not _is_list(raw_rules):
                    return r[list[dict[str, object]]].fail("Expected rules list")
                rules = [item for item in raw_rules if _is_dict(item)]
                return r[list[dict[str, object]]].ok(rules)
            except Exception as e:
                return r[list[dict[str, object]]].fail(f"Failed to load rules: {e}")

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
            except Exception as e:
                return r[str].fail(f"Command error: {e}")


# Short alias for imports
u = FlextQualityUtilities
