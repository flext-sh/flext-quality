"""FLEXT Quality Web - Web service endpoints for quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, Response as FlaskResponse, jsonify, request
from werkzeug.wrappers import Response as WerkzeugResponse

from flext_core import FlextContainer, FlextLogger
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.api import QualityAPI

ResponseType = FlaskResponse | WerkzeugResponse | tuple[FlaskResponse, int]


class FlextQualityWeb:
    """Unified quality web class following FLEXT architecture patterns.

    Single responsibility: Quality web interface and service management
    Contains all web functionality as nested classes and methods.
    """

    def __init__(self) -> None:
        """Initialize quality web interface."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Create Flask app directly
        self.app = Flask(__name__)

        # Initialize quality components
        self.quality_api = QualityAPI()

        # Register quality-specific routes
        self._register_routes()

    def _register_routes(self) -> None:
        """Register quality analysis routes with Flask app."""
        # Dashboard
        self.app.route("/quality")(self.quality_dashboard)

        # API endpoints
        self.app.route("/api/quality/analyze", methods=["POST"])(self.analyze_project)
        self.app.route("/api/quality/metrics", methods=["GET"])(self.get_metrics)
        self.app.route("/api/quality/report/<format>", methods=["GET"])(self.get_report)

    def quality_dashboard(self) -> str:
        """Render quality dashboard."""
        return """

      <!DOCTYPE html>
      <html>
      <head>
          <title>FLEXT Quality Analysis</title>
          <style>
              body { font-family: "Arial", sans-serif; margin: 20px; }
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
                      method: "POST",
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

    def analyze_project(self) -> ResponseType:
        """Analyze a project and return results."""
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"success": False, "error": "Invalid JSON data"}), 400

        project_path = data.get("path", ".")

        # Create analyzer for the specific path
        analyzer = CodeAnalyzer(Path(project_path))
        result = analyzer.analyze_project()

        if not hasattr(result, "overall_metrics"):
            return jsonify({"success": False, "error": "Analysis failed"}), 500

        return jsonify(
            {
                "success": True,
                "data": {
                    "path": project_path,
                    "files_analyzed": getattr(
                        result.overall_metrics, "files_analyzed", 0
                    ),
                    "issues": getattr(result, "total_issues", 0),
                    "metrics": {
                        "quality_score": getattr(
                            result.overall_metrics, "quality_score", 0.0
                        ),
                        "security_score": getattr(
                            result.overall_metrics, "security_score", 0.0
                        ),
                        "coverage_score": getattr(
                            result.overall_metrics, "coverage_score", 0.0
                        ),
                    },
                },
            },
        )

    def get_metrics(self) -> ResponseType:
        """Get quality metrics."""
        # Use simple placeholder metrics for now
        return jsonify({"success": True, "data": {}})

    def get_report(self, report_format: str) -> ResponseType:
        """Generate and return quality report."""
        if report_format not in {"json", "html", "pdf"}:
            return jsonify({"success": False, "error": "Invalid format"}), 400

        return jsonify({"success": True, "data": {}})

    def run(
        self,
        host: str = "localhost",
        port: int = 8080,
        *,
        debug: bool = True,
    ) -> None:
        """Run the quality web server."""
        self._logger.info("Starting FLEXT Quality Web Interface on %s:%s", host, port)
        self.app.run(host=host, port=port, debug=debug)

    @staticmethod
    def web_main() -> None:
        """Main entry point for quality web interface."""
        interface = FlextQualityWeb()
        interface.run()


# Backward compatibility aliases for existing code
web_main = FlextQualityWeb.web_main
FlextQualityWebInterface = FlextQualityWeb
main = web_main

__all__ = [
    "FlextQualityWeb",
    "FlextQualityWebInterface",
    "main",  # Legacy compatibility
    "web_main",
]

if __name__ == "__main__":
    web_main()
