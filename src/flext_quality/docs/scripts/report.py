"""FLEXT Quality Documentation Reporting System.

Generates comprehensive quality reports, analytics, and dashboards
from audit, validation, and optimization results.

Usage:
    python report.py --format html
    python report.py --monthly-trends --notify
    python report.py --dashboard --serve

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Final, override

from flext_cli import cli, u as cli_u

from flext_quality import c, m, p, r, s, t, u

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableSequence

_QUALITY_SCORE_EXCELLENT: Final[int] = 80
_QUALITY_SCORE_GOOD: Final[int] = 60
_QUALITY_SCORE_ACCEPTABLE: Final[int] = 40
_TEMPLATES_DIR: Final[Path] = Path(__file__).parent / "templates"
_HTML_REPORT_TEMPLATE_NAME: Final[str] = "report.html.j2"


class FlextQualityDocumentationReporter:
    """Documentation quality reporting and analytics system."""

    logger = u.fetch_logger(__name__)

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
        audit: t.MappingKV[str, u.Quality.DocumentationReportValue] | None
        validation: t.MappingKV[str, u.Quality.DocumentationReportValue] | None
        optimization: t.MappingKV[str, u.Quality.DocumentationReportValue] | None
        summary: FlextQualityDocumentationReporter.SummaryMetrics
        trends: FlextQualityDocumentationReporter.TrendData | None
        recommendations: t.SequenceOf[FlextQualityDocumentationReporter.Recommendation]

    def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
        """Initialize the documentation reporter with reports directory."""
        self.reports_dir = Path(reports_dir)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.template_dir = Path(__file__).parent / "templates"
        self.audit_data: t.MappingKV[str, u.Quality.DocumentationReportValue] | None = (
            None
        )
        self.validation_data: (
            t.MappingKV[str, u.Quality.DocumentationReportValue] | None
        ) = None
        self.optimization_data: (
            t.MappingKV[str, u.Quality.DocumentationReportValue] | None
        ) = None
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.load_latest_reports()

    @staticmethod
    def write_report_and_latest(
        output_dir: Path,
        filename: str,
        latest_filename: str,
        report_content: str,
        results: t.JsonPayload,
    ) -> p.Result[str]:
        """Write the timestamped report plus the latest pointer for one lane.

        Returns:
            The resulting ``p.Result[str]`` carrying the written report path.

        """
        filepath = output_dir / filename
        report_write = u.Cli.atomic_write_text_file(filepath, report_content)
        if report_write.failure:
            return r[str].from_failure(report_write)
        latest_write = u.Cli.json_write(
            output_dir / latest_filename,
            results,
            options=m.Cli.JsonWriteOptions(indent=2),
        )
        if latest_write.failure:
            return r[str].from_failure(latest_write)
        return r[str].ok(str(filepath))

    def load_latest_reports(self) -> None:
        """Load the most recent audit, validation, and optimization reports."""
        self.audit_data = self._load_json_report("latest_audit.json")
        self.validation_data = self._load_json_report("latest_validation.json")
        self.optimization_data = self._load_json_report("latest_optimization.json")

    def _load_json_report(
        self,
        filename: str,
    ) -> t.MappingKV[str, u.Quality.DocumentationReportValue] | None:
        """Load a JSON report file.

        Returns:
            The resulting ``t.MappingKV[str, u.Quality.DocumentationReportValue] |
                None``.
        """
        filepath = self.reports_dir / filename
        read = u.Cli.files_read_text(filepath)
        loaded: t.MappingKV[str, u.Quality.DocumentationReportValue] | None = None
        if read.success:
            try:
                loaded = u.Quality.REPORT_VALUE_MAPPING_ADAPTER.validate_json(
                    read.value,
                )
            except c.EXC_OS_VALUE as exc:
                self.logger.warning("Failed to parse report %s: %s", filename, exc)
                loaded = None
        return loaded

    def generate_quality_report(
        self,
        report_format: str = "html",
        *,
        include_trends: bool = False,
    ) -> str:
        """Generate comprehensive quality report.

        Returns:
            The resulting ``str``.

        Raises:
            ValueError: If Unsupported format.
        """
        report_data = FlextQualityDocumentationReporter.ReportData(
            timestamp=u.now().isoformat(),
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
            adapter = u.type_adapter(FlextQualityDocumentationReporter.ReportData)
            report_text: str = adapter.dump_json(report_data, indent=2).decode()
            return report_text
        if report_format == "markdown":
            return self._generate_markdown_report(report_data)
        msg = f"Unsupported format: {report_format}"
        raise ValueError(msg)

    def _calculate_summary_metrics(
        self,
    ) -> FlextQualityDocumentationReporter.SummaryMetrics:
        """Calculate summary metrics from all available data.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.SummaryMetrics``.
        """
        overall_score, audit_issues = self._audit_summary_counts()
        links_checked, validation_issues = self._validation_summary_counts()
        optimizations_applied = self._optimization_summary_count()
        total_issues = audit_issues + validation_issues

        return FlextQualityDocumentationReporter.SummaryMetrics(
            overall_score=overall_score,
            total_issues=total_issues,
            files_analyzed=self._files_analyzed_count(),
            links_checked=links_checked,
            optimizations_applied=optimizations_applied,
            quality_trend=self._quality_trend(overall_score),
        )

    def _audit_summary_counts(self) -> tuple[int, int]:
        """Extract the audit quality score and issue count.

        Returns:
            The resulting ``tuple[int, int]``.
        """
        if not self.audit_data or not isinstance(self.audit_data, dict):
            return (0, 0)
        score = 0
        metrics = self.audit_data.get("metrics")
        if isinstance(metrics, dict):
            score_raw = metrics.get("quality_score", 0)
            if isinstance(score_raw, int):
                score = score_raw
        issues = self.audit_data.get("issues")
        issue_count = len(issues) if isinstance(issues, list) else 0
        return (score, issue_count)

    def _validation_summary_counts(self) -> tuple[int, int]:
        """Extract the link-check count and validation issue count.

        Returns:
            The resulting ``tuple[int, int]``.
        """
        if not self.validation_data or not isinstance(self.validation_data, dict):
            return (0, 0)
        links_checked = 0
        issue_count = 0
        link_validation = self.validation_data.get("link_validation")
        if isinstance(link_validation, dict):
            links_checked_raw = link_validation.get("links_checked", 0)
            if isinstance(links_checked_raw, int):
                links_checked = links_checked_raw
            errors = link_validation.get("errors")
            if isinstance(errors, list):
                issue_count += len(errors)
        content_validation = self.validation_data.get("content_validation")
        if isinstance(content_validation, dict):
            content_issues = content_validation.get("content_issues")
            if isinstance(content_issues, list):
                issue_count += len(content_issues)
        return (links_checked, issue_count)

    def _optimization_summary_count(self) -> int:
        """Extract the applied optimization change count.

        Returns:
            The resulting ``int``.
        """
        if not self.optimization_data or not isinstance(self.optimization_data, dict):
            return 0
        changes_made = self.optimization_data.get("changes_made", 0)
        return changes_made if isinstance(changes_made, int) else 0

    def _files_analyzed_count(self) -> int:
        """Extract the analyzed file count from audit data.

        Returns:
            The resulting ``int``.
        """
        if not self.audit_data or not isinstance(self.audit_data, dict):
            return 0
        files_analyzed_raw = self.audit_data.get("files_analyzed", 0)
        return files_analyzed_raw if isinstance(files_analyzed_raw, int) else 0

    @staticmethod
    def _quality_trend(overall_score: int) -> str:
        """Classify an overall quality score into a trend label.

        Returns:
            The resulting ``str``.
        """
        if overall_score >= _QUALITY_SCORE_EXCELLENT:
            return "excellent"
        if overall_score >= _QUALITY_SCORE_GOOD:
            return "good"
        if overall_score >= _QUALITY_SCORE_ACCEPTABLE:
            return "needs_improvement"
        return "critical"

    @staticmethod
    def _analyze_trends() -> FlextQualityDocumentationReporter.TrendData | None:
        """Analyze quality trends over time.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.TrendData | None``.
        """
        return None

    def _generate_recommendations(
        self,
    ) -> MutableSequence[FlextQualityDocumentationReporter.Recommendation]:
        """Generate actionable recommendations based on current data.

        Returns:
            The resulting
                ``MutableSequence[FlextQualityDocumentationReporter.Recommendation]``.
        """
        recommendations: MutableSequence[
            FlextQualityDocumentationReporter.Recommendation
        ] = []
        self._append_audit_recommendations(recommendations)
        if self._append_link_recommendations(recommendations):
            return recommendations
        self._append_optimization_recommendations(recommendations)
        if not recommendations:
            recommendations.append(
                FlextQualityDocumentationReporter.Recommendation(
                    priority="low",
                    category="maintenance_setup",
                    title="Establish Regular Maintenance Schedule",
                    description=(
                        "Set up automated quality checks and maintenance procedures"
                    ),
                    actions=[
                        "Schedule weekly audits",
                        "Configure automated reporting",
                        "Set up team notifications",
                    ],
                ),
            )
        return recommendations

    def _append_audit_recommendations(
        self,
        recommendations: MutableSequence[
            FlextQualityDocumentationReporter.Recommendation
        ],
    ) -> None:
        """Append audit-driven recommendations for critical and outdated issues."""
        if not self.audit_data or not isinstance(self.audit_data, dict):
            return
        audit_issues = self.audit_data.get("issues")
        if not isinstance(audit_issues, list):
            return
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
                    description=("Address critical documentation issues immediately"),
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
                    description=(
                        "Review and update documentation that hasn't been "
                        "modified recently"
                    ),
                    actions=[
                        "Identify documents needing updates",
                        "Review content accuracy",
                        "Update timestamps and version info",
                    ],
                ),
            )

    def _append_link_recommendations(
        self,
        recommendations: MutableSequence[
            FlextQualityDocumentationReporter.Recommendation
        ],
    ) -> bool:
        """Append a link-maintenance recommendation for collected broken links.

        Returns:
            The resulting ``bool``: ``True`` when recommendation collection
            must abort early (malformed link-validation errors payload).
        """
        if not self.validation_data or not isinstance(self.validation_data, dict):
            return False
        link_validation = self.validation_data.get("link_validation")
        if not isinstance(link_validation, dict):
            return False
        validation_errors_raw = link_validation.get("errors")
        if not isinstance(validation_errors_raw, list):
            return True
        broken_links = self._collect_broken_link_entries(validation_errors_raw)
        if not broken_links:
            return False
        recommendations.append(
            FlextQualityDocumentationReporter.Recommendation(
                priority="high",
                category="link_maintenance",
                title=f"Fix {len(broken_links)} Broken Links",
                description=("Repair or remove broken internal and external links"),
                actions=[
                    "Review broken link report",
                    "Update or remove invalid URLs",
                    "Test links after fixes",
                ],
            ),
        )
        return False

    def _collect_broken_link_entries(
        self,
        validation_errors_raw: list[t.JsonValue],
    ) -> MutableSequence[Mapping[str, t.Primitives]]:
        """Normalize link-validation error entries into broken-link mappings.

        Returns:
            The resulting ``MutableSequence[Mapping[str, t.Primitives]]``.
        """
        broken_links: MutableSequence[Mapping[str, t.Primitives]] = []
        for e_raw in validation_errors_raw:
            try:
                error_entry: t.JsonMapping = (
                    u.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(e_raw)
                )
            except c.EXC_TYPE_VALIDATION as exc:
                self.logger.warning(
                    "Skipping unparsable validation error entry %s: %s",
                    e_raw,
                    exc,
                )
                continue
            error_type = error_entry.get("type")
            if error_type in {
                "broken_external_link",
                "broken_internal_link",
            }:
                normalized: t.MappingKV[str, t.Primitives] = {
                    key: value
                    for key, value in error_entry.items()
                    if isinstance(value, c.PRIMITIVES_TYPES)
                }
                if normalized:
                    broken_links.append(normalized)
        return broken_links

    def _append_optimization_recommendations(
        self,
        recommendations: MutableSequence[
            FlextQualityDocumentationReporter.Recommendation
        ],
    ) -> None:
        """Append an automation-setup recommendation when optimizations are missing."""
        if not self.optimization_data or not isinstance(self.optimization_data, dict):
            return
        optimizations = self.optimization_data.get("optimizations")
        if not optimizations or (isinstance(optimizations, list) and not optimizations):
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

    def _generate_html_report(
        self,
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> str:
        """Generate HTML quality report from the fixed on-disk template.

        Returns:
            The resulting ``str``.
        """
        timestamp = datetime.fromisoformat(data.timestamp).strftime("%Y-%m-%d %H:%M:%S")
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
        environment = cli_u.Cli.template_environment(_TEMPLATES_DIR)
        template = environment.get_template(_HTML_REPORT_TEMPLATE_NAME)
        return template.render(**template_data)

    @staticmethod
    def _generate_markdown_report(
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> str:
        """Generate markdown quality report.

        Returns:
            The resulting ``str``.
        """
        md = [f"# {data.title}", "", f"**Generated:** {data.timestamp}", ""]
        summary = data.summary
        md.extend([
            "## Summary",
            "",
            (
                f"- **Overall Quality Score:** {summary.overall_score}% "
                f"({summary.quality_trend})"
            ),
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

    @staticmethod
    def _summarize_audit_data(
        audit_data: t.MappingKV[str, u.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.AuditSummary | None:
        """Summarize audit data for reporting.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.AuditSummary | None``.
        """
        if not audit_data or not isinstance(audit_data, dict):
            return None
        issues_raw_obj = audit_data.get("issues")
        issues_raw_val: list[u.Quality.DocumentationReportValue] = (
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

    @staticmethod
    def _summarize_validation_data(
        validation_data: t.MappingKV[str, u.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.ValidationSummary | None:
        """Summarize validation data for reporting.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.ValidationSummary |
                None``.
        """
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

    @staticmethod
    def _summarize_optimization_data(
        optimization_data: t.MappingKV[str, u.Quality.DocumentationReportValue] | None,
    ) -> FlextQualityDocumentationReporter.OptimizationSummary | None:
        """Summarize optimization data for reporting.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.OptimizationSummary |
                None``.
        """
        if not optimization_data or not isinstance(optimization_data, dict):
            return None
        files_processed_raw = optimization_data.get("files_processed", 0)
        changes_made_raw = optimization_data.get("changes_made", 0)
        backups_created_raw: t.JsonValue = optimization_data.get(
            "backups_created",
            [],
        )
        optimizations_raw: t.JsonValue = optimization_data.get(
            "optimizations",
            [],
        )
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

    @staticmethod
    def _generate_charts(
        data: FlextQualityDocumentationReporter.ReportData,
    ) -> t.StrMapping | None:
        """Generate charts for the report (placeholder for future implementation).

        Returns:
            The resulting ``t.StrMapping | None``.
        """
        _ = data
        return None

    def generate_trend_report(self, days: int = 30) -> str:
        """Generate trend analysis report over specified time period.

        Returns:
            The resulting ``str``.
        """
        report_files = list(self.reports_dir.glob("*.json"))
        recent_reports: MutableSequence[
            t.MappingKV[str, u.Quality.DocumentationReportValue | datetime]
        ] = []
        cutoff_date = u.now() - timedelta(days=days)
        for report_file in report_files:
            if "latest_" in report_file.name:
                continue
            try:
                report_data_dict = self._load_recent_report(report_file, cutoff_date)
            except (ValueError, KeyError) as exc:
                self.logger.warning(
                    "Skipping unreadable trend report %s: %s",
                    report_file,
                    exc,
                )
                continue
            if report_data_dict is not None:
                recent_reports.append(report_data_dict)
        trend_data = self._analyze_trend_data(recent_reports)
        if isinstance(trend_data, FlextQualityDocumentationReporter.TrendData):
            return trend_data.model_dump_json(indent=2)
        return "; ".join(f"{key}={value}" for key, value in trend_data.items())

    @staticmethod
    def _load_recent_report(
        report_file: Path,
        cutoff_date: datetime,
    ) -> t.MappingKV[str, u.Quality.DocumentationReportValue | datetime] | None:
        """Load one historical report when it falls inside the trend window.

        Returns:
            The resulting ``t.MappingKV[str, u.Quality.DocumentationReportValue |
                datetime] | None``.

        Raises:
            ValueError: If unreadable report.
        """
        date_str = report_file.name.split("_")[1]
        report_date = datetime.strptime(date_str[:8], "%Y%m%d").replace(
            tzinfo=u.configured_timezone(),
        )
        if report_date < cutoff_date:
            return None
        read = u.Cli.files_read_text(report_file)
        if read.failure:
            msg = f"unreadable report {report_file}: {read.error}"
            raise ValueError(msg)
        report_data_raw: t.MappingKV[str, u.Quality.DocumentationReportValue] = (
            u.Quality.REPORT_VALUE_MAPPING_ADAPTER.validate_json(read.value)
        )
        report_data_dict: t.MappingKV[
            str,
            u.Quality.DocumentationReportValue | datetime,
        ] = {**report_data_raw, "date": report_date}
        return report_data_dict

    @staticmethod
    def _analyze_trend_data(
        reports: t.SequenceOf[
            Mapping[str, u.Quality.DocumentationReportValue | datetime]
        ],
    ) -> FlextQualityDocumentationReporter.TrendData | t.StrMapping:
        """Analyze trend data from historical reports.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.TrendData |
                t.StrMapping``.
        """
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
            date_val = FlextQualityDocumentationReporter._report_date(report)
            audit_entry = FlextQualityDocumentationReporter._audit_trend_entry(
                report,
                date_val,
            )
            if audit_entry is not None:
                audit_trends.append(audit_entry)
            validation_entry = (
                FlextQualityDocumentationReporter._validation_trend_entry(
                    report,
                    date_val,
                )
            )
            if validation_entry is not None:
                validation_trends.append(validation_entry)
            optimization_entry = (
                FlextQualityDocumentationReporter._optimization_trend_entry(
                    report,
                    date_val,
                )
            )
            if optimization_entry is not None:
                optimization_trends.append(optimization_entry)

        def _trend_entry_date(
            entry: FlextQualityDocumentationReporter.TrendEntry,
        ) -> datetime:
            """Sort key for trend entries (typed, not a lambda, for pyrefly).

            Returns:
                The resulting ``datetime``.
            """
            return entry.date

        return FlextQualityDocumentationReporter.TrendData(
            audit_trends=sorted(audit_trends, key=_trend_entry_date),
            validation_trends=sorted(validation_trends, key=_trend_entry_date),
            optimization_trends=sorted(optimization_trends, key=_trend_entry_date),
        )

    @staticmethod
    def _report_date(
        report: Mapping[str, u.Quality.DocumentationReportValue | datetime],
    ) -> datetime:
        """Extract the report date, falling back to the current time.

        Returns:
            The resulting ``datetime``.
        """
        date_val_raw = report.get("date")
        if date_val_raw is None:
            date_val_raw = report.get("timestamp", u.now())
        return date_val_raw if isinstance(date_val_raw, datetime) else u.now()

    @staticmethod
    def _audit_trend_entry(
        report: Mapping[str, u.Quality.DocumentationReportValue | datetime],
        date_val: datetime,
    ) -> FlextQualityDocumentationReporter.TrendEntry | None:
        """Build the audit trend entry for one historical report.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.TrendEntry | None``.
        """
        if "metrics" not in report:
            return None
        metrics = report.get("metrics")
        if not isinstance(metrics, dict):
            return None
        quality_score = metrics.get("quality_score")
        issues = report.get("issues")
        if not (isinstance(quality_score, int) and isinstance(issues, list)):
            return None
        return FlextQualityDocumentationReporter.TrendEntry(
            date=date_val,
            quality_score=quality_score,
            total_issues=len(issues),
        )

    @staticmethod
    def _validation_trend_entry(
        report: Mapping[str, u.Quality.DocumentationReportValue | datetime],
        date_val: datetime,
    ) -> FlextQualityDocumentationReporter.TrendEntry | None:
        """Build the link-validation trend entry for one historical report.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.TrendEntry | None``.
        """
        if "link_validation" not in report:
            return None
        link_validation = report.get("link_validation")
        if not isinstance(link_validation, dict):
            return None
        links_checked = link_validation.get("links_checked", 0)
        broken_links = link_validation.get("broken_links", 0)
        if not (isinstance(links_checked, int) and isinstance(broken_links, int)):
            return None
        return FlextQualityDocumentationReporter.TrendEntry(
            date=date_val,
            links_checked=links_checked,
            broken_links=broken_links,
        )

    @staticmethod
    def _optimization_trend_entry(
        report: Mapping[str, u.Quality.DocumentationReportValue | datetime],
        date_val: datetime,
    ) -> FlextQualityDocumentationReporter.TrendEntry | None:
        """Build the optimization trend entry for one historical report.

        Returns:
            The resulting ``FlextQualityDocumentationReporter.TrendEntry | None``.
        """
        if "changes_made" not in report:
            return None
        changes_made = report.get("changes_made")
        files_processed = report.get("files_processed", 0)
        if not (isinstance(changes_made, int) and isinstance(files_processed, int)):
            return None
        return FlextQualityDocumentationReporter.TrendEntry(
            date=date_val,
            changes_made=changes_made,
            files_processed=files_processed,
        )

    def save_report(
        self,
        content: str,
        filename: str,
        report_format: str = "html",
    ) -> p.Result[Path]:
        """Save report to file.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        filepath = self.reports_dir / f"{filename}.{report_format}"
        write = u.Cli.atomic_write_text_file(filepath, content)
        if write.failure:
            return r[Path].from_failure(write)
        return r[Path].ok(filepath)

    class Run(s[bool]):
        """CLI command for FLEXT Quality documentation reporting."""

        output_format: Annotated[
            str,
            u.Field(
                alias="format",
                description="Report output format",
                validate_default=True,
            ),
        ] = "html"
        output: str = u.Field(
            "docs/maintenance/reports/",
            description="Report output directory",
            validate_default=True,
        )
        filename: str | None = u.Field(
            None,
            description="Optional report filename",
            validate_default=True,
        )
        monthly_trends: bool = u.Field(
            default=False,
            description="Generate monthly trend report",
            validate_default=True,
        )
        weekly_trends: bool = u.Field(
            default=False,
            description="Generate weekly trend report",
            validate_default=True,
        )
        include_trends: bool = u.Field(
            default=False,
            description="Include trend data",
            validate_default=True,
        )
        notify: bool = u.Field(
            default=False,
            description="Send report notification",
            validate_default=True,
        )
        webhook_url: str | None = u.Field(
            None,
            description="Notification webhook URL",
            validate_default=True,
        )
        serve: bool = u.Field(
            default=False,
            description="Serve the report dashboard",
            validate_default=True,
        )

        @override
        def execute(self) -> p.Result[bool]:
            """Generate the requested report.

            Returns:
                The resulting ``p.Result[bool]``.
            """
            reporter = FlextQualityDocumentationReporter(self.output)
            if self.monthly_trends:
                trend_report = reporter.generate_trend_report(days=30)
                filename = (
                    self.filename or f"monthly_trends_{u.now().strftime('%Y%m%d')}"
                )
                save_result = reporter.save_report(trend_report, filename, "md")
                if save_result.failure:
                    return r[bool].from_failure(save_result)
            elif self.weekly_trends:
                trend_report = reporter.generate_trend_report(days=7)
                filename = (
                    self.filename or f"weekly_trends_{u.now().strftime('%Y%m%d')}"
                )
                save_result = reporter.save_report(trend_report, filename, "md")
                if save_result.failure:
                    return r[bool].from_failure(save_result)
            else:
                report_content = reporter.generate_quality_report(
                    self.output_format,
                    include_trends=self.include_trends,
                )
                filename = (
                    self.filename
                    or f"quality_report_{u.now().strftime('%Y%m%d_%H%M%S')}"
                )
                save_result = reporter.save_report(
                    report_content,
                    filename,
                    self.output_format,
                )
                if save_result.failure:
                    return r[bool].from_failure(save_result)
            return r[bool].ok(value=True)

    @staticmethod
    def _run_handler(params: FlextQualityDocumentationReporter.Run) -> p.Result[bool]:
        """Execute the reporter ``Run`` route (typed, not a lambda, for pyrefly).

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return params.execute()

    @staticmethod
    def main(args: t.StrSequence | None = None) -> int:
        """Run the reporting system via the canonical cli facade.

        Returns:
            The resulting ``int``.
        """
        exit_code: int = u.Quality.execute_result_command(
            args=args,
            app_name="flext-quality-docs-report",
            app_help="FLEXT Quality Documentation Reporting",
            route=m.Cli.ResultCommandRoute(
                name="run",
                help_text="Generate a documentation quality report",
                model_cls=FlextQualityDocumentationReporter.Run,
                handler=FlextQualityDocumentationReporter._run_handler,
            ),
        )
        return exit_code


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).


if __name__ == "__main__":
    cli.exit(FlextQualityDocumentationReporter.main())

__all__: list[str] = ["FlextQualityDocumentationReporter"]
