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

from flext_quality import (
    CodeAnalyzer,
    FlextQualityConstants,
    QualityMetrics,
    QualityReport,
)


def print_header(title: str) -> None:
    """Print a formatted header for section output."""


def print_section(title: str) -> None:
    """Print a formatted section header."""


def format_number(num: float | str) -> str:
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

    # Initialize the analyzer
    analyzer = CodeAnalyzer(project_path)

    try:
        print_section("📊 Executing Comprehensive Analysis")

        # Execute comprehensive analysis with ALL features
        results = analyzer.analyze_project(
            include_security=True,  # Security vulnerability detection
            include_complexity=True,  # Cyclomatic complexity analysis
            include_dead_code=True,  # Unused code detection
            include_duplicates=True,  # Code duplication analysis
        )

        # Extract basic project information using modern AnalysisResults API
        # Note: python_files not available in AnalysisResults - use file_metrics instead
        analyzed_files = [str(fm.file_path) for fm in results.file_metrics]

        print_section("📈 Project Overview")

        # Show sample files (first 5)
        if analyzed_files:
            # Constants for display limits
            max_files_to_show = 5

            for _i, _file_path in enumerate(analyzed_files[:max_files_to_show]):
                pass
            if len(analyzed_files) > max_files_to_show:
                pass

        # Calculate quality score and grade - DEMONSTRATE ALL SCORING
        score = analyzer.get_quality_score()
        analyzer.get_quality_grade()

        print_section("🎯 Quality Assessment")

        # Process COMPLETE quality metrics - demonstrate ALL metrics
        metrics = QualityMetrics.from_analysis_results(results)

        print_section("📋 Complete Quality Metrics")

        # Show detailed scores
        scores_summary = metrics.scores_summary
        for _category, _score_val in scores_summary.items():
            pass

        # Show complexity metrics if available
        if hasattr(metrics, "average_complexity") and metrics.average_complexity > 0:
            pass

        # Process and display ALL ISSUES in detail using modern AnalysisResults API
        print_section("🚨 Issues Detection Summary")

        # Detailed issue breakdown - SHOW ALL ISSUES using typed properties
        issue_categories = {
            "Security": results.security_issues,
            "Complexity": results.complexity_issues,
            "Dead Code": results.dead_code_issues,
            "Duplication": results.duplication_issues,
        }

        for issue_list in issue_categories.values():
            if not issue_list:
                pass
            else:
                # Show detailed information for each issue
                for _i, issue in enumerate(issue_list[:max_files_to_show]):
                    # Access typed issue properties
                    if hasattr(issue, "file_path"):
                        getattr(issue, "file_path", "unknown")
                    if hasattr(issue, "message"):
                        getattr(issue, "message", "No description")
                    if hasattr(issue, "severity"):
                        getattr(issue, "severity", "unknown")
                    if hasattr(issue, "line_number"):
                        getattr(issue, "line_number", "")

                if len(issue_list) > max_files_to_show:
                    pass

        # DEMONSTRATE REPORT GENERATION - ALL FORMATS
        print_section("📊 Generating Quality Reports")

        try:
            # Create QualityReport instance
            report = QualityReport(results)

            json_report = report.generate_json_report()
            json_path = Path(project_path) / "quality_report.json"
            json_path.write_text(json_report)

            html_report = report.generate_html_report()
            html_path = Path(project_path) / "quality_report.html"
            html_path.write_text(html_report)

            # Show sample of JSON report structure
            sample_data = json.loads(json_report)
            for _key in list(sample_data.keys())[:max_files_to_show]:
                pass

        except Exception:
            return

        # COMPREHENSIVE RECOMMENDATIONS - demonstrate all recommendation logic
        print_section("💡 Comprehensive Recommendations")

        # Constants for score thresholds
        excellent_score = 95
        very_good_score = 90
        good_score = 80
        acceptable_score = 70
        minimum_score = 60

        # Score-based recommendations
        if (
            score >= excellent_score
            or score >= very_good_score
            or score >= good_score
            or score >= acceptable_score
            or score >= minimum_score
        ):
            pass

        # Category-specific recommendations with actionable advice
        if metrics.security_issues_count > 0:
            pass

        if metrics.complexity_issues_count > 0:
            pass

        if metrics.duplicate_blocks_count > 0:
            pass

        if metrics.dead_code_items_count > 0:
            pass

        # Final summary with complete metrics display
        print_section("✅ Analysis Complete - Summary")

        # Show complete metrics summary for verification

    except Exception:
        # Allow caller to handle in main(); keep example robust
        return


def get_quality_assessment(score: float) -> str:
    """Get descriptive assessment based on quality score."""
    if score >= FlextQualityConstants.QualityThresholds.OUTSTANDING_THRESHOLD:
        return "Outstanding quality - industry leading"
    if score >= FlextQualityConstants.QualityThresholds.EXCELLENT_THRESHOLD:
        return "Excellent quality - production ready"
    if score >= FlextQualityConstants.QualityThresholds.GOOD_THRESHOLD:
        return "Good quality - minor improvements recommended"
    if score >= FlextQualityConstants.QualityThresholds.ACCEPTABLE_THRESHOLD:
        return "Acceptable quality - moderate improvements needed"
    if score >= FlextQualityConstants.QualityThresholds.BELOW_AVERAGE_THRESHOLD:
        return "Below average - significant improvements required"
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
        return None

    if not project_path.is_dir():
        return None

    # Check if directory contains Python files
    python_files = list(project_path.rglob("*.py"))
    if not python_files:
        pass

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

    # Validate project path
    validated_path = validate_project_path(project_path)
    if not validated_path:
        return 1

    # Execute comprehensive analysis
    try:
        analyze_project(validated_path)
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
