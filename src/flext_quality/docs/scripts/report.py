"""FLEXT Quality Documentation Reporting System.

Generates comprehensive quality reports, analytics, and dashboards
from audit, validation, and optimization results.

Usage:
    python report.py --format html
    python report.py --monthly-trends --notify
    python report.py --dashboard --serve
"""

from __future__ import annotations

import sys
from collections.abc import (
    Callable,
    Mapping,
    MutableSequence,
)
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated, ClassVar, override

from flext_cli import cli
from jinja2 import Template

from flext_quality import c, m, p, r, s, t, u


class FlextQualityDocumentationReporter:
    """Documentation quality reporting and analytics system."""

    class AuditSummary(m.BaseModel):
        """Audit data summary structure."""

        quality_score: int
        total_issues: int
        critical_issues: int
        high_issues: int
        medium_issues: int
        low_issues: int

    class ValidationSummary(m.BaseModel):
        """Validation data summary structure."""

        links_checked: int
        valid_links: int
        broken_links: int
        warnings: int

    class OptimizationSummary(m.BaseModel):
        """Optimization data summary structure."""

        files_processed: int
        changes_made: int
        backups_created: int
        optimizations_applied: int

    class SummaryMetrics(m.BaseModel):
        """Summary metrics structure."""

        overall_score: int
        total_issues: int
        files_analyzed: int
        links_checked: int
        optimizations_applied: int
        quality_trend: str

    class Recommendation(m.BaseModel):
        """Recommendation structure."""

        priority: str
        category: str
        title: str
        description: str
        actions: t.StrSequence

    class TrendEntry(m.BaseModel):
        """Trend entry structure."""

        date: datetime
        quality_score: int | None = None
        total_issues: int | None = None
        links_checked: int | None = None
        broken_links: int | None = None
        changes_made: int | None = None
        files_processed: int | None = None

    class TrendData(m.BaseModel):
        """Trend data structure."""

        audit_trends: t.SequenceOf[FlextQualityDocumentationReporter.TrendEntry]
        validation_trends: t.SequenceOf[FlextQualityDocumentationReporter.TrendEntry]
        optimization_trends: t.SequenceOf[FlextQualityDocumentationReporter.TrendEntry]

    class ReportData(m.BaseModel):
        """Report data structure."""

        timestamp: str
        title: str
        audit: t.MappingKV[str, t.Quality.DocumentationReportValue] | None
        validation: t.MappingKV[str, t.Quality.DocumentationReportValue] | None
        optimization: t.MappingKV[str, t.Quality.DocumentationReportValue] | None
        summary: FlextQualityDocumentationReporter.SummaryMetrics
        trends: FlextQualityDocumentationReporter.TrendData | None
        recommendations: t.SequenceOf[FlextQualityDocumentationReporter.Recommendation]

    REPORT_DATA_ADAPTER: ClassVar[m.TypeAdapter[ReportData]] = m.TypeAdapter(ReportData)

    def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
        """Initialize the documentation reporter with reports directory."""
        self.reports_dir = Path(reports_dir)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.template_dir = Path(__file__).parent / "templates"
        self.audit_data: t.MappingKV[str, t.Quality.DocumentationReportValue] | None = (
            None
        )
        self.validation_data: (
            t.MappingKV[str, t.Quality.DocumentationReportValue] | None
        ) = None
        self.optimization_data: (
            t.MappingKV[str, t.Quality.DocumentationReportValue] | None
        ) = None
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.load_latest_reports()

    def load_latest_reports(self) -> None:
        """Load the most recent audit, validation, and optimization reports."""
        self.audit_data = self._load_json_report("latest_audit.json")
        self.validation_data = self._load_json_report("latest_validation.json")
        self.optimization_data = self._load_json_report("latest_optimization.json")

    def _load_json_report(
        self,
        filename: str,
    ) -> t.MappingKV[str, t.Quality.DocumentationReportValue] | None:
        """Load a JSON report file."""
        filepath = self.reports_dir / filename
        if filepath.exists():
            try:
                result: t.MappingKV[str, t.Quality.DocumentationReportValue] = (
                    t.Quality.REPORT_VALUE_MAPPING_ADAPTER.validate_json(
                        Path(filepath).read_bytes()
                    )
                )
                return result
            except c.EXC_OS_VALUE:
                pass
        return None

    def generate_quality_report(
        self,
        report_format: str = "html",
        *,
        include_trends: bool = False,
    ) -> str:
        """Generate comprehensive quality report."""
        report_data = FlextQualityDocumentationReporter.ReportData(
            timestamp=datetime.now(UTC).isoformat(),
            title="FLEXT Quality Documentation Report",
            audit=self.audit_data,
            validation=self.validation_data,
            optimization=self.optimization_data,
            summary=self._calculate_summary_metrics(),
            trends=self._analyze_trends() if include_trends else None,
            recommendations=self._generate_recommendations(),
        )
        if report_format == "html":
            return self._generate_html_report(report_data)
        if report_format == "json":
            report_text: str = self.REPORT_DATA_ADAPTER.dump_json(
                report_data,
                indent=2,
            ).decode()
            return report_text
        if report_format == "markdown":
            return self._generate_markdown_report(report_data)
        msg = f"Unsupported format: {report_format}"
        raise ValueError(msg)

    def _calculate_summary_metrics(
        self,
    ) -> FlextQualityDocumentationReporter.SummaryMetrics:
        """Calculate summary metrics from all available data."""
        overall_score = 0
        total_issues = 0
        files_analyzed = 0
        links_checked = 0
        optimizations_applied = 0
        quality_trend = "unknown"

        if self.audit_data and isinstance(self.audit_data, dict):
            metrics = self.audit_data.get("metrics")
            if isinstance(metrics, dict):
                score = metrics.get("quality_score", 0)
                if isinstance(score, int):
                    overall_score = score
            issues = self.audit_data.get("issues")
            if isinstance(issues, list):
                total_issues += len(issues)
            files_analyzed_raw = self.audit_data.get("files_analyzed", 0)
            if isinstance(files_analyzed_raw, int):
                files_analyzed = max(files_analyzed, files_analyzed_raw)
        if self.validation_data and isinstance(self.validation_data, dict):
            link_validation = self.validation_data.get("link_validation")
            if isinstance(link_validation, dict):
                links_checked_raw = link_validation.get("links_checked", 0)
                if isinstance(links_checked_raw, int):
                    links_checked = links_checked_raw
                errors = link_validation.get("errors")
                if isinstance(errors, list):
                    total_issues += len(errors)
            content_validation = self.validation_data.get("content_validation")
            if isinstance(content_validation, dict):
                content_issues = content_validation.get("content_issues")
                if isinstance(content_issues, list):
                    total_issues += len(content_issues)
        if self.optimization_data and isinstance(self.optimization_data, dict):
            changes_made = self.optimization_data.get("changes_made", 0)
            if isinstance(changes_made, int):
                optimizations_applied = changes_made
        if overall_score >= 80:
            quality_trend = "excellent"
        elif overall_score >= 60:
            quality_trend = "good"
        elif overall_score >= 40:
            quality_trend = "needs_improvement"
        else:
            quality_trend = "critical"

        return FlextQualityDocumentationReporter.SummaryMetrics(
            overall_score=overall_score,
            total_issues=total_issues,
            files_analyzed=files_analyzed,
            links_checked=links_checked,
            optimizations_applied=optimizations_applied,
            quality_trend=quality_trend,
        )

    def _analyze_trends(
        self,
    ) -> FlextQualityDocumentationReporter.TrendData | None:
        """Analyze quality trends over time."""
        return None

    def _generate_recommendations(
        self,
    ) -> MutableSequence[FlextQualityDocumentationReporter.Recommendation]:
        """Generate actionable recommendations based on current data."""
        recommendations: MutableSequence[
            FlextQualityDocumentationReporter.Recommendation
        ] = []
        if self.audit_data and isinstance(self.audit_data, dict):
            audit_issues = self.audit_data.get("issues")
            if isinstance(audit_issues, list):
                critical_issues: MutableSequence[Mapping[str, t.Primitives]] = [
                    i
                    for i in audit_issues
                    if isinstance(i, dict) and i.get("severity") == "critical"
                ]
                if critical_issues:
                    recommendations.append(
                        FlextQualityDocumentationReporter.Recommendation(
                            priority="critical",
                            category="immediate_fixes",
                            title=f"Fix {len(critical_issues)} Critical Issues",
                            description="Address critical documentation issues immediately",
                            actions=[
                                "Review critical issues in audit report",
                                "Prioritize fixes",
                                "Re-run audit after fixes",
                            ],
                        ),
                    )
                outdated: MutableSequence[Mapping[str, t.Primitives]] = [
                    i
                    for i in audit_issues
                    if isinstance(i, dict) and i.get("type") == "outdated_content"
                ]
                if outdated:
                    recommendations.append(
                        FlextQualityDocumentationReporter.Recommendation(
                            priority="high",
                            category="content_freshness",
                            title=f"Update {len(outdated)} Outdated Documents",
                            description="Review and update documentation that hasn't been modified recently",
                            actions=[
                                "Identify documents needing updates",
                                "Review content accuracy",
                                "Update timestamps and version info",
                            ],
                        ),
                    )
        if self.validation_data and isinstance(self.validation_data, dict):
            link_validation = self.validation_data.get("link_validation")
            if isinstance(link_validation, dict):
                validation_errors_raw = link_validation.get("errors")
                if not isinstance(validation_errors_raw, list):
                    return recommendations
                validation_errors_list: t.JsonList = list(
                    validation_errors_raw,
                )
                if validation_errors_list:
                    broken_links: MutableSequence[Mapping[str, t.Primitives]] = []
                    for e_raw in validation_errors_list:
                        try:
                            error_entry: t.JsonMapping = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(
                                e_raw
                            )
                        except c.EXC_TYPE_VALIDATION:
                            continue
                        error_type = error_entry.get("type")
                        if error_type in {
                            "broken_external_link",
                            "broken_internal_link",
                        }:
                            normalized: t.MappingKV[str, t.Primitives] = {
                                key: value
                                for key, value in error_entry.items()
                                if isinstance(value, (str, int, float, bool))
                            }
                            if normalized:
                                broken_links.append(normalized)
                    if broken_links:
                        recommendations.append(
                            FlextQualityDocumentationReporter.Recommendation(
                                priority="high",
                                category="link_maintenance",
                                title=f"Fix {len(broken_links)} Broken Links",
                                description="Repair or remove broken internal and external links",
                                actions=[
                                    "Review broken link report",
                                    "Update or remove invalid URLs",
                                    "Test links after fixes",
                                ],
                            ),
                        )
        if self.optimization_data and isinstance(self.optimization_data, dict):
            optimizations = self.optimization_data.get("optimizations")
            if not optimizations or (
                isinstance(optimizations, list) and not optimizations
            ):
                recommendations.append(
                    FlextQualityDocumentationReporter.Recommendation(
                        priority="medium",
                        category="automation_setup",
                        title="Set Up Automated Optimization",
                        description="Configure automated formatting and style fixes",
                        actions=[
                            "Set up pre-commit hooks",
                            "Configure CI/CD optimization",
                            "Schedule regular optimization runs",
                        ],
                    ),
                )
        if not recommendations:
            recommendations.append(
                FlextQualityDocumentationReporter.Recommendation(
                    priority="low",
                    category="maintenance_setup",
                    title="Establish Regular Maintenance Schedule",
                    description="Set up automated quality checks and maintenance procedures",
                    actions=[
                        "Schedule weekly audits",
                        "Configure automated reporting",
                        "Set up team notifications",
                    ],
                ),
            )
        return recommendations

    def _generate_html_report(
        self,
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> str:
        """Generate HTML quality report."""
        template = self._get_html_template()
        timestamp = datetime.fromisoformat(data.timestamp).strftime(
            "%Y-%m-%d %H:%M:%S",
        )
        template_data = {
            "title": data.title,
            "timestamp": timestamp,
            "summary": data.summary,
            "audit_summary": self._summarize_audit_data(data.audit),
            "validation_summary": self._summarize_validation_data(data.validation),
            "optimization_summary": self._summarize_optimization_data(
                data.optimization,
            ),
            "recommendations": data.recommendations,
            "charts": self._generate_charts(data) if data.trends else None,
        }
        render_method: Callable[..., str] = getattr(template, "render")
        rendered: str = render_method(**template_data)
        return rendered

    def _get_html_template(self) -> Template:
        """Get HTML report template."""
        template_content = '\n<!DOCTYPE html>\n<html>\n<head>\n    <title>{{ title }}</title>\n    <style>\n        body { font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }\n        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }\n        .header { text-align: center; border-bottom: 2px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }\n        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }\n        .metric-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007acc; }\n        .metric-value { font-size: 2.5em; font-weight: bold; color: #007acc; margin: 10px 0; }\n        .metric-label { color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }\n        .section { margin: 40px 0; }\n        .section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }\n        .recommendations { display: grid; gap: 15px; }\n        .recommendation { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; }\n        .priority-critical { border-left: 4px solid #dc3545; background: #f8d7da; }\n        .priority-high { border-left: 4px solid #fd7e14; background: #fff3cd; }\n        .priority-medium { border-left: 4px solid #ffc107; background: #fff3cd; }\n        .priority-low { border-left: 4px solid #28a745; background: #d4edda; }\n        .issue-list { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto; }\n        .issue-item { background: white; margin: 5px 0; padding: 8px; border-radius: 3px; border-left: 3px solid #dc3545; }\n        .timestamp { color: #666; font-size: 0.9em; text-align: center; margin-top: 30px; }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="header">\n            <h1>{{ title }}</h1>\n            <p>Generated: {{ timestamp }}</p>\n        </div>\n\n        <div class="summary-grid">\n            <div class="metric-card">\n                <div class="metric-label">Overall Quality Score</div>\n                <div class="metric-value">{{ summary.overall_score }}%</div>\n                <div>Trend: {{ summary.quality_trend|title }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Files Analyzed</div>\n                <div class="metric-value">{{ summary.files_analyzed }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Total Issues</div>\n                <div class="metric-value">{{ summary.total_issues }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Links Checked</div>\n                <div class="metric-value">{{ summary.links_checked }}</div>\n            </div>\n        </div>\n\n        {% if audit_summary %}\n        <div class="section">\n            <h2>Content Audit Results</h2>\n            <p>Quality Score: {{ audit_summary.quality_score }}%</p>\n            <p>Issues Found: {{ audit_summary.total_issues }}</p>\n            <p>Critical: {{ audit_summary.critical_issues }}, High: {{ audit_summary.high_issues }}</p>\n        </div>\n        {% endif %}\n\n        {% if validation_summary %}\n        <div class="section">\n            <h2>Link Validation Results</h2>\n            <p>Links Checked: {{ validation_summary.links_checked }}</p>\n            <p>Valid: {{ validation_summary.valid_links }}, Broken: {{ validation_summary.broken_links }}</p>\n        </div>\n        {% endif %}\n\n        {% if optimization_summary %}\n        <div class="section">\n            <h2>Optimization Results</h2>\n            <p>Files Processed: {{ optimization_summary.files_processed }}</p>\n            <p>Changes Made: {{ optimization_summary.changes_made }}</p>\n            <p>Backups Created: {{ optimization_summary.backups_created }}</p>\n        </div>\n        {% endif %}\n\n        <div class="section">\n            <h2>Recommendations</h2>\n            <div class="recommendations">\n                {% for rec in recommendations %}\n                <div class="recommendation priority-{{ rec.priority }}">\n                    <h3>{{ rec.title }}</h3>\n                    <p>{{ rec.description }}</p>\n                    <ul>\n                        {% for action in rec.actions %}\n                        <li>{{ action }}</li>\n                        {% endfor %}\n                    </ul>\n                </div>\n                {% endfor %}\n            </div>\n        </div>\n\n        <div class="timestamp">\n            Report generated by FLEXT Quality Documentation Maintenance System\n        </div>\n    </div>\n</body>\n</html>\n        '
        return Template(template_content)

    def _generate_markdown_report(
        self,
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> str:
        """Generate markdown quality report."""
        md = [f"# {data.title}", "", f"**Generated:** {data.timestamp}", ""]
        summary = data.summary
        md.extend([
            "## Summary",
            "",
            f"- **Overall Quality Score:** {summary.overall_score}% ({summary.quality_trend})",
            f"- **Files Analyzed:** {summary.files_analyzed}",
            f"- **Total Issues:** {summary.total_issues}",
            f"- **Links Checked:** {summary.links_checked}",
            "",
        ])
        if data.recommendations:
            md.extend(["## Recommendations", ""])
            for rec in data.recommendations:
                md.extend([
                    f"### {rec.title} ({rec.priority.upper()})",
                    "",
                    rec.description,
                    "",
                    "**Actions:**",
                ])
                md.extend(f"- {action}" for action in rec.actions)
                md.append("")
        return "\n".join(md)

    def _summarize_audit_data(
        self,
        audit_data: t.MappingKV[str, t.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.AuditSummary | None:
        """Summarize audit data for reporting."""
        if not audit_data or not isinstance(audit_data, dict):
            return None
        issues_raw_obj = audit_data.get("issues")
        issues_raw_val: list[t.Quality.DocumentationReportValue] = (
            list(issues_raw_obj) if isinstance(issues_raw_obj, list) else []
        )
        metrics_raw_obj = audit_data.get("metrics")
        metrics_raw_val = (
            dict(metrics_raw_obj) if isinstance(metrics_raw_obj, dict) else {}
        )
        quality_score_raw = metrics_raw_val.get("quality_score", 0)
        if not isinstance(quality_score_raw, int):
            quality_score_raw = 0
        critical_count = len([
            i
            for i in issues_raw_val
            if isinstance(i, dict) and i.get("severity") == "critical"
        ])
        high_count = len([
            i
            for i in issues_raw_val
            if isinstance(i, dict) and i.get("severity") == "high"
        ])
        medium_count = len([
            i
            for i in issues_raw_val
            if isinstance(i, dict) and i.get("severity") == "medium"
        ])
        low_count = len([
            i
            for i in issues_raw_val
            if isinstance(i, dict) and i.get("severity") == "low"
        ])
        return FlextQualityDocumentationReporter.AuditSummary(
            quality_score=quality_score_raw,
            total_issues=len(issues_raw_val),
            critical_issues=critical_count,
            high_issues=high_count,
            medium_issues=medium_count,
            low_issues=low_count,
        )

    def _summarize_validation_data(
        self,
        validation_data: t.MappingKV[str, t.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.ValidationSummary | None:
        """Summarize validation data for reporting."""
        if not validation_data or not isinstance(validation_data, dict):
            return None
        link_data_raw_obj = validation_data.get("link_validation")
        link_data_raw = (
            dict(link_data_raw_obj) if isinstance(link_data_raw_obj, dict) else {}
        )
        links_checked_raw = link_data_raw.get("links_checked", 0)
        valid_links_raw = link_data_raw.get("valid_links", 0)
        broken_links_raw = link_data_raw.get("broken_links", 0)
        warnings_raw = link_data_raw.get("warnings", 0)
        return FlextQualityDocumentationReporter.ValidationSummary(
            links_checked=links_checked_raw
            if isinstance(links_checked_raw, int)
            else 0,
            valid_links=valid_links_raw if isinstance(valid_links_raw, int) else 0,
            broken_links=broken_links_raw if isinstance(broken_links_raw, int) else 0,
            warnings=warnings_raw if isinstance(warnings_raw, int) else 0,
        )

    def _summarize_optimization_data(
        self,
        optimization_data: t.MappingKV[str, t.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.OptimizationSummary | None:
        """Summarize optimization data for reporting."""
        if not optimization_data or not isinstance(optimization_data, dict):
            return None
        files_processed_raw = optimization_data.get("files_processed", 0)
        changes_made_raw = optimization_data.get("changes_made", 0)
        backups_created_raw = optimization_data.get("backups_created", [])
        optimizations_raw = optimization_data.get("optimizations", [])
        return FlextQualityDocumentationReporter.OptimizationSummary(
            files_processed=files_processed_raw
            if isinstance(files_processed_raw, int)
            else 0,
            changes_made=changes_made_raw if isinstance(changes_made_raw, int) else 0,
            backups_created=len(backups_created_raw)
            if isinstance(backups_created_raw, list)
            else 0,
            optimizations_applied=len(optimizations_raw)
            if isinstance(optimizations_raw, list)
            else 0,
        )

    def _generate_charts(
        self,
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> t.StrMapping | None:
        """Generate charts for the report (placeholder for future implementation)."""
        _ = data
        return None

    def generate_trend_report(self, days: int = 30) -> str:
        """Generate trend analysis report over specified time period."""
        report_files = list(self.reports_dir.glob("*.json"))
        recent_reports: MutableSequence[
            t.MappingKV[str, t.Quality.DocumentationReportValue | datetime]
        ] = []
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        for report_file in report_files:
            if "latest_" in report_file.name:
                continue
            try:
                date_str = report_file.name.split("_")[1]
                report_date = datetime.strptime(date_str[:8], "%Y%m%d").replace(
                    tzinfo=UTC,
                )
                if report_date >= cutoff_date:
                    report_data_raw: t.MappingKV[
                        str, t.Quality.DocumentationReportValue
                    ] = t.Quality.REPORT_VALUE_MAPPING_ADAPTER.validate_json(
                        Path(report_file).read_bytes(),
                    )
                    report_data_dict: t.MappingKV[
                        str, t.Quality.DocumentationReportValue | datetime
                    ] = {
                        **report_data_raw,
                        "date": report_date,
                    }
                    recent_reports.append(report_data_dict)
            except (ValueError, KeyError):
                continue
        trend_data = self._analyze_trend_data(recent_reports)
        return self._generate_trend_report(trend_data, days)

    def _analyze_trend_data(
        self,
        reports: t.SequenceOf[
            Mapping[str, t.Quality.DocumentationReportValue | datetime]
        ],
    ) -> FlextQualityDocumentationReporter.TrendData | t.StrMapping:
        """Analyze trend data from historical reports."""
        if not reports:
            return {"error": "No historical data available"}
        audit_trends: MutableSequence[FlextQualityDocumentationReporter.TrendEntry] = []
        validation_trends: MutableSequence[
            FlextQualityDocumentationReporter.TrendEntry
        ] = []
        optimization_trends: MutableSequence[
            FlextQualityDocumentationReporter.TrendEntry
        ] = []
        for report in reports:
            date_val_raw = report.get("date")
            if date_val_raw is None:
                date_val_raw = report.get("timestamp", datetime.now(UTC))
            if isinstance(date_val_raw, datetime):
                date_val = date_val_raw
            else:
                date_val = datetime.now(UTC)
            if "metrics" in report:
                metrics = report.get("metrics")
                if isinstance(metrics, dict):
                    quality_score = metrics.get("quality_score")
                    issues = report.get("issues")
                    if isinstance(quality_score, int) and isinstance(issues, list):
                        audit_trends.append(
                            FlextQualityDocumentationReporter.TrendEntry(
                                date=date_val,
                                quality_score=quality_score,
                                total_issues=len(issues),
                            ),
                        )
            if "link_validation" in report:
                link_validation = report.get("link_validation")
                if isinstance(link_validation, dict):
                    links_checked = link_validation.get("links_checked", 0)
                    broken_links = link_validation.get("broken_links", 0)
                    if isinstance(links_checked, int) and isinstance(broken_links, int):
                        validation_trends.append(
                            FlextQualityDocumentationReporter.TrendEntry(
                                date=date_val,
                                links_checked=links_checked,
                                broken_links=broken_links,
                            ),
                        )
            if "changes_made" in report:
                changes_made = report.get("changes_made")
                files_processed = report.get("files_processed", 0)
                if isinstance(changes_made, int) and isinstance(files_processed, int):
                    optimization_trends.append(
                        FlextQualityDocumentationReporter.TrendEntry(
                            date=date_val,
                            changes_made=changes_made,
                            files_processed=files_processed,
                        ),
                    )
        return FlextQualityDocumentationReporter.TrendData(
            audit_trends=sorted(audit_trends, key=lambda e: e.date),
            validation_trends=sorted(validation_trends, key=lambda e: e.date),
            optimization_trends=sorted(optimization_trends, key=lambda e: e.date),
        )

    def _generate_trend_report(
        self,
        trend_data: FlextQualityDocumentationReporter.TrendData | t.StrMapping,
        days: int,
    ) -> str:
        """Generate trend analysis report."""
        md = [
            f"# Documentation Quality Trends - Last {days} Days",
            "",
            f"Generated: {datetime.now(UTC).isoformat()}",
            "",
        ]
        if isinstance(trend_data, dict) and "error" in trend_data:
            error_val = trend_data.get("error")
            if isinstance(error_val, str):
                md.extend([f"**Error:** {error_val}", ""])
            return "\n".join(md)
        if isinstance(trend_data, dict):
            return "\n".join(md)
        # trend_data is TrendData BaseModel
        if not isinstance(trend_data, FlextQualityDocumentationReporter.TrendData):
            return "\n".join(md)
        typed_trend_data: FlextQualityDocumentationReporter.TrendData = trend_data
        if typed_trend_data.audit_trends:
            md.extend(["## Quality Score Trends", ""])
            md.extend((
                "| Date | Quality Score | Issues |",
                "|------|---------------|--------|",
            ))
            for trend in typed_trend_data.audit_trends[-10:]:
                date_str = trend.date.strftime("%Y-%m-%d")
                md.append(
                    f"| {date_str} | {trend.quality_score}% | {trend.total_issues} |",
                )
            md.append("")
        if typed_trend_data.validation_trends:
            md.extend(["## Link Validation Trends", ""])
            md.extend((
                "| Date | Links Checked | Broken Links |",
                "|------|---------------|--------------|",
            ))
            for trend in typed_trend_data.validation_trends[-10:]:
                date_str = trend.date.strftime("%Y-%m-%d")
                md.append(
                    f"| {date_str} | {trend.links_checked} | {trend.broken_links} |",
                )
            md.append("")
        if typed_trend_data.optimization_trends:
            md.extend(["## Optimization Trends", ""])
            md.extend((
                "| Date | Files Processed | Changes Made |",
                "|------|-----------------|--------------|",
            ))
            for trend in typed_trend_data.optimization_trends[-10:]:
                date_str = trend.date.strftime("%Y-%m-%d")
                md.append(
                    f"| {date_str} | {trend.files_processed} | {trend.changes_made} |",
                )
            md.append("")
        return "\n".join(md)

    def save_report(
        self,
        content: str,
        filename: str,
        report_format: str = "html",
    ) -> Path:
        """Save report to file."""
        filepath = self.reports_dir / f"{filename}.{report_format}"
        _ = filepath.write_text(content, encoding="utf-8")
        return filepath


class _ReportCommand(s[bool]):
    """CLI command for FLEXT Quality documentation reporting."""

    output_format: Annotated[
        str,
        u.Field(
            default="html",
            alias="format",
            description="Report format (html|json|markdown)",
        ),
    ] = "html"
    output: Annotated[
        str,
        u.Field(
            default="docs/maintenance/reports/",
            description="Output directory for reports",
        ),
    ] = "docs/maintenance/reports/"
    filename: Annotated[
        str | None,
        u.Field(default=None, description="Custom filename for the report"),
    ] = None
    monthly_trends: Annotated[
        bool,
        u.Field(default=False, description="Generate monthly trend analysis"),
    ] = False
    weekly_trends: Annotated[
        bool,
        u.Field(default=False, description="Generate weekly trend analysis"),
    ] = False
    include_trends: Annotated[
        bool,
        u.Field(default=False, description="Include trend analysis in quality report"),
    ] = False
    notify: Annotated[
        bool,
        u.Field(default=False, description="Send notifications"),
    ] = False
    webhook_url: Annotated[
        str | None,
        u.Field(default=None, description="Webhook URL for notifications"),
    ] = None
    serve: Annotated[
        bool,
        u.Field(default=False, description="Serve dashboard (not implemented yet)"),
    ] = False

    @override
    def execute(self) -> p.Result[bool]:
        """Generate the requested report."""
        reporter = FlextQualityDocumentationReporter(self.output)
        if self.monthly_trends:
            trend_report = reporter.generate_trend_report(days=30)
            filename = (
                self.filename
                or f"monthly_trends_{datetime.now(UTC).strftime('%Y%m%d')}"
            )
            reporter.save_report(trend_report, filename, "md")
        elif self.weekly_trends:
            trend_report = reporter.generate_trend_report(days=7)
            filename = (
                self.filename or f"weekly_trends_{datetime.now(UTC).strftime('%Y%m%d')}"
            )
            reporter.save_report(trend_report, filename, "md")
        else:
            report_content = reporter.generate_quality_report(
                self.output_format,
                include_trends=self.include_trends,
            )
            filename = (
                self.filename
                or f"quality_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
            )
            reporter.save_report(report_content, filename, self.output_format)
        return r[bool].ok(value=True)


def main(args: t.StrSequence | None = None) -> int:
    """Main entry point for reporting system via the canonical cli facade."""
    app = cli.create_app_with_common_params(
        name="flext-quality-docs-report",
        help_text="FLEXT Quality Documentation Reporting",
    )
    cli.register_result_routes(
        app,
        [
            m.Cli.ResultCommandRoute(
                name="run",
                help_text="Generate a documentation quality report",
                model_cls=_ReportCommand,
                handler=lambda params: params.execute(),
            ),
        ],
    )
    outcome = cli.execute_app(
        app,
        prog_name="flext-quality-docs-report",
        args=list(args) if args is not None else sys.argv[1:],
    )
    return 0 if outcome.success else 1


if __name__ == "__main__":
    cli.exit(main())
