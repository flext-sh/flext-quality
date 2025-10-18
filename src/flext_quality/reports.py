"""Quality report generation and formatting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

from .grade_calculator import FlextQualityGradeCalculator
from .models import FlextQualityModels
from .utilities import FlextQualityUtilities
from .value_objects import IssueSeverity

# Constants for display limits
ISSUE_PREVIEW_LIMIT = 5
HTML_ISSUE_LIMIT = 10
HIGH_ISSUE_THRESHOLD = 50
MIN_COVERAGE_THRESHOLD = 80
MIN_SCORE_THRESHOLD = 70
HIGH_TYPE_ERROR_THRESHOLD = 10


class FlextQualityReportGenerator:
    """Generates quality reports from analysis results."""

    def __init__(self, analysis_results: FlextQualityModels.AnalysisResults) -> None:
        """Initialize the quality report generator.

        Args:
            analysis_results: Strongly-typed analysis results and metrics.

        Returns:
            object: Description of return value.

        """
        # Store analysis results directly
        self.results: FlextQualityModels.AnalysisResults = analysis_results

    def generate_text_report(self) -> str:
        """Generate a text-based quality report."""
        grade = self._get_quality_grade()
        score = self._get_quality_score()
        total_issues = self._get_total_issues()
        critical_issues = self._get_critical_issues()

        report_lines = [
            "=" * 60,
            "FLEXT QUALITY REPORT",
            "=" * 60,
            f"Overall Grade: {grade}",
            f"Quality Score: {score}/100",
            f"Total Issues: {total_issues}",
            f"Critical Issues: {critical_issues}",
            f"Files Analyzed: {self._get_files_analyzed()}",
            f"Code Coverage: {self._get_coverage_percent()}%",
            "",
            "ISSUES BY CATEGORY:",
            "-" * 30,
        ]

        # Add issue details using utilities for proper typing
        issue_categories: dict[str, list[object]] = (
            FlextQualityUtilities.format_issue_categories(self.results)
        )

        for category, issue_list in issue_categories.items():
            if issue_list:
                report_lines.append(f"\n{category} ({len(issue_list)} issues):")
                # Show first few issues
                for issue in issue_list[:ISSUE_PREVIEW_LIMIT]:
                    summary = FlextQualityUtilities.get_issue_summary(issue)
                    message = getattr(issue, "message", "No description available")
                    report_lines.append(f"  - {summary}: {message}")

                if len(issue_list) > ISSUE_PREVIEW_LIMIT:
                    report_lines.append(
                        f"  ... and {len(issue_list) - ISSUE_PREVIEW_LIMIT} more",
                    )

        # Add recommendations
        recommendations = self._generate_recommendations()
        if recommendations:
            report_lines.extend(
                [
                    "",
                    "RECOMMENDATIONS:",
                    "-" * 20,
                ],
            )
            report_lines.extend(f"• {rec}" for rec in recommendations)

        return "\n".join(report_lines)

    def generate_json_report(self) -> str:
        """Generate a JSON-formatted quality report."""
        report_data: dict[str, object] = {
            "summary": {
                "grade": self._get_quality_grade(),
                "score": self._get_quality_score(),
                "total_issues": self._get_total_issues(),
                "critical_issues": self._get_critical_issues(),
                "files_analyzed": self._get_files_analyzed(),
                "coverage_percent": self._get_coverage_percent(),
            },
            "analysis_results": self.results,
            "recommendations": self._generate_recommendations(),
        }

        return json.dumps(report_data, indent=2, default=str)

    def to_json(self) -> str:
        """Alias for generate_json_report for compatibility."""
        return self.generate_json_report()

    def to_html(self) -> str:
        """Alias for generate_html_report for compatibility."""
        return self.generate_html_report()

    def generate_html_report(self) -> str:
        """Generate an HTML-formatted quality report."""
        grade_color = self._get_grade_color()
        quality_grade = self._get_quality_grade()
        quality_score = self._get_quality_score()
        total_issues = self._get_total_issues()
        critical_issues = self._get_critical_issues()
        files_analyzed = self._get_files_analyzed()
        coverage_percent = self._get_coverage_percent()
        issues_html = self._generate_issues_html()

        # Build HTML with proper string concatenation
        html_parts = [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            "    <title>FLEXT Quality Report</title>",
            "    <style>",
            "        body { font-family: 'Arial', sans-serif; margin: 20px; }",
            "        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }",
            "        .summary { margin: 20px 0; }",
            f"        .grade {{ font-size: 3em; font-weight: bold; color: {grade_color}; }}",
            "        .score { font-size: 1.5em; }",
            "        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }",
            "        .issue { margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 3px; }",
            "        .metric { display: inline-block; margin: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }",
            "        .high-severity { background: #ff6b6b; color: white; }",
            "        .medium-severity { background: #ffa726; color: white; }",
            "        .low-severity { background: #66bb6a; color: white; }",
            "    </style>",
            "</head>",
            "<body>",
            '    <div class="header">',
            "        <h1>FLEXT Quality Report</h1>",
            "    </div>",
            "",
            '    <div class="summary">',
            f'        <div class="grade">{quality_grade}</div>',
            f'        <div class="score">Score: {quality_score}/100</div>',
            "    </div>",
            "",
            '    <div class="section">',
            "        <h2>Quality Metrics</h2>",
            f'        <div class="metric"><strong>Total Issues:</strong> {total_issues}</div>',
            f'        <div class="metric"><strong>Critical Issues:</strong> {critical_issues}</div>',
            f'        <div class="metric"><strong>Files Analyzed:</strong> {files_analyzed}</div>',
            f'        <div class="metric"><strong>Code Coverage:</strong> {coverage_percent}%</div>',
            "    </div>",
            "",
            f"    {issues_html}",
            "",
            '    <div class="section">',
            "        <h2>Recommendations</h2>",
            "        <ul>",
        ]

        # Add recommendations
        html_parts.extend(
            f"            <li>{rec}</li>" for rec in self._generate_recommendations()
        )

        html_parts.extend(
            [
                "        </ul>",
                "    </div>",
                "</body>",
                "</html>",
            ],
        )

        return "\n".join(html_parts)

    def save_report(self, output_path: Path, format_type: str = "text") -> None:
        """Save report to file."""
        if format_type == "json":
            content = self.generate_json_report()
        elif format_type == "html":
            content = self.generate_html_report()
        else:
            content = self.generate_text_report()

        output_path.write_text(content, encoding="utf-8")

    def _get_quality_grade(self) -> str:
        """Calculate quality grade - DRY refactored."""
        score = self._get_quality_score()
        grade = FlextQualityGradeCalculator.calculate_grade(float(score))
        return grade.value

    def _get_quality_score(self) -> int:
        """Calculate overall quality score."""
        total_issues = self._get_total_issues()
        critical_issues = self._get_critical_issues()

        # Base score of 100, subtract points for issues
        score = 100
        score -= critical_issues * 10  # Critical issues cost 10 points each
        score -= (total_issues - critical_issues) * 2  # Other issues cost 2 points each

        return max(0, score)

    def _get_grade_color(self) -> str:
        """Get color for the grade."""
        grade = self._get_quality_grade()
        colors = {
            "A": "#2e7d32",
            "B": "#388e3c",
            "C": "#f57c00",
            "D": "#f44336",
            "F": "#d32f2f",
        }
        return colors.get(grade, "#757575")

    def _get_total_issues(self) -> int:
        """Get total number of issues."""
        # Use modern FlextQualityModels.AnalysisResults API only
        return self.results.total_issues

    def _get_critical_issues(self) -> int:
        """Get number of critical issues."""
        # Count high severity issues across all categories
        critical_count = 0
        for issue in self.results.security_issues:
            if getattr(issue, "severity", None) == IssueSeverity.CRITICAL:
                critical_count += 1
        for issue in self.results.complexity_issues:
            if getattr(issue, "severity", None) == IssueSeverity.CRITICAL:
                critical_count += 1
        return critical_count

    def _get_files_analyzed(self) -> int:
        """Get number of files analyzed."""
        return int(self.results.overall_metrics.files_analyzed)

    def _get_coverage_percent(self) -> float:
        """Get code coverage percentage."""
        return float(self.results.overall_metrics.coverage_score)

    def _generate_issues_html(self) -> str:
        """Generate HTML for issues section."""
        html_parts: list[str] = FlextQualityUtilities.create_report_lines()
        issue_categories: dict[str, list[object]] = {
            "security": FlextQualityUtilities.safe_issue_list(
                self.results.security_issues,
            ),
            "complexity": FlextQualityUtilities.safe_issue_list(
                self.results.complexity_issues,
            ),
            "dead_code": FlextQualityUtilities.safe_issue_list(
                self.results.dead_code_issues,
            ),
            "duplication": FlextQualityUtilities.safe_issue_list(
                self.results.duplication_issues,
            ),
        }

        for category, issue_list in issue_categories.items():
            if not issue_list:
                continue

            html_parts.extend(
                [
                    '    <div class="section">',
                    f"        <h2>{category.title()} Issues ({len(issue_list)})</h2>",
                ],
            )

            for issue in issue_list[:10]:  # Show first 10 issues
                # Get attributes based on issue type
                if hasattr(issue, "severity"):
                    severity = getattr(issue, "severity", "low")
                else:
                    severity = "low"

                if hasattr(issue, "file_path"):
                    file_path = str(getattr(issue, "file_path", "Unknown"))
                else:
                    file_path = "Unknown"

                message = getattr(issue, "message", "No message")

                if hasattr(issue, "line_number"):
                    line = getattr(issue, "line_number", "")
                    line_info = f" (line {line})" if line else ""
                else:
                    line_info = ""

                html_parts.append(
                    f'        <div class="issue {severity}-severity"><strong>{file_path}{line_info}:</strong> {message}</div>',
                )

            if len(issue_list) > HTML_ISSUE_LIMIT:
                html_parts.append(
                    f'        <div class="issue">... and {len(issue_list) - HTML_ISSUE_LIMIT} more issues</div>',
                )

            html_parts.append("    </div>")

        return "\n".join(html_parts)

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations based on analysis results."""
        recommendations: list[str] = FlextQualityUtilities.create_report_lines()

        total_issues = self._get_total_issues()
        critical_issues = self._get_critical_issues()
        score = self._get_quality_score()

        if critical_issues > 0:
            recommendations.append(
                f"Fix {critical_issues} critical security/error issues immediately",
            )

        if total_issues > HIGH_ISSUE_THRESHOLD:
            recommendations.append(
                "Consider breaking down large files and reducing complexity",
            )

        if score < MIN_SCORE_THRESHOLD:
            FlextQualityUtilities.safe_extend_lines(
                recommendations,
                [
                    "Implement automated code quality checks in your CI/CD pipeline",
                    "Add comprehensive unit tests to improve coverage",
                ],
            )

        coverage = self._get_coverage_percent()
        if coverage < MIN_COVERAGE_THRESHOLD:
            recommendations.append(
                f"Increase test coverage from {coverage}% to at least {MIN_COVERAGE_THRESHOLD}%",
            )

        if self.results.duplication_issues:
            recommendations.append("Refactor duplicate code to improve maintainability")

        if self.results.complexity_issues:
            recommendations.append("Simplify complex functions and classes")

        if not recommendations:
            recommendations.append(
                "Great job! Your code quality is excellent. Keep up the good work!",
            )

        return recommendations


# Legacy compatibility facade - DEPRECATED
FlextQualityReport = (
    FlextQualityReportGenerator  # Keep old name for backward compatibility
)
QualityReport = FlextQualityReportGenerator
warnings.warn(
    "QualityReport is deprecated; use FlextQualityReportGenerator",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "HIGH_ISSUE_THRESHOLD",
    "HIGH_TYPE_ERROR_THRESHOLD",
    "HTML_ISSUE_LIMIT",
    # Constants
    "ISSUE_PREVIEW_LIMIT",
    "MIN_COVERAGE_THRESHOLD",
    "MIN_SCORE_THRESHOLD",
    "FlextQualityReport",  # Legacy compatibility
    "FlextQualityReportGenerator",
    "QualityReport",  # Legacy compatibility
]
