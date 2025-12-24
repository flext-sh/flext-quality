"""Test assistance helper - Simple test quality analysis using coverage.py.

Pragmatic, lightweight utilities for:
- Identifying test coverage gaps
- Suggesting missing tests based on coverage data
- Validating test patterns

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path

from flext import FlextResult

from flext_quality.subprocess_utils import SubprocessUtils

# Test coverage thresholds
MIN_TEST_COVERAGE_THRESHOLD = 80


def suggest_tests_from_coverage(project_path: Path) -> FlextResult[list[str]]:
    """Suggest tests for untested code based on coverage analysis.

    Args:
        project_path: Project directory to analyze

    Returns:
        FlextResult with list of test suggestions

    """
    try:
        # Run coverage to generate report
        result = SubprocessUtils.run_external_command(
            [
                "pytest",
                str(project_path),
                "--cov=.",
                "--cov-report=json",
                "-q",
            ],
            capture_output=True,
            timeout=120.0,
            cwd=str(project_path),
        )

        if result.is_failure:
            return _handle_coverage_error(result.error or "")

        suggestions = _extract_low_coverage_files(project_path)
        return FlextResult.ok(
            suggestions or ["All modules have >80% coverage - good job!"],
        )

    except Exception as e:
        return FlextResult.fail(f"Coverage analysis failed: {e}")


def _handle_coverage_error(error_msg: str) -> FlextResult[list[str]]:
    """Handle coverage command errors.

    Args:
        error_msg: Error message from command

    Returns:
        FlextResult with appropriate message

    """
    if "not found" in error_msg.lower():
        return FlextResult.ok([
            "Install pytest and coverage to analyze test coverage",
        ])
    if "timed out" in error_msg.lower():
        return FlextResult.fail("Coverage analysis timed out")
    return FlextResult.fail(f"Coverage analysis failed: {error_msg}")


def _extract_low_coverage_files(project_path: Path) -> list[str]:
    """Extract files with low test coverage.

    Args:
        project_path: Path to project root

    Returns:
        List of suggestions for files with low coverage

    """
    suggestions = []
    coverage_file = project_path / ".coverage.json"
    if not coverage_file.exists():
        return suggestions

    with Path(coverage_file).open(encoding="utf-8") as f:
        coverage_data = json.load(f)

    # Extract files with low coverage
    if "files" not in coverage_data:
        return suggestions

    for file_path, file_data in coverage_data["files"].items():
        if "summary" not in file_data:
            continue
        coverage = file_data["summary"].get("percent_covered", 100)
        if coverage < MIN_TEST_COVERAGE_THRESHOLD:
            suggestions.append(
                f"Add tests for {file_path} ({coverage:.1f}% coverage)",
            )

    return suggestions


def check_test_quality(test_file: Path) -> FlextResult[dict[str, object]]:
    """Check test file quality and patterns.

    Args:
        test_file: Test file to analyze

    Returns:
        FlextResult with quality analysis dict

    """
    try:
        with Path(test_file).open(encoding="utf-8") as f:
            content = f.read()

        issues = []

        # Simple pattern checks
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            # Look ahead for assertions
            next_lines = "\n".join(lines[i : min(i + 20, len(lines))])

            # Check for tests without assertions
            if (
                "def test_" in line
                and "assert" not in next_lines
                and "assert" not in next_lines
            ):
                issues.append(f"Line {i}: Test function may lack assertions")

            # Check for bare except
            if "except:" in line and "Exception" not in line:
                issues.append(f"Line {i}: Bare except clause found - too broad")

            # Check for try/except hiding failures
            if "except:" in line and "pass" in next_lines:
                issues.append(f"Line {i}: Exception caught and ignored with pass")

        return FlextResult.ok({
            "file": str(test_file),
            "total_issues": len(issues),
            "issues": issues,
            "quality": "good" if len(issues) == 0 else "needs_improvement",
        })

    except Exception as e:
        return FlextResult.fail(f"Test quality check failed: {e}")


def validate_test_execution(test_path: Path) -> FlextResult[dict[str, object]]:
    """Validate that tests execute successfully.

    Args:
        test_path: Path to test file or directory

    Returns:
        FlextResult with test execution results

    """
    try:
        result = SubprocessUtils.run_external_command(
            ["pytest", str(test_path), "-v", "--tb=short"],
            capture_output=True,
            timeout=120.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "not found" in error_msg.lower():
                return FlextResult.ok({
                    "file": str(test_path),
                    "status": "tool_not_found",
                    "message": "pytest not installed",
                })
            if "timed out" in error_msg.lower():
                return FlextResult.fail("Test execution timed out")
            return FlextResult.fail(f"Test execution failed: {error_msg}")

        wrapper = result.value

        # Parse output for summary
        output_lines = wrapper.stdout.splitlines()
        summary_line = [
            line for line in output_lines if "passed" in line or "failed" in line
        ]

        return FlextResult.ok({
            "file": str(test_path),
            "status": "passed" if wrapper.returncode == 0 else "failed",
            "return_code": wrapper.returncode,
            "summary": summary_line[-1] if summary_line else "No summary",
        })

    except Exception as e:
        return FlextResult.fail(f"Test execution failed: {e}")
