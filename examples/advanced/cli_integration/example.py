#!/usr/bin/env python3
"""FLEXT Quality - Advanced CLI Integration Example.

This example demonstrates advanced usage patterns including:
- CLI command execution and automation
- Quality thresholds and automated decision making
- Integration with CI/CD workflows
- Batch project analysis
- Custom reporting formats

This showcases enterprise-grade automation capabilities for quality gates.
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def run_cli_analysis(project_path: str, format_type: str = "json") -> dict[str, Any]:
    """Run FLEXT Quality CLI analysis and return parsed results.

    Args:
        project_path: Path to project to analyze
        format_type: Output format (json, html, text)

    Returns:
        Parsed analysis results

    """
    # Build CLI command with correct arguments
    cmd = [
        sys.executable,
        "-m",
        "flext_quality.cli",
        "analyze",
        project_path,
        "--format",
        format_type,
        # Note: All analysis types are enabled by default
        # Use --no-security, --no-complexity, etc. to disable
    ]

    try:
        # Execute CLI command
        result = subprocess.run(  # noqa: S603 - CLI quality tool execution, cmd is constructed from validated params
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
        )

        # CLI may return non-zero exit code for validation but still output valid JSON
        if format_type == "json" and result.stdout.strip():
            import json

            try:
                parsed_json = json.loads(result.stdout)
                if result.returncode != 0:
                    pass
                return parsed_json
            except json.JSONDecodeError:
                return {"error": "JSON parsing failed", "raw_output": result.stdout}
        elif result.returncode == 0:
            return {"output": result.stdout, "format": format_type}
        else:
            return {
                "error": f"CLI failed: {result.stderr}",
                "exit_code": result.returncode,
            }

    except subprocess.TimeoutExpired:
        return {"error": "Analysis timeout"}
    except Exception as e:
        return {"error": str(e)}


def check_quality_thresholds(results: dict[str, Any]) -> dict[str, Any]:
    """Check analysis results against quality thresholds.

    Args:
        results: Analysis results from CLI

    Returns:
        Quality gate decision and details

    """
    # Define enterprise quality thresholds
    thresholds = {
        "min_score": 80.0,  # Minimum overall score
        "max_security_issues": 0,  # Zero security issues allowed
        "max_complexity_issues": 5,  # Maximum complexity issues
        "max_critical_issues": 2,  # Maximum critical issues
        "min_files_analyzed": 1,  # Must analyze at least 1 file
    }

    # Extract metrics for threshold checking
    analysis_results = results.get("analysis_results", {})
    issues = analysis_results.get("issues", {})

    # Count issues by category
    security_count = len(issues.get("security", []))
    complexity_count = len(issues.get("complexity", []))

    # Calculate total critical issues (security + high complexity)
    critical_issues = security_count
    for issue in issues.get("complexity", []):
        if isinstance(issue, dict) and issue.get("severity") == "high":
            critical_issues += 1

    files_analyzed = analysis_results.get("files_analyzed", 0)

    # Mock quality score calculation (would come from actual analysis)
    total_issues = sum(
        len(issue_list)
        for issue_list in issues.values()
        if isinstance(issue_list, list)
    )
    estimated_score = max(0, 100 - (total_issues * 10) - (security_count * 20))

    # Check each threshold
    checks = {
        "score_check": {
            "passed": estimated_score >= thresholds["min_score"],
            "value": estimated_score,
            "threshold": thresholds["min_score"],
            "message": f"Quality Score: {estimated_score:.1f} (min: {thresholds['min_score']})",
        },
        "security_check": {
            "passed": security_count <= thresholds["max_security_issues"],
            "value": security_count,
            "threshold": thresholds["max_security_issues"],
            "message": f"Security Issues: {security_count} (max: {thresholds['max_security_issues']})",
        },
        "complexity_check": {
            "passed": complexity_count <= thresholds["max_complexity_issues"],
            "value": complexity_count,
            "threshold": thresholds["max_complexity_issues"],
            "message": f"Complexity Issues: {complexity_count} (max: {thresholds['max_complexity_issues']})",
        },
        "critical_check": {
            "passed": critical_issues <= thresholds["max_critical_issues"],
            "value": critical_issues,
            "threshold": thresholds["max_critical_issues"],
            "message": f"Critical Issues: {critical_issues} (max: {thresholds['max_critical_issues']})",
        },
        "files_check": {
            "passed": files_analyzed >= thresholds["min_files_analyzed"],
            "value": files_analyzed,
            "threshold": thresholds["min_files_analyzed"],
            "message": f"Files Analyzed: {files_analyzed} (min: {thresholds['min_files_analyzed']})",
        },
    }

    # Display results
    passed_checks = 0
    for check_data in checks.values():
        "✅ PASS" if check_data["passed"] else "❌ FAIL"
        if check_data["passed"]:
            passed_checks += 1

    # Overall decision
    all_passed = passed_checks == len(checks)
    return {
        "quality_gate_passed": all_passed,
        "passed_checks": passed_checks,
        "total_checks": len(checks),
        "checks": checks,
        "recommendation": "APPROVE" if all_passed else "REJECT",
    }


def demonstrate_batch_analysis() -> None:
    """Demonstrate batch analysis of multiple projects."""
    # Create sample projects for demonstration
    projects = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample project 1: High quality
        proj1 = temp_path / "high_quality_project"
        proj1.mkdir()
        (proj1 / "main.py").write_text('''
def hello_world():
    """Simple hello world function."""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
''')

        # Create sample project 2: Low quality with issues
        proj2 = temp_path / "low_quality_project"
        proj2.mkdir()
        (proj2 / "problematic.py").write_text("""
