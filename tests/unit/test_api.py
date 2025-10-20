"""Test suite for FlextQualityServices.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_quality import FlextQualityServices


class TestFlextQualityServices:
    """Test FlextQualityServices functionality."""

    @pytest.fixture
    def services(self) -> FlextQualityServices:
        """Create FlextQualityServices instance."""
        return FlextQualityServices()

    def test_services_instantiation(self, services: FlextQualityServices) -> None:
        """Test services can be instantiated."""
        assert services is not None
        assert services.project_service is not None
        assert services.analysis_service is not None
        assert services.issue_service is not None
        assert services.report_service is not None

    def test_create_project_through_services(
        self,
        services: FlextQualityServices,
    ) -> None:
        """Test creating a project through services."""
        result = services.project_service.create_project(
            name="test_project",
            path="./test_project",
        )

        assert result.is_success
        project = result.unwrap()
        assert project is not None
        assert project.name == "test_project"
        assert project.path == "./test_project"

    def test_create_analysis_through_services(
        self,
        services: FlextQualityServices,
    ) -> None:
        """Test creating an analysis through services."""
        result = services.analysis_service.create_analysis(
            project_id="project_test",
        )

        assert result.is_success
        analysis = result.unwrap()
        assert analysis is not None
        assert analysis.project_id == "project_test"

    def test_create_issue_through_services(
        self,
        services: FlextQualityServices,
    ) -> None:
        """Test creating an issue through services."""
        result = services.issue_service.create_issue(
            analysis_id="analysis_test",
            severity="HIGH",
            issue_type="style_violation",
            file_path="test.py",
            message="Test issue",
        )

        assert result.is_success
        issue = result.unwrap()
        assert issue is not None
        assert issue.analysis_id == "analysis_test"
        assert issue.severity == "HIGH"

    def test_create_report_through_services(
        self,
        services: FlextQualityServices,
    ) -> None:
        """Test creating a report through services."""
        result = services.report_service.create_report(
            analysis_id="analysis_test",
            format_type="HTML",
        )

        assert result.is_success
        report = result.unwrap()
        assert report is not None
        assert report.analysis_id == "analysis_test"
        assert report.format_type == "HTML"
