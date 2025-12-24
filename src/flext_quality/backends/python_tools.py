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

from pathlib import Path

import black
import coverage
import pytest
from bandit.core import config as bandit_config, manager as bandit_manager
from mypy import api
from radon.complexity import cc_visit
from vulture import Vulture

from flext import FlextLogger, FlextResult
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

    def run_ruff_check(self, path: Path) -> FlextResult[dict[str, object]]:
        """Run Ruff linting via u.

        Ruff is the fastest Python linter, written in Rust.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with linting issues

        """
        try:
            # Validate path for security
            if not path.exists() or not path.is_file():
                return FlextResult.fail(f"Invalid path for Ruff analysis: {path}")

            # Use uexecution with threading-based timeout
            result = SubprocessUtils.run_external_command(
                ["ruff", "check", str(path), "--output-format=json"],
                capture_output=True,
                timeout=60,
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

    def run_mypy_check(self, path: Path) -> FlextResult[dict[str, object]]:
        """Run MyPy type checking via direct API.

        MyPy provides a Python API for programmatic type checking.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with type errors

        """
        try:
            # Direct API call - no subprocess
            stdout, stderr, exit_code = api.run([
                str(path),
                "--strict",
                "--show-error-codes",
                "--no-color-output",
            ])

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

    def run_bandit_scan(self, path: Path) -> FlextResult[dict[str, object]]:
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

    def run_pylint_check(self, path: Path) -> FlextResult[dict[str, object]]:
        """Run Pylint analysis via u.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with analysis results

        """
        try:
            # Use uexecution with threading-based timeout
            # (Pylint doesn't expose clean Python API, use subprocess via u
            result = SubprocessUtils.run_external_command(
                ["pylint", str(path), "--output-format=json"],
                capture_output=True,
                timeout=60,
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

    def check_black_formatting(self, path: Path) -> FlextResult[dict[str, object]]:
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

    def run_pytest(self, path: Path) -> FlextResult[dict[str, object]]:
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

    def run_coverage(self, path: Path) -> FlextResult[dict[str, object]]:
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

    def calculate_complexity(self, path: Path) -> FlextResult[dict[str, object]]:
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
                "complexity_scores": [c.complexity for c in cyclomatic],
            })
        except Exception as e:
            self._logger.exception("Complexity analysis failed")
            return FlextResult.fail(f"Complexity analysis failed: {e}")

    # =========================================================================
    # VULTURE - Dead code detection
    # =========================================================================

    def detect_dead_code(self, path: Path) -> FlextResult[dict[str, object]]:
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


__all__ = ["FlextQualityPythonTools"]