import os
import unused_module  # Dead code

def complex_function(x, y, z, a, b, c):
    if x > 0:
        if y > 0:
            if z > 0:
                if a > 0:
                    if b > 0:
                        if c > 0:
                            return eval(f"{x} + {y}")  # Security issue
                        else:
                            return x * y
                    else:
                        return x + y
                else:
                    return x - y
            else:
                return x / 2
        else:
            return x
    else:
        return 0

# Duplicate code
def another_complex_function(x, y, z, a, b, c):
    if x > 0:
        if y > 0:
            if z > 0:
                if a > 0:
                    if b > 0:
                        if c > 0:
                            return eval(f"{x} + {y}")  # Security issue
                        else:
                            return x * y
                    else:
                        return x + y
                else:
                    return x - y
            else:
                return x / 2
        else:
            return x
    else:
        return 0
""")

        projects = [
            {"name": "High Quality Project", "path": str(proj1)},
            {"name": "Low Quality Project", "path": str(proj2)},
        ]

        # Analyze each project
        results_summary = []

        for project in projects:
            # Run analysis
            results = run_cli_analysis(project["path"], "json")

            if "error" in results:
                results_summary.append(
                    {
                        "name": project["name"],
                        "status": "FAILED",
                        "error": results["error"],
                    },
                )
            else:
                # Check quality gates
                decision = check_quality_thresholds(results)

                results_summary.append(
                    {
                        "name": project["name"],
                        "status": "COMPLETED",
                        "quality_gate": decision["recommendation"],
                        "passed_checks": f"{decision['passed_checks']}/{decision['total_checks']}",
                    },
                )

        # Display batch summary

        for summary in results_summary:
            summary["name"]
            status = summary["status"]

            if status == "COMPLETED":
                summary["quality_gate"]
                summary["passed_checks"]


def demonstrate_ci_cd_integration() -> None:
    """Demonstrate CI/CD integration patterns."""
    # Simulate CI/CD environment variables
    ci_env = {
        "CI": "true",
        "BRANCH_NAME": "feature/quality-improvements",
        "BUILD_NUMBER": "123",
        "PR_NUMBER": "456",
    }

    for _key, _value in ci_env.items():
        pass

    # Create sample workflow

    # Simulate the workflow
    project_path = Path(__file__).parent.parent.parent.parent / "src"

    results = run_cli_analysis(str(project_path), "json")

    if "error" not in results:
        decision = check_quality_thresholds(results)

        # Simulate posting to PR (would integrate with GitHub API, etc.)

        return 0 if decision["quality_gate_passed"] else 1

    return 1


def main() -> int:
    """Main demonstration of advanced CLI integration patterns."""
    try:
        # Demonstrate basic CLI integration
        project_path = Path(__file__).parent.parent.parent.parent / "src"

        results = run_cli_analysis(str(project_path), "json")

        if "error" not in results:
            check_quality_thresholds(results)

        # Demonstrate batch analysis
        demonstrate_batch_analysis()

        # Demonstrate CI/CD integration
        demonstrate_ci_cd_integration()

        return 0

    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
