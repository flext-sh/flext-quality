"""Tests for the Quality Web Interface module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from flext_quality.web import FlextQualityWeb


class TestFlextQualityWeb:
    """Test FlextQualityWeb class."""

    @patch("flext_quality.web.create_fastapi_app")
    @patch("flext_quality.web.FlextQualitySettings")
    def test_init(
        self,
        mock_config: MagicMock,
        mock_create_app: MagicMock,
    ) -> None:
        """Test FlextQualityWeb initialization."""
        # Setup mocks
        mock_app = MagicMock()
        mock_app_result = MagicMock()
        mock_app_result.is_failure = False
        mock_app_result.value = mock_app
        mock_create_app.return_value = mock_app_result

        # Create interface
        interface = FlextQualityWeb()

        # Verify initialization
        assert interface.app == mock_app
        assert interface.quality_api is not None
        mock_create_app.assert_called_once()
