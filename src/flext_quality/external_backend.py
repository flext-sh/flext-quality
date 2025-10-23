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

import contextlib
import json
import tempfile
from pathlib import Path
from typing import Any, override

from flext_core import FlextResult, FlextUtilities

from .backend_type import BackendType
from .base import FlextQualityAnalyzer


class FlextQualityExternalBackend(FlextQualityAnalyzer):
    """Backend using external Python quality tools via subprocess."""

    @override
    def get_backend_type(self: object) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self: object) -> list[str]:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture", "coverage", "radon"]

    def analyze(  # type: ignore[override]
        self,
        code: str,
        file_path: Path | None = None,
        tool: str = "ruff",
    ) -> FlextResult[dict[str, Any]]:
        """Analyze code using external tools.

        Args:
            code: Python source code to analyze
            file_path: Optional file path for context
            tool: Tool to use (ruff, mypy, bandit, vulture, coverage, radon)

        Returns:
            FlextResult containing analysis results dict

        """
        # Create temporary file for analysis
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8",
            ) as f:
                f.write(code)
                temp_path = Path(f.name)

            # Route to appropriate tool
            if tool == "ruff":
                return self._run_ruff(temp_path)
            if tool == "mypy":
                return self._run_mypy(temp_path)
            if tool == "bandit":
                return self._run_bandit(temp_path)
            if tool == "vulture":
                return self._run_vulture(temp_path)
            if tool == "coverage":
                return self._run_coverage(temp_path)
            if tool == "radon":
                return self._run_radon(temp_path)
            return FlextResult.fail(f"Unknown tool: {tool}")

        except Exception as e:
            return FlextResult.fail(f"Analysis setup failed: {e}")
        finally:
            # Cleanup temp file
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)

    # =========================================================================
    # RUFF - Fast linting and formatting
    # =========================================================================

    def _run_ruff(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run ruff linter with JSON output."""
        result = FlextUtilities.run_external_command(
            ["ruff", "check", str(file_path), "--output-format=json"],
            capture_output=True,
            timeout=30.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "not found" in error_msg.lower():
                return FlextResult.ok({
                    "tool": "ruff",
                    "issues": [],
                    "issue_count": 0,
                    "status": "tool_not_found",
                    "message": "ruff not installed",
                })
            if "timed out" in error_msg.lower():
                return FlextResult.fail("ruff analysis timed out")
            return FlextResult.fail(f"ruff analysis failed: {error_msg}")

        wrapper = result.unwrap()

        issues = []
        if wrapper.stdout.strip():
            try:
                data = json.loads(wrapper.stdout)
                if isinstance(data, list):
                    issues = data
            except json.JSONDecodeError:
                pass

        return FlextResult.ok({
            "tool": "ruff",
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    # =========================================================================
    # MYPY - Type checking
    # =========================================================================

    def _run_mypy(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run mypy type checker."""
        result = FlextUtilities.run_external_command(
            ["mypy", str(file_path), "--json-report=/tmp", "--no-incremental"],
            capture_output=True,
            timeout=30.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "not found" in error_msg.lower():
                return FlextResult.ok({
                    "tool": "mypy",
                    "issues": [],
                    "issue_count": 0,
                    "status": "tool_not_found",
                    "message": "mypy not installed",
                })
            if "timed out" in error_msg.lower():
                return FlextResult.fail("mypy analysis timed out")
            return FlextResult.fail(f"mypy analysis failed: {error_msg}")

        wrapper = result.unwrap()

        issues = []
        # Parse mypy output line by line
        for line in wrapper.stdout.splitlines():
            if line.strip():
                try:
                    error_data = json.loads(line)
                    issues.append(error_data)
                except json.JSONDecodeError:
                    # Fall back to simple parsing
                    if "error:" in line or "note:" in line:
                        issues.append({"message": line.strip()})

        return FlextResult.ok({
            "tool": "mypy",
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    # =========================================================================
    # BANDIT - Security scanning
    # =========================================================================

    def _run_bandit(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run bandit security scanner."""
        result = FlextUtilities.run_external_command(
            ["bandit", "-f", "json", str(file_path)],
            capture_output=True,
            timeout=30.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "not found" in error_msg.lower():
                return FlextResult.ok({
                    "tool": "bandit",
                    "issues": [],
                    "issue_count": 0,
                    "status": "tool_not_found",
                    "message": "bandit not installed",
                })
            if "timed out" in error_msg.lower():
                return FlextResult.fail("bandit analysis timed out")
            return FlextResult.fail(f"bandit analysis failed: {error_msg}")

        wrapper = result.unwrap()

        issues = []
        if wrapper.stdout.strip():
            try:
                data = json.loads(wrapper.stdout)
                # Extract issues from bandit JSON output
                if isinstance(data, dict) and "results" in data:
                    issues = data["results"]
            except json.JSONDecodeError:
                pass

        return FlextResult.ok({
            "tool": "bandit",
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    # =========================================================================
    # VULTURE - Dead code detection
    # =========================================================================

    def _run_vulture(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run vulture dead code detector."""
        result = FlextUtilities.run_external_command(
            ["vulture", str(file_path), "--json"],
            capture_output=True,
            timeout=30.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "not found" in error_msg.lower():
                return FlextResult.ok({
                    "tool": "vulture",
                    "issues": [],
                    "issue_count": 0,
                    "status": "tool_not_found",
                    "message": "vulture not installed",
                })
            if "timed out" in error_msg.lower():
                return FlextResult.fail("vulture analysis timed out")
            return FlextResult.fail(f"vulture analysis failed: {error_msg}")

        wrapper = result.unwrap()

        issues = []
        if wrapper.stdout.strip():
            try:
                data = json.loads(wrapper.stdout)
                if isinstance(data, list):
                    issues = data
            except json.JSONDecodeError:
                pass

        return FlextResult.ok({
            "tool": "vulture",
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    # =========================================================================
    # COVERAGE - Test coverage measurement
    # =========================================================================

    def _run_coverage(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run coverage to measure test coverage."""
        result = FlextUtilities.run_external_command(
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
            error_msg = result.error or ""
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

        wrapper = result.unwrap()

        coverage_data = {}
        if wrapper.stdout.strip():
            # Try to parse coverage JSON if it was generated
            coverage_path = Path(tempfile.gettempdir()) / ".coverage.json"
            if coverage_path.exists():
                try:
                    with Path(coverage_path).open(encoding="utf-8") as f:
                        coverage_data = json.load(f)
                except json.JSONDecodeError:
                    # Invalid JSON in coverage file - use empty data instead
                    coverage_data = {}
                except FileNotFoundError:
                    # Coverage file was not created - use empty data
                    coverage_data = {}
                except Exception:
                    # Unexpected error reading coverage file - use empty data
                    coverage_data = {}

        return FlextResult.ok({
            "tool": "coverage",
            "coverage_data": coverage_data,
            "status": "success" if wrapper.returncode == 0 else "incomplete",
            "message": "Coverage measurement complete"
            if coverage_data
            else "No coverage data",
        })

    # =========================================================================
    # RADON - Complexity metrics
    # =========================================================================

    def _run_radon(self, file_path: Path) -> FlextResult[dict[str, Any]]:
        """Run radon for complexity metrics."""
        # First call: complexity
        result_cc = FlextUtilities.run_external_command(
            ["radon", "cc", str(file_path), "-j"],
            capture_output=True,
            timeout=30.0,
        )

        if result_cc.is_failure:
            error_msg = result_cc.error or ""
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

        wrapper_cc = result_cc.unwrap()

        metrics = {}
        if wrapper_cc.stdout.strip():
            with contextlib.suppress(json.JSONDecodeError):
                metrics = json.loads(wrapper_cc.stdout)

        # Also get maintainability index
        result_mi = FlextUtilities.run_external_command(
            ["radon", "mi", str(file_path), "-j"],
            capture_output=True,
            timeout=30.0,
        )

        maintainability = {}
        if result_mi.is_success:
            wrapper_mi = result_mi.unwrap()
            if wrapper_mi.stdout.strip():
                with contextlib.suppress(json.JSONDecodeError):
                    maintainability = json.loads(wrapper_mi.stdout)

        return FlextResult.ok({
            "tool": "radon",
            "complexity": metrics,
            "maintainability": maintainability,
            "status": "success",
        })
