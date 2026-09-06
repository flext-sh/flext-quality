"""Behavioral tests for ``FlextQualityCodeExecutionBridge``.

Exercises command-building and request-creation against real files on
``tmp_path`` — no mocks, no patched collaborators, and no real subprocess
execution (this bridge only builds command sequences).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_quality import FlextQualityCodeExecutionBridge
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextQualityCodeExecutionBridge:
    """Contract tests for the code execution command-building bridge."""

    def test_build_basedpyright_command_resolves_target_path(
        self, tmp_path: Path
    ) -> None:
        """The basedpyright command resolves the target path and emits JSON output."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_basedpyright_command(tmp_path)
        tm.that(result.success, eq=True)
        tm.that(result.value[0], eq="basedpyright")
        tm.that(result.value, has=str(tmp_path.resolve()))

    def test_build_python_command_fails_for_missing_script(
        self, tmp_path: Path
    ) -> None:
        """Building a Python command for a nonexistent script fails."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_python_command(tmp_path / "missing.py")
        tm.that(result.failure, eq=True)

    def test_build_python_command_succeeds_for_real_script(
        self, tmp_path: Path
    ) -> None:
        """Building a Python command for a real script includes its path."""
        script = tmp_path / "script.py"
        script.write_text("print('hi')\n", encoding="utf-8")
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_python_command(script)
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=["python", str(script)])

    def test_build_python_command_appends_extra_args(self, tmp_path: Path) -> None:
        """Extra positional args are appended after the script path."""
        script = tmp_path / "script.py"
        script.write_text("print('hi')\n", encoding="utf-8")
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_python_command(script, args=["--flag", "value"])
        tm.that(result.value, eq=["python", str(script), "--flag", "value"])

    def test_build_ruff_command_defaults_to_json_output(self, tmp_path: Path) -> None:
        """The ruff command defaults to JSON output without a fix flag."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_ruff_command(tmp_path)
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=["ruff", "check", str(tmp_path), "--output-format=json"])

    def test_build_ruff_command_honors_fix_and_output_format(
        self, tmp_path: Path
    ) -> None:
        """An explicit fix flag and output format are reflected in the command."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_ruff_command(tmp_path, fix=True, output_format="text")
        tm.that(result.value[-1], eq="--fix")
        tm.that(result.value, has="--output-format=text")

    def test_build_typescript_command_fails_for_missing_script(
        self, tmp_path: Path
    ) -> None:
        """Building a TypeScript command for a nonexistent script fails."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_typescript_command(tmp_path / "missing.ts")
        tm.that(result.failure, eq=True)

    def test_build_typescript_command_succeeds_for_real_script(
        self, tmp_path: Path
    ) -> None:
        """Building a TypeScript command for a real script uses ``npx tsx``."""
        script = tmp_path / "script.ts"
        script.write_text("console.log('hi');\n", encoding="utf-8")
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.build_typescript_command(script, args=["--verbose"])
        tm.that(result.value, eq=["npx", "tsx", str(script), "--verbose"])

    def test_create_execution_request_fails_for_unknown_runtime(
        self, tmp_path: Path
    ) -> None:
        """An unrecognized runtime name is rejected before request construction."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.create_execution_request(tmp_path / "x.py", "cobol")
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="Unknown runtime")

    def test_create_execution_request_succeeds_for_known_runtime(
        self, tmp_path: Path
    ) -> None:
        """A supported runtime yields a fully populated execution request."""
        bridge = FlextQualityCodeExecutionBridge(timeout_ms=5000)
        result = bridge.create_execution_request(
            tmp_path / "x.py", "python", args=["--fast"]
        )
        tm.that(result.success, eq=True)
        tm.that(result.value.runtime, eq="python")
        tm.that(result.value.timeout_ms, eq=5000)
        tm.that(list(result.value.args), eq=["--fast"])

    def test_health_check_reports_working_dir_and_supported_runtimes(
        self, tmp_path: Path
    ) -> None:
        """Health check reports the configured working directory and runtimes."""
        bridge = FlextQualityCodeExecutionBridge(working_dir=tmp_path)
        result = bridge.health_check()
        tm.that(result.success, eq=True)
        tm.that(result.value.get("working_dir"), eq=str(tmp_path))
        tm.that(result.value.get("available"), eq=True)
        tm.that(result.value.get("supported_runtimes"), has="ruff")

    def test_health_check_defaults_working_dir_to_cwd(self) -> None:
        """Omitting ``working_dir`` defaults the bridge to the current directory."""
        bridge = FlextQualityCodeExecutionBridge()
        result = bridge.health_check()
        tm.that(result.value.get("working_dir"), is_=str)


__all__: list[str] = ["TestsFlextQualityCodeExecutionBridge"]
