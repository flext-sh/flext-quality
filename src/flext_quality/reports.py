"""Quality report generation and formatting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path

from flext_core import FlextResult
from pydantic import BaseModel, Field

from .constants import FlextQualityConstants
from .grade_calculator import FlextQualityGradeCalculator
from .models import FlextQualityModels

IssueSeverity = FlextQualityModels.IssueSeverity


# =====================================================================
# Configuration Models (Pydantic 2) - SOLID Data-Driven Approach
# =====================================================================


class ReportFormat(StrEnum):
    """Supported report formats - removes .get() fallback."""

    TEXT = "text"
    JSON = "json"
    HTML = "html"


class ReportThresholds(BaseModel):
    """Quality report threshold configuration."""

    issue_preview_limit: int = Field(default=5, ge=1)
    html_issue_limit: int = Field(default=10, ge=1)
    high_issue_threshold: int = Field(default=50, ge=0)
    min_coverage_threshold: float = Field(default=80.0, ge=0.0, le=100.0)
    min_score_threshold: float = Field(default=70.0, ge=0.0, le=100.0)
    high_type_error_threshold: int = Field(default=10, ge=0)


class GradeColors:
    """Grade-to-color mapping - fixed enum-based colors."""

    # Color map for each grade - no .get() fallback needed
    COLOR_A = "#2e7d32"
    COLOR_B = "#388e3c"
    COLOR_C = "#f57c00"
    COLOR_D = "#f44336"
    COLOR_F = "#d32f2f"
    COLOR_UNKNOWN = "#757575"

    @staticmethod
    def get_color_for_grade(grade: str) -> str:
        """Get color for grade - fail-fast with proper type."""
        match grade:
            case "A+" | "A" | "A-":
                return GradeColors.COLOR_A
            case "B+" | "B" | "B-":
                return GradeColors.COLOR_B
            case "C+" | "C" | "C-":
                return GradeColors.COLOR_C
            case "D+" | "D":
                return GradeColors.COLOR_D
            case "F":
                return GradeColors.COLOR_F
            case _:
                return GradeColors.COLOR_UNKNOWN


class ReportData(BaseModel):
    """Validated report data - encapsulates all calculated metrics."""

    grade: str = Field(description="Quality grade (A+ to F)")
    score: int = Field(ge=0, le=100, description="Overall quality score")
    critical_issues: int = Field(ge=0, description="Number of critical issues")
    total_issues: int = Field(ge=0, description="Total number of issues")
    files_analyzed: int = Field(ge=0, description="Number of files analyzed")
    coverage_percent: float = Field(
        ge=0.0, le=100.0, description="Test coverage percentage"
    )


# =====================================================================
# Score Calculator - Pure function replacement for nested class
# =====================================================================


class ScoreCalculator:
    """Calculates quality metrics from analysis results - no static nesting."""

    # Constants replacing hardcoded magic numbers
    CRITICAL_ISSUE_PENALTY = 10
    NORMAL_ISSUE_PENALTY = 2
    BASE_SCORE = 100

    @staticmethod
    def calculate_quality_score(
        critical_count: int,
        total_count: int,
    ) -> int:
        """Calculate overall quality score from issue counts.

        No fallbacks, no fake data - pure calculation.
        Returns 0-100 range score.
        """
        if critical_count < 0 or total_count < 0:
            return 0

        score = ScoreCalculator.BASE_SCORE
        score -= critical_count * ScoreCalculator.CRITICAL_ISSUE_PENALTY
        score -= (total_count - critical_count) * ScoreCalculator.NORMAL_ISSUE_PENALTY

        return max(0, min(100, score))

    @staticmethod
    def calculate_quality_grade(
        score: int,
    ) -> str:
        """Calculate grade from score - uses FlextQualityGradeCalculator."""
        grade_result = FlextQualityGradeCalculator.calculate_grade(float(score))
        return grade_result.value

    @staticmethod
    def count_critical_issues(
        issues: list[FlextQualityModels.IssueProtocol],
    ) -> int:
        """Count critical issues - type-safe using Protocol."""
        return len([i for i in issues if i.severity == IssueSeverity.CRITICAL])


# =====================================================================
# Recommendation Generator - Pure function replacement
# =====================================================================


class RecommendationGenerator:
    """Generates recommendations based on analysis results."""

    @staticmethod
    def generate(
        results: FlextQualityModels.AnalysisResults,
        thresholds: ReportThresholds,
    ) -> list[str]:
        """Generate recommendations - returns empty list if no issues."""
        recommendations: list[str] = []

        critical = len(results.security_issues or []) + len(
            results.complexity_issues or []
        )
        total = (
            len(results.security_issues or [])
            + len(results.complexity_issues or [])
            + len(results.dead_code_issues or [])
            + len(results.duplication_issues or [])
        )
        score = ScoreCalculator.calculate_quality_score(critical, total)
        coverage = (
            float(results.overall_metrics.coverage_score)
            if results.overall_metrics
            else 0.0
        )

        if critical > 0:
            recommendations.append(
                f"Fix {critical} critical security/error issues immediately"
            )
        if total > thresholds.high_issue_threshold:
            recommendations.append(
                "Consider breaking down large files and reducing complexity"
            )
        if score < thresholds.min_score_threshold:
            recommendations.extend([
                "Implement automated code quality checks in your CI/CD pipeline",
                "Add complete unit tests to improve coverage",
            ])
        if coverage < thresholds.min_coverage_threshold:
            recommendations.append(
                f"Increase test coverage from {coverage:.1f}% to at least {thresholds.min_coverage_threshold}%"
            )
        if results.duplication_issues:
            recommendations.append("Refactor duplicate code to improve maintainability")
        if results.complexity_issues:
            recommendations.append("Simplify complex functions and classes")

        # Return recommendations or empty list (never fake "Great job!" message)
        return recommendations


# =====================================================================
# Report Builders - Top-level classes, not nested
# =====================================================================


class TextReportBuilder:
    """Builds text-formatted quality reports."""

    @staticmethod
    def build(
        results: FlextQualityModels.AnalysisResults,
        thresholds: ReportThresholds,
    ) -> FlextResult[str]:
        """Build text report with proper validation."""
        if results is None:
            return FlextResult[str].fail("Analysis results cannot be None")

        # Calculate metrics - fail-fast on invalid data
        security_issues = results.security_issues or []
        complexity_issues = results.complexity_issues or []
        dead_code_issues = results.dead_code_issues or []
        duplication_issues = results.duplication_issues or []

        critical = ScoreCalculator.count_critical_issues(
            security_issues + complexity_issues
        )
        total = (
            len(security_issues)
            + len(complexity_issues)
            + len(dead_code_issues)
            + len(duplication_issues)
        )
        score = ScoreCalculator.calculate_quality_score(critical, total)
        grade = ScoreCalculator.calculate_quality_grade(score)

        files_analyzed = (
            int(results.overall_metrics.files_analyzed)
            if results.overall_metrics
            else 0
        )
        coverage = (
            float(results.overall_metrics.coverage_score)
            if results.overall_metrics
            else 0.0
        )

        lines = [
            "=" * 60,
            "FLEXT QUALITY REPORT",
            "=" * 60,
            f"Overall Grade: {grade}",
            f"Quality Score: {score}/100",
            f"Total Issues: {total}",
            f"Critical Issues: {critical}",
            f"Files Analyzed: {files_analyzed}",
            f"Code Coverage: {coverage:.1f}%",
            "",
            "ISSUES BY CATEGORY:",
            "-" * 30,
        ]

        for category, issues in [
            ("security", security_issues),
            ("complexity", complexity_issues),
            ("dead_code", dead_code_issues),
            ("duplication", duplication_issues),
        ]:
            if issues:
                lines.append(f"\n{category} ({len(issues)} issues):")
                lines.extend([
                    f"  - {issue.message}"
                    for issue in issues[: thresholds.issue_preview_limit]
                ])
                if len(issues) > thresholds.issue_preview_limit:
                    remaining = len(issues) - thresholds.issue_preview_limit
                    lines.append(f"  ... and {remaining} more")

        recommendations = RecommendationGenerator.generate(results, thresholds)
        if recommendations:
            lines.extend(["", "RECOMMENDATIONS:", "-" * 20])
            lines.extend([f"• {rec}" for rec in recommendations])

        return FlextResult[str].ok("\n".join(lines))


class JsonReportBuilder:
    """Builds JSON-formatted quality reports."""

    @staticmethod
    def build(
        results: FlextQualityModels.AnalysisResults,
        thresholds: ReportThresholds,
    ) -> FlextResult[str]:
        """Build JSON report with proper validation."""
        if results is None:
            return FlextResult[str].fail("Analysis results cannot be None")

        # Calculate metrics
        security_issues = results.security_issues or []
        complexity_issues = results.complexity_issues or []
        dead_code_issues = results.dead_code_issues or []
        duplication_issues = results.duplication_issues or []

        critical = ScoreCalculator.count_critical_issues(
            security_issues + complexity_issues
        )
        total = (
            len(security_issues)
            + len(complexity_issues)
            + len(dead_code_issues)
            + len(duplication_issues)
        )
        score = ScoreCalculator.calculate_quality_score(critical, total)
        grade = ScoreCalculator.calculate_quality_grade(score)

        files_analyzed = (
            int(results.overall_metrics.files_analyzed)
            if results.overall_metrics
            else 0
        )
        coverage = (
            float(results.overall_metrics.coverage_score)
            if results.overall_metrics
            else 0.0
        )

        # Build report data with validated model
        report_dict = {
            "summary": {
                "grade": grade,
                "score": score,
                "total_issues": total,
                "critical_issues": critical,
                "files_analyzed": files_analyzed,
                "coverage_percent": coverage,
            },
            "recommendations": RecommendationGenerator.generate(results, thresholds),
        }

        try:
            json_str = json.dumps(report_dict, indent=2, default=str)
            return FlextResult[str].ok(json_str)
        except (TypeError, ValueError) as e:
            return FlextResult[str].fail(f"Failed to serialize JSON: {e}")


class HtmlReportBuilder:
    """Builds HTML-formatted quality reports."""

    @staticmethod
    def build(
        results: FlextQualityModels.AnalysisResults,
        thresholds: ReportThresholds,
    ) -> FlextResult[str]:
        """Build HTML report with proper validation."""
        if results is None:
            return FlextResult[str].fail("Analysis results cannot be None")

        # Calculate metrics
        security_issues = results.security_issues or []
        complexity_issues = results.complexity_issues or []
        dead_code_issues = results.dead_code_issues or []
        duplication_issues = results.duplication_issues or []

        critical = ScoreCalculator.count_critical_issues(
            security_issues + complexity_issues
        )
        total = (
            len(security_issues)
            + len(complexity_issues)
            + len(dead_code_issues)
            + len(duplication_issues)
        )
        score = ScoreCalculator.calculate_quality_score(critical, total)
        grade = ScoreCalculator.calculate_quality_grade(score)
        grade_color = GradeColors.get_color_for_grade(grade)

        files_analyzed = (
            int(results.overall_metrics.files_analyzed)
            if results.overall_metrics
            else 0
        )
        coverage = (
            float(results.overall_metrics.coverage_score)
            if results.overall_metrics
            else 0.0
        )

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
            f'        <div class="metric"><strong>Total Issues:</strong> {total}</div>',
            f'        <div class="metric"><strong>Critical Issues:</strong> {critical}</div>',
            f'        <div class="metric"><strong>Files Analyzed:</strong> {files_analyzed}</div>',
            f'        <div class="metric"><strong>Code Coverage:</strong> {coverage:.1f}%</div>',
            "    </div>",
        ]

        # Add issues section
        for category, issues in [
            ("security", security_issues),
            ("complexity", complexity_issues),
            ("dead_code", dead_code_issues),
            ("duplication", duplication_issues),
        ]:
            if issues:
                lines.extend([
                    '    <div class="section">',
                    f"        <h2>{category.title()} Issues ({len(issues)})</h2>",
                ])
                for issue in issues[: thresholds.html_issue_limit]:
                    severity_class = (
                        "high-severity"
                        if issue.severity == IssueSeverity.CRITICAL
                        else "medium-severity"
                        if issue.severity == IssueSeverity.HIGH
                        else "low-severity"
                    )
                    line_info = (
                        f" (line {issue.line_number})" if issue.line_number else ""
                    )
                    lines.append(
                        f'        <div class="issue {severity_class}"><strong>{issue.file_path}{line_info}:</strong> {issue.message}</div>'
                    )
                if len(issues) > thresholds.html_issue_limit:
                    remaining = len(issues) - thresholds.html_issue_limit
                    lines.append(
                        f'        <div class="issue">... and {remaining} more issues</div>'
                    )
                lines.append("    </div>")

        # Add recommendations
        recommendations = RecommendationGenerator.generate(results, thresholds)
        lines.extend([
            '    <div class="section">',
            "        <h2>Recommendations</h2>",
            "        <ul>",
        ])
        if recommendations:
            lines.extend([f"            <li>{rec}</li>" for rec in recommendations])
        lines.extend(["        </ul>", "    </div>", "</body>", "</html>"])

        return FlextResult[str].ok("\n".join(lines))


# =====================================================================
# Main Report Generator - Facade with FlextResult
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

    def generate_report(
        self,
        format_type: ReportFormat,
    ) -> FlextResult[str]:
        """Generate report in specified format - proper Enum dispatch."""
        match format_type:
            case ReportFormat.TEXT:
                return TextReportBuilder.build(self.results, self.thresholds)
            case ReportFormat.JSON:
                return JsonReportBuilder.build(self.results, self.thresholds)
            case ReportFormat.HTML:
                return HtmlReportBuilder.build(self.results, self.thresholds)

    def generate_text_report(self) -> FlextResult[str]:
        """Generate text-formatted report."""
        return self.generate_report(ReportFormat.TEXT)

    def generate_json_report(self) -> FlextResult[str]:
        """Generate JSON-formatted report."""
        return self.generate_report(ReportFormat.JSON)

    def generate_html_report(self) -> FlextResult[str]:
        """Generate HTML-formatted report."""
        return self.generate_report(ReportFormat.HTML)

    def save_report(
        self,
        output_path: Path,
        format_type: ReportFormat = ReportFormat.TEXT,
    ) -> FlextResult[bool]:
        """Save report to file with proper error handling."""
        report_result = self.generate_report(format_type)

        if report_result.is_failure:
            return FlextResult[bool].fail(
                f"Failed to generate report: {report_result.error}"
            )

        content = report_result.value

        try:
            output_path.write_text(content, encoding="utf-8")
            return FlextResult[bool].ok(True)
        except OSError as e:
            return FlextResult[bool].fail(f"Failed to write report file: {e}")


__all__ = [
    "FlextQualityReportGenerator",
    "GradeColors",
    "HtmlReportBuilder",
    "JsonReportBuilder",
    "RecommendationGenerator",
    "ReportData",
    "ReportFormat",
    "ReportThresholds",
    "ScoreCalculator",
    "TextReportBuilder",
]
