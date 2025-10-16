"""Tests for the Quality Web Interface module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from flask import Flask
from flext_core import FlextTypes

from flext_quality import FlextQualityWebInterface as QualityWebInterface, main


class TestQualityWebInterface:
    """Test Quality Web Interface class."""

    def test_init(self) -> None:
        """Test QualityWebInterface initialization."""
        with (
            patch("flext_quality.web.get_web_settings") as mock_get_settings,
            patch("flext_quality.web.create_service") as mock_create_service,
        ):
            # Setup mocks
            mock_config = MagicMock()
            mock_get_settings.return_value = mock_config

            mock_service = MagicMock()
            mock_app = Flask(__name__)
            mock_service.app = mock_app
            mock_create_service.return_value = mock_service

            # Create interface
            interface = QualityWebInterface()

            # Verify initialization
            assert interface.config == mock_config
            assert interface.web_service == mock_service
            assert interface.quality_api is not None
            mock_get_settings.assert_called_once()
            mock_create_service.assert_called_once_with(mock_config)

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    def test_register_routes(
        self,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test route registration."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = MagicMock(spec=Flask)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        # Create interface
        QualityWebInterface()

        # Verify routes registered
        assert mock_app.route.call_count >= 4
        mock_app.route.assert_any_call("/quality")
        mock_app.route.assert_any_call("/api/quality/analyze", methods=["POST"])
        mock_app.route.assert_any_call("/api/quality/metrics", methods=["GET"])
        mock_app.route.assert_any_call("/api/quality/report/<format>", methods=["GET"])

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    def test_quality_dashboard(
        self,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test quality dashboard method."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        # Create interface
        interface = QualityWebInterface()

        # Test dashboard
        html = interface.quality_dashboard()

        # Verify HTML content
        assert "<!DOCTYPE html>" in html
        assert "FLEXT Quality Analysis" in html
        assert "Code Coverage" in html
        assert "Quality Score" in html
        assert "Issues Found" in html

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    def test_analyze_project(
        self,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test analyze_project method."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        # Create interface
        interface = QualityWebInterface()

        # Use Flask test client context
        with mock_app.test_request_context(
            "/api/quality/analyze",
            method="POST",
            json={"path": "/test/path"},
        ):
            # Import inside context to avoid issues
            # Call method (it's )
            result = interface.analyze_project()

            # Verify response structure
            # The actual jsonify returns a Response object in test context
            # We just verify the method runs without error
            assert result is not None

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    @patch("flext_quality.web.jsonify")
    def test_get_metrics(
        self,
        mock_jsonify: MagicMock,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test get_metrics method."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        mock_jsonify.return_value = "metrics_response"

        # Create interface
        interface = QualityWebInterface()

        # Test metrics
        result = interface.get_metrics()

        # Verify
        assert result is not None  # Response object returned
        mock_jsonify.assert_called_once()
        call_args = mock_jsonify.call_args[0][0]
        assert call_args["success"] is True
        assert "data" in call_args
        assert "coverage" in call_args["data"]
        assert "complexity" in call_args["data"]

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    @patch("flext_quality.web.jsonify")
    def test_get_report_valid_format(
        self,
        mock_jsonify: MagicMock,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test get_report with valid format."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        mock_jsonify.return_value = "report_response"

        # Create interface
        interface = QualityWebInterface()

        # Test report
        result = interface.get_report("json")

        # Verify
        assert result is not None  # Response object returned
        mock_jsonify.assert_called_once()
        call_args = mock_jsonify.call_args[0][0]
        assert call_args["success"] is True
        assert "data" in call_args
        assert call_args["data"]["format"] == "json"

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    @patch("flext_quality.web.jsonify")
    def test_get_report_invalid_format(
        self,
        mock_jsonify: MagicMock,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test get_report with invalid format."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_create_service.return_value = mock_service

        # Mock for error response - jsonify returns tuple for error cases
        def jsonify_side_effect(
            data: FlextTypes.Dict | str,
            *_: object,
        ) -> str:
            if "error" in data:
                return "error_response"
            return "success_response"

        mock_jsonify.side_effect = jsonify_side_effect

        # Create interface
        interface = QualityWebInterface()

        # Test report with invalid format
        result = interface.get_report("invalid")

        # Verify error response - get_report returns tuple
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[1] == 400

    @patch("flext_quality.web.get_web_settings")
    @patch("flext_quality.web.create_service")
    @patch("flext_quality.web.logger")
    def test_run(
        self,
        mock_logger: MagicMock,
        mock_create_service: MagicMock,
        mock_get_settings: MagicMock,
    ) -> None:
        """Test run method."""
        # Setup mocks
        mock_config = MagicMock()
        mock_get_settings.return_value = mock_config

        mock_service = MagicMock()
        mock_app = Flask(__name__)
        mock_service.app = mock_app
        mock_service.run = MagicMock()
        mock_create_service.return_value = mock_service

        # Create interface and run
        interface = QualityWebInterface()
        interface.run(host="127.0.0.1", port=9000, debug=False)

        # Verify
        mock_service.run.assert_called_once_with(
            host="127.0.0.1",
            port=9000,
            debug=False,
        )
        mock_logger.info.assert_called()

    @patch("flext_quality.web.QualityWebInterface")
    def test_self(self, mock_interface_class: MagicMock) -> None:
        """Test main function."""
        # Setup mock
        mock_interface = MagicMock()
        mock_interface_class.return_value = mock_interface

        # Call main
        main()

        # Verify
        mock_interface_class.assert_called_once()
        mock_interface.run.assert_called_once()
