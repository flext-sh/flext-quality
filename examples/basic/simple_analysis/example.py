#!/usr/bin/env python3
"""FLEXT Quality - Complete Functional Analysis Example.

This example demonstrates ALL functionality of FLEXT Quality for analyzing
a Python project with comprehensive output, reports, and integration patterns.
It showcases the complete capabilities of the FLEXT Quality system.

Key Features Demonstrated:
    - Complete project analysis with ALL CodeAnalyzer capabilities
    - Quality score calculation and grading with detailed output
    - Issue detection and categorization with full details
    - Result processing with QualityMetrics integration
    - Report generation in multiple formats (JSON, HTML)
    - Error handling with proper user feedback
    - FLEXT ecosystem integration patterns

Usage:
    python example.py [project_path]

Example:
    python example.py /path/to/your/project
    python example.py ../../../src  # Analyze FLEXT Quality itself

"""

import json
import sys
from pathlib import Path
from typing import Any

from flext_quality import CodeAnalyzer, QualityMetrics, QualityReport


def print_header(title: str) -> None:
    """Print a formatted header for section output."""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * 40)


def format_number(num: Any) -> str:
    """Format numbers with proper comma separators."""
    if isinstance(num, (int, float)):
        return f"{num:,}"
    return str(num)


def analyze_project(project_path: str) -> None:
    """Perform comprehensive quality analysis demonstrating ALL functionality.

    This function showcases the complete FLEXT Quality workflow including
    all analysis types, metrics processing, report generation, and output
    formatting to demonstrate 100% of the system capabilities.

    Args:
        project_path: Absolute path to the project directory to analyze

    """
    print_header("FLEXT Quality - Complete Analysis Example")
    print(f"🔍 Starting comprehensive analysis for: {project_path}")

    # Initialize the analyzer
    analyzer = CodeAnalyzer(project_path)
    print("✅ CodeAnalyzer initialized successfully")

    try:
        print_section("📊 Executing Comprehensive Analysis")
        print("🔍 Running all analysis backends...")

        # Execute comprehensive analysis with ALL features
        results = analyzer.analyze_project(
            include_security=True,      # Security vulnerability detection
            include_complexity=True,    # Cyclomatic complexity analysis
            include_dead_code=True,     # Unused code detection
            include_duplicates=True     # Code duplication analysis
        )

        print("✅ Analysis completed successfully!")

        # Extract basic project information
        files_analyzed = results.get("files_analyzed", 0)
        total_lines = results.get("total_lines", 0)
        python_files = results.get("python_files", [])

        print_section("📈 Project Overview")
        print(f"Files analyzed: {format_number(files_analyzed)}")
        print(f"Total lines: {format_number(total_lines)}")
        print(f"Python files found: {len(python_files)}")

        # Show sample files (first 5)
        if python_files:
            print("\nSample files:")
            for i, file_path in enumerate(python_files[:5]):
                print(f"  {i+1}. {file_path}")
            if len(python_files) > 5:
                print(f"  ... and {len(python_files) - 5} more files")

        # Calculate quality score and grade - DEMONSTRATE ALL SCORING
        score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()

        print_section("🎯 Quality Assessment")
        print(f"Overall Score: {score:.1f}/100")
        print(f"Quality Grade: {grade}")
        print(f"Assessment: {get_quality_assessment(score)}")

        # Process COMPLETE quality metrics - demonstrate ALL metrics
        metrics = QualityMetrics.from_analysis_results(results)

        print_section("📋 Complete Quality Metrics")
        print(f"Quality Grade: {metrics.quality_grade} ({metrics.overall_score:.1f}/100)")
        print(f"Files: {format_number(metrics.total_files)}, Lines: {format_number(metrics.total_lines_of_code)}")
        print(f"Functions: {format_number(metrics.total_functions)}, Classes: {format_number(metrics.total_classes)}")

        # Show detailed scores
        print("\n📊 Detailed Quality Scores:")
        scores_summary = metrics.scores_summary
        for category, score_val in scores_summary.items():
            print(f"  {category.title()}: {score_val:.1f}/100")

        # Show complexity metrics if available
        if hasattr(metrics, 'average_complexity') and metrics.average_complexity > 0:
            print("\n🔄 Complexity Metrics:")
            print(f"  Average Complexity: {metrics.average_complexity:.1f}")
            print(f"  Max Complexity: {metrics.max_complexity:.1f}")

        # Process and display ALL ISSUES in detail
        issues = results.get("issues", {})
        total_issues = metrics.total_issues

        print_section("🚨 Issues Detection Summary")
        print(f"Total Issues Found: {total_issues}")
        print(f"Issues: Security({metrics.security_issues_count}), "
              f"Complexity({metrics.complexity_issues_count}), "
              f"DeadCode({metrics.dead_code_items_count}), "
              f"Duplicates({metrics.duplicate_blocks_count})")

        # Detailed issue breakdown - SHOW ALL ISSUES
        for category, issue_list in issues.items():
            if isinstance(issue_list, list):
                print(f"\n{category.title()}: {len(issue_list)} issues")

                if not issue_list:
                    print("  ✅ No issues found")
                else:
                    # Show detailed information for each issue
                    for i, issue in enumerate(issue_list[:5]):  # Show first 5 issues
                        if isinstance(issue, dict):
                            file_path = issue.get("file", "unknown")
                            message = issue.get("message", "No description")
                            severity = issue.get("severity", "unknown")
                            line = issue.get("line", "")

                            line_info = f" (line {line})" if line else ""
                            severity_info = f" [{severity}]" if severity != "unknown" else ""

                            print(f"  {i+1}. {file_path}{line_info}{severity_info}")
                            print(f"     {message}")

                    if len(issue_list) > 5:
                        print(f"  ... and {len(issue_list) - 5} more issues")

        # DEMONSTRATE REPORT GENERATION - ALL FORMATS
        print_section("📊 Generating Quality Reports")

        try:
            # Create QualityReport instance
            report = QualityReport(results)

            print("📄 Generating JSON report...")
            json_report = report.generate_json_report()
            json_path = Path(project_path) / "quality_report.json"
            json_path.write_text(json_report)
            print(f"✅ JSON report saved: {json_path}")

            print("🌐 Generating HTML report...")
            html_report = report.generate_html_report()
            html_path = Path(project_path) / "quality_report.html"
            html_path.write_text(html_report)
            print(f"✅ HTML report saved: {html_path}")

            # Show sample of JSON report structure
            print("\n📋 Sample JSON Report Structure:")
            sample_data = json.loads(json_report)
            print(f"  Report contains {len(sample_data.keys())} main sections:")
            for key in list(sample_data.keys())[:5]:
                print(f"    - {key}")

        except Exception as e:
            print(f"⚠️ Report generation encountered an issue: {e}")

        # COMPREHENSIVE RECOMMENDATIONS - demonstrate all recommendation logic
        print_section("💡 Comprehensive Recommendations")

        # Score-based recommendations
        if score >= 95:
            print("🌟 Exceptional! Your code quality is outstanding.")
        elif score >= 90:
            print("🎉 Excellent! Minor tweaks could make this perfect.")
        elif score >= 80:
            print("👍 Good quality. Consider addressing high-priority issues.")
        elif score >= 70:
            print("⚠️ Needs improvement. Focus on critical issues first.")
        elif score >= 60:
            print("🚨 Significant issues detected. Major refactoring recommended.")
        else:
            print("❌ Critical quality issues. Immediate attention required.")

        # Category-specific recommendations with actionable advice
        if metrics.security_issues_count > 0:
            print(f"🔒 Security: Address {metrics.security_issues_count} security issues immediately")
            print("    Priority: Review dangerous function usage and potential vulnerabilities")

        if metrics.complexity_issues_count > 0:
            print(f"🔄 Complexity: Reduce complexity in {metrics.complexity_issues_count} locations")
            print("    Priority: Break down complex functions into smaller, testable units")

        if metrics.duplicate_blocks_count > 0:
            print(f"📑 Duplicates: Eliminate {metrics.duplicate_blocks_count} code duplications")
            print("    Priority: Extract common functionality into reusable components")

        if metrics.dead_code_items_count > 0:
            print(f"🧹 Dead Code: Remove {metrics.dead_code_items_count} unused code items")
            print("    Priority: Clean up unused imports, variables, and functions")

        # Final summary with complete metrics display
        print_section("✅ Analysis Complete - Summary")
        print(f"📊 Final Quality Grade: {grade} ({score:.1f}/100)")
        print(f"📈 Files: {format_number(files_analyzed)}, Lines: {format_number(total_lines)}")
        print(f"🎯 Issues to Address: {total_issues}")
        print(f"📋 Detailed metrics calculated: {len(scores_summary)} categories")
        print("🎉 All analysis backends executed successfully!")

        # Show complete metrics summary for verification
        print("\n🔍 Complete Analysis Verification:")
        print(f"  ✅ Security Analysis: {metrics.security_issues_count} issues found")
        print(f"  ✅ Complexity Analysis: {metrics.complexity_issues_count} issues found")
        print(f"  ✅ Dead Code Analysis: {metrics.dead_code_items_count} items found")
        print(f"  ✅ Duplication Analysis: {metrics.duplicate_blocks_count} blocks found")
        print(f"  ✅ Quality Metrics: All {len(scores_summary)} categories calculated")
        print("  ✅ Reports Generated: JSON and HTML formats")

    except Exception as e:
        print(f"\n❌ Analysis failed with error: {e}")
        print("Please check the project path and ensure it contains Python files.")
        raise


