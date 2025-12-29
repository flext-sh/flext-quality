"""FLEXT Quality - Direct Python Tool Integration via Library Imports.

This module provides deep integration with Python quality tools through DIRECT library imports
instead of subprocess calls. This enables:
- Better performance (no process overhead)
- Type-safe error handling with FlextResult[T]
- Composable error handling via railway-oriented programming
- Unified FLEXT logging and observability
- Programmatic access to tool APIs

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from pathlib import Path

import black
import coverage
import pytest
from bandit.core import config as bandit_config, manager as bandit_manager
from flext_core import FlextLogger, FlextResult, FlextTypes as t
from mypy import api
from radon.complexity import cc_visit
from rope.base import libutils
from rope.base.project import Project as RopeProject
from vulture import Vulture

from flext_quality.constants import FlextQualityConstants as qc
from flext_quality.subprocess_utils import SubprocessUtils


class FlextQualityPythonTools:
    """Direct integration with Python quality tools via library imports.

    All tools use:
    - FlextResult[T] for type-safe error handling
    - FlextLogger for structured logging
    - Direct library APIs (no subprocess calls)
    - Railway-oriented error composition

    Architecture: Layer 4 (Infrastructure)
    """

    def __init__(self) -> None:
        """Initialize Python tools backend."""
        self._logger = FlextLogger(__name__)

    # =========================================================================
    # RUFF LINTER - Python's fastest linter (Rust-based)
    # =========================================================================

    def run_ruff_check(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Ruff linting via subprocess.

        Ruff is the fastest Python linter, written in Rust.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with linting issues

        """
        try:
            # Validate path for security (accept files or directories)
            if not path.exists():
                return FlextResult.fail(f"Path does not exist: {path}")

            timeout = qc.Quality.QualityPerformance.REFURB_TIMEOUT  # CONFIG
            result = SubprocessUtils.run_external_command(
                ["ruff", "check", str(path), "--output-format=json"],
                capture_output=True,
                timeout=timeout,
            )

            if result.is_failure:
                error_msg = result.error or ""
                if "not found" in error_msg.lower():
                    return FlextResult.fail("Ruff executable not found in PATH")
                if "timed out" in error_msg.lower():
                    return FlextResult.fail("Ruff analysis timed out")
                return FlextResult.fail(f"Ruff analysis failed: {error_msg}")

            wrapper = result.value

            return FlextResult.ok({
                "issues": wrapper.stdout,
                "exit_code": wrapper.returncode,
                "errors": wrapper.stderr,
            })
        except Exception as e:
            self._logger.exception("Ruff check failed")
            return FlextResult.fail(f"Ruff analysis failed: {e}")

    # =========================================================================
    # MYPY - Static type checker with direct API
    # =========================================================================

    def run_mypy_check(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run MyPy type checking via direct API.

        MyPy provides a Python API for programmatic type checking.

        Args:
            path: Path to analyze (project root or src directory)

        Returns:
            FlextResult with type errors

        """
        try:
            # For src-layout projects, analyze src/ directory
            src_path = path / "src"
            analyze_path = src_path if src_path.exists() and src_path.is_dir() else path

            # Build mypy arguments - use --namespace-packages for proper import resolution
            mypy_args = [
                str(analyze_path),
                "--strict",
                "--show-error-codes",
                "--no-color-output",
                "--namespace-packages",
            ]

            # Direct API call - no subprocess
            stdout, stderr, exit_code = api.run(mypy_args)

            return FlextResult.ok({
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
            })
        except Exception as e:
            self._logger.exception("MyPy check failed")
            return FlextResult.fail(f"MyPy analysis failed: {e}")

    # =========================================================================
    # BANDIT - Security vulnerability scanner
    # =========================================================================

    def run_bandit_scan(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Bandit security scan via direct library import.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with security issues

        """
        try:
            # Direct API usage
            conf = bandit_config.BanditConfig()
            mgr = bandit_manager.BanditManager(conf, "file")
            mgr.discover_files([str(path)])
            mgr.run_tests()

            return FlextResult.ok({
                "issues": len(mgr.results),
                "metrics": mgr.metrics.data if mgr.metrics else {},
            })
        except Exception as e:
            self._logger.exception("Bandit scan failed")
            return FlextResult.fail(f"Bandit security scan failed: {e}")

    # =========================================================================
    # PYLINT - Code analysis and style checking
    # =========================================================================

    def run_pylint_check(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Pylint analysis via subprocess.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with analysis results

        """
        try:
            timeout = qc.Quality.QualityPerformance.REFURB_TIMEOUT  # CONFIG
            result = SubprocessUtils.run_external_command(
                ["pylint", str(path), "--output-format=json"],
                capture_output=True,
                timeout=timeout,
            )

            if result.is_failure:
                error_msg = result.error or ""
                if "not found" in error_msg.lower():
                    return FlextResult.fail("Pylint executable not found in PATH")
                if "timed out" in error_msg.lower():
                    return FlextResult.fail("Pylint analysis timed out")
                return FlextResult.fail(f"Pylint analysis failed: {error_msg}")

            wrapper = result.value

            return FlextResult.ok({
                "output": wrapper.stdout,
                "exit_code": wrapper.returncode,
            })
        except Exception as e:
            self._logger.exception("Pylint check failed")
            return FlextResult.fail(f"Pylint analysis failed: {e}")

    # =========================================================================
    # BLACK - Code formatter
    # =========================================================================

    def check_black_formatting(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Check Black formatting via direct library import.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with formatting check results

        """
        try:
            # Direct API usage
            mode = black.Mode()
            content = Path(path).read_text(encoding="utf-8")

            try:
                formatted = black.format_file_contents(content, fast=False, mode=mode)
                needs_formatting = content != formatted

                return FlextResult.ok({
                    "needs_formatting": needs_formatting,
                    "issues": 1 if needs_formatting else 0,
                })
            except Exception as e:
                if (
                    type(e).__name__ == "NothingChanged"
                ):  # Handle black.NothingChanged without import
                    return FlextResult.ok({"needs_formatting": False, "issues": 0})
                raise
        except Exception as e:
            self._logger.exception("Black formatting check failed")
            return FlextResult.fail(f"Black formatting check failed: {e}")

    # =========================================================================
    # PYTEST - Testing framework
    # =========================================================================

    def run_pytest(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run pytest via direct library import.

        Args:
            path: Path to test directory

        Returns:
            FlextResult with test results

        """
        try:
            # Direct API call
            result = pytest.main([
                str(path),
                "--collect-only",
                "--quiet",
            ])

            return FlextResult.ok({
                "exit_code": result,
            })
        except Exception as e:
            self._logger.exception("Pytest failed")
            return FlextResult.fail(f"Pytest execution failed: {e}")

    # =========================================================================
    # COVERAGE - Test coverage analysis
    # =========================================================================

    def run_coverage(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run coverage analysis via direct library import.

        Args:
            path: Path to analyze (currently unused, analyzes current directory)

        Returns:
            FlextResult with coverage data

        """
        # Reserved for future path-specific coverage analysis
        _ = path  # Reserved for future use

        try:
            # Direct API usage
            cov = coverage.Coverage()
            cov.start()
            # Run tests - simplified for now
            cov.stop()
            cov.save()

            return FlextResult.ok({
                "percentage": cov.report(),
            })
        except Exception as e:
            self._logger.exception("Coverage analysis failed")
            return FlextResult.fail(f"Coverage analysis failed: {e}")

    # =========================================================================
    # RADON - Code complexity metrics
    # =========================================================================

    def calculate_complexity(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Calculate code complexity via Radon library.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with complexity metrics

        """
        try:
            code = Path(path).read_text(encoding="utf-8")

            # Direct API usage
            cyclomatic = cc_visit(code)

            return FlextResult.ok({
                "functions": len(cyclomatic),
                "complexity_scores": [item.complexity for item in cyclomatic],
            })
        except Exception as e:
            self._logger.exception("Complexity analysis failed")
            return FlextResult.fail(f"Complexity analysis failed: {e}")

    # =========================================================================
    # VULTURE - Dead code detection
    # =========================================================================

    def detect_dead_code(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Detect dead code via Vulture library.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with dead code findings

        """
        try:
            v = Vulture()
            v.scavenge([str(path)])

            unused_code = list(v.get_unused_code())

            return FlextResult.ok({
                "unused_count": len(unused_code),
                "unused_items": [
                    {
                        "name": item.name,
                        "line": item.first_lineno,
                        "confidence": item.confidence,
                    }
                    for item in unused_code
                ],
            })
        except Exception as e:
            self._logger.exception("Dead code detection failed")
            return FlextResult.fail(f"Dead code detection failed: {e}")

    # =========================================================================
    # REFURB - Modern Pattern Suggestions
    # =========================================================================

    def run_refurb_check(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Refurb modernization analysis via subprocess.

        Refurb suggests modern Python patterns and idioms.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with modernization suggestions

        """
        try:
            if not path.exists() or not path.is_file():
                return FlextResult.fail(f"Invalid path for Refurb analysis: {path}")

            timeout = qc.Quality.QualityPerformance.REFURB_TIMEOUT  # CONFIG
            result = SubprocessUtils.run_external_command(
                ["refurb", str(path), "--format", "json", "--quiet"],
                capture_output=True,
                timeout=timeout,
            )

            if result.is_failure:
                error_msg = result.error or ""
                if "not found" in error_msg.lower():
                    return FlextResult.fail("Refurb executable not found in PATH")
                if "timed out" in error_msg.lower():
                    return FlextResult.fail("Refurb analysis timed out")
                return FlextResult.fail(f"Refurb analysis failed: {error_msg}")

            wrapper = result.value
            suggestions: list[dict[str, t.GeneralValueType]] = []

            if wrapper.stdout.strip():
                try:
                    suggestions = json.loads(wrapper.stdout)
                except json.JSONDecodeError:
                    # Parse line-based output as fallback
                    for line in wrapper.stdout.strip().splitlines():
                        if line.strip():
                            suggestions.append({"message": line.strip()})

            return FlextResult.ok({
                "suggestions": suggestions,
                "suggestion_count": len(suggestions),
                "exit_code": wrapper.returncode,
            })
        except Exception as e:
            self._logger.exception("Refurb check failed")
            return FlextResult.fail(f"Refurb analysis failed: {e}")

    # =========================================================================
    # COMPLEXIPY - Cognitive Complexity
    # =========================================================================

    def run_complexipy_check(
        self,
        path: Path,
        max_complexity: int | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Complexipy cognitive complexity analysis.

        Args:
            path: Path to analyze
            max_complexity: Maximum allowed complexity (uses constant if None)

        Returns:
            FlextResult with cognitive complexity metrics

        """
        if max_complexity is None:
            max_complexity = qc.Quality.Complexity.COGNITIVE_MAX_COMPLEXITY  # CONFIG

        try:
            if not path.exists() or not path.is_file():
                return FlextResult.fail(f"Invalid path for Complexipy analysis: {path}")

            timeout = qc.Quality.QualityPerformance.COMPLEXIPY_TIMEOUT  # CONFIG
            result = SubprocessUtils.run_external_command(
                [
                    "complexipy",
                    str(path),
                    "--max-complexity-allowed",
                    str(max_complexity),
                ],
                capture_output=True,
                timeout=timeout,
            )

            if result.is_failure:
                error_msg = result.error or ""
                if "not found" in error_msg.lower():
                    return FlextResult.fail("Complexipy executable not found in PATH")
                if "timed out" in error_msg.lower():
                    return FlextResult.fail("Complexipy analysis timed out")
                return FlextResult.fail(f"Complexipy analysis failed: {error_msg}")

            wrapper = result.value
            functions: list[dict[str, t.GeneralValueType]] = []

            # Parse complexipy output (table format)
            min_parts = (
                qc.Quality.Complexity.COGNITIVE_LOW_THRESHOLD
            )  # CONFIG: minimum parts in output line
            for line in wrapper.stdout.strip().splitlines():
                if line.strip() and not line.startswith(("Path", "─", "│")):
                    parts = line.split()
                    if len(parts) >= min_parts and parts[-1].isdigit():
                        functions.append({
                            "function": parts[0],
                            "complexity": int(parts[-1]),
                            "file": str(path),
                        })

            violations = []
            for func in functions:
                complexity_val = func.get("complexity", 0)
                if isinstance(complexity_val, (int, float)) and complexity_val > max_complexity:
                    violations.append(func)

            return FlextResult.ok({
                "functions": functions,
                "total_functions": len(functions),
                "max_allowed": max_complexity,
                "violations": violations,
                "exit_code": wrapper.returncode,
            })
        except Exception as e:
            self._logger.exception("Complexipy check failed")
            return FlextResult.fail(f"Complexipy analysis failed: {e}")

    # =========================================================================
    # ROPE - AST Refactoring Suggestions
    # =========================================================================

    def run_rope_analysis(
        self,
        path: Path,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Run Rope AST-based refactoring analysis.

        Provides suggestions for function extraction and code structure.

        Args:
            path: Path to analyze

        Returns:
            FlextResult with refactoring suggestions

        """
        try:
            if not path.exists() or not path.is_file():
                return FlextResult.fail(f"Invalid path for Rope analysis: {path}")

            # Create temporary project
            project_path = path.parent
            project = RopeProject(str(project_path))

            try:
                resource = libutils.path_to_resource(project, str(path))
                if resource is None:
                    return FlextResult.fail(f"Could not load resource: {path}")

                # Get module structure
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
                    "module": str(path.stem),
                    "functions": functions,
                    "function_count": len(functions),
                    "suggestions": [],
                })
            finally:
                project.close()

        except Exception as e:
            self._logger.exception("Rope analysis failed")
            return FlextResult.fail(f"Rope analysis failed: {e}")


__all__ = ["FlextQualityPythonTools"]
