"""FLEXT Quality Documentation Health Dashboard.

Real-time monitoring dashboard for documentation quality metrics.
Provides web interface to view audit results, trends, and quality scores.
"""

from __future__ import annotations

import operator
import sys
from collections.abc import (
    Mapping,
    MutableSequence,
)
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated, override

from flask import Flask, Response, render_template_string, request

from flext_cli import cli, m as cli_m, u as cli_u
from flext_core import r, s
from flext_quality import c, m, p, t, u


class FlextQualityDocumentationDashboard:
    """Documentation health monitoring dashboard."""

    def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
        """Initialize documentation dashboard with reports directory."""
        self.reports_dir = Path(reports_dir)
        self.app = Flask(__name__)
        self._logger_instance: p.Logger = u.fetch_logger(__name__)
        self.setup_routes()

    @property
    def logger(self) -> p.Logger:
        """Return the module logger."""
        return self._logger_instance

    def setup_routes(self) -> None:
        """Setup Flask routes for the dashboard."""

        @self.app.route("/")
        def index() -> str:
            """Main dashboard page."""
            return render_template_string(self.get_dashboard_html())

        _ = index

        @self.app.route("/api/metrics")
        def api_metrics() -> Response:
            """API endpoint for current metrics."""
            return Response(
                t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.dump_json(
                    self.get_current_metrics()
                ).decode(),
                mimetype="application/json",
            )

        _ = api_metrics

        @self.app.route("/api/trends")
        def api_trends() -> Response:
            """API endpoint for quality trends."""
            days = int(request.args.get("days", 30))
            return Response(
                t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.dump_json(
                    self.get_quality_trends(days)
                ).decode(),
                mimetype="application/json",
            )

        _ = api_trends

        @self.app.route("/api/reports")
        def api_reports() -> Response:
            """API endpoint for recent reports."""
            limit = int(request.args.get("limit", 10))
            return Response(
                t.Quality.RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER.dump_json(
                    self.get_recent_reports(limit)
                ).decode(),
                mimetype="application/json",
            )

        _ = api_reports

    def get_current_metrics(
        self,
    ) -> t.JsonMapping:
        """Get current quality metrics from latest audit."""
        latest_audit = self.reports_dir / "latest_audit.json"

        if not latest_audit.exists():
            return {
                "quality_score": 0,
                "files_analyzed": 0,
                "total_issues": 0,
                "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "timestamp": datetime.now(UTC).isoformat(),
                "status": "No audit data available",
            }

        try:
            data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                Path(latest_audit).read_bytes()
            )
            metrics_raw = data.get("metrics")
            metrics: t.JsonMapping = (
                metrics_raw if isinstance(metrics_raw, Mapping) else {}
            )
            severity_raw = metrics.get("severity_breakdown")
            severity: t.JsonDict = {}
            if isinstance(severity_raw, Mapping):
                for key, value in severity_raw.items():
                    severity[key] = value if isinstance(value, int) else 0
            files_analyzed_raw = data.get("files_analyzed")
            timestamp_raw = data.get("timestamp")
            qs_raw = metrics.get("quality_score", 0)
            quality_score_int: int = qs_raw if isinstance(qs_raw, int) else 0
            ti_raw = metrics.get("total_issues", 0)
            total_issues_int: int = ti_raw if isinstance(ti_raw, int) else 0
            return {
                "quality_score": quality_score_int,
                "files_analyzed": (
                    files_analyzed_raw if isinstance(files_analyzed_raw, int) else 0
                ),
                "total_issues": total_issues_int,
                "severity_breakdown": severity,
                "timestamp": (
                    timestamp_raw
                    if isinstance(timestamp_raw, str)
                    else datetime.now(UTC).isoformat()
                ),
                "status": "Current",
            }
        except c.EXC_FS_KEY_VALUE as e:
            return {
                "quality_score": 0,
                "files_analyzed": 0,
                "total_issues": 0,
                "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "timestamp": datetime.now(UTC).isoformat(),
                "status": f"Error: {e!s}",
            }

    def get_quality_trends(
        self,
        days: int = 30,
    ) -> t.JsonMapping:
        """Get quality trends over the specified number of days."""
        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        trend_data: t.MutableSequenceOf[t.JsonDict] = []
        reports_dir = self.reports_dir

        # Find all audit reports
        for report_file in reports_dir.glob("audit_report_*.json"):
            try:
                # Extract date from filename
                date_str = report_file.stem.replace("audit_report_", "").replace(
                    "_",
                    " ",
                )
                report_date = datetime.strptime(date_str, "%Y%m%d %H%M%S").replace(
                    tzinfo=UTC,
                )

                if report_date >= cutoff_date:
                    data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                        Path(report_file).read_bytes()
                    )
                    metrics_v = data.get("metrics")
                    metrics_m: t.JsonMapping = (
                        t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(
                            metrics_v
                        )
                        if isinstance(metrics_v, Mapping)
                        else {}
                    )
                    audit_metrics = m.Quality.AuditMetrics.model_validate(metrics_m)
                    trend_entry: t.JsonDict = {
                        "date": report_date.isoformat(),
                        "quality_score": audit_metrics.quality_score,
                        "total_issues": audit_metrics.total_issues,
                        "critical_issues": audit_metrics.severity_breakdown.get(
                            "critical",
                            0,
                        ),
                        "high_issues": audit_metrics.severity_breakdown.get(
                            "high",
                            0,
                        ),
                    }
                    trend_data.append(trend_entry)
            except c.EXC_FS_KEY_VALUE as e:
                self._logger_instance.warning(
                    "Failed to process trend data: %s",
                    str(e),
                )
                continue

        # Sort by date
        trend_data = sorted(trend_data, key=operator.itemgetter("date"))
        trend_values: list[t.JsonValue] = [
            t.json_value_adapter().validate_python(entry) for entry in trend_data
        ]

        return {
            "period_days": days,
            "data_points": len(trend_data),
            "trends": trend_values,
        }

    def get_recent_reports(self, limit: int = 10) -> t.SequenceOf[t.JsonMapping]:
        """Get list of recent audit reports."""
        reports: MutableSequence[t.JsonMapping] = []

        for report_file in self.reports_dir.glob("audit_report_*.json"):
            try:
                date_str = report_file.stem.replace("audit_report_", "").replace(
                    "_",
                    " ",
                )
                report_date = datetime.strptime(date_str, "%Y%m%d %H%M%S").replace(
                    tzinfo=UTC,
                )

                data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                    Path(report_file).read_bytes()
                )

                metrics_rv = data.get("metrics")
                metrics_rm: t.JsonMapping = (
                    metrics_rv if isinstance(metrics_rv, Mapping) else {}
                )
                qs_rv = metrics_rm.get("quality_score", 0)
                r_quality_score: int = qs_rv if isinstance(qs_rv, int) else 0
                ti_rv = metrics_rm.get("total_issues", 0)
                r_total_issues: int = ti_rv if isinstance(ti_rv, int) else 0
                fa_rv = data.get("files_analyzed", 0)
                r_files_analyzed: int = fa_rv if isinstance(fa_rv, int) else 0
                reports.append({
                    "filename": report_file.name,
                    "date": report_date.isoformat(),
                    "quality_score": r_quality_score,
                    "total_issues": r_total_issues,
                    "files_analyzed": r_files_analyzed,
                })
            except c.EXC_FS_KEY_VALUE as e:
                self._logger_instance.warning(
                    "Failed to process report file: %s",
                    str(e),
                )
                continue

        # Sort by date descending and limit
        reports = sorted(reports, key=operator.itemgetter("date"), reverse=True)
        return reports[:limit]

    def get_dashboard_html(self) -> str:
        """Generate the main dashboard HTML."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FLEXT Quality Documentation Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        .metric-label {
            color: #666;
            font-size: 0.9em;
        }
        .quality-score {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
        }
        .issues-count {
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
        }
        .charts-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chart-card h3 {
            margin-bottom: 20px;
            color: #333;
        }
        .recent-reports {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .report-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .report-item:last-child {
            border-bottom: none;
        }
        .report-date {
            color: #666;
            font-size: 0.9em;
        }
        .report-score {
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 5px;
            color: white;
        }
        .score-excellent { background: #4CAF50; }
        .score-good { background: #FF9800; }
        .score-poor { background: #f44336; }
        @media (max-width: 768px) {
            .charts-container {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 FLEXT Quality Documentation Dashboard</h1>
            <p>Real-time monitoring of documentation health and quality metrics</p>
            <div id="last-updated">Loading...</div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card quality-score">
                <div class="metric-value" id="quality-score">--</div>
                <div class="metric-label">Quality Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="files-analyzed">--</div>
                <div class="metric-label">Files Analyzed</div>
            </div>
            <div class="metric-card issues-count">
                <div class="metric-value" id="total-issues">--</div>
                <div class="metric-label">Total Issues</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="critical-issues">--</div>
                <div class="metric-label">Critical Issues</div>
            </div>
        </div>

        <div class="charts-container">
            <div class="chart-card">
                <h3>Quality Score Trend (30 days)</h3>
                <canvas id="qualityChart" width="400" height="200"></canvas>
            </div>
            <div class="chart-card">
                <h3>Issues Breakdown</h3>
                <canvas id="issuesChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="recent-reports">
            <h3>Recent Audit Reports</h3>
            <div id="recent-reports-list">
                <div class="report-item">
                    <div>Loading recent reports...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let qualityChart, issuesChart;

        async function loadDashboard() {
            try {
                // Load current metrics
                const metricsResponse = await fetch('/api/metrics');
                const metrics = await metricsResponse.json();

                document.getElementById('quality-score').textContent = metrics.quality_score;
                document.getElementById('files-analyzed').textContent = metrics.files_analyzed;
                document.getElementById('total-issues').textContent = metrics.total_issues;
                document.getElementById('critical-issues').textContent = metrics.severity_breakdown.critical || 0;

                // Update last updated time
                const lastUpdated = new Date(metrics.timestamp);
                document.getElementById('last-updated').textContent =
                    `Last updated: ${lastUpdated.toLocaleString()}`;

                // Load trends
                const trendsResponse = await fetch('/api/trends');
                const trends = await trendsResponse.json();

                updateQualityChart(trends.trends);
                updateIssuesChart(metrics.severity_breakdown);

                // Load recent reports
                const reportsResponse = await fetch('/api/reports');
                const reports = await reportsResponse.json();

                updateRecentReports(reports);

            } catch (error) {
                console.error('Error loading dashboard:', error);
                document.getElementById('last-updated').textContent = 'Error loading data';
            }
        }

        function updateQualityChart(trendData) {
            const ctx = document.getElementById('qualityChart').getContext('2d');

            if (qualityChart) {
                qualityChart.destroy();
            }

            const labels = trendData.map(d => new Date(d.date).toLocaleDateString());
            const scores = trendData.map(d => d.quality_score);

            qualityChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Quality Score',
                        data: scores,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function updateIssuesChart(severityBreakdown) {
            const ctx = document.getElementById('issuesChart').getContext('2d');

            if (issuesChart) {
                issuesChart.destroy();
            }

            issuesChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Critical', 'High', 'Medium', 'Low'],
                    datasets: [{
                        data: [
                            severityBreakdown.critical || 0,
                            severityBreakdown.high || 0,
                            severityBreakdown.medium || 0,
                            severityBreakdown.low || 0
                        ],
                        backgroundColor: [
                            '#f44336',
                            '#ff9800',
                            '#ffeb3b',
                            '#4caf50'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        function updateRecentReports(reports) {
            const container = document.getElementById('recent-reports-list');
            container.innerHTML = '';

            if (reports.length === 0) {
                container.innerHTML = '<div class="report-item">No recent reports found</div>';
                return;
            }

            reports.forEach(report => {
                const date = new Date(report.date);
                const scoreClass = report.quality_score >= 80 ? 'score-excellent' :
                                 report.quality_score >= 60 ? 'score-good' : 'score-poor';

                const item = document.createElement('div');
                item.className = 'report-item';
                item.innerHTML = `
                    <div>
                        <strong>${report.filename}</strong>
                        <div class="report-date">${date.toLocaleString()}</div>
                    </div>
                    <div>
                        <span class="report-score ${scoreClass}">${report.quality_score}</span>
                        <div style="font-size: 0.8em; color: #666;">${report.total_issues} issues</div>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        // Load dashboard on page load
        loadDashboard();

        // Refresh every 5 minutes
        setInterval(loadDashboard, 5 * 60 * 1000);
    </script>
</body>
</html>
        """

    def run(
        self,
        host: str = "localhost",
        port: int = 8080,
        *,
        debug: bool = False,
    ) -> None:
        """Run the dashboard server."""
        self.app.run(host=host, port=port, debug=debug)