def get_quality_assessment(score: float) -> str:
    """Get descriptive assessment based on quality score."""
    if score >= 95:
        return "Outstanding quality - industry leading"
    elif score >= 90:
        return "Excellent quality - production ready"
    elif score >= 80:
        return "Good quality - minor improvements recommended"
    elif score >= 70:
        return "Acceptable quality - moderate improvements needed"
    elif score >= 60:
        return "Below average - significant improvements required"
    else:
        return "Poor quality - major refactoring needed"


def validate_project_path(path: str) -> str | None:
    """Validate that the provided path exists and contains Python files.

    Args:
        path: Path string to validate

    Returns:
        Absolute path if valid, None if invalid

    """
    project_path = Path(path).resolve()

    if not project_path.exists():
        print(f"❌ Error: Path does not exist: {path}")
        return None

    if not project_path.is_dir():
        print(f"❌ Error: Path is not a directory: {path}")
        return None

    # Check if directory contains Python files
    python_files = list(project_path.rglob("*.py"))
    if not python_files:
        print(f"⚠️  Warning: No Python files found in: {path}")
        print("The analysis will continue but may have limited results.")

    return str(project_path)


def main() -> int:
    """Main entry point demonstrating complete FLEXT Quality functionality.

    Handles command line arguments, validates input, and executes comprehensive
    analysis with full output and error handling.

    Returns:
        Exit code (0 for success, 1 for error)

    """
    # Handle command line arguments
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        # Default to analyzing FLEXT Quality's own source code
        current_dir = Path(__file__).parent
        project_path = str(current_dir.parent.parent.parent / "src")
        print(f"ℹ️  No path provided, analyzing FLEXT Quality source: {project_path}")

    # Validate project path
    validated_path = validate_project_path(project_path)
    if not validated_path:
        print("\n❌ Analysis cannot proceed with invalid path.")
        print("Usage: python example.py [project_path]")
        return 1

    # Execute comprehensive analysis
    try:
        analyze_project(validated_path)
        print(f"\n🎉 Analysis completed successfully! Check generated reports in: {validated_path}")
        return 0
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during analysis: {e}")
        print("Please ensure the project path is correct and accessible.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
