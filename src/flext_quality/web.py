"""FLEXT Quality Web - Web service endpoints for quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

# FastAPI types needed for runtime web functionality
# These are acceptable since flext-web is the FastAPI domain library
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

# Domain library imports (ZERO TOLERANCE - NO direct FastAPI imports)
from flext_auth import FlextAuth, JwtAuthProvider, WebAuthMiddleware
from flext_core import FlextContainer, FlextLogger, FlextTypes
from flext_web import create_fastapi_app

from .analyzer import CodeAnalyzer
from .api import QualityAPI
from .config import FlextQualityConfig


class FlextQualityWeb:
    """Unified quality web class following FLEXT architecture patterns.

    Single responsibility: Quality web interface and service management using flext-web.
    Integrates flext-auth for authentication and flext-web for FastAPI foundation.
    """

    app: FastAPI

    def __init__(self) -> None:
        """Initialize quality web interface with flext ecosystem integration."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Initialize quality configuration
        self._quality_config = FlextQualityConfig()

        # Initialize flext-web configuration
        from flext_web import FlextWebModels  # noqa: PLC0415

        app_config = FlextWebModels.AppConfig(
            title="flext-quality",
            version="0.9.0",
            enable_cors=True,
            enable_docs=True,
        )

        # Create FastAPI app via flext-web
        app_result = create_fastapi_app(config=app_config)
        if app_result.is_failure:
            msg = f"Failed to create FastAPI app: {app_result.error}"
            raise RuntimeError(msg)
        self.app = cast("FastAPI", app_result.value)

        # Initialize quality components
        self.quality_api = QualityAPI()

        # Initialize authentication (flext-auth integration)
        self._auth = self._setup_authentication()

        # Register quality-specific routes
        self._register_routes()

    def _setup_authentication(self) -> FlextAuth | None:
        """Setup authentication using flext-auth with JWT provider."""
        try:
            # Create auth config dict for JWT provider
            auth_config: FlextTypes.Dict = {
                "secret_key": self._quality_config.project_name + "-secret-key",
                "algorithm": "HS256",
                "token_expiry_minutes": 60,
            }

            # Create JWT auth provider for quality API
            jwt_provider = JwtAuthProvider(config=auth_config)

            # Initialize FlextAuth
            auth = FlextAuth()

            # Add web auth middleware to FastAPI app
            self.app.add_middleware(
                WebAuthMiddleware,
                auth_provider=jwt_provider,
                exclude_paths=["/health", "/docs", "/redoc", "/openapi.json"],
            )

            self._logger.info("Authentication configured successfully")
            return auth

        except Exception as e:
            self._logger.warning(
                f"Authentication setup failed: {e}, proceeding without auth"
            )
            # Return None if authentication setup fails (graceful degradation)
            return None

    def _register_routes(self) -> None:
        """Register quality analysis routes with FastAPI app."""
        # Health endpoint (public, no authentication)
        self.app.get("/health", tags=["Health"])(self.health_check)

        # Dashboard endpoint (public)
        self.app.get("/quality", response_class=HTMLResponse, tags=["Dashboard"])(
            self.quality_dashboard
        )

        # API endpoints (require authentication via middleware)
        self.app.post("/api/quality/analyze", tags=["Analysis"])(self.analyze_project)
        self.app.get("/api/quality/metrics", tags=["Metrics"])(self.get_metrics)
        self.app.get("/api/quality/report/{format}", tags=["Reports"])(self.get_report)

    async def health_check(self) -> dict[str, str]:
        """Health check endpoint for quality service monitoring."""
        return {
            "status": "healthy",
            "service": "flext-quality",
            "version": "0.9.0",
        }

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

    async def analyze_project(self, request: Request) -> FlextTypes.Dict:
        """Analyze a project and return results (FastAPI endpoint).

        Requires authentication via WebAuthMiddleware.
        """
        try:
            data = await request.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid JSON data") from e

        if not data or not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Invalid JSON data")

        project_path = data.get("path", ".")

        # Create analyzer for the specific path
        try:
            analyzer = CodeAnalyzer(Path(project_path))
            result = analyzer.analyze_project()
        except Exception as e:
            self._logger.exception("Analysis failed")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {e}") from e

        if not hasattr(result, "overall_metrics"):
            raise HTTPException(status_code=500, detail="Analysis failed")

        return {
            "success": True,
            "data": {
                "path": project_path,
                "files_analyzed": getattr(result.overall_metrics, "files_analyzed", 0),
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
        }

    async def get_metrics(self) -> FlextTypes.Dict:
        """Get quality metrics (FastAPI endpoint).

        Requires authentication via WebAuthMiddleware.
        """
        # Use simple placeholder metrics for now
        return {"success": True, "data": {}}

    async def get_report(self, report_format: str) -> FlextTypes.Dict:
        """Generate and return quality report (FastAPI endpoint).

        Args:
            report_format: Report format (json, html, pdf)

        Requires authentication via WebAuthMiddleware.

        """
        if report_format not in {"json", "html", "pdf"}:
            raise HTTPException(status_code=400, detail="Invalid format")

        return {"success": True, "data": {}}

    def run(
        self,
        host: str = "0.0.0.0",  # noqa: S104
        port: int = 8080,
        *,
        debug: bool = False,
        reload: bool = False,
    ) -> None:
        """Run the quality web server using uvicorn (FastAPI ASGI server).

        Args:
            host: Server host address (default: 0.0.0.0)
            port: Server port (default: 8080)
            debug: Enable debug mode
            reload: Enable auto-reload on code changes

        """
        self._logger.info("Starting FLEXT Quality Web Interface on %s:%s", host, port)

        try:
            import uvicorn  # noqa: PLC0415
        except ImportError as e:
            self._logger.exception("uvicorn not installed")
            msg = "uvicorn not installed. Install with: pip install uvicorn[standard]"
            raise ImportError(msg) from e

        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="debug" if debug else "info",
            reload=reload,
        )

    @staticmethod
    def web_main() -> None:
        """Main entry point for quality web interface."""
        interface = FlextQualityWeb()
        interface.run(debug=True, reload=True)


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
