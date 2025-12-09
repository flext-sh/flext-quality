#!/usr/bin/env python3
"""FLEXT Quality Documentation Reporting System.

Generates comprehensive quality reports, analytics, and dashboards
from audit, validation, and optimization results.

Usage:
    python report.py --format html
    python report.py --monthly-trends --notify
    python report.py --dashboard --serve
"""

import argparse
import json
import operator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from jinja2 import Template


class DocumentationReporter:
    """Documentation quality reporting and analytics system."""

    def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
        """Initialize the documentation reporter with reports directory."""
        self.reports_dir = Path(reports_dir)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.template_dir = Path(__file__).parent / "templates"

        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Load latest data
        self.load_latest_reports()

    def load_latest_reports(self) -> None:
        """Load the most recent audit, validation, and optimization reports."""
        self.audit_data = self._load_json_report("latest_audit.json")
        self.validation_data = self._load_json_report("latest_validation.json")
        self.optimization_data = self._load_json_report("latest_optimization.json")

    def _load_json_report(self, filename: str) -> dict[str, Any] | None:
        """Load a JSON report file."""
        filepath = self.reports_dir / filename
        if filepath.exists():
            try:
                with Path(filepath).open(encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return None

    def generate_quality_report(
        self,
        report_format: str = "html",
        **kwargs: dict,
    ) -> str:
        """Generate comprehensive quality report."""
        # Collect all available data
        report_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "title": "FLEXT Quality Documentation Report",
            "audit": self.audit_data,
            "validation": self.validation_data,
            "optimization": self.optimization_data,
            "summary": self._calculate_summary_metrics(),
            "trends": self._analyze_trends() if kwargs.get("include_trends") else None,
            "recommendations": self._generate_recommendations(),
        }

        if report_format == "html":
            return self._generate_html_report(report_data)
        if report_format == "json":
            return json.dumps(report_data, indent=2, default=str)
        if report_format == "markdown":
            return self._generate_markdown_report(report_data)
        msg = f"Unsupported format: {report_format}"
        raise ValueError(msg)

    def _calculate_summary_metrics(self) -> dict[str, Any]:
        """Calculate summary metrics from all available data."""
        summary = {
            "overall_score": 0,
            "total_issues": 0,
            "files_analyzed": 0,
            "links_checked": 0,
            "optimizations_applied": 0,
            "quality_trend": "unknown",
        }

        # Aggregate from audit data
        if self.audit_data:
            summary["overall_score"] = self.audit_data.get("metrics", {}).get(
                "quality_score",
                0,
            )
            summary["total_issues"] += len(self.audit_data.get("issues", []))
            summary["files_analyzed"] = max(
                summary["files_analyzed"],
                self.audit_data.get("files_analyzed", 0),
            )

        # Aggregate from validation data
        if self.validation_data:
            summary["links_checked"] = self.validation_data.get(
                "link_validation",
                {},
            ).get("links_checked", 0)
            summary["total_issues"] += len(
                self.validation_data.get("link_validation", {}).get("errors", []),
            )
            summary["total_issues"] += len(
                self.validation_data.get("content_validation", {}).get(
                    "content_issues",
                    [],
                ),
            )

        # Aggregate from optimization data
        if self.optimization_data:
            summary["optimizations_applied"] = self.optimization_data.get(
                "changes_made",
                0,
            )

        # Determine quality trend (simplified - would need historical data)
        if summary["overall_score"] >= 80:
            summary["quality_trend"] = "excellent"
        elif summary["overall_score"] >= 60:
            summary["quality_trend"] = "good"
        elif summary["overall_score"] >= 40:
            summary["quality_trend"] = "needs_improvement"
        else:
            summary["quality_trend"] = "critical"

        return summary

    def _analyze_trends(self) -> dict[str, Any] | None:
        """Analyze quality trends over time."""
        # This would require historical report data
        # For now, return None as we don't have historical data structure
        return None

    def _generate_recommendations(self) -> list[dict[str, Any]]:
        """Generate actionable recommendations based on current data."""
        recommendations = []

        if self.audit_data:
            audit_issues = self.audit_data.get("issues", [])

            # Check for critical issues
            critical_issues = [
                i for i in audit_issues if i.get("severity") == "critical"
            ]
            if critical_issues:
                recommendations.append({
                    "priority": "critical",
                    "category": "immediate_fixes",
                    "title": f"Fix {len(critical_issues)} Critical Issues",
                    "description": "Address critical documentation issues immediately",
                    "actions": [
                        "Review critical issues in audit report",
                        "Prioritize fixes",
                        "Re-run audit after fixes",
                    ],
                })

            # Check for outdated content
            outdated = [i for i in audit_issues if i.get("type") == "outdated_content"]
            if outdated:
                recommendations.append({
                    "priority": "high",
                    "category": "content_freshness",
                    "title": f"Update {len(outdated)} Outdated Documents",
                    "description": "Review and update documentation that hasn't been modified recently",
                    "actions": [
                        "Identify documents needing updates",
                        "Review content accuracy",
                        "Update timestamps and version info",
                    ],
                })

        if self.validation_data:
            validation_errors = self.validation_data.get("link_validation", {}).get(
                "errors",
                [],
            )
            if validation_errors:
                broken_links = [
                    e
                    for e in validation_errors
                    if e.get("type") in {"broken_external_link", "broken_internal_link"}
                ]
                if broken_links:
                    recommendations.append({
                        "priority": "high",
                        "category": "link_maintenance",
                        "title": f"Fix {len(broken_links)} Broken Links",
                        "description": "Repair or remove broken internal and external links",
                        "actions": [
                            "Review broken link report",
                            "Update or remove invalid URLs",
                            "Test links after fixes",
                        ],
                    })

        if self.optimization_data:
            optimizations = self.optimization_data.get("optimizations", [])
            if not optimizations:
                recommendations.append({
                    "priority": "medium",
                    "category": "automation_setup",
                    "title": "Set Up Automated Optimization",
                    "description": "Configure automated formatting and style fixes",
                    "actions": [
                        "Set up pre-commit hooks",
                        "Configure CI/CD optimization",
                        "Schedule regular optimization runs",
                    ],
                })

        # Default recommendations if no specific issues found
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "category": "maintenance_setup",
                "title": "Establish Regular Maintenance Schedule",
                "description": "Set up automated quality checks and maintenance procedures",
                "actions": [
                    "Schedule weekly audits",
                    "Configure automated reporting",
                    "Set up team notifications",
                ],
            })

        return recommendations

    def _generate_html_report(self, data: dict[str, Any]) -> str:
        """Generate HTML quality report."""
        template = self._get_html_template()

        # Prepare data for template
        template_data = {
            "title": data["title"],
            "timestamp": datetime.fromisoformat(data["timestamp"]).strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
            "summary": data["summary"],
            "audit_summary": self._summarize_audit_data(data["audit"]),
            "validation_summary": self._summarize_validation_data(data["validation"]),
            "optimization_summary": self._summarize_optimization_data(
                data["optimization"],
            ),
            "recommendations": data["recommendations"],
            "charts": self._generate_charts(data) if data.get("trends") else None,
        }

        return template.render(**template_data)

    def _get_html_template(self) -> Template:
        """Get HTML report template."""
        template_content = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 2px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .metric-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007acc; }
        .metric-value { font-size: 2.5em; font-weight: bold; color: #007acc; margin: 10px 0; }
        .metric-label { color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }
        .section { margin: 40px 0; }
        .section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .recommendations { display: grid; gap: 15px; }
        .recommendation { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; }
        .priority-critical { border-left: 4px solid #dc3545; background: #f8d7da; }
        .priority-high { border-left: 4px solid #fd7e14; background: #fff3cd; }
        .priority-medium { border-left: 4px solid #ffc107; background: #fff3cd; }
        .priority-low { border-left: 4px solid #28a745; background: #d4edda; }
        .issue-list { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto; }
        .issue-item { background: white; margin: 5px 0; padding: 8px; border-radius: 3px; border-left: 3px solid #dc3545; }
        .timestamp { color: #666; font-size: 0.9em; text-align: center; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <p>Generated: {{ timestamp }}</p>
        </div>

        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-label">Overall Quality Score</div>
                <div class="metric-value">{{ summary.overall_score }}%</div>
                <div>Trend: {{ summary.quality_trend|title }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Files Analyzed</div>
                <div class="metric-value">{{ summary.files_analyzed }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Issues</div>
                <div class="metric-value">{{ summary.total_issues }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Links Checked</div>
                <div class="metric-value">{{ summary.links_checked }}</div>
            </div>
        </div>

        {% if audit_summary %}
        <div class="section">
            <h2>Content Audit Results</h2>
            <p>Quality Score: {{ audit_summary.quality_score }}%</p>
            <p>Issues Found: {{ audit_summary.total_issues }}</p>
            <p>Critical: {{ audit_summary.critical_issues }}, High: {{ audit_summary.high_issues }}</p>
        </div>
        {% endif %}

        {% if validation_summary %}
        <div class="section">
            <h2>Link Validation Results</h2>
            <p>Links Checked: {{ validation_summary.links_checked }}</p>
            <p>Valid: {{ validation_summary.valid_links }}, Broken: {{ validation_summary.broken_links }}</p>
        </div>
        {% endif %}

        {% if optimization_summary %}
        <div class="section">
            <h2>Optimization Results</h2>
            <p>Files Processed: {{ optimization_summary.files_processed }}</p>
            <p>Changes Made: {{ optimization_summary.changes_made }}</p>
            <p>Backups Created: {{ optimization_summary.backups_created }}</p>
        </div>
        {% endif %}

        <div class="section">
            <h2>Recommendations</h2>
            <div class="recommendations">
                {% for rec in recommendations %}
                <div class="recommendation priority-{{ rec.priority }}">
                    <h3>{{ rec.title }}</h3>
                    <p>{{ rec.description }}</p>
                    <ul>
                        {% for action in rec.actions %}
                        <li>{{ action }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="timestamp">
            Report generated by FLEXT Quality Documentation Maintenance System
        </div>
    </div>
</body>
</html>
        """
        return Template(template_content)

    def _generate_markdown_report(self, data: dict[str, Any]) -> str:
        """Generate markdown quality report."""
        md = [f"# {data['title']}", "", f"**Generated:** {data['timestamp']}", ""]

        # Summary
        summary = data["summary"]
        md.extend([
            "## Summary",
            "",
            f"- **Overall Quality Score:** {summary['overall_score']}% ({summary['quality_trend']})",
            f"- **Files Analyzed:** {summary['files_analyzed']}",
            f"- **Total Issues:** {summary['total_issues']}",
            f"- **Links Checked:** {summary['links_checked']}",
            "",
        ])

        # Recommendations
        if data["recommendations"]:
            md.extend(["## Recommendations", ""])
            for rec in data["recommendations"]:
                md.extend([
                    f"### {rec['title']} ({rec['priority'].upper()})",
                    "",
                    rec["description"],
                    "",
                    "**Actions:**",
                ])
                md.extend(f"- {action}" for action in rec["actions"])
                md.append("")

        return "\n".join(md)

    def _summarize_audit_data(
        self,
        audit_data: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Summarize audit data for reporting."""
        if not audit_data:
            return None

        issues = audit_data.get("issues", [])
        return {
            "quality_score": audit_data.get("metrics", {}).get("quality_score", 0),
            "total_issues": len(issues),
            "critical_issues": len([
                i for i in issues if i.get("severity") == "critical"
            ]),
            "high_issues": len([i for i in issues if i.get("severity") == "high"]),
            "medium_issues": len([i for i in issues if i.get("severity") == "medium"]),
            "low_issues": len([i for i in issues if i.get("severity") == "low"]),
        }

    def _summarize_validation_data(
        self,
        validation_data: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Summarize validation data for reporting."""
        if not validation_data:
            return None

        link_data = validation_data.get("link_validation", {})
        return {
            "links_checked": link_data.get("links_checked", 0),
            "valid_links": link_data.get("valid_links", 0),
            "broken_links": link_data.get("broken_links", 0),
            "warnings": link_data.get("warnings", 0),
        }

    def _summarize_optimization_data(
        self,
        optimization_data: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Summarize optimization data for reporting."""
        if not optimization_data:
            return None

        return {
            "files_processed": optimization_data.get("files_processed", 0),
            "changes_made": optimization_data.get("changes_made", 0),
            "backups_created": len(optimization_data.get("backups_created", [])),
            "optimizations_applied": len(optimization_data.get("optimizations", [])),
        }

    def _generate_charts(self, data: dict[str, Any]) -> dict[str, str] | None:
        """Generate charts for the report (placeholder for future implementation)."""
        # Reserved for future matplotlib chart generation
        _ = data  # Reserved for future use

        # This would generate matplotlib charts and return base64 encoded images
        # For now, return None
        return None

    def generate_trend_report(self, days: int = 30) -> str:
        """Generate trend analysis report over specified time period."""
        # Find all historical reports
        report_files = list(self.reports_dir.glob("*.json"))
        recent_reports = []

        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        for report_file in report_files:
            if "latest_" in report_file.name:
                continue

            try:
                # Extract date from filename
                date_str = report_file.name.split("_")[
                    1
                ]  # e.g., audit_report_20241201_120000.json
                report_date = datetime.strptime(date_str[:8], "%Y%m%d").replace(
                    tzinfo=UTC,
                )

                if report_date >= cutoff_date:
                    with Path(report_file).open(encoding="utf-8") as f:
                        report_data = json.load(f)
                        report_data["date"] = report_date
                        recent_reports.append(report_data)
            except (ValueError, json.JSONDecodeError, KeyError):
                continue

        # Analyze trends
        trend_data = self._analyze_trend_data(recent_reports)

        # Generate report
        return self._generate_trend_report(trend_data, days)

    def _analyze_trend_data(self, reports: list[dict]) -> dict[str, Any]:
        """Analyze trend data from historical reports."""
        if not reports:
            return {"error": "No historical data available"}

        # Group by report type and date
        audit_trends = []
        validation_trends = []
        optimization_trends = []

        for report in reports:
            date = report.get("date", report.get("timestamp", datetime.now(UTC)))

            if "metrics" in report and "quality_score" in report["metrics"]:
                audit_trends.append({
                    "date": date,
                    "quality_score": report["metrics"]["quality_score"],
                    "total_issues": len(report.get("issues", [])),
                })
            elif "link_validation" in report:
                validation_trends.append({
                    "date": date,
                    "links_checked": report["link_validation"].get("links_checked", 0),
                    "broken_links": report["link_validation"].get("broken_links", 0),
                })
            elif "changes_made" in report:
                optimization_trends.append({
                    "date": date,
                    "changes_made": report["changes_made"],
                    "files_processed": report["files_processed"],
                })

        return {
            "audit_trends": sorted(audit_trends, key=operator.itemgetter("date")),
            "validation_trends": sorted(
                validation_trends,
                key=operator.itemgetter("date"),
            ),
            "optimization_trends": sorted(
                optimization_trends,
                key=operator.itemgetter("date"),
            ),
        }

    def _generate_trend_report(self, trend_data: dict[str, Any], days: int) -> str:
        """Generate trend analysis report."""
        md = [
            f"# Documentation Quality Trends - Last {days} Days",
            "",
            f"Generated: {datetime.now(UTC).isoformat()}",
            "",
        ]

        if "error" in trend_data:
            md.extend([f"**Error:** {trend_data['error']}", ""])
            return "\n".join(md)

        # Quality Score Trends
        if trend_data["audit_trends"]:
            md.extend(["## Quality Score Trends", ""])
            audit_trends = trend_data["audit_trends"]
            md.extend((
                "| Date | Quality Score | Issues |",
                "|------|---------------|--------|",
            ))

            for trend in audit_trends[-10:]:  # Last 10 entries
                date_str = (
                    trend["date"].strftime("%Y-%m-%d")
                    if hasattr(trend["date"], "strftime")
                    else str(trend["date"])[:10]
                )
                md.append(
                    f"| {date_str} | {trend['quality_score']}% | {trend['total_issues']} |",
                )

            md.append("")

        # Link Validation Trends
        if trend_data["validation_trends"]:
            md.extend(["## Link Validation Trends", ""])
            validation_trends = trend_data["validation_trends"]
            md.extend((
                "| Date | Links Checked | Broken Links |",
                "|------|---------------|--------------|",
            ))

            for trend in validation_trends[-10:]:
                date_str = (
                    trend["date"].strftime("%Y-%m-%d")
                    if hasattr(trend["date"], "strftime")
                    else str(trend["date"])[:10]
                )
                md.append(
                    f"| {date_str} | {trend['links_checked']} | {trend['broken_links']} |",
                )

            md.append("")

        # Optimization Trends
        if trend_data["optimization_trends"]:
            md.extend(["## Optimization Trends", ""])
            optimization_trends = trend_data["optimization_trends"]
            md.extend((
                "| Date | Files Processed | Changes Made |",
                "|------|-----------------|--------------|",
            ))

            for trend in optimization_trends[-10:]:
                date_str = (
                    trend["date"].strftime("%Y-%m-%d")
                    if hasattr(trend["date"], "strftime")
                    else str(trend["date"])[:10]
                )
                md.append(
                    f"| {date_str} | {trend['files_processed']} | {trend['changes_made']} |",
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
        filepath.write_text(content, encoding="utf-8")
        return filepath


def main() -> None:
    """Main entry point for reporting system."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Reporting",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["html", "json", "markdown"],
        default="html",
        help="Report format",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/maintenance/reports/",
        help="Output directory for reports",
    )
    parser.add_argument("--filename", type=str, help="Custom filename for the report")
    parser.add_argument(
        "--monthly-trends",
        action="store_true",
        help="Generate monthly trend analysis",
    )
    parser.add_argument(
        "--weekly-trends",
        action="store_true",
        help="Generate weekly trend analysis",
    )
    parser.add_argument(
        "--include-trends",
        action="store_true",
        help="Include trend analysis in quality report",
    )
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Send notifications (requires webhook URL)",
    )
    parser.add_argument("--webhook-url", type=str, help="Webhook URL for notifications")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve dashboard (not implemented yet)",
    )

    args = parser.parse_args()

    # Initialize reporter
    reporter = DocumentationReporter(args.output)

    if args.monthly_trends:
        # Generate monthly trend report
        trend_report = reporter.generate_trend_report(days=30)
        filename = (
            args.filename or f"monthly_trends_{datetime.now(UTC).strftime('%Y%m%d')}"
        )
        reporter.save_report(trend_report, filename, "md")

    elif args.weekly_trends:
        # Generate weekly trend report
        trend_report = reporter.generate_trend_report(days=7)
        filename = (
            args.filename or f"weekly_trends_{datetime.now(UTC).strftime('%Y%m%d')}"
        )
        reporter.save_report(trend_report, filename, "md")

    else:
        # Generate comprehensive quality report
        kwargs = {"include_trends": args.include_trends}
        report_content = reporter.generate_quality_report(args.format, **kwargs)

        filename = (
            args.filename
            or f"quality_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
        )
        reporter.save_report(report_content, filename, args.format)

        # Send notifications if requested
        if args.notify and args.webhook_url:
            # This would implement webhook notifications
            # For now, just print
            pass

    if args.serve:
        pass


if __name__ == "__main__":
    main()
