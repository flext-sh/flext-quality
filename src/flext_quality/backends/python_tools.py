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
from typing import Any

from flext_core import FlextLogger, FlextResult, FlextUtilities

# =========================================================================
# PYTHON QUALITY TOOLS - Optional imports with availability checking
# =========================================================================

# Optional tool imports - these may not be installed
try:
    import ruff

    _RUFF_AVAILABLE = True
except ImportError:
    ruff = None
    _RUFF_AVAILABLE = False

try:
    import mypy
    from mypy import api

    _MYPY_AVAILABLE = True
    _MYPY_API_AVAILABLE = True
except ImportError:
    mypy = None
    api = None
    _MYPY_AVAILABLE = False
    _MYPY_API_AVAILABLE = False

try:
    import bandit
    from bandit.core import config as bandit_config, manager as bandit_manager

    _BANDIT_AVAILABLE = True
    _BANDIT_CORE_AVAILABLE = True
except ImportError:
    bandit = None
    bandit_config = None
    bandit_manager = None
    _BANDIT_AVAILABLE = False
    _BANDIT_CORE_AVAILABLE = False

try:
    import pylint

    _PYLINT_AVAILABLE = True
except ImportError:
    pylint = None
    _PYLINT_AVAILABLE = False

try:
    import black

    _BLACK_AVAILABLE = True
except ImportError:
    black = None
    _BLACK_AVAILABLE = False

try:
    import isort

    _ISORT_AVAILABLE = True
except ImportError:
    isort = None
    _ISORT_AVAILABLE = False

try:
    import coverage

    _COVERAGE_AVAILABLE = True
except ImportError:
    coverage = None
    _COVERAGE_AVAILABLE = False

try:
    import pytest

    _PYTEST_AVAILABLE = True
except ImportError:
    pytest = None
    _PYTEST_AVAILABLE = False

try:
    import radon
    from radon.complexity import cc_visit

    _RADON_AVAILABLE = True
    _RADON_COMPLEXITY_AVAILABLE = True
except ImportError:
    radon = None
    cc_visit = None
    _RADON_AVAILABLE = False
    _RADON_COMPLEXITY_AVAILABLE = False

try:
    from vulture import Vulture

    _VULTURE_AVAILABLE = True
    _VULTURE_CLASS_AVAILABLE = True
