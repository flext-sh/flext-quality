"""Test suite for application services."""

from __future__ import annotations

import pytest

from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.domain.entities import IssueSeverity, IssueType


class TestQualityProjectService:
    """Test QualityProjectService functionality."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create a QualityProjectService instance."""
        return QualityProjectService()

    async def test_create_project_success(self, service: QualityProjectService) -> None:
        """Test successful project creation."""
        result = await service.create_project(
            name="test_project",
            project_path="/tmp/test",
            repository_url="https://github.com/test/repo",
            language="python",
        )

        assert result.is_success
        assert result.data is not None
        assert result.data.project_path == "/tmp/test"
        assert result.data.repository_url == "https://github.com/test/repo"
        assert result.data.language == "python"

    async def test_get_project_success(self, service: QualityProjectService) -> None:
        """Test getting an existing project."""
        # First create a project
        create_result = await service.create_project(
            name="test_project",
            project_path="/tmp/test",
        )
        assert create_result.is_success
        project_id = create_result.data.id

        # Then get it
        result = await service.get_project(project_id)
        assert result.is_success
        assert result.data is not None
        assert result.data.id == project_id

    async def test_get_project_not_found(self, service: QualityProjectService) -> None:
        """Test getting a non-existent project."""
        result = await service.get_project("non-existent-id")
        assert result.is_success
        assert result.data is None

    async def test_list_projects(self, service: QualityProjectService) -> None:
        """Test listing projects."""
        # Create a few projects
        await service.create_project("test1", "/tmp/test1")
        await service.create_project("test2", "/tmp/test2")

        result = await service.list_projects()
        assert result.is_success
        assert len(result.data) == 2

    async def test_update_project(self, service: QualityProjectService) -> None:
        """Test updating a project."""
        # Create a project
        create_result = await service.create_project("test", "/tmp/test")
        assert create_result.is_success
        project_id = create_result.data.id

        # Update it
        updates = {"language": "go", "min_coverage": 80.0}
        result = await service.update_project(project_id, updates)
        assert result.is_success
        assert result.data.language == "go"

    async def test_update_project_not_found(self, service: QualityProjectService) -> None:
        """Test updating a non-existent project."""
        result = await service.update_project("non-existent", {})
        assert result.is_failure
        assert "not found" in result.error.lower()

    async def test_delete_project(self, service: QualityProjectService) -> None:
        """Test deleting a project."""
        # Create a project
        create_result = await service.create_project("test", "/tmp/test")
        assert create_result.is_success
        project_id = create_result.data.id

        # Delete it
        result = await service.delete_project(project_id)
        assert result.is_success
        assert result.data is True

    async def test_delete_project_not_found(self, service: QualityProjectService) -> None:
        """Test deleting a non-existent project."""
        result = await service.delete_project("non-existent")
        assert result.is_failure
        assert "not found" in result.error.lower()


class TestQualityAnalysisService:
    """Test QualityAnalysisService functionality."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create a QualityAnalysisService instance."""
        return QualityAnalysisService()

    async def test_create_analysis(self, service: QualityAnalysisService) -> None:
        """Test creating an analysis."""
        result = await service.create_analysis(
            project_id="test-project-id",
            commit_hash="abc123",
            branch="main",
        )
        assert result.is_success

    async def test_update_metrics(self, service: QualityAnalysisService) -> None:
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

    async def test_update_scores(self, service: QualityAnalysisService) -> None:
        """Test updating analysis scores."""
        result = await service.update_scores(
            analysis_id="test-analysis-id",
            coverage_score=95.0,
            complexity_score=90.0,
            duplication_score=85.0,
            security_score=100.0,
            maintainability_score=88.0,
        )
        assert result.is_failure  # Analysis not found

    async def test_complete_analysis(self, service: QualityAnalysisService) -> None:
        """Test completing an analysis."""
        result = await service.complete_analysis("test-analysis-id")
        assert result.is_failure  # Analysis not found

    async def test_fail_analysis(self, service: QualityAnalysisService) -> None:
        """Test failing an analysis."""
        result = await service.fail_analysis("test-analysis-id", "Test error")
        assert result.is_failure  # Analysis not found


class TestQualityIssueService:
    """Test QualityIssueService functionality."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create a QualityIssueService instance."""
        return QualityIssueService()

    async def test_create_issue(self, service: QualityIssueService) -> None:
        """Test creating an issue."""
        result = await service.create_issue(
            analysis_id="test-analysis-id",
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
            line_number=10,
        )
        assert result.is_success
        assert result.data.issue_type == IssueType.STYLE
        assert result.data.severity == IssueSeverity.MEDIUM

    async def test_get_issue(self, service: QualityIssueService) -> None:
        """Test getting an issue."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.is_success
        issue_id = create_result.data.id

        # Get the issue
        result = await service.get_issue(issue_id)
        assert result.is_success
        assert result.data.id == issue_id

    async def test_mark_fixed(self, service: QualityIssueService) -> None:
        """Test marking an issue as fixed."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.is_success
        issue_id = create_result.data.id

        # Mark it as fixed
        result = await service.mark_fixed(issue_id)
        assert result.is_success
        assert result.data.is_fixed is True

    async def test_suppress_issue(self, service: QualityIssueService) -> None:
        """Test suppressing an issue."""
        # Create an issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis-id",
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.is_success
        issue_id = create_result.data.id

        # Suppress it
        reason = "False positive"
        result = await service.suppress_issue(issue_id, reason)
        assert result.is_success
        assert result.data.is_suppressed is True
        assert result.data.suppression_reason == reason


class TestQualityReportService:
    """Test QualityReportService functionality."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create a QualityReportService instance."""
        return QualityReportService()

    async def test_create_report(self, service: QualityReportService) -> None:
        """Test creating a report."""
        result = await service.create_report(
            analysis_id="test-analysis-id",
            report_type="html",
            report_format="detailed",
        )
        assert result.is_success
        assert result.data.report_type == "html"
        assert result.data.report_format == "detailed"

    async def test_get_report(self, service: QualityReportService) -> None:
        """Test getting a report."""
        # Create a report first
        create_result = await service.create_report(
            analysis_id="test-analysis-id",
            report_type="json",
        )
        assert create_result.is_success
        report_id = create_result.data.id

        # Get the report
        result = await service.get_report(report_id)
        assert result.is_success
        assert result.data.id == report_id
        assert result.data.access_count == 1  # Incremented on access

    async def test_delete_report(self, service: QualityReportService) -> None:
        """Test deleting a report."""
        # Create a report first
        create_result = await service.create_report(
            analysis_id="test-analysis-id",
            report_type="pdf",
        )
        assert create_result.is_success
        report_id = create_result.data.id

        # Delete it
        result = await service.delete_report(report_id)
        assert result.is_success
        assert result.data is True
