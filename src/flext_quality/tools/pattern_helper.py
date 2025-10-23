"""FLEXT pattern validation helper - Check code for FLEXT architecture patterns.

Pragmatic utilities for:
- Validating import patterns (root-level only)
- Detecting exception-based error handling
- Verifying single-class-per-module rule
- Checking FlextResult[T] usage patterns

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult


def check_all_flext_patterns(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Run all FLEXT pattern validation checks on a project.

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with comprehensive pattern validation results

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()

        # Run all pattern checks
        import_check = pattern_auditor.check_import_patterns(str(project_path))
        exception_check = pattern_auditor.check_exception_patterns(str(project_path))
        module_check = pattern_auditor.check_module_structure(str(project_path))
        result_check = pattern_auditor.check_flext_result_usage(str(project_path))

        # Combine results
        all_issues = []
        if import_check.is_success:
            import_data = import_check.value
            all_issues.extend(import_data.get("violations", []))

        if exception_check.is_success:
            exc_data = exception_check.value
            all_issues.extend(exc_data.get("issues", []))

        if module_check.is_success:
            module_data = module_check.value
            all_issues.extend(module_data.get("issues", []))

        if result_check.is_success:
            result_data = result_check.value
            all_issues.extend(result_data.get("issues", []))

        return FlextResult.ok({
            "project": str(project_path),
            "total_issues": len(all_issues),
            "issues": all_issues,
            "checks": {
                "import_patterns": import_check.value
                if import_check.is_success
                else {},
                "exception_patterns": exception_check.value
                if exception_check.is_success
                else {},
                "module_structure": module_check.value
                if module_check.is_success
                else {},
                "result_usage": result_check.value if result_check.is_success else {},
            },
            "status": "all_passed" if len(all_issues) == 0 else "issues_found",
        })

    except Exception as e:
        return FlextResult.fail(f"Pattern validation failed: {e}")


def check_import_patterns(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Check for FLEXT import pattern violations.

    FLEXT requires root-level imports:
    ✅ from flext_core import FlextResult
    ❌ from flext_core.result import FlextResult

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with import pattern violations

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()
        return pattern_auditor.check_import_patterns(str(project_path))

    except Exception as e:
        return FlextResult.fail(f"Import pattern check failed: {e}")


def check_exception_patterns(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Check for exception-based error handling in business logic.

    FLEXT requires FlextResult[T] for business logic errors:
    ✅ return FlextResult[Data].fail("error message")
    ❌ raise ValueError("error message")

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with exception usage findings

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()
        return pattern_auditor.check_exception_patterns(str(project_path))

    except Exception as e:
        return FlextResult.fail(f"Exception pattern check failed: {e}")


def check_module_structure(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Check for single-class-per-module FLEXT rule.

    FLEXT requires each module to contain one primary class:
    ✅ one main class per module (nested helper classes OK)
    ❌ multiple public classes in one module

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with module structure findings

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()
        return pattern_auditor.check_module_structure(str(project_path))

    except Exception as e:
        return FlextResult.fail(f"Module structure check failed: {e}")


def check_flext_result_usage(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Check FlextResult[T] usage patterns comprehensively.

    Validates:
    - Functions returning FlextResult have proper type parameters
    - Error handling uses railway-oriented pattern
    - No direct exception raising in business logic

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with usage pattern findings

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()
        return pattern_auditor.check_flext_result_usage(str(project_path))

    except Exception as e:
        return FlextResult.fail(f"FlextResult usage check failed: {e}")


def audit_flext_patterns(
    project_path: Path,
) -> FlextResult[dict[str, object]]:
    """Run the original pattern audit (validates FlextResult return patterns).

    This is the foundational pattern check that validates FlextResult[T]
    methods are using proper return patterns.

    Args:
        project_path: Directory to analyze

    Returns:
        FlextResult with audit results

    """
    try:
        from .quality_operations import FlextQualityOperations

        pattern_auditor = FlextQualityOperations.PatternAuditor()
        return pattern_auditor.audit_patterns(str(project_path))

    except Exception as e:
        return FlextResult.fail(f"Pattern audit failed: {e}")
