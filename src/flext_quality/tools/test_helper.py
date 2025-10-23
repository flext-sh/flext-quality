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

from flext_core import FlextResult, FlextUtilities


def suggest_tests_from_coverage(project_path: Path) -> FlextResult[list[str]]:
    """Suggest tests for untested code based on coverage analysis.

    Args:
        project_path: Project directory to analyze

    Returns:
        FlextResult with list of test suggestions

    """
    try:
        # Run coverage to generate report
        result = FlextUtilities.run_external_command(
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
            if "not found" in result.error.lower():
                return FlextResult.ok([
                    "Install pytest and coverage to analyze test coverage"
                ])
            if "timed out" in result.error.lower():
                return FlextResult.fail("Coverage analysis timed out")
            return FlextResult.fail(f"Coverage analysis failed: {result.error}")

        suggestions = []

        # Try to parse coverage JSON
        coverage_file = project_path / ".coverage.json"
        if coverage_file.exists():
            with Path(coverage_file).open(encoding="utf-8") as f:
                coverage_data = json.load(f)

            # Extract files with low coverage
            if "files" in coverage_data:
                for file_path, file_data in coverage_data["files"].items():
                    if "summary" in file_data:
                        coverage = file_data["summary"].get("percent_covered", 100)
                        if coverage < 80:
                            suggestions.append(
                                f"Add tests for {file_path} ({coverage:.1f}% coverage)"
                            )

        return FlextResult.ok(
            suggestions or ["All modules have >80% coverage - good job!"]
        )

    except Exception as e:
        return FlextResult.fail(f"Coverage analysis failed: {e}")


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
            # Check for tests without assertions
            if "def test_" in line:
                # Look ahead for assertions
                next_lines = "\n".join(lines[i : min(i + 20, len(lines))])
                if "assert" not in next_lines and "assert" not in next_lines:
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
        result = FlextUtilities.run_external_command(
            ["pytest", str(test_path), "-v", "--tb=short"],
            capture_output=True,
            timeout=120.0,
        )

        if result.is_failure:
            if "not found" in result.error.lower():
                return FlextResult.ok({
                    "file": str(test_path),
                    "status": "tool_not_found",
                    "message": "pytest not installed",
                })
            if "timed out" in result.error.lower():
                return FlextResult.fail("Test execution timed out")
            return FlextResult.fail(f"Test execution failed: {result.error}")

        wrapper = result.unwrap()

        # Parse output for summary
        output_lines = wrapper.stdout.splitlines()
        summary_line = [l for l in output_lines if "passed" in l or "failed" in l]

        return FlextResult.ok({
            "file": str(test_path),
            "status": "passed" if wrapper.returncode == 0 else "failed",
            "return_code": wrapper.returncode,
            "summary": summary_line[-1] if summary_line else "No summary",
        })

    except Exception as e:
        return FlextResult.fail(f"Test execution failed: {e}")
