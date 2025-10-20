"""Quality report generation and formatting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from .grade_calculator import FlextQualityGradeCalculator
from .models import FlextQualityModels

IssueSeverity = FlextQualityModels.IssueSeverity


# =====================================================================
# Configuration Models (Pydantic 2) - SOLID Data-Driven Approach
# =====================================================================


class ReportThresholds(BaseModel):
    """Quality report threshold configuration."""

    issue_preview_limit: int = Field(default=5, ge=1)
    html_issue_limit: int = Field(default=10, ge=1)
    high_issue_threshold: int = Field(default=50, ge=0)
    min_coverage_threshold: int = Field(default=80, ge=0, le=100)
    min_score_threshold: int = Field(default=70, ge=0, le=100)
    high_type_error_threshold: int = Field(default=10, ge=0)


class GradeColors(BaseModel):
    """Grade-to-color mapping."""

    grades: dict[str, str] = Field(
        default_factory=lambda: {
            "A": "#2e7d32",
            "B": "#388e3c",
            "C": "#f57c00",
            "D": "#f44336",
            "F": "#d32f2f",
        }
    )


# =====================================================================
# Main Report Generator - SOLID Delegation Pattern
# =====================================================================


class FlextQualityReportGenerator:
    """Generates quality reports from analysis results."""

    def __init__(
        self,
        analysis_results: FlextQualityModels.AnalysisResults,
        thresholds: ReportThresholds | None = None,
        colors: GradeColors | None = None,
    ) -> None:
        """Initialize the quality report generator."""
        self.results = analysis_results
        self.thresholds = thresholds or ReportThresholds()
        self.colors = colors or GradeColors()

    def generate_text_report(self) -> str:
        """Generate a text-based quality report."""
        return "\n".join(self._TextReportBuilder.build(self.results, self.thresholds))

    def generate_json_report(self) -> str:
        """Generate a JSON-formatted quality report."""
        return json.dumps(
            self._JsonReportBuilder.build(self.results, self.thresholds),
            indent=2,
            default=str,
        )

    def to_json(self) -> str:
        """Alias for generate_json_report for compatibility."""
        return self.generate_json_report()

    def to_html(self) -> str:
        """Alias for generate_html_report for compatibility."""
        return self.generate_html_report()

    def generate_html_report(self) -> str:
        """Generate an HTML-formatted quality report."""
        return "\n".join(
            self._HtmlReportBuilder.build(self.results, self.thresholds, self.colors)
        )

    def save_report(self, output_path: Path, format_type: str = "text") -> None:
        """Save report to file."""
        content = {
            "json": self.generate_json_report,
            "html": self.generate_html_report,
        }.get(format_type, self.generate_text_report)()

        output_path.write_text(content, encoding="utf-8")

    # =====================================================================
    # Nested Utility Classes - Single Responsibility Each
    # =====================================================================

    class _ScoreCalculator:
        """Single responsibility: Calculate quality metrics."""

        @staticmethod
        def get_quality_score(results: FlextQualityModels.AnalysisResults) -> int:
            """Calculate overall quality score."""
            total = results.total_issues
            critical = len([
                i
                for i in (results.security_issues + results.complexity_issues)
                if getattr(i, "severity", None) == IssueSeverity.CRITICAL
            ])
            score = 100
            score -= critical * 10
            score -= (total - critical) * 2
            return max(0, score)

        @staticmethod
        def get_quality_grade(
            results: FlextQualityModels.AnalysisResults,
        ) -> str:
            """Calculate quality grade."""
            score = FlextQualityReportGenerator._ScoreCalculator.get_quality_score(
                results
            )
            grade = FlextQualityGradeCalculator.calculate_grade(float(score))
            return grade.value

        @staticmethod
        def get_critical_issues(results: FlextQualityModels.AnalysisResults) -> int:
            """Get number of critical issues."""
            return len([
                i
                for i in (results.security_issues + results.complexity_issues)
                if getattr(i, "severity", None) == IssueSeverity.CRITICAL
            ])

    class _RecommendationGenerator:
        """Single responsibility: Generate recommendations."""

        @staticmethod
        def generate(
            results: FlextQualityModels.AnalysisResults,
            thresholds: ReportThresholds,
        ) -> list[str]:
            """Generate recommendations based on analysis results."""
            score = FlextQualityReportGenerator._ScoreCalculator.get_quality_score(
                results
            )
            critical = FlextQualityReportGenerator._ScoreCalculator.get_critical_issues(
                results
            )
            coverage = float(results.overall_metrics.coverage_score)
            total = results.total_issues

            recs = []
            if critical > 0:
                recs.append(
                    f"Fix {critical} critical security/error issues immediately"
                )
            if total > thresholds.high_issue_threshold:
                recs.append(
                    "Consider breaking down large files and reducing complexity"
                )
            if score < thresholds.min_score_threshold:
                recs.extend([
                    "Implement automated code quality checks in your CI/CD pipeline",
                    "Add comprehensive unit tests to improve coverage",
                ])
            if coverage < thresholds.min_coverage_threshold:
                recs.append(
                    f"Increase test coverage from {coverage}% to at least {thresholds.min_coverage_threshold}%"
                )
            if results.duplication_issues:
                recs.append("Refactor duplicate code to improve maintainability")
            if results.complexity_issues:
                recs.append("Simplify complex functions and classes")

            return recs or [
                "Great job! Your code quality is excellent. Keep up the good work!"
            ]

    class _TextReportBuilder:
        """Single responsibility: Build text reports."""

        @staticmethod
        def build(
            results: FlextQualityModels.AnalysisResults,
            thresholds: ReportThresholds,
        ) -> list[str]:
            """Build text report."""
            calc = FlextQualityReportGenerator._ScoreCalculator
            grade = calc.get_quality_grade(results)
            score = calc.get_quality_score(results)
            critical = calc.get_critical_issues(results)

            lines = [
                "=" * 60,
                "FLEXT QUALITY REPORT",
                "=" * 60,
                f"Overall Grade: {grade}",
                f"Quality Score: {score}/100",
                f"Total Issues: {results.total_issues}",
                f"Critical Issues: {critical}",
                f"Files Analyzed: {int(results.overall_metrics.files_analyzed)}",
                f"Code Coverage: {float(results.overall_metrics.coverage_score)}%",
                "",
                "ISSUES BY CATEGORY:",
                "-" * 30,
            ]

            for category, issues in {
                "security": results.security_issues,
                "complexity": results.complexity_issues,
                "dead_code": results.dead_code_issues,
                "duplication": results.duplication_issues,
            }.items():
                if issues:
                    lines.append(f"\n{category} ({len(issues)} issues):")
                    for issue in issues[: thresholds.issue_preview_limit]:
                        msg = getattr(issue, "message", "No description")
                        lines.append(f"  - {msg}")
                    if len(issues) > thresholds.issue_preview_limit:
                        lines.append(
                            f"  ... and {len(issues) - thresholds.issue_preview_limit} more"
                        )

            recs = FlextQualityReportGenerator._RecommendationGenerator.generate(
                results, thresholds
            )
            if recs:
                lines.extend(["", "RECOMMENDATIONS:", "-" * 20])
                lines.extend(f"• {rec}" for rec in recs)

            return lines

    class _JsonReportBuilder:
        """Single responsibility: Build JSON reports."""

        @staticmethod
        def build(
            results: FlextQualityModels.AnalysisResults,
            thresholds: ReportThresholds,
        ) -> dict[str, object]:
            """Build JSON report."""
            calc = FlextQualityReportGenerator._ScoreCalculator
            return {
                "summary": {
                    "grade": calc.get_quality_grade(results),
                    "score": calc.get_quality_score(results),
                    "total_issues": results.total_issues,
                    "critical_issues": calc.get_critical_issues(results),
                    "files_analyzed": int(results.overall_metrics.files_analyzed),
                    "coverage_percent": float(results.overall_metrics.coverage_score),
                },
                "analysis_results": results,
                "recommendations": FlextQualityReportGenerator._RecommendationGenerator.generate(
                    results, thresholds
                ),
            }

    class _HtmlReportBuilder:
        """Single responsibility: Build HTML reports."""

        @staticmethod
        def build(
            results: FlextQualityModels.AnalysisResults,
            thresholds: ReportThresholds,
            colors: GradeColors,
        ) -> list[str]:
            """Build HTML report."""
            calc = FlextQualityReportGenerator._ScoreCalculator
            grade = calc.get_quality_grade(results)
            grade_color = colors.grades.get(grade, "#757575")
            score = calc.get_quality_score(results)
            critical = calc.get_critical_issues(results)
            coverage = float(results.overall_metrics.coverage_score)

            lines = [
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
                '    <div class="summary">',
                f'        <div class="grade">{grade}</div>',
                f'        <div class="score">Score: {score}/100</div>',
                "    </div>",
                '    <div class="section">',
                "        <h2>Quality Metrics</h2>",
                f'        <div class="metric"><strong>Total Issues:</strong> {results.total_issues}</div>',
                f'        <div class="metric"><strong>Critical Issues:</strong> {critical}</div>',
                f'        <div class="metric"><strong>Files Analyzed:</strong> {int(results.overall_metrics.files_analyzed)}</div>',
                f'        <div class="metric"><strong>Code Coverage:</strong> {coverage}%</div>',
                "    </div>",
            ]

            # Add issues section
            for category, issues in {
                "security": results.security_issues,
                "complexity": results.complexity_issues,
                "dead_code": results.dead_code_issues,
                "duplication": results.duplication_issues,
            }.items():
                if issues:
                    lines.extend([
                        '    <div class="section">',
                        f"        <h2>{category.title()} Issues ({len(issues)})</h2>",
                    ])
                    for issue in issues[: thresholds.html_issue_limit]:
                        severity = getattr(issue, "severity", "low")
                        file_path = str(getattr(issue, "file_path", "Unknown"))
                        line_num = getattr(issue, "line_number", "")
                        line_info = f" (line {line_num})" if line_num else ""
                        msg = getattr(issue, "message", "No message")
                        lines.append(
                            f'        <div class="issue {severity}-severity"><strong>{file_path}{line_info}:</strong> {msg}</div>'
                        )
                    if len(issues) > thresholds.html_issue_limit:
                        lines.append(
                            f'        <div class="issue">... and {len(issues) - thresholds.html_issue_limit} more issues</div>'
                        )
                    lines.append("    </div>")

            # Add recommendations
            recs = FlextQualityReportGenerator._RecommendationGenerator.generate(
                results, thresholds
            )
            lines.extend([
                '    <div class="section">',
                "        <h2>Recommendations</h2>",
                "        <ul>",
            ])
            lines.extend(f"            <li>{rec}</li>" for rec in recs)
            lines.extend(["        </ul>", "    </div>", "</body>", "</html>"])

            return lines


__all__ = [
    "FlextQualityReportGenerator",
    "GradeColors",
    "ReportThresholds",
]
