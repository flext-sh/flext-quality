"""Test suite for application services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_quality import (
    IssueSeverity,
    IssueType,
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)

from .conftest import (
    assert_result_failure_with_error,
    assert_result_success_with_data,
)


class TestQualityProjectService:
    """Test QualityProjectService functionality."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create a QualityProjectService instance."""
        return QualityProjectService()

    async def test_create_project_success(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project creation."""
        result = await service.create_project(
            name="test_project",
            project_path=secure_temp_dir,
            repository_url="https://github.com/test/repo",
            language="python",
        )

        assert result.success
        assert result.value is not None
        assert result.value.project_path == secure_temp_dir
        assert result.value.repository_url == "https://github.com/test/repo"
        assert result.value.language == "python"

    async def test_get_project_success(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test getting an existing project."""
        # First create a project
        create_result = await service.create_project(
            name="test_project",
            project_path=secure_temp_dir,
        )
        project_data = assert_result_success_with_data(create_result)
        project_id = project_data.id

        # Then get it
        result = await service.get_project(str(project_id))
        retrieved_data = assert_result_success_with_data(result)
        assert retrieved_data.id == project_id

    async def test_get_nonexistent_project(self, service: QualityProjectService) -> None:
        """Test getting a non-existent project."""
        result = await service.get_project("non-existent-id")
        error_msg = assert_result_failure_with_error(result)
        assert "not found" in error_msg.lower()

    async def test_list_projects(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test listing projects."""
        # Create a few projects
        await service.create_project("test1", f"{secure_temp_dir}/test1")
        await service.create_project("test2", f"{secure_temp_dir}/test2")

        result = await service.list_projects()
        projects_data = assert_result_success_with_data(result)
        assert len(projects_data) == 2

    async def test_update_project(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test updating a project."""
        # Create a project
        create_result = await service.create_project("test", secure_temp_dir)
        project_data = assert_result_success_with_data(create_result)
        project_id = project_data.id

        # Update it
        updates = {"language": "go", "min_coverage": 80.0}
        result = await service.update_project(str(project_id), updates)
        updated_data = assert_result_success_with_data(result)
        assert updated_data.language == "go"

    async def test_update_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test updating a non-existent project."""
        result = await service.update_project("non-existent", {})
        error_msg = assert_result_failure_with_error(result)
        assert "not found" in error_msg.lower()

    async def test_delete_project(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test deleting a project."""
        # Create a project
        create_result = await service.create_project("test", secure_temp_dir)
        project_data = assert_result_success_with_data(create_result)
        project_id = project_data.id

        # Delete it
        result = await service.delete_project(str(project_id))
        assert result.success
        assert result.value is True

    async def test_delete_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test deleting a non-existent project."""
        result = await service.delete_project("non-existent")
        error_msg = assert_result_failure_with_error(result)
        assert "not found" in error_msg.lower()


class TestQualityAnalysisService:
    """Test QualityAnalysisService functionality."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create a QualityAnalysisService instance."""
        return QualityAnalysisService()

    async def test_create_analysis_basic(self, service: QualityAnalysisService) -> None:
        """Test creating an analysis."""
        result = await service.create_analysis(
            project_id="test-project-id",
            commit_hash="abc123",
            branch="main",
        )
        assert result.success

    async def test_update_analysis_metrics(self, service: QualityAnalysisService) -> None:
        """Test updating analysis metrics."""
        result = await service.update_metrics(
            analysis_id="test-analysis-id",
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )
        assert result.is_failure  # Analysis not found

    async def test_update_analysis_scores(self, service: QualityAnalysisService) -> None:
        """Test updating analysis scores."""
        result = await service.update_scores(
            analysis_id="test-analysis-id",
            coverage_score=95.0,
            complexity_score=90.0,
            maintainability_score=88.0,
            security_score=100.0,
            overall_score=90.5,
        )
        assert result.is_failure  # Analysis not found

    async def test_complete_analysis_basic(self, service: QualityAnalysisService) -> None:
        """Test completing an analysis."""
        result = await service.complete_analysis("test-analysis-id")
        assert result.is_failure  # Analysis not found

    async def test_fail_analysis_basic(self, service: QualityAnalysisService) -> None:
        """Test failing an analysis."""
        result = await service.fail_analysis("test-analysis-id", "Test error")
        assert result.is_failure  # Analysis not found


class TestQualityIssueService:
    """Test QualityIssueService functionality."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create a QualityIssueService instance."""
        return QualityIssueService()

    async def test_create_issue_basic(self, service: QualityIssueService) -> None:
        """Test creating an issue."""
        result = await service.create_issue(
            analysis_id="test-analysis-id",
            file_path="test.py",
            line_number=10,
            column_number=None,
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Missing blank line",
            rule="E302",
        )
        issue_data = assert_result_success_with_data(result)
        assert issue_data.issue_type == IssueType.STYLE_VIOLATION
        assert issue_data.severity == IssueSeverity.MEDIUM

    async def test_get_issue_basic(self, service: QualityIssueService) -> None:
        """Test getting an issue."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            file_path="test.py",
            line_number=10,
            column_number=None,
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Missing blank line",
            rule="E302",
        )
        created_issue = assert_result_success_with_data(create_result)
        issue_id = created_issue.id

        # Get the issue
        result = await service.get_issue(str(issue_id))
        retrieved_issue = assert_result_success_with_data(result)
        assert retrieved_issue.id == issue_id

    async def test_mark_issue_fixed(self, service: QualityIssueService) -> None:
        """Test marking an issue as fixed."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            file_path="test.py",
            line_number=10,
            column_number=None,
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Missing blank line",
            rule="E302",
        )
        created_issue = assert_result_success_with_data(create_result)
        issue_id = created_issue.id

        # Mark it as fixed
        result = await service.mark_fixed(str(issue_id))
        fixed_issue = assert_result_success_with_data(result)
        assert fixed_issue.is_fixed is True

    async def test_suppress_issue_basic(self, service: QualityIssueService) -> None:
        """Test suppressing an issue."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            file_path="test.py",
            line_number=10,
            column_number=None,
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Missing blank line",
            rule="E302",
        )
        created_issue = assert_result_success_with_data(create_result)
        issue_id = created_issue.id

        # Suppress it
        reason = "False positive"
        result = await service.suppress_issue(str(issue_id), reason)
        suppressed_issue = assert_result_success_with_data(result)
        assert suppressed_issue.is_suppressed is True
        assert suppressed_issue.suppression_reason == reason


class TestQualityReportService:
    """Test QualityReportService functionality."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create a QualityReportService instance."""
        return QualityReportService()

    async def test_create_report_basic(self, service: QualityReportService) -> None:
        """Test creating a report."""
        result = await service.create_report(
            analysis_id="test-analysis-id",
            format_type="html",
            content="<html>Test Report</html>",
        )
        report_data = assert_result_success_with_data(result)
        assert (
            report_data.report_type == "html"
        )  # Entity uses report_type, not format_type
        assert hasattr(report_data, "analysis_id")

    async def test_get_report_basic(self, service: QualityReportService) -> None:
        """Test getting a report."""
        # Create a report first
        create_result = await service.create_report(
            analysis_id="test-analysis-id",
            report_type="json",
        )
        created_report = assert_result_success_with_data(create_result)
        report_id = created_report.id

        # Get the report
        result = await service.get_report(str(report_id))
        retrieved_report = assert_result_success_with_data(result)
        assert retrieved_report.id == report_id
        assert retrieved_report.access_count == 1  # Incremented on access

    async def test_delete_report_basic(self, service: QualityReportService) -> None:
        """Test deleting a report."""
        # Create a report first
        create_result = await service.create_report(
            analysis_id="test-analysis-id",
            report_type="pdf",
        )
        created_report = assert_result_success_with_data(create_result)
        report_id = created_report.id

        # Delete it
        result = await service.delete_report(str(report_id))
        assert result.success
        assert result.value is True
