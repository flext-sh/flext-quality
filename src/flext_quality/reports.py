"""Quality report generation and formatting."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


class QualityReport:
    """Generates quality reports from analysis results."""

    def __init__(self, analysis_results: dict[str, Any]) -> None:
        self.results = analysis_results

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

        # Add issue details
        issues = self.results.get("issues", {})
        for category, issue_list in issues.items():
            if issue_list:
                report_lines.append(f"\n{category.upper()} ({len(issue_list)} issues):")
                # Show first 5 issues
                report_lines.extend(f"  - {issue.get('file', 'Unknown')}: {issue.get('message', 'No message')}" for issue in issue_list[:5])
                if len(issue_list) > 5:
                    report_lines.append(f"  ... and {len(issue_list) - 5} more")

        # Add recommendations
        recommendations = self._generate_recommendations()
        if recommendations:
            report_lines.extend([
                "",
                "RECOMMENDATIONS:",
                "-" * 20,
            ])
            report_lines.extend(f"• {rec}" for rec in recommendations)

        return "\n".join(report_lines)

    def generate_json_report(self) -> str:
        """Generate a JSON-formatted quality report."""
        report_data = {
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
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
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
        html_parts.extend(f"            <li>{rec}</li>" for rec in self._generate_recommendations())

        html_parts.extend([
            "        </ul>",
            "    </div>",
            "</body>",
            "</html>",
        ])

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
        """Calculate quality grade."""
        score = self._get_quality_score()
        if score >= 90:
            return "A"
        if score >= 80:
            return "B"
        if score >= 70:
            return "C"
        if score >= 60:
            return "D"
        return "F"

    def _get_quality_score(self) -> int:
        """Calculate overall quality score."""
        # Simple scoring based on issue count
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
        issues = self.results.get("issues", {})
        return sum(len(issue_list) for issue_list in issues.values())

    def _get_critical_issues(self) -> int:
        """Get number of critical issues."""
        issues = self.results.get("issues", {})
        critical_categories = ["security", "errors", "critical"]
        return sum(
            len(issues.get(category, []))
            for category in critical_categories
        )

    def _get_files_analyzed(self) -> int:
        """Get number of files analyzed."""
        return self.results.get("metrics", {}).get("files_analyzed", 0)

    def _get_coverage_percent(self) -> float:
        """Get code coverage percentage."""
        return self.results.get("metrics", {}).get("coverage_percent", 0.0)

    def _generate_issues_html(self) -> str:
        """Generate HTML for issues section."""
        html_parts = []
        issues = self.results.get("issues", {})

        for category, issue_list in issues.items():
            if not issue_list:
                continue

            html_parts.extend([
                '    <div class="section">',
                f"        <h2>{category.title()} Issues ({len(issue_list)})</h2>",
            ])

            for issue in issue_list[:10]:  # Show first 10 issues
                severity = issue.get("severity", "low")
                file_path = issue.get("file", "Unknown")
                message = issue.get("message", "No message")
                line = issue.get("line", "")
                line_info = f" (line {line})" if line else ""

                html_parts.append(
                    f'        <div class="issue {severity}-severity">'
                    f'<strong>{file_path}{line_info}:</strong> {message}</div>',
                )

            if len(issue_list) > 10:
                html_parts.append(f'        <div class="issue">... and {len(issue_list) - 10} more issues</div>')

            html_parts.append("    </div>")

        return "\n".join(html_parts)

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []

        total_issues = self._get_total_issues()
        critical_issues = self._get_critical_issues()
        score = self._get_quality_score()

        if critical_issues > 0:
            recommendations.append(f"Fix {critical_issues} critical security/error issues immediately")

        if total_issues > 50:
            recommendations.append("Consider breaking down large files and reducing complexity")

        if score < 70:
            recommendations.extend(("Implement automated code quality checks in your CI/CD pipeline", "Add comprehensive unit tests to improve coverage"))

        coverage = self._get_coverage_percent()
        if coverage < 80:
            recommendations.append(f"Increase test coverage from {coverage}% to at least 80%")

        issues = self.results.get("issues", {})
        if issues.get("duplicates"):
            recommendations.append("Refactor duplicate code to improve maintainability")

        if issues.get("complexity"):
            recommendations.append("Simplify complex functions and classes")

        if not recommendations:
            recommendations.append("Great job! Your code quality is excellent. Keep up the good work!")

        return recommendations