class _DashboardCommand(s[bool]):
    """CLI command for the FLEXT Quality Documentation Dashboard."""

    host: Annotated[str, cli_u.Field(default="localhost")] = "localhost"
    port: Annotated[int, cli_u.Field(default=8080)] = 8080
    debug: Annotated[bool, cli_u.Field(default=False)] = False
    reports_dir: Annotated[str, cli_u.Field(default="docs/maintenance/reports/")] = (
        "docs/maintenance/reports/"
    )

    @override
    def execute(self) -> p.Result[bool]:
        """Run the dashboard server."""
        dashboard = FlextQualityDocumentationDashboard(self.reports_dir)
        dashboard.run(host=self.host, port=self.port, debug=self.debug)
        return r[bool].ok(value=True)


def main(args: t.StrSequence | None = None) -> int:
    """Main entry point for the dashboard via the canonical cli facade."""
    app = cli.create_app_with_common_params(
        name="flext-quality-dashboard",
        help_text="FLEXT Quality Documentation Dashboard",
    )
    cli.register_result_routes(
        app,
        [
            cli_m.Cli.ResultCommandRoute(
                name="run",
                help_text="Start the dashboard server",
                model_cls=_DashboardCommand,
                handler=lambda params: params.execute(),
            ),
        ],
    )
    outcome = cli.execute_app(
        app,
        prog_name="flext-quality-dashboard",
        args=list(args) if args is not None else sys.argv[1:],
    )
    return 0 if outcome.success else 1


if __name__ == "__main__":
    cli.exit(main())
