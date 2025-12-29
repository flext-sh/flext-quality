"""External tools backend - pragmatic integration with Python ecosystem tools.

Uses subprocess to run industry-standard quality analysis tools:
- ruff: Fast linting and formatting
- mypy: Static type checking
- bandit: Security vulnerability scanning
- vulture: Dead code detection
- coverage: Test coverage measurement
- radon: Cyclomatic complexity analysis
- refurb: Modern pattern suggestions
- complexipy: Cognitive complexity analysis
- rope: AST-based refactoring analysis

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import override

from flext_core import (
    FlextDecorators as d,
    FlextLogger,
    FlextMixins as x,
    FlextResult,
    FlextService,
    FlextTypes as t,
)
from rope.base import libutils
from rope.base.project import Project as RopeProject

from .backend_type import BackendType
from .base import FlextQualityAnalyzer
from .constants import FlextQualityConstants as qc
from .plugins.duplication_plugin import FlextDuplicationPlugin
from .protocols import FlextQualityProtocols as p
from .subprocess_utils import SubprocessUtils

# Module-level logger instance
_logger = FlextLogger(name="flext_quality.external_backend")


class FlextQualityExternalBackend(
    FlextQualityAnalyzer,
    FlextService[dict[str, t.GeneralValueType]],
    x,
):
    """Backend using external Python quality tools via subprocess."""

    @override
    def get_backend_type(self) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        return [
            "ruff",
            "mypy",
            "bandit",
            "vulture",
            "coverage",
            "radon",
            "refurb",
            "complexipy",
            "rope",
            "duplication",
        ]

    def execute(self) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute main analysis operation."""
        # For external backend, execute a basic ruff check as default operation
        return self.analyze_with_tool("", tool="ruff")

    @override
    def analyze(
        self,
        _code: str,
        file_path: Path | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Analyze code using default ruff tool.

        Args:
            _code: Python source code to analyze
            file_path: Optional file path for context (unused in external backend)

        Returns:
            FlextResult containing analysis results dict

        """
        _ = file_path  # Unused in external backend, analysis uses temp file
        return self.analyze_with_tool(_code, tool="ruff")

    @d.log_operation("analyze_code")
    def analyze_with_tool(
        self,
        code: str,
        tool: str = "ruff",
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Analyze code using specified external tool.

        Args:
            code: Python source code to analyze
            tool: Tool to use (ruff, mypy, bandit, vulture, coverage, radon,
                  refurb, complexipy, rope)

        Returns:
            FlextResult containing analysis results dict

        """
        temp_file_result = self._create_temp_file(code)
        if temp_file_result.is_failure:
            return FlextResult.fail(
                temp_file_result.error or "Failed to create temp file",
            )

        # Execute analysis with cleanup
        temp_path = temp_file_result.value
        try:
            return self._route_tool_analysis(tool, temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

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
        self,
        tool: str,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Route analysis to appropriate tool method."""
        tool_runners = {
            "ruff": self._run_ruff,
            "mypy": self._run_mypy,
            "bandit": self._run_bandit,
            "vulture": self._run_vulture,
            "coverage": self._run_coverage,
            "radon": self._run_radon,
            "refurb": self._run_refurb,
            "complexipy": self._run_complexipy,
            "rope": self._run_rope,
            "duplication": self._run_duplication,
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
        timeout: float | None = None,
        json_parser: p.Quality.JsonParserProtocol | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Generic method for running tools that output JSON.

        Args:
            tool_name: Name of the tool being run
            command: Command line arguments to execute
            file_path: Path to file being analyzed
            timeout: Timeout in seconds (uses DEFAULT_TOOL_TIMEOUT if None)
            json_parser: Optional parser implementing JsonParserProtocol

        Returns:
            FlextResult with tool analysis results

        """
        if not file_path.exists():
            return FlextResult.fail("Invalid file path")

        effective_timeout = float(
            timeout
            if timeout is not None
            else qc.Quality.QualityPerformance.DEFAULT_TOOL_TIMEOUT  # CONFIG
        )

        result = SubprocessUtils.run_external_command(
            command,
            capture_output=True,
            timeout=effective_timeout,
        )

        if result.is_failure:
            return self._handle_tool_error(result.error or "", tool_name)

        wrapper = result.value

        # Default parser: parse JSON array from stdout
        def _default_parser(stdout: str) -> list[dict[str, t.GeneralValueType]]:
            return json.loads(stdout) if stdout.strip() else []

        parser = json_parser if json_parser is not None else _default_parser

        issues: list[dict[str, t.GeneralValueType]] = []
        if wrapper.stdout.strip():
            try:
                issues = parser(wrapper.stdout)
            except json.JSONDecodeError:
                _logger.warning("Failed to parse %s JSON output", tool_name)

        return FlextResult.ok({
            "tool": tool_name,
            "issues": issues,
            "issue_count": len(issues),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    def _handle_tool_error(
        self,
        error_msg: str,
        tool_name: str,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
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

    def _run_ruff(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
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

    def _run_mypy(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run mypy type checker."""
        return self._run_tool_with_json_output(
            tool_name="mypy",
            command=["mypy", str(file_path), "--json-report=/tmp", "--no-incremental"],
            file_path=file_path,
            json_parser=self._parse_mypy_output,
        )

    def _parse_mypy_output(
        self,
        stdout: str,
    ) -> list[dict[str, t.GeneralValueType]]:
        """Parse mypy JSON output from stdout string."""
        issues: list[dict[str, t.GeneralValueType]] = []
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

    def _run_bandit(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run bandit security scanner."""
        return self._run_tool_with_json_output(
            tool_name="bandit",
            command=["bandit", "-f", "json", str(file_path)],
            file_path=file_path,
            json_parser=lambda stdout: (
                json.loads(stdout).get("results", []) if stdout.strip() else []
            ),
        )

    # =========================================================================
    # VULTURE - Dead code detection
    # =========================================================================

    def _run_vulture(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
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

    def _run_coverage(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run coverage to measure test coverage."""
        timeout = qc.Quality.QualityPerformance.COVERAGE_TIMEOUT  # CONFIG
        result = SubprocessUtils.run_external_command(
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
            timeout=float(timeout),
            cwd=tempfile.gettempdir(),
        )

        if result.is_failure:
            return self._handle_coverage_error(result.error or "")

        wrapper = result.value
        coverage_data = self._parse_coverage_data()

        return FlextResult.ok({
            "tool": "coverage",
            "coverage_data": coverage_data,
            "status": "success" if wrapper.returncode == 0 else "incomplete",
            "message": "Coverage measurement complete"
            if coverage_data
            else "No coverage data",
        })

    def _handle_coverage_error(
        self,
        error_msg: str,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
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

    def _parse_coverage_data(self) -> dict[str, t.GeneralValueType]:
        """Parse coverage JSON data from temp directory."""
        coverage_path = Path(tempfile.gettempdir()) / ".coverage.json"
        if not coverage_path.exists():
            return {}

        try:
            with coverage_path.open(encoding="utf-8") as f:
                raw_data = json.load(f)
            # Validate and convert to proper type
            if isinstance(raw_data, dict):
                parsed: dict[str, t.GeneralValueType] = {
                    str(k): v for k, v in raw_data.items()
                }
                return parsed
            return {}
        except (json.JSONDecodeError, FileNotFoundError, TypeError, Exception):
            return {}

    # =========================================================================
    # RADON - Complexity metrics
    # =========================================================================

    def _run_radon(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run radon for complexity metrics."""
        timeout = qc.Quality.QualityPerformance.RADON_TIMEOUT  # CONFIG
        # First call: complexity
        result_cc = SubprocessUtils.run_external_command(
            ["radon", "cc", str(file_path), "-j"],
            capture_output=True,
            timeout=float(timeout),
        )

        if result_cc.is_failure:
            return self._handle_radon_error(result_cc.error or "")

        wrapper_cc = result_cc.value
        metrics = self._parse_radon_json(wrapper_cc.stdout)

        # Also get maintainability index
        maintainability = self._run_radon_maintainability(file_path)

        return FlextResult.ok({
            "tool": "radon",
            "complexity": metrics,
            "maintainability": maintainability,
            "status": "success",
        })

    def _handle_radon_error(
        self,
        error_msg: str,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
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

    def _run_radon_maintainability(
        self,
        file_path: Path,
    ) -> dict[str, t.GeneralValueType]:
        """Run radon maintainability index analysis."""
        timeout = qc.Quality.QualityPerformance.RADON_TIMEOUT  # CONFIG
        result_mi = SubprocessUtils.run_external_command(
            ["radon", "mi", str(file_path), "-j"],
            capture_output=True,
            timeout=float(timeout),
        )

        if result_mi.is_success and result_mi.value.stdout.strip():
            return self._parse_radon_json(result_mi.value.stdout)
        return {}

    def _parse_radon_json(self, stdout: str) -> dict[str, t.GeneralValueType]:
        """Parse radon JSON output."""
        if not stdout.strip():
            return {}
        try:
            raw_data = json.loads(stdout)
            if isinstance(raw_data, dict):
                parsed: dict[str, t.GeneralValueType] = {
                    str(k): v for k, v in raw_data.items()
                }
                return parsed
            return {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def _parse_ruff_output(
        self,
        output: str,
    ) -> list[dict[str, t.GeneralValueType]]:
        """Parse ruff JSON output into structured format."""
        try:
            return json.loads(output) if output.strip() else []
        except json.JSONDecodeError:
            return []

    # =========================================================================
    # REFURB - Modern Pattern Suggestions
    # =========================================================================

    def _run_refurb(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run refurb modernization check.

        Refurb suggests modern Python patterns and idioms.

        Args:
            file_path: Path to file to analyze

        Returns:
            FlextResult with modernization suggestions

        """
        timeout = qc.Quality.QualityPerformance.REFURB_TIMEOUT  # CONFIG
        return self._run_tool_with_json_output(
            tool_name="refurb",
            command=["refurb", str(file_path), "--format", "json", "--quiet"],
            file_path=file_path,
            timeout=float(timeout),
            json_parser=self._parse_refurb_output,
        )

    def _parse_refurb_output(
        self,
        stdout: str,
    ) -> list[dict[str, t.GeneralValueType]]:
        """Parse refurb JSON output."""
        if not stdout.strip():
            return []
        try:
            raw_data = json.loads(stdout)
            if isinstance(raw_data, list):
                parsed: list[dict[str, t.GeneralValueType]] = [
                    {str(k): v for k, v in item.items()}
                    for item in raw_data
                    if isinstance(item, dict)
                ]
                return parsed
            return []
        except (json.JSONDecodeError, TypeError):
            # Parse line-based output as fallback
            suggestions: list[dict[str, t.GeneralValueType]] = [
                {"message": line.strip()}
                for line in stdout.strip().splitlines()
                if line.strip()
            ]
            return suggestions

    # =========================================================================
    # COMPLEXIPY - Cognitive Complexity
    # =========================================================================

    def _run_complexipy(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run complexipy cognitive complexity check.

        Args:
            file_path: Path to file to analyze

        Returns:
            FlextResult with cognitive complexity metrics

        """
        max_complexity = qc.Quality.Complexity.COGNITIVE_MAX_COMPLEXITY  # CONFIG
        timeout = qc.Quality.QualityPerformance.COMPLEXIPY_TIMEOUT  # CONFIG

        result = SubprocessUtils.run_external_command(
            [
                "complexipy",
                str(file_path),
                "--max-complexity-allowed",
                str(max_complexity),
            ],
            capture_output=True,
            timeout=float(timeout),
        )

        if result.is_failure:
            return self._handle_tool_error(result.error or "", "complexipy")

        wrapper = result.value
        functions = self._parse_complexipy_output(
            wrapper.stdout, file_path, max_complexity
        )

        # Helper to safely extract complexity
        def get_complexity(func: dict[str, t.GeneralValueType]) -> int:
            complexity = func.get("complexity", 0)
            if isinstance(complexity, int):
                return complexity
            if isinstance(complexity, float):
                return int(complexity)
            if isinstance(complexity, str) and complexity.isdigit():
                return int(complexity)
            return 0

        violations = [f for f in functions if get_complexity(f) > max_complexity]

        return FlextResult.ok({
            "tool": "complexipy",
            "functions": functions,
            "total_functions": len(functions),
            "max_allowed": max_complexity,
            "violations": violations,
            "issue_count": len(violations),
            "status": "success" if wrapper.returncode == 0 else "issues_found",
        })

    def _parse_complexipy_output(
        self,
        stdout: str,
        file_path: Path,
        max_complexity: int,
    ) -> list[dict[str, t.GeneralValueType]]:
        """Parse complexipy table output."""
        functions: list[dict[str, t.GeneralValueType]] = []
        min_parts = (
            qc.Quality.Complexity.COGNITIVE_LOW_THRESHOLD
        )  # CONFIG: minimum parts in output line

        for line in stdout.strip().splitlines():
            if line.strip() and not line.startswith(("Path", "─", "│", "Function")):
                parts = line.split()
                if len(parts) >= min_parts and parts[-1].isdigit():
                    complexity_value = int(parts[-1])
                    functions.append({
                        "function": parts[0],
                        "complexity": complexity_value,
                        "file": str(file_path),
                        "exceeds_threshold": complexity_value > max_complexity,
                    })

        return functions

    # =========================================================================
    # ROPE - AST Refactoring Analysis
    # =========================================================================

    def _run_rope(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run rope AST-based refactoring analysis.

        Provides module structure and function information for refactoring guidance.

        Args:
            file_path: Path to file to analyze

        Returns:
            FlextResult with refactoring suggestions

        """
        if not file_path.exists():
            return FlextResult.ok({
                "tool": "rope",
                "functions": [],
                "function_count": 0,
                "status": "invalid_path",
                "message": f"File not found: {file_path}",
            })

        project = RopeProject(str(file_path.parent))
        try:
            resource = libutils.path_to_resource(project, str(file_path))
            if resource is None:
                return FlextResult.ok({
                    "tool": "rope",
                    "functions": [],
                    "function_count": 0,
                    "status": "no_resource",
                    "message": f"Could not load resource: {file_path}",
                })

            pymodule = project.get_pymodule(resource)

            # Collect function info using module's defined names
            functions: list[dict[str, t.GeneralValueType]] = []
            defined_names = (
                pymodule.get_defined_names()
                if hasattr(pymodule, "get_defined_names")
                else {}
            )
            for name, pyname in defined_names.items():
                if not name.startswith("_"):
                    functions.append({
                        "name": name,
                        "type": str(type(pyname).__name__),
                    })

            return FlextResult.ok({
                "tool": "rope",
                "module": str(file_path.stem),
                "functions": functions,
                "function_count": len(functions),
                "suggestions": [],
                "issue_count": 0,
                "status": "success",
            })
        except Exception as err:
            _logger.warning(f"Rope analysis failed: {err}")
            return FlextResult.ok({
                "tool": "rope",
                "functions": [],
                "function_count": 0,
                "status": "error",
                "message": str(err),
            })
        finally:
            project.close()

    # =========================================================================
    # DUPLICATION - Code clone detection
    # =========================================================================

    def _run_duplication(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run duplication analysis on a file/directory.

        Uses FlextDuplicationPlugin for line-based similarity detection.

        Args:
            file_path: Path to file or directory to analyze.

        Returns:
            FlextResult with duplication analysis results.

        """
        plugin = FlextDuplicationPlugin()

        # If file, analyze against siblings in same directory
        if file_path.is_file():
            parent = file_path.parent
            python_files = list(parent.glob("*.py"))
        else:
            python_files = list(file_path.rglob("*.py"))

        result = plugin.check(python_files)

        if result.is_failure:
            return FlextResult.fail(result.error or "Duplication check failed")

        check_result = result.value
        duplicates_list: list[dict[str, t.GeneralValueType]] = [
            {
                "file1": str(d.file1),
                "file2": str(d.file2),
                "similarity": d.similarity,
                "shared_lines": d.shared_lines,
            }
            for d in check_result.duplicates
        ]

        return FlextResult.ok({
            "tool": "duplication",
            "duplicate_count": check_result.duplicate_count,
            "files_checked": check_result.files_checked,
            "duplicates": duplicates_list,
            "status": "success" if check_result.duplicate_count == 0 else "issues_found",
        })
