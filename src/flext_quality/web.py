"""FLEXT Quality Web - Web service endpoints for quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flask import Response as FlaskResponse, jsonify, request
from flext_core import FlextLogger, FlextTypes
from flext_web import FlextWebServices
from flext_web.config import FlextWebConfigs
from werkzeug.wrappers import Response as WerkzeugResponse

from flext_quality.analyzer import CodeAnalyzer
from flext_quality.api import QualityAPI

# Use aliases simples para funções existentes no flext-web


# Aliases simples para compatibilidade dos testes
def create_service(config: dict[str, object] | None = None) -> object | None:
    """Alias simples para FlextWebServices.create_web_service."""
    # Convert dict to proper WebConfig if provided
    web_config = None
    if config:
        try:
            web_config = FlextWebConfigs.WebConfig(**config)
        except Exception:
            # Log the exception but continue with None config
            logger.warning(
                "Failed to create WebConfig from provided dict, using default"
            )
            web_config = None

    result = FlextWebServices.create_web_service(web_config)
    return result.value if result.is_success else None


def get_web_settings() -> dict[str, object]:
    """Alias simples para FlextWebConfigs.get_web_settings."""
    # Type conversion for compatibility
    result = FlextWebConfigs.get_web_settings()
    return dict(result) if hasattr(result, "__dict__") else {}


ResponseType = FlaskResponse | WerkzeugResponse | tuple[FlaskResponse, int]

logger = FlextLogger(__name__)


class FlextQualityWebInterface:
    """Quality analysis web interface that extends flext-web."""

    def __init__(self) -> None:
        """Initialize quality web interface."""
        # Create base web service from flext-web
        self.config = get_web_settings()
        web_service = create_service(self.config)

        if web_service is None:
            error_msg = "Failed to create web service"
            raise RuntimeError(error_msg)

        self.web_service = web_service

        # Initialize quality components
        self.quality_api = QualityAPI()

        # Register quality-specific routes
        self._register_routes()

    def _register_routes(self) -> None:
        """Register quality analysis routes with Flask app."""
        if not hasattr(self.web_service, "app"):
            msg = "Web service does not have an 'app' attribute"
            raise AttributeError(msg)
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

        # Extract data from AnalysisResults
        files_count = result.overall_metrics.files_analyzed

        return jsonify(
            {
                "success": True,
                "data": {
                    "path": project_path,
                    "files_analyzed": files_count,
                    "issues": result.total_issues,
                    "metrics": {
                        "quality_score": result.overall_metrics.quality_score,
                        "security_score": result.overall_metrics.security_score,
                        "coverage_score": result.overall_metrics.coverage_score,
                    },
                },
            },
        )

    def get_metrics(self) -> ResponseType:
        """Get quality metrics."""
        # Use simple placeholder metrics for now
        metrics: FlextTypes.Core.Dict = {
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

        report: FlextTypes.Core.Dict = {
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
        logger.info("Starting FLEXT Quality Web Interface on %s:%s", host, port)
        if not hasattr(self.web_service, "run"):
            msg = "Web service does not have a 'run' method"
            raise AttributeError(msg)
        self.web_service.run(host=host, port=port, debug=debug)


def web_main() -> None:
    """Provide entry point for quality web interface."""
    interface = FlextQualityWebInterface()
    interface.run()


# Legacy compatibility alias
main = web_main

__all__ = [
    "FlextQualityWebInterface",
    "main",  # Legacy compatibility
    "web_main",
]

if __name__ == "__main__":
    web_main()
