"""FLEXT Quality Documentation Health Dashboard.

Real-time monitoring dashboard for documentation quality metrics.
Provides web interface to view audit results, trends, and quality scores.
"""

import argparse
import json
import logging
import operator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, render_template_string, request

logger = logging.getLogger(__name__)


class DocumentationDashboard:
    """Documentation health monitoring dashboard."""

    def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
        """Initialize documentation dashboard with reports directory."""
        self.reports_dir = Path(reports_dir)
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self) -> None:
        """Setup Flask routes for the dashboard."""

        @self.app.route("/")
        def index() -> Response:
            """Main dashboard page."""
            return render_template_string(self.get_dashboard_html())

        @self.app.route("/api/metrics")
        def api_metrics() -> Response:
            """API endpoint for current metrics."""
            return jsonify(self.get_current_metrics())

        @self.app.route("/api/trends")
        def api_trends() -> Response:
            """API endpoint for quality trends."""
            days = int(request.args.get("days", 30))
            return jsonify(self.get_quality_trends(days))

        @self.app.route("/api/reports")
        def api_reports() -> Response:
            """API endpoint for recent reports."""
            limit = int(request.args.get("limit", 10))
            return jsonify(self.get_recent_reports(limit))

    def get_current_metrics(self) -> dict[str, Any]:
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
            with Path(latest_audit).open(encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "quality_score": data.get("metrics", {}).get("quality_score", 0),
                    "files_analyzed": data.get("files_analyzed", 0),
                    "total_issues": data.get("metrics", {}).get("total_issues", 0),
                    "severity_breakdown": data.get("metrics", {}).get(
                        "severity_breakdown",
                        {},
                    ),
                    "timestamp": data.get("timestamp", datetime.now(UTC).isoformat()),
                    "status": "Current",
                }
        except Exception as e:
            return {
                "quality_score": 0,
                "files_analyzed": 0,
                "total_issues": 0,
                "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "timestamp": datetime.now(UTC).isoformat(),
                "status": f"Error: {e!s}",
            }

    def get_quality_trends(self, days: int = 30) -> dict[str, Any]:
        """Get quality trends over the specified number of days."""
        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        trend_data = []
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
                    with Path(report_file).open(encoding="utf-8") as f:
                        data = json.load(f)
                        trend_data.append(
                            {
                                "date": report_date.isoformat(),
                                "quality_score": data.get("metrics", {}).get(
                                    "quality_score",
                                    0,
                                ),
                                "total_issues": data.get("metrics", {}).get(
                                    "total_issues",
                                    0,
                                ),
                                "critical_issues": data.get("metrics", {})
                                .get("severity_breakdown", {})
                                .get("critical", 0),
                                "high_issues": data.get("metrics", {})
                                .get("severity_breakdown", {})
                                .get("high", 0),
                            }
                        )
            except Exception as e:
                logger.warning("Failed to process trend data: %s", e)
                continue

        # Sort by date
        trend_data.sort(key=operator.itemgetter("date"))

        return {
            "period_days": days,
            "data_points": len(trend_data),
            "trends": trend_data,
        }

    def get_recent_reports(self, limit: int = 10) -> list:
        """Get list of recent audit reports."""
        reports = []

        for report_file in self.reports_dir.glob("audit_report_*.json"):
            try:
                date_str = report_file.stem.replace("audit_report_", "").replace(
                    "_",
                    " ",
                )
                report_date = datetime.strptime(date_str, "%Y%m%d %H%M%S").replace(
                    tzinfo=UTC,
                )

                with Path(report_file).open(encoding="utf-8") as f:
                    data = json.load(f)

                reports.append(
                    {
                        "filename": report_file.name,
                        "date": report_date.isoformat(),
                        "quality_score": data.get("metrics", {}).get(
                            "quality_score", 0
                        ),
                        "total_issues": data.get("metrics", {}).get("total_issues", 0),
                        "files_analyzed": data.get("files_analyzed", 0),
                    }
                )
            except Exception as e:
                logger.warning("Failed to process report file: %s", e)
                continue

        # Sort by date descending and limit
        reports.sort(key=operator.itemgetter("date"), reverse=True)
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


def main() -> None:
    """Main entry point for the dashboard."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Dashboard",
    )
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--reports-dir",
        default="docs/maintenance/reports/",
        help="Directory containing audit reports",
    )

    args = parser.parse_args()

    dashboard = DocumentationDashboard(args.reports_dir)
    dashboard.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
