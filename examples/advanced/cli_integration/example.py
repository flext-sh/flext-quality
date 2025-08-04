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
from typing import Dict, Any

def run_cli_analysis(project_path: str, format_type: str = "json") -> Dict[str, Any]:
    """Run FLEXT Quality CLI analysis and return parsed results.
    
    Args:
        project_path: Path to project to analyze
        format_type: Output format (json, html, text)
        
    Returns:
        Parsed analysis results
    """
    print(f"🔍 Running CLI analysis on: {project_path}")

    # Build CLI command with correct arguments
    cmd = [
        sys.executable,
        "-m", "flext_quality.cli",
        "analyze",
        project_path,
        "--format", format_type
        # Note: All analysis types are enabled by default
        # Use --no-security, --no-complexity, etc. to disable
    ]

    print(f"📋 Command: {' '.join(cmd)}")

    try:
        # Execute CLI command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        print(f"✅ CLI execution completed (exit code: {result.returncode})")

        # CLI may return non-zero exit code for validation but still output valid JSON
        if format_type == "json" and result.stdout.strip():
            import json
            try:
                parsed_json = json.loads(result.stdout)
                if result.returncode != 0:
                    print(f"⚠️ CLI returned exit code {result.returncode} but provided valid output")
                return parsed_json
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed: {e}")
                print(f"Raw output: {result.stdout[:500]}...")
                return {"error": "JSON parsing failed", "raw_output": result.stdout}
        elif result.returncode == 0:
            return {"output": result.stdout, "format": format_type}
        else:
            print(f"❌ CLI failed with exit code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return {"error": f"CLI failed: {result.stderr}", "exit_code": result.returncode}

    except subprocess.TimeoutExpired:
        print("⏰ CLI analysis timed out after 2 minutes")
        return {"error": "Analysis timeout"}
    except Exception as e:
        print(f"❌ CLI execution failed: {e}")
        return {"error": str(e)}


def check_quality_thresholds(results: Dict[str, Any]) -> Dict[str, Any]:
    """Check analysis results against quality thresholds.
    
    Args:
        results: Analysis results from CLI
        
    Returns:
        Quality gate decision and details
    """
    print("\n🎯 Checking Quality Thresholds")
    print("-" * 40)

    # Define enterprise quality thresholds
    thresholds = {
        "min_score": 80.0,           # Minimum overall score
        "max_security_issues": 0,    # Zero security issues allowed
        "max_complexity_issues": 5,  # Maximum complexity issues
        "max_critical_issues": 2,    # Maximum critical issues
        "min_files_analyzed": 1      # Must analyze at least 1 file
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
    total_issues = sum(len(issue_list) for issue_list in issues.values() if isinstance(issue_list, list))
    estimated_score = max(0, 100 - (total_issues * 10) - (security_count * 20))

    # Check each threshold
    checks = {
        "score_check": {
            "passed": estimated_score >= thresholds["min_score"],
            "value": estimated_score,
            "threshold": thresholds["min_score"],
            "message": f"Quality Score: {estimated_score:.1f} (min: {thresholds['min_score']})"
        },
        "security_check": {
            "passed": security_count <= thresholds["max_security_issues"],
            "value": security_count,
            "threshold": thresholds["max_security_issues"],
            "message": f"Security Issues: {security_count} (max: {thresholds['max_security_issues']})"
        },
        "complexity_check": {
            "passed": complexity_count <= thresholds["max_complexity_issues"],
            "value": complexity_count,
            "threshold": thresholds["max_complexity_issues"],
            "message": f"Complexity Issues: {complexity_count} (max: {thresholds['max_complexity_issues']})"
        },
        "critical_check": {
            "passed": critical_issues <= thresholds["max_critical_issues"],
            "value": critical_issues,
            "threshold": thresholds["max_critical_issues"],
            "message": f"Critical Issues: {critical_issues} (max: {thresholds['max_critical_issues']})"
        },
        "files_check": {
            "passed": files_analyzed >= thresholds["min_files_analyzed"],
            "value": files_analyzed,
            "threshold": thresholds["min_files_analyzed"],
            "message": f"Files Analyzed: {files_analyzed} (min: {thresholds['min_files_analyzed']})"
        }
    }

    # Display results
    passed_checks = 0
    for check_name, check_data in checks.items():
        status = "✅ PASS" if check_data["passed"] else "❌ FAIL"
        print(f"{status} {check_data['message']}")
        if check_data["passed"]:
            passed_checks += 1

    # Overall decision
    all_passed = passed_checks == len(checks)
    decision = {
        "quality_gate_passed": all_passed,
        "passed_checks": passed_checks,
        "total_checks": len(checks),
        "checks": checks,
        "recommendation": "APPROVE" if all_passed else "REJECT"
    }

    print(f"\n🏆 Quality Gate Decision: {decision['recommendation']}")
    print(f"📊 Checks Passed: {passed_checks}/{len(checks)}")

    return decision


def demonstrate_batch_analysis() -> None:
    """Demonstrate batch analysis of multiple projects."""
    print("\n" + "="*60)
    print("🚀 Batch Analysis Demonstration")
    print("="*60)

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
        (proj2 / "problematic.py").write_text('''
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
''')

        projects = [
            {"name": "High Quality Project", "path": str(proj1)},
            {"name": "Low Quality Project", "path": str(proj2)}
        ]

        # Analyze each project
        results_summary = []

        for project in projects:
            print(f"\n📁 Analyzing: {project['name']}")
            print("-" * 40)

            # Run analysis
            results = run_cli_analysis(project["path"], "json")

            if "error" in results:
                print(f"❌ Analysis failed: {results['error']}")
                results_summary.append({
                    "name": project["name"],
                    "status": "FAILED",
                    "error": results["error"]
                })
            else:
                # Check quality gates
                decision = check_quality_thresholds(results)

                results_summary.append({
                    "name": project["name"],
                    "status": "COMPLETED",
                    "quality_gate": decision["recommendation"],
                    "passed_checks": f"{decision['passed_checks']}/{decision['total_checks']}"
                })

        # Display batch summary
        print("\n" + "="*60)
        print("📊 Batch Analysis Summary")
        print("="*60)

        for summary in results_summary:
            name = summary["name"]
            status = summary["status"]

            if status == "COMPLETED":
                gate = summary["quality_gate"]
                checks = summary["passed_checks"]
                gate_icon = "✅" if gate == "APPROVE" else "❌"
                print(f"{gate_icon} {name}: {gate} ({checks} checks passed)")
            else:
                print(f"❌ {name}: FAILED - {summary.get('error', 'Unknown error')}")

        print("\n🎯 Batch Analysis Complete!")


def demonstrate_ci_cd_integration() -> None:
    """Demonstrate CI/CD integration patterns."""
    print("\n" + "="*60)
    print("🚀 CI/CD Integration Demonstration")
    print("="*60)

    # Simulate CI/CD environment variables
    ci_env = {
        "CI": "true",
        "BRANCH_NAME": "feature/quality-improvements",
        "BUILD_NUMBER": "123",
        "PR_NUMBER": "456"
    }

    print("🔧 CI/CD Environment:")
    for key, value in ci_env.items():
        print(f"  {key}={value}")

    # Create sample workflow
    print("\n📋 Quality Gate Workflow:")
    print(f"  1. Checkout code from {ci_env['BRANCH_NAME']}")
    print("  2. Run FLEXT Quality analysis")
    print("  3. Check quality thresholds")
    print(f"  4. Post results to PR #{ci_env['PR_NUMBER']}")
    print("  5. Approve/reject based on quality gates")

    # Simulate the workflow
    project_path = Path(__file__).parent.parent.parent.parent / "src"

    print(f"\n🔍 Running quality analysis for build #{ci_env['BUILD_NUMBER']}...")
    results = run_cli_analysis(str(project_path), "json")

    if "error" not in results:
        decision = check_quality_thresholds(results)

        # Simulate posting to PR (would integrate with GitHub API, etc.)
        print(f"\n💬 Posting results to PR #{ci_env['PR_NUMBER']}:")
        print(f"  Quality Gate: {decision['recommendation']}")
        print(f"  Checks: {decision['passed_checks']}/{decision['total_checks']} passed")

        if decision['quality_gate_passed']:
            print("  ✅ PR approved for merge")
            exit_code = 0
        else:
            print("  ❌ PR blocked - quality issues must be resolved")
            exit_code = 1

        return exit_code
    else:
        print(f"❌ CI/CD build failed: {results['error']}")
        return 1


def main() -> int:
    """Main demonstration of advanced CLI integration patterns."""
    print("🚀 FLEXT Quality - Advanced CLI Integration")
    print("="*60)
    print("This example demonstrates enterprise-grade automation capabilities:")
    print("• CLI command automation")
    print("• Quality threshold enforcement")
    print("• Batch project analysis")
    print("• CI/CD integration patterns")

    try:
        # Demonstrate basic CLI integration
        project_path = Path(__file__).parent.parent.parent.parent / "src"

        print("\n📋 1. Basic CLI Integration")
        print("-" * 40)
        results = run_cli_analysis(str(project_path), "json")

        if "error" not in results:
            decision = check_quality_thresholds(results)
            print("✅ CLI integration successful!")
        else:
            print(f"⚠️ CLI analysis had issues: {results['error']}")

        # Demonstrate batch analysis
        print("\n📋 2. Batch Analysis")
        demonstrate_batch_analysis()

        # Demonstrate CI/CD integration
        print("\n📋 3. CI/CD Integration")
        ci_exit_code = demonstrate_ci_cd_integration()

        print("\n🎉 All demonstrations completed successfully!")
        print(f"CI/CD Exit Code: {ci_exit_code}")

        return 0

    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
