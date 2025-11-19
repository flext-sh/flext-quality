"""External tools backend - pragmatic integration with Python ecosystem tools.

Uses subprocess to run industry-standard quality analysis tools:
- ruff: Fast linting and formatting
- mypy: Static type checking
- bandit: Security vulnerability scanning
- vulture: Dead code detection
- coverage: Test coverage measurement
- radon: Cyclomatic complexity analysis

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, override

from flext_core import (
    FlextDecorators,
    FlextLogger,
    FlextMixins,
    FlextResult,
    FlextService,
    FlextUtilities,
)

from .backend_type import BackendType
from .base import FlextQualityAnalyzer


class FlextQualityExternalBackend(FlextQualityAnalyzer, FlextService, FlextMixins):
    """Backend using external Python quality tools via subprocess."""

    @override
    def get_backend_type(self) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture", "coverage", "radon"]

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute main analysis operation."""
        # For external backend, execute a basic ruff check as default operation
        return self.analyze("", tool="ruff")

    @FlextDecorators.log_operation("analyze_code")
    def analyze(
        self,
        code: str,
        _file_path: Path | None = None,
        tool: str = "ruff",
    ) -> FlextResult[dict[str, Any]]:
        """Analyze code using external tools.

        Args:
            code: Python source code to analyze
            tool: Tool to use (ruff, mypy, bandit, vulture, coverage, radon)

        Returns:
            FlextResult containing analysis results dict

        """
        temp_file_result = self._create_temp_file(code)
        if temp_file_result.is_failure:
            return temp_file_result.map(lambda _: {})
        
        # Use with_resource pattern for automatic cleanup
        temp_path = temp_file_result.unwrap()
        return temp_file_result.with_resource(
            resource_factory=lambda: temp_path,
            operation=lambda _, temp_path: self._route_tool_analysis(tool, temp_path),
            cleanup=lambda temp_path: temp_path.unlink(missing_ok=True),
        )

    def _create_temp_file(self, code: str) -> FlextResult[Path]:
        """Create temporary file with code content."""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8",
            ) as f:
                f.write(code)
                return FlextResult.ok(Path(f.name))
        except Exception as e:
            return FlextResult.fail(f"Failed to create temp file: {e}")

    def _route_tool_analysis(
        self, tool: str, file_path: Path
    ) -> FlextResult[dict[str, Any]]:
        """Route analysis to appropriate tool method."""
        tool_runners = {
            "ruff": self._run_ruff,
            "mypy": self._run_mypy,
            "bandit": self._run_bandit,
            "vulture": self._run_vulture,
            "coverage": self._run_coverage,
            "radon": self._run_radon,
        }

        runner = tool_runners.get(tool)
        if not runner:
            return FlextResult.fail(f"Unknown tool: {tool}")

        return runner(file_path)

    def _run_tool_with_json_output(
        self,
        tool_name: str,
        command: list[str],
        file_path: Path,
        timeout: float = 30.0,
        json_parser: callable = lambda stdout: json.loads(stdout)
        if stdout.strip()
        else [],
    ) -> FlextResult[dict[str, Any]]:
        """Generic method for running tools that output JSON."""
        if not file_path.exists():
            return FlextResult.fail("Invalid file path")

        result = FlextUtilities.CommandExecution.run_external_command(
            command,
            capture_output=True,
            timeout=timeout,
        )

        if result.is_failure:
            return self._handle_tool_error(result.error or "", tool_name)

        wrapper = result.unwrap()

        issues = []
        if wrapper.stdout.strip():
            try:
                issues = json_parser(wrapper.stdout)
            except json.JSONDecodeError:
                FlextLogger.warning(f"Failed to parse {tool_name} JSON output")

        return FlextResult.ok({
            "tool": tool_name,
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    def _handle_tool_error(
        self, error_msg: str, tool_name: str
    ) -> FlextResult[dict[str, Any]]:
        """Handle common tool execution errors."""
        if "not found" in error_msg.lower():
            return FlextResult.ok({
                "tool": tool_name,
                "issues": [],
                "issue_count": 0,
                "status": "tool_not_found",
                "message": f"{tool_name} not installed",
            })
        if "timed out" in error_msg.lower():
            return FlextResult.fail(f"{tool_name} analysis timed out")
        return FlextResult.fail(f"{tool_name} analysis failed: {error_msg}")

    # =========================================================================
    # RUFF - Fast linting and formatting
    # =========================================================================

    def _run_ruff(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run ruff linter with JSON output."""
        return self._run_tool_with_json_output(
            tool_name="ruff",
            command=["ruff", "check", str(file_path), "--output-format=json"],
            file_path=file_path,
            json_parser=lambda stdout: json.loads(stdout) if stdout.strip() else [],
        )

    # =========================================================================
    # MYPY - Type checking
    # =========================================================================

    def _run_mypy(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run mypy type checker."""
        return self._run_tool_with_json_output(
            tool_name="mypy",
            command=["mypy", str(file_path), "--json-report=/tmp", "--no-incremental"],
            file_path=file_path,
            json_parser=self._parse_mypy_output,
        )

    def _parse_mypy_output(self, stdout: str) -> list[dict[str, Any]]:
        """Parse mypy JSON output from stdout string."""
        issues = []
        for line in stdout.splitlines():
            if line.strip():
                try:
                    error_data = json.loads(line)
                    issues.append(error_data)
                except json.JSONDecodeError:
                    # Fall back to simple parsing
                    if "error:" in line or "note:" in line:
                        issues.append({"message": line.strip()})
        return issues

    # =========================================================================
    # BANDIT - Security scanning
    # =========================================================================

    def _run_bandit(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run bandit security scanner."""
        return self._run_tool_with_json_output(
            tool_name="bandit",
            command=["bandit", "-f", "json", str(file_path)],
            file_path=file_path,
            json_parser=lambda stdout: json.loads(stdout).get("results", [])
            if stdout.strip()
            else [],
        )

    # =========================================================================
    # VULTURE - Dead code detection
    # =========================================================================

    def _run_vulture(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run vulture dead code detector."""
        return self._run_tool_with_json_output(
            tool_name="vulture",
            command=["vulture", str(file_path), "--json"],
            file_path=file_path,
            json_parser=lambda stdout: json.loads(stdout) if stdout.strip() else [],
        )

    # =========================================================================
    # COVERAGE - Test coverage measurement
    # =========================================================================

    def _run_coverage(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run coverage to measure test coverage."""
        result = FlextUtilities.CommandExecution.run_external_command(
            [
                "coverage",
                "run",
                "-m",
                "pytest",
                str(file_path),
                "--cov=.",
                "--cov-report=json",
            ],
            capture_output=True,
            timeout=60.0,
            cwd=tempfile.gettempdir(),
        )

        if result.is_failure:
            return self._handle_coverage_error(result.error or "")

        wrapper = result.unwrap()
        coverage_data = self._parse_coverage_data()

        return FlextResult.ok({
            "tool": "coverage",
            "coverage_data": coverage_data,
            "status": "success" if wrapper.returncode == 0 else "incomplete",
            "message": "Coverage measurement complete"
            if coverage_data
            else "No coverage data",
        })

    def _handle_coverage_error(self, error_msg: str) -> FlextResult[dict[str, Any]]:
        """Handle coverage-specific errors."""
        if "not found" in error_msg.lower():
            return FlextResult.ok({
                "tool": "coverage",
                "coverage_data": {},
                "status": "tool_not_found",
                "message": "coverage/pytest not installed",
            })
        if "timed out" in error_msg.lower():
            return FlextResult.fail("coverage analysis timed out")
        return FlextResult.fail(f"coverage analysis failed: {error_msg}")

    def _parse_coverage_data(self) -> dict[str, Any]:
        """Parse coverage JSON data from temp directory."""
        coverage_path = Path(tempfile.gettempdir()) / ".coverage.json"
        if not coverage_path.exists():
            return {}

        try:
            with coverage_path.open(encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, Exception):
            return {}

    # =========================================================================
    # RADON - Complexity metrics
    # =========================================================================

    def _run_radon(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run radon for complexity metrics."""
        # First call: complexity
        result_cc = FlextUtilities.CommandExecution.run_external_command(
            ["radon", "cc", str(file_path), "-j"],
            capture_output=True,
            timeout=30.0,
        )

        if result_cc.is_failure:
            return self._handle_radon_error(result_cc.error or "")

        wrapper_cc = result_cc.unwrap()
        metrics = self._parse_radon_json(wrapper_cc.stdout)

        # Also get maintainability index
        maintainability = self._run_radon_maintainability(file_path)

        return FlextResult.ok({
            "tool": "radon",
            "complexity": metrics,
            "maintainability": maintainability,
            "status": "success",
        })

    def _handle_radon_error(self, error_msg: str) -> FlextResult[dict[str, Any]]:
        """Handle radon-specific errors."""
        if "not found" in error_msg.lower():
            return FlextResult.ok({
                "tool": "radon",
                "complexity": {},
                "maintainability": {},
                "status": "tool_not_found",
                "message": "radon not installed",
            })
        if "timed out" in error_msg.lower():
            return FlextResult.fail("radon analysis timed out")
        return FlextResult.fail(f"radon analysis failed: {error_msg}")

    def _run_radon_maintainability(self, file_path: Path) -> dict[str, Any]:
        """Run radon maintainability index analysis."""
        result_mi = FlextUtilities.CommandExecution.run_external_command(
            ["radon", "mi", str(file_path), "-j"],
            capture_output=True,
            timeout=30.0,
        )

        if result_mi.is_success and result_mi.unwrap().stdout.strip():
            return self._parse_radon_json(result_mi.unwrap().stdout)
        return {}

    def _parse_radon_json(self, stdout: str) -> dict[str, Any]:
        """Parse radon JSON output."""
        if not stdout.strip():
            return {}
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {}

    def _parse_ruff_output(self, output: str) -> list[dict[str, Any]]:
        """Parse ruff JSON output into structured format."""
        try:
            return json.loads(output) if output.strip() else []
        except json.JSONDecodeError:
            return []
