"""FLEXT Quality Web - Web service endpoints for quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flask import Response as FlaskResponse, jsonify, request
from Flext_web.config import FlextWebConfig
from werkzeug.wrappers import Response as WerkzeugResponse

from flext_core import FlextContainer, FlextLogger, FlextResult, FlextTypes
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.api import QualityAPI
from flext_web import FlextWebServices

ResponseType = (FlaskResponse | WerkzeugResponse) | tuple[FlaskResponse, int]


class FlextQualityWeb:
    """Unified quality web class following FLEXT architecture patterns.

    Single responsibility: Quality web interface and service management
    Contains all web functionality as nested classes and methods.
    """

    def __init__(self: object) -> None:
        """Initialize quality web interface."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Create base web service from flext-web
        self.config: dict[str, object] = self._get_web_settings()
        web_service = self._create_service(self.config)

        if web_service is None:
            error_msg = "Failed to create web service"
            raise RuntimeError(error_msg)

        # Type annotation and assignment combined
        self.web_service: object = web_service

        # Initialize quality components
        self.quality_api = QualityAPI()

        # Register quality-specific routes
        self._register_routes()

    @staticmethod
    def _create_service(config: dict[str, object] | None = None) -> object | None:
        """Create web service using flext-web patterns."""
        logger = FlextLogger(__name__)

        # Convert dict to proper WebConfig with explicit validation - no try/except fallbacks
        web_config = None
        if config and isinstance(config, dict):
            # Extract values with proper type checking
            def safe_int(value: object, default: int) -> int:
                return int(value) if isinstance(value, (int, float)) else default

            def safe_str(value: object, default: str) -> str:
                return str(value) if isinstance(value, str) else default

            def safe_bool(value: object, *, default: bool) -> bool:
                return bool(value) if isinstance(value, bool) else default

            # Validate required config parameters explicitly
            if all(key in config for key in ["host", "port"]):
                web_config = FlextWebConfig.WebConfig(
                    host=safe_str(config.get("host"), "localhost"),
                    port=safe_int(config.get("port"), 8000),
                    debug=safe_bool(config.get("debug"), default=False),
                    max_workers=safe_int(config.get("max_workers"), 1),
                )
            else:
                logger.warning("Invalid WebConfig dict: missing required fields")
                web_config = None

        result: FlextResult[object] = FlextWebServices.create_web_service(web_config)
        return result.value if result.is_success else None

    @staticmethod
    def _get_web_settings() -> dict[str, object]:
        """Get web settings using flext-web patterns."""
        # Type conversion for compatibility
        result: FlextResult[object] = FlextWebConfig.get_web_settings()
        return dict(result) if hasattr(result, "__dict__") else {}

    @staticmethod
    def web_main() -> None:
        """Main entry point for quality web interface."""
        interface = FlextQualityWeb()
        interface.run()

    def _register_routes(self: object) -> None:
        """Register quality analysis routes with Flask app."""
        if not hasattr(self.web_service, "app"):
            msg = "Web service does not have an 'app' attribute"
            raise AttributeError(msg)
        app = getattr(self.web_service, "app")

        # Dashboard
        app.route("/quality")(self.quality_dashboard)

        # API endpoints
        app.route("/api/quality/analyze", methods=["POST"])(self.analyze_project)
        app.route("/api/quality/metrics", methods=["GET"])(self.get_metrics)
        app.route("/api/quality/report/<format>", methods=["GET"])(self.get_report)

    def quality_dashboard(self: object) -> str:
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
                  const data: dict[str, object] = await response.json();
                  document.getElementById('results').innerHTML =
                      '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
              }
          </script>
      </body>
      </html>
      """

    async def analyze_project(self) -> ResponseType:
        """Analyze a project and return results."""
        data: dict[str, object] = request.get_json()
        project_path = data.get("path", ".")

        # Create analyzer for the specific path
        analyzer = CodeAnalyzer(Path(project_path))
        result: FlextResult[object] = analyzer.analyze_project()

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

    def get_metrics(self: object) -> ResponseType:
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
        self._logger.info("Starting FLEXT Quality Web Interface on %s:%s", host, port)
        if not hasattr(self.web_service, "run"):
            msg = "Web service does not have a 'run' method"
            raise AttributeError(msg)
        run_method = getattr(self.web_service, "run")
        run_method(host=host, port=port, debug=debug)


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
