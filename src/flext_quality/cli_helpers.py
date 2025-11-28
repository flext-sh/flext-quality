"""CLI commands for quality helpers - test, documentation, example, and pattern validation.

Provides command-line interface for:
- Test quality analysis and coverage suggestions
- Documentation quality checking (docstrings, API docs)
- Example validation and execution
- FLEXT pattern compliance checking

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult

from .tools import (
    analyze_api_documentation,
    audit_flext_patterns,
    check_all_flext_patterns,
    check_docstring_coverage,
    check_example_structure,
    check_exception_patterns,
    check_flext_result_usage,
    check_import_patterns,
    check_module_structure,
    check_test_quality,
    run_example_safely,
    suggest_docstring_improvements,
    suggest_tests_from_coverage,
    validate_example_imports,
    validate_examples_directory,
    validate_google_style_docstrings,
    validate_test_execution,
)


class QualityHelperCommands:
    """Unified interface for quality helper CLI commands."""

    # ==========================================================================
    # TEST COMMANDS
    # ==========================================================================

    @staticmethod
    def test_coverage(project_path: str) -> FlextResult[list[str]]:
        """Suggest tests for untested code based on coverage analysis.

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with test suggestions

        """
        return suggest_tests_from_coverage(Path(project_path))

    @staticmethod
    def test_quality(test_file: str) -> FlextResult[dict[str, object]]:
        """Check test file quality and patterns.

        Args:
            test_file: Path to test file to analyze

        Returns:
            FlextResult with quality analysis

        """
        return check_test_quality(Path(test_file))

    @staticmethod
    def test_execute(test_path: str) -> FlextResult[dict[str, object]]:
        """Validate that tests execute successfully.

        Args:
            test_path: Path to test file or directory

        Returns:
            FlextResult with execution results

        """
        return validate_test_execution(Path(test_path))

    # ==========================================================================
    # DOCUMENTATION COMMANDS
    # ==========================================================================

    @staticmethod
    def docs_coverage(module_path: str) -> FlextResult[dict[str, object]]:
        """Check docstring coverage percentage in module.

        Args:
            module_path: Path to Python module

        Returns:
            FlextResult with coverage statistics

        """
        return check_docstring_coverage(Path(module_path))

    @staticmethod
    def docs_validate(module_path: str) -> FlextResult[dict[str, object]]:
        """Validate docstrings follow Google style format.

        Args:
            module_path: Path to Python module

        Returns:
            FlextResult with validation results

        """
        return validate_google_style_docstrings(Path(module_path))

    @staticmethod
    def docs_suggest(module_path: str) -> FlextResult[list[str]]:
        """Suggest docstring improvements.

        Args:
            module_path: Path to Python module

        Returns:
            FlextResult with list of suggestions

        """
        return suggest_docstring_improvements(Path(module_path))

    @staticmethod
    def docs_analyze(module_path: str) -> FlextResult[dict[str, object]]:
        """Analyze API documentation completeness.

        Args:
            module_path: Path to Python module

        Returns:
            FlextResult with API documentation analysis

        """
        return analyze_api_documentation(Path(module_path))

    # ==========================================================================
    # EXAMPLE COMMANDS
    # ==========================================================================

    @staticmethod
    def examples_validate(examples_dir: str) -> FlextResult[dict[str, object]]:
        """Run all example.py files and validate they work.

        Args:
            examples_dir: Directory containing examples

        Returns:
            FlextResult with validation results

        """
        return validate_examples_directory(Path(examples_dir))

    @staticmethod
    def examples_structure(example_dir: str) -> FlextResult[dict[str, object]]:
        """Check if example directory has proper structure.

        Args:
            example_dir: Path to example directory

        Returns:
            FlextResult with structure validation

        """
        return check_example_structure(Path(example_dir))

    @staticmethod
    def examples_imports(example_file: str) -> FlextResult[dict[str, object]]:
        """Check that all imports in example file are available.

        Args:
            example_file: Path to example Python file

        Returns:
            FlextResult with import validation

        """
        return validate_example_imports(Path(example_file))

    @staticmethod
    def examples_run(
        example_file: str, timeout: int = 30
    ) -> FlextResult[dict[str, object]]:
        """Safely run an example file with timeout and output capture.

        Args:
            example_file: Path to example file
            timeout: Timeout in seconds (default 30)

        Returns:
            FlextResult with execution results

        """
        return run_example_safely(Path(example_file), timeout=timeout)

    # ==========================================================================
    # PATTERN VALIDATION COMMANDS
    # ==========================================================================

    @staticmethod
    def patterns_all(project_path: str) -> FlextResult[dict[str, object]]:
        """Run all FLEXT pattern validation checks.

        Validates:
        - Import patterns (root-level only)
        - Exception patterns (use FlextResult instead)
        - Module structure (single-class-per-module)
        - FlextResult[T] usage patterns

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with comprehensive validation results

        """
        return check_all_flext_patterns(Path(project_path))

    @staticmethod
    def patterns_imports(project_path: str) -> FlextResult[dict[str, object]]:
        """Check for FLEXT import pattern violations.

        FLEXT requires root-level imports only:
        ✅ from flext_core import FlextResult
        ❌ from flext_core.result import FlextResult

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with import pattern violations

        """
        return check_import_patterns(Path(project_path))

    @staticmethod
    def patterns_exceptions(project_path: str) -> FlextResult[dict[str, object]]:
        """Check for exception-based error handling (should use FlextResult).

        FLEXT requires FlextResult[T] for business logic errors:
        ✅ return FlextResult[Data].fail("error message")
        ❌ raise ValueError("error message")

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with exception usage findings

        """
        return check_exception_patterns(Path(project_path))

    @staticmethod
    def patterns_structure(project_path: str) -> FlextResult[dict[str, object]]:
        """Check for single-class-per-module FLEXT rule.

        FLEXT requires each module to contain one primary class:
        ✅ one main class per module (nested helper classes OK)
        ❌ multiple public classes in one module

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with module structure findings

        """
        return check_module_structure(Path(project_path))

    @staticmethod
    def patterns_result(project_path: str) -> FlextResult[dict[str, object]]:
        """Check FlextResult[T] usage patterns comprehensively.

        Validates:
        - Functions returning FlextResult have proper type parameters
        - Error handling uses railway-oriented pattern
        - No direct exception raising in business logic

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with usage pattern findings

        """
        return check_flext_result_usage(Path(project_path))

    @staticmethod
    def patterns_audit(project_path: str) -> FlextResult[dict[str, object]]:
        """Run foundational pattern audit (validates FlextResult return patterns).

        This checks that FlextResult[T] methods are using proper return patterns.

        Args:
            project_path: Path to project directory

        Returns:
            FlextResult with audit results

        """
        return audit_flext_patterns(Path(project_path))


__all__ = ["QualityHelperCommands"]
