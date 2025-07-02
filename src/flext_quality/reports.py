"""Quality report generation and formatting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics import QualityMetrics


class QualityReport:
    """Generates quality reports from analysis results."""

    def __init__(self, analysis_results: dict[str, Any]) -> None:
        """Initialize report generator.

        Args:
            analysis_results: Results from CodeAnalyzer.
        """
        self.results = analysis_results
        self.metrics = QualityMetrics.from_analysis_results(analysis_results)

    def generate_text_report(self) -> str:
        """Generate a text-based quality report.

        Returns:
            Formatted text report.
        """
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("FLEXT QUALITY - CODE ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")

        # Project info
        lines.append(f"Project: {self.results.get('project_path', 'Unknown')}")
        lines.append(f"Files Analyzed: {self.metrics.total_files:,}")
        lines.append(f"Total Lines of Code: {self.metrics.total_lines_of_code:,}")
        lines.append("")

        # Overall score
        lines.append("OVERALL QUALITY")
        lines.append("-" * 20)
        lines.append(f"Grade: {self.metrics.quality_grade}")
        lines.append(f"Score: {self.metrics.overall_score:.1f}/100")
        lines.append("")

        # Component scores
        lines.append("COMPONENT SCORES")
        lines.append("-" * 20)
        lines.append(f"Complexity:      {self.metrics.complexity_score:.1f}/100")
        lines.append(f"Security:        {self.metrics.security_score:.1f}/100")
        lines.append(f"Maintainability: {self.metrics.maintainability_score:.1f}/100")
        lines.append(f"Duplication:     {self.metrics.duplication_score:.1f}/100")
        lines.append(f"Documentation:   {self.metrics.documentation_score:.1f}/100")
        lines.append("")

        # Code metrics
        lines.append("CODE METRICS")
        lines.append("-" * 20)
        lines.append(f"Functions: {self.metrics.total_functions:,}")
        lines.append(f"Classes: {self.metrics.total_classes:,}")
        lines.append(f"Average Complexity: {self.metrics.average_complexity:.1f}")
        lines.append(f"Max Complexity: {self.metrics.max_complexity:.1f}")
        lines.append("")

        # Issues summary
        lines.append("ISSUES FOUND")
        lines.append("-" * 20)
        issues = self.results.get("issues", {})

        security_issues = issues.get("security", [])
        if security_issues:
            lines.append(f"Security Issues: {len(security_issues)}")
            for issue in security_issues[:5]:  # Show first 5
                lines.append(
                    f"  • {issue.get('message', 'Unknown issue')} ({issue.get('file', 'unknown')})"
                )
            if len(security_issues) > 5:
                lines.append(f"  ... and {len(security_issues) - 5} more")
            lines.append("")

        complexity_issues = issues.get("complexity", [])
        if complexity_issues:
            lines.append(f"Complexity Issues: {len(complexity_issues)}")
            for issue in complexity_issues[:5]:
                lines.append(
                    f"  • {issue.get('message', 'Unknown issue')} ({issue.get('file', 'unknown')})"
                )
            if len(complexity_issues) > 5:
                lines.append(f"  ... and {len(complexity_issues) - 5} more")
            lines.append("")

        dead_code_issues = issues.get("dead_code", [])
        if dead_code_issues:
            lines.append(f"Dead Code Issues: {len(dead_code_issues)}")
            for issue in dead_code_issues[:5]:
                lines.append(
                    f"  • {issue.get('message', 'Unknown issue')} ({issue.get('file', 'unknown')})"
                )
            if len(dead_code_issues) > 5:
                lines.append(f"  ... and {len(dead_code_issues) - 5} more")
            lines.append("")

        duplicate_issues = issues.get("duplicates", [])
        if duplicate_issues:
            lines.append(f"Duplicate Code Issues: {len(duplicate_issues)}")
            for issue in duplicate_issues[:3]:
                files = issue.get("files", [])
                if len(files) >= 2:
                    lines.append(f"  • Similar files: {files[0]} & {files[1]}")
            if len(duplicate_issues) > 3:
                lines.append(f"  ... and {len(duplicate_issues) - 3} more")
            lines.append("")

        # Recommendations
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 20)

        recommendations = []
        if self.metrics.security_issues_count > 0:
            recommendations.append("• Review and fix security issues immediately")
        if self.metrics.complexity_issues_count > 0:
            recommendations.append(
                "• Refactor complex functions to improve maintainability"
            )
        if self.metrics.dead_code_items_count > 0:
            recommendations.append("• Remove unused code to improve clarity")
        if self.metrics.duplicate_blocks_count > 0:
            recommendations.append("• Extract common code into reusable functions")
        if self.metrics.overall_score < 70:
            recommendations.append("• Consider implementing code review processes")

        if recommendations:
            lines.extend(recommendations)
        else:
            lines.append("• Code quality is good! Keep up the excellent work.")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def generate_json_report(self) -> str:
        """Generate a JSON-formatted quality report.

        Returns:
            JSON report string.
        """
        report_data = {
            "summary": {
                "overall_score": self.metrics.overall_score,
                "quality_grade": self.metrics.quality_grade,
                "total_files": self.metrics.total_files,
                "total_lines_of_code": self.metrics.total_lines_of_code,
            },
            "metrics": self.metrics.to_dict(),
            "analysis_results": self.results,
            "recommendations": self._generate_recommendations(),
        }

        return json.dumps(report_data, indent=2, default=str)

    def generate_html_report(self) -> str:
        """Generate an HTML-formatted quality report.

        Returns:
            HTML report string.
        """
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FLEXT Quality Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .grade {{ font-size: 3em; font-weight: bold; color: {self._get_grade_color()}; }}
        .score {{ font-size: 1.5em; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .issue {{ margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 3px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }}
        .high-severity {{ background: #ff6b6b; color: white; }}
        .medium-severity {{ background: #ffa726; color: white; }}
        .low-severity {{ background: #66bb6a; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FLEXT Quality Report</h1>
        <p>Project: {self.results.get("project_path", "Unknown")}</p>
    </div>
    
    <div class="summary">
        <div class="grade">{self.metrics.quality_grade}</div>
        <div class="score">{self.metrics.overall_score:.1f}/100</div>
    </div>
    
    <div class="section">
        <h2>Code Metrics</h2>
        <div class="metric">Files: {self.metrics.total_files:,}</div>
        <div class="metric">Lines: {self.metrics.total_lines_of_code:,}</div>
        <div class="metric">Functions: {self.metrics.total_functions:,}</div>
        <div class="metric">Classes: {self.metrics.total_classes:,}</div>
        <div class="metric">Avg Complexity: {self.metrics.average_complexity:.1f}</div>
    </div>
    
    <div class="section">
        <h2>Component Scores</h2>
        <div class="metric">Complexity: {self.metrics.complexity_score:.1f}/100</div>
        <div class="metric">Security: {self.metrics.security_score:.1f}/100</div>
        <div class="metric">Maintainability: {self.metrics.maintainability_score:.1f}/100</div>
        <div class="metric">Duplication: {self.metrics.duplication_score:.1f}/100</div>
        <div class="metric">Documentation: {self.metrics.documentation_score:.1f}/100</div>
    </div>
    
    {self._generate_issues_html()}
    
    <div class="section">
        <h2>Recommendations</h2>
        <ul>
        """

        for rec in self._generate_recommendations():
            html += f"<li>{rec}</li>"

        html += """
        </ul>
    </div>
</body>
</html>
        """

        return html

    def save_report(self, output_path: str | Path, format: str = "text") -> None:
        """Save report to file.

        Args:
            output_path: Path to save the report.
            format: Report format ("text", "json", or "html").
        """
        output_path = Path(output_path)

        if format == "text":
            content = self.generate_text_report()
        elif format == "json":
            content = self.generate_json_report()
        elif format == "html":
            content = self.generate_html_report()
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []

        if self.metrics.security_issues_count > 0:
            recommendations.append("Review and fix security issues immediately")

        if self.metrics.complexity_issues_count > 0:
            recommendations.append(
                "Refactor complex functions to improve maintainability"
            )

        if self.metrics.dead_code_items_count > 0:
            recommendations.append("Remove unused code to improve clarity")

        if self.metrics.duplicate_blocks_count > 0:
            recommendations.append("Extract common code into reusable functions")

        if self.metrics.overall_score < 70:
            recommendations.append("Consider implementing code review processes")

        if not recommendations:
            recommendations.append("Code quality is good! Keep up the excellent work.")

        return recommendations

    def _get_grade_color(self) -> str:
        """Get color for quality grade."""
        grade = self.metrics.quality_grade
        if grade.startswith("A"):
            return "#4CAF50"  # Green
        elif grade.startswith("B"):
            return "#2196F3"  # Blue
        elif grade.startswith("C"):
            return "#FF9800"  # Orange
        elif grade.startswith("D"):
            return "#FF5722"  # Red-Orange
        else:
            return "#F44336"  # Red

    def _generate_issues_html(self) -> str:
        """Generate HTML for issues section."""
        html = ""
        issues = self.results.get("issues", {})

        for issue_type, issue_list in issues.items():
            if issue_list:
                html += f"""
    <div class="section">
        <h2>{issue_type.title()} Issues ({len(issue_list)})</h2>
                """

                for issue in issue_list[:10]:  # Show first 10
                    severity_class = self._get_severity_class(
                        issue.get("severity", "low")
                    )
                    html += f"""
        <div class="issue {severity_class}">
            <strong>{issue.get("message", "Unknown issue")}</strong><br>
            File: {issue.get("file", "unknown")}
        </div>
                    """

                if len(issue_list) > 10:
                    html += f"<p>... and {len(issue_list) - 10} more issues</p>"

                html += "</div>"

        return html

    def _get_severity_class(self, severity: str) -> str:
        """Get CSS class for severity level."""
        if severity == "high":
            return "high-severity"
        elif severity == "medium":
            return "medium-severity"
        else:
            return "low-severity"
