"""Quality report generation and formatting.

REFACTORED: Complete rewrite due to corrupted file with 286+ syntax errors.
Uses flext-core patterns for standardization.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from flext_quality.metrics import QualityMetrics

if TYPE_CHECKING:
    from pathlib import Path


class QualityReport:
    """Generates quality reports from analysis results."""

    def __init__(self, analysis_results: dict[str, Any]) -> None:
        """Initialize quality report with analysis results."""
        self.results = analysis_results
        self.metrics = QualityMetrics.from_analysis_results(analysis_results)

    def generate_text_report(self) -> str:
        """Generate human-readable text report."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("FLEXT QUALITY ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")

        # Summary section
        lines.append("SUMMARY")
        lines.append("-" * 20)
        lines.append(f"Total files analyzed: {self.metrics.total_files}")
        lines.append(f"Total issues found: {self.metrics.total_issues}")
        lines.append(f"Quality score: {self.metrics.quality_score:.1f}%")
        lines.append("")

        # Issues by category
        if self.metrics.issues_by_category:
            lines.extend(("ISSUES BY CATEGORY", "-" * 20))
            for category, count in self.metrics.issues_by_category.items():
                lines.append(f"{category}: {count}")
            lines.append("")

        # Top problematic files
        if self.metrics.problematic_files:
            lines.extend(("TOP PROBLEMATIC FILES", "-" * 20))
            lines.extend(
                f"{file_info['file']}: {file_info['issues']} issues"
                for file_info in self.metrics.problematic_files[:10]
            )
            lines.append("")

        # Recommendations
        lines.extend(("RECOMMENDATIONS", "-" * 20))
        lines.extend(self._generate_recommendations())

        return "\n".join(lines)

    def generate_json_report(self) -> str:
        """Generate machine-readable JSON report."""
        report_data = {
            "summary": {
                "total_files": self.metrics.total_files,
                "total_issues": self.metrics.total_issues,
                "quality_score": self.metrics.quality_score,
                "timestamp": self.metrics.timestamp,
            },
            "metrics": self.metrics.to_dict(),
            "issues_by_category": self.metrics.issues_by_category,
            "problematic_files": self.metrics.problematic_files,
            "recommendations": self._generate_recommendations(),
        }
        return json.dumps(report_data, indent=2, ensure_ascii=False)

    def save_report(self, output_path: Path, format_type: str = "text") -> None:
        """Save report to file."""
        if format_type == "json":
            content = self.generate_json_report()
            output_path = output_path.with_suffix(".json")
        else:
            content = self.generate_text_report()
            output_path = output_path.with_suffix(".txt")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    def _generate_recommendations(self) -> list[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        if self.metrics.quality_score < 70:
            recommendations.append(
                "Quality score is below 70%. Consider addressing high-priority issues first.",
            )

        if "syntax_errors" in self.metrics.issues_by_category:
            syntax_count = self.metrics.issues_by_category["syntax_errors"]
            if syntax_count > 0:
                recommendations.append(
                    f"Fix {syntax_count} syntax errors immediately - these prevent execution.",
                )

        if "security_issues" in self.metrics.issues_by_category:
            security_count = self.metrics.issues_by_category["security_issues"]
            if security_count > 0:
                recommendations.append(
                    f"Address {security_count} security issues to prevent vulnerabilities.",
                )

        if "type_errors" in self.metrics.issues_by_category:
            type_count = self.metrics.issues_by_category["type_errors"]
            if type_count > 10:
                recommendations.append(
                    "Consider adding comprehensive type annotations for better code quality.",
                )

        if not recommendations:
            recommendations.append(
                "Quality looks good! Consider running tests and benchmarks.",
            )

        return recommendations


class QualityDashboard:
    """Dashboard for quality metrics visualization."""

    def __init__(self, reports: list[QualityReport]) -> None:
        """Initialize dashboard with multiple reports."""
        self.reports = reports

    def generate_summary_dashboard(self) -> str:
        """Generate summary dashboard across all reports."""
        lines = []

        lines.extend(("=" * 80, "FLEXT QUALITY DASHBOARD", "=" * 80, ""))

        # Overall statistics
        total_files = sum(report.metrics.total_files for report in self.reports)
        total_issues = sum(report.metrics.total_issues for report in self.reports)
        avg_quality = sum(
            report.metrics.quality_score for report in self.reports
        ) / len(self.reports)

        lines.append("OVERALL STATISTICS")
        lines.append("-" * 30)
        lines.append(f"Total projects analyzed: {len(self.reports)}")
        lines.append(f"Total files: {total_files}")
        lines.append(f"Total issues: {total_issues}")
        lines.append(f"Average quality score: {avg_quality:.1f}%")
        lines.append("")

        # Project breakdown
        lines.append("PROJECT BREAKDOWN")
        lines.append("-" * 30)
        for i, report in enumerate(self.reports, 1):
            lines.extend(
                (
                    f"Project {i}:",
                    f"  Files: {report.metrics.total_files}",
                    f"  Issues: {report.metrics.total_issues}",
                    f"  Quality: {report.metrics.quality_score:.1f}%",
                    "",
                ),
            )

        return "\n".join(lines)

    def export_dashboard(self, output_path: Path) -> None:
        """Export dashboard to file."""
        content = self.generate_summary_dashboard()
        output_path.write_text(content, encoding="utf-8")
