"""FLEXT Quality Web Interface Extension.

This module extends flext-web Flask service with quality analysis capabilities,
reusing existing analysis components from flext-quality.

Architecture:
    - Properly extends flext-web without violating dependency hierarchy
    - Reuses existing analysis backends and metrics collectors
    - Provides REST API and simple dashboard

Author: FLEXT Development Team
Version: 0.9.0
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flask import jsonify, request
from flext_core import get_logger
from flext_web import create_service, get_web_settings

from flext_quality.analyzer import CodeAnalyzer
from flext_quality.simple_api import QualityAPI

if TYPE_CHECKING:
    from flask import Response as FlaskResponse
    from werkzeug.wrappers import Response as WerkzeugResponse

    ResponseType = FlaskResponse | WerkzeugResponse | tuple[FlaskResponse, int]

logger = get_logger(__name__)


class QualityWebInterface:
    """Quality analysis web interface that extends flext-web."""

    def __init__(self) -> None:
        """Initialize quality web interface."""
        # Create base web service from flext-web
        self.config = get_web_settings()
        self.web_service = create_service(self.config)

        # Initialize quality components
        self.quality_api = QualityAPI()

        # Register quality-specific routes
        self._register_routes()

    def _register_routes(self) -> None:
        """Register quality analysis routes with Flask app."""
        app = self.web_service.app

        # Dashboard
        app.route("/quality")(self.quality_dashboard)

        # API endpoints
        app.route("/api/quality/analyze", methods=["POST"])(self.analyze_project)
        app.route("/api/quality/metrics", methods=["GET"])(self.get_metrics)
        app.route("/api/quality/report/<format>", methods=["GET"])(self.get_report)

    def quality_dashboard(self) -> str:
        """Render quality dashboard."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FLEXT Quality Analysis</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #333; }
                .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
                .metric-card {
                    background: #f5f5f5;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .metric-value { font-size: 2em; font-weight: bold; color: #007bff; }
                .analyze-form {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-top: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                button {
                    background: #007bff;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover { background: #0056b3; }
                input {
                    width: 100%;
                    padding: 8px;
                    margin: 10px 0;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 FLEXT Quality Analysis</h1>

                <div class="metrics">
                    <div class="metric-card">
                        <h3>Code Coverage</h3>
                        <div class="metric-value">95%</div>
                    </div>
                    <div class="metric-card">
                        <h3>Quality Score</h3>
                        <div class="metric-value">A</div>
                    </div>
                    <div class="metric-card">
                        <h3>Issues Found</h3>
                        <div class="metric-value">12</div>
                    </div>
                </div>

                <div class="analyze-form">
                    <h2>Analyze Project</h2>
                    <input type="text" id="project-path" placeholder="Enter project path">
                    <button onclick="analyzeProject()">Start Analysis</button>
                    <div id="results"></div>
                </div>
            </div>

            <script>
                async function analyzeProject() {
                    const path = document.getElementById('project-path').value;
                    const response = await fetch('/api/quality/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({path: path})
                    });
                    const data = await response.json();
                    document.getElementById('results').innerHTML =
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }
            </script>
        </body>
        </html>
        """

    async def analyze_project(self) -> ResponseType:
        """Analyze a project and return results."""
        data = request.get_json()
        project_path = data.get("path", ".")

        # Create analyzer for the specific path
        analyzer = CodeAnalyzer(Path(project_path))
        result = analyzer.analyze_project()

        # Safely extract files list
        files_data = result.get("files", [])
        files_count = len(files_data) if isinstance(files_data, list) else 0

        return jsonify(
            {
                "success": True,
                "data": {
                    "path": project_path,
                    "files_analyzed": files_count,
                    "issues": result.get("issues", []),
                    "metrics": result.get("metrics", {}),
                },
            },
        )

    def get_metrics(self) -> ResponseType:
        """Get quality metrics."""
        # Use simple placeholder metrics for now
        metrics = {
            "coverage": 95.0,
            "complexity": 10.0,
            "duplication": 5.0,
            "issues": 12,
        }
        return jsonify({"success": True, "data": metrics})

    def get_report(self, report_format: str) -> ResponseType:
        """Generate and return quality report."""
        if report_format not in {"json", "html", "pdf"}:
            return jsonify({"success": False, "error": "Invalid format"}), 400

        # Simple report placeholder
        report = {
            "format": report_format,
            "generated_at": "2025-01-08",
            "quality_score": "A",
            "coverage": 95.0,
        }
        return jsonify({"success": True, "data": report})

    def run(
        self,
        host: str = "localhost",
        port: int = 8080,
        *,
        debug: bool = True,
    ) -> None:
        """Run the quality web server."""
        logger.info(f"Starting FLEXT Quality Web Interface on {host}:{port}")
        self.web_service.run(host=host, port=port, debug=debug)


def main() -> None:
    """Provide entry point for quality web interface."""
    interface = QualityWebInterface()
    interface.run()


if __name__ == "__main__":
    main()