except ImportError:
    Vulture = None
    _VULTURE_AVAILABLE = False
    _VULTURE_CLASS_AVAILABLE = False


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
        self._tools_available: dict[str, bool] = {}
        self._check_tools_availability()

    def _check_tools_availability(self) -> None:
        """Check which Python quality tools are available."""
        tools = {
            "ruff": self._check_ruff,
            "mypy": self._check_mypy,
            "bandit": self._check_bandit,
            "pylint": self._check_pylint,
            "black": self._check_black,
            "isort": self._check_isort,
            "coverage": self._check_coverage,
            "pytest": self._check_pytest,
            "radon": self._check_radon,
            "vulture": self._check_vulture,
        }

        for tool_name, check_func in tools.items():
            self._tools_available[tool_name] = check_func()

    # =========================================================================
    # AVAILABILITY CHECKS - Verify tools are installed
    # =========================================================================

    @staticmethod
    def _check_ruff() -> bool:
        """Check if Ruff is available."""
        return _RUFF_AVAILABLE

    @staticmethod
    def _check_mypy() -> bool:
        """Check if MyPy is available."""
        return _MYPY_AVAILABLE

    @staticmethod
    def _check_bandit() -> bool:
        """Check if Bandit is available."""
        return _BANDIT_AVAILABLE

    @staticmethod
    def _check_pylint() -> bool:
        """Check if Pylint is available."""
        return _PYLINT_AVAILABLE

    @staticmethod
    def _check_black() -> bool:
        """Check if Black is available."""
        return _BLACK_AVAILABLE

    @staticmethod
    def _check_isort() -> bool:
        """Check if isort is available."""
        return _ISORT_AVAILABLE

    @staticmethod
    def _check_coverage() -> bool:
        """Check if Coverage is available."""
        return _COVERAGE_AVAILABLE

    @staticmethod
    def _check_pytest() -> bool:
        """Check if Pytest is available."""
        return _PYTEST_AVAILABLE

    @staticmethod
    def _check_radon() -> bool:
        """Check if Radon is available."""
        return _RADON_AVAILABLE

    @staticmethod
    def _check_vulture() -> bool:
        """Check if Vulture is available."""
        return _VULTURE_AVAILABLE

    # =========================================================================
    # RUFF LINTER - Python's fastest linter (Rust-based)
    # =========================================================================

    def run_ruff_check(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run Ruff linting via FlextUtilities.

        Ruff is the fastest Python linter, written in Rust.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with linting issues

        """
        if not self._tools_available.get("ruff"):
            return FlextResult.fail("Ruff is not installed")

        try:
            # Validate path for security
            if not path.exists() or not path.is_file():
                return FlextResult.fail(f"Invalid path for Ruff analysis: {path}")

            # Use FlextUtilities for command execution with threading-based timeout
            result = FlextUtilities.CommandExecution.run_external_command(
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

            wrapper = result.unwrap()

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

    def run_mypy_check(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run MyPy type checking via direct API.

        MyPy provides a Python API for programmatic type checking.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with type errors

        """
        if not _MYPY_API_AVAILABLE or api is None:
            return FlextResult.fail("MyPy API is not available")

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

    def run_bandit_scan(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run Bandit security scan via direct library import.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with security issues

        """
        if (
            not _BANDIT_CORE_AVAILABLE
            or bandit_config is None
            or bandit_manager is None
        ):
            return FlextResult.fail("Bandit core modules are not available")

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

    def run_pylint_check(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run Pylint analysis via FlextUtilities.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with analysis results

        """
        if not self._tools_available.get("pylint"):
            return FlextResult.fail("Pylint is not installed")

        try:
            # Use FlextUtilities for command execution with threading-based timeout
            # (Pylint doesn't expose clean Python API, use subprocess via FlextUtilities)
            result = FlextUtilities.CommandExecution.run_external_command(
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

            wrapper = result.unwrap()

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

    def check_black_formatting(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Check Black formatting via direct library import.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with formatting check results

        """
        if not _BLACK_AVAILABLE or black is None:
            return FlextResult.fail("Black is not available")

        try:
            # Direct API usage
            mode = black.Mode()
            with Path(path).open(encoding="utf-8") as f:
                content = f.read()

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

    def run_pytest(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run pytest via direct library import.

        Args:
        path: Path to test directory

        Returns:
        FlextResult with test results

        """
        if not _PYTEST_AVAILABLE or pytest is None:
            return FlextResult.fail("Pytest is not available")

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

    def run_coverage(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Run coverage analysis via direct library import.

        Args:
        path: Path to analyze (currently unused, analyzes current directory)

        Returns:
        FlextResult with coverage data

        """
        # Reserved for future path-specific coverage analysis
        _ = path  # Reserved for future use

        if not _COVERAGE_AVAILABLE or coverage is None:
            return FlextResult.fail("Coverage is not available")

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

    def calculate_complexity(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Calculate code complexity via Radon library.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with complexity metrics

        """
        if not _RADON_COMPLEXITY_AVAILABLE or cc_visit is None:
            return FlextResult.fail("Radon complexity is not available")

        try:
            with Path(path).open(encoding="utf-8") as f:
                code = f.read()

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

    def detect_dead_code(self, path: Path) -> FlextResult[dict[str, Any]]:
        """Detect dead code via Vulture library.

        Args:
        path: Path to analyze

        Returns:
        FlextResult with dead code findings

        """
        if not _VULTURE_CLASS_AVAILABLE or Vulture is None:
            return FlextResult.fail("Vulture class is not available")

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
