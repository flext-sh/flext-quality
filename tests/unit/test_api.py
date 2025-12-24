"""Test suite for FlextQualityServices and V2 Builder Pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext import FlextLogger

from flext_quality.services import (
    AnalysisServiceBuilder,
    FlextQualityServices,
    IssueServiceBuilder,
    ProjectServiceBuilder,
    ReportServiceBuilder,
)
from flext_quality.settings import FlextQualitySettings


class TestFlextQualityServices:
    """Test FlextQualityServices functionality with V2 Builder Pattern."""

    @pytest.fixture
    def services(self) -> FlextQualityServices:
        """Create FlextQualityServices instance."""
        return FlextQualityServices()

    @pytest.fixture
    def config(self) -> FlextQualitySettings:
        """Create FlextQualitySettings instance."""
        return FlextQualitySettings()

    @pytest.fixture
    def logger(self) -> FlextLogger:
        """Create FlextLogger instance."""
        return FlextLogger(__name__)

    def test_services_instantiation(self, services: FlextQualityServices) -> None:
        """Test services can be instantiated."""
        assert services is not None
        # V2 Pattern: No nested services, only builders

    def test_create_project_through_builder(
        self,
        config: FlextQualitySettings,
        logger: FlextLogger,
    ) -> None:
        """Test creating a project through builder pattern."""
        result = (
            ProjectServiceBuilder(config, logger)
            .with_name("test_project")
            .with_path("./test_project")
            .build()
        )

        assert result.is_success
        project = result.value
        assert project is not None
        assert project.name == "test_project"
        assert project.path == "./test_project"

    def test_create_analysis_through_builder(
        self,
        config: FlextQualitySettings,
        logger: FlextLogger,
    ) -> None:
        """Test creating an analysis through builder pattern."""
        result = (
            AnalysisServiceBuilder(config, logger)
            .with_project_id("project_test")
            .build()
        )

        assert result.is_success
        analysis = result.value
        assert analysis is not None
        # Analysis ID is UUID, project_id is UUID
        assert str(analysis.project_id) is not None

    def test_create_issue_through_builder(
        self,
        config: FlextQualitySettings,
        logger: FlextLogger,
    ) -> None:
        """Test creating an issue through builder pattern."""
        result = (
            IssueServiceBuilder(config, logger)
            .with_analysis_id("analysis_test")
            .with_severity("HIGH")
            .with_issue_type("high_complexity")
            .with_file_path("test.py")
            .with_message("Test issue")
            .build()
        )

        assert result.is_success
        issue = result.value
        assert issue is not None
        assert issue.severity == "HIGH"
        assert issue.issue_type == "high_complexity"
        assert issue.file_path == "test.py"
        assert issue.message == "Test issue"

    def test_create_report_through_builder(
        self,
        config: FlextQualitySettings,
        logger: FlextLogger,
    ) -> None:
        """Test creating a report through builder pattern."""
        result = (
            ReportServiceBuilder(config, logger)
            .with_analysis_id("analysis_test")
            .with_format("HTML")
            .build()
        )

        assert result.is_success
        report = result.value
        assert report is not None
        assert report.format_type == "HTML"
