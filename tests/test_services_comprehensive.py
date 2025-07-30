"""Comprehensive functional tests for application services to achieve 100% coverage.

Real functional tests covering all service functionality following flext-core patterns.
Tests all success paths, error handling, and business logic for production-grade coverage.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from flext_core import FlextResult

from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.domain.entities import (
    AnalysisStatus,
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
)
from tests.conftest import (
    assert_result_failure_with_error,
    assert_result_success_with_data,
)


class TestQualityProjectServiceComprehensive:
    """Comprehensive functional tests for QualityProjectService."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create service instance."""
        return QualityProjectService()

    async def test_create_project_success_minimal_params(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test successful project creation with minimal parameters."""
        result = await service.create_project(
            name="minimal_project",
            project_path=secure_temp_dir,
        )

        project = assert_result_success_with_data(result)

        assert isinstance(project, QualityProject)
        assert project.project_path == secure_temp_dir
        assert project.language == "python"  # default
        assert project.repository_url is None
        assert project.id is not None

    async def test_create_project_success_full_params(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test successful project creation with all parameters."""
        result = await service.create_project(
            name="full_project",
            project_path=secure_temp_dir,
            repository_url="https://github.com/test/repo",
            language="go",
        )

        project = assert_result_success_with_data(result)

        assert isinstance(project, QualityProject)
        assert project.project_path == secure_temp_dir
        assert project.language == "go"
        assert project.repository_url == "https://github.com/test/repo"

    async def test_get_project_success(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test successful project retrieval."""
        # First create a project
        create_result = await service.create_project(
            name="test_project",
            project_path=secure_temp_dir,
        )
        created_project = assert_result_success_with_data(create_result)

        # Then retrieve it
        result = await service.get_project(created_project.id)

        project = assert_result_success_with_data(result)
        assert project.id == created_project.id
        assert project.project_path == secure_temp_dir

    async def test_get_project_not_found(self, service: QualityProjectService) -> None:
        """Test get_project with non-existent ID."""
        result = await service.get_project("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error

    async def test_list_projects_empty(self, service: QualityProjectService) -> None:
        """Test list_projects when no projects exist."""
        result = await service.list_projects()

        projects = assert_result_success_with_data(result)
        assert isinstance(projects, list)
        assert len(projects) == 0

    async def test_list_projects_with_data(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test list_projects with existing projects."""
        # Create multiple projects
        await service.create_project("project1", secure_temp_dir)
        await service.create_project("project2", secure_temp_dir)

        result = await service.list_projects()

        projects = assert_result_success_with_data(result)
        assert isinstance(projects, list)
        assert len(projects) == 2

        paths = [p.project_path for p in projects]
        assert secure_temp_dir in paths

    async def test_update_project_success(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test successful project update."""
        # Create a project
        create_result = await service.create_project("original_name", secure_temp_dir)
        project = assert_result_success_with_data(create_result)

        # Update it
        updates = {
            "language": "javascript",
        }
        result = await service.update_project(project.id, updates)

        updated_project = assert_result_success_with_data(result)
        assert updated_project.language == "javascript"
        assert updated_project.id == project.id  # ID should remain the same

    async def test_update_project_not_found(self, service: QualityProjectService) -> None:
        """Test update_project with non-existent ID."""
        result = await service.update_project("non-existent-id", {"language": "new_language"})

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error

    async def test_delete_project_success(self, service: QualityProjectService, secure_temp_dir: str) -> None:
        """Test successful project deletion."""
        # Create a project
        create_result = await service.create_project("to_delete", secure_temp_dir)
        project = assert_result_success_with_data(create_result)

        # Delete it
        result = await service.delete_project(project.id)

        assert_result_success_with_data(result)

        # Verify it's gone
        get_result = await service.get_project(project.id)
        assert get_result.is_failure

    async def test_delete_project_not_found(self, service: QualityProjectService) -> None:
        """Test delete_project with non-existent ID."""
        result = await service.delete_project("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error


class TestQualityAnalysisServiceComprehensive:
    """Comprehensive functional tests for QualityAnalysisService."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create service instance."""
        return QualityAnalysisService()

    async def test_create_analysis_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis creation."""
        project_id = str(uuid.uuid4())

        result = await service.create_analysis(project_id=project_id)

        analysis = assert_result_success_with_data(result)

        assert isinstance(analysis, QualityAnalysis)
        assert analysis.project_id == project_id
        assert analysis.status == AnalysisStatus.QUEUED
        assert analysis.id is not None

    async def test_get_analysis_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis retrieval."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Retrieve it
        result = await service.get_analysis(analysis.id)

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == analysis.id
        assert retrieved.project_id == project_id

    async def test_get_analysis_not_found(self, service: QualityAnalysisService) -> None:
        """Test get_analysis with non-existent ID."""
        result = await service.get_analysis("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Analysis not found" in error

    async def test_list_analyses_success(self, service: QualityAnalysisService) -> None:
        """Test successful analyses listing."""
        project_id = str(uuid.uuid4())

        # Create multiple analyses
        await service.create_analysis(project_id=project_id)
        await service.create_analysis(project_id=project_id)

        result = await service.list_analyses(project_id)

        analyses = assert_result_success_with_data(result)
        assert isinstance(analyses, list)
        assert len(analyses) == 2

        # All should belong to the same project
        for analysis in analyses:
            assert analysis.project_id == project_id

    async def test_update_metrics_success(self, service: QualityAnalysisService) -> None:
        """Test successful metrics update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update metrics
        result = await service.update_metrics(
            analysis_id=analysis.id,
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        updated = assert_result_success_with_data(result)
        assert updated.total_files == 10
        assert updated.total_lines == 1000
        assert updated.code_lines == 800
        assert updated.comment_lines == 100
        assert updated.blank_lines == 100

    async def test_update_metrics_not_found(self, service: QualityAnalysisService) -> None:
        """Test update_metrics with non-existent analysis."""
        result = await service.update_metrics(
            analysis_id="non-existent",
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        error = assert_result_failure_with_error(result)
        assert "Analysis not found" in error

    async def test_update_scores_success(self, service: QualityAnalysisService) -> None:
        """Test successful scores update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update scores
        result = await service.update_scores(
            analysis_id=analysis.id,
            coverage_score=95.0,
            complexity_score=88.0,
            duplication_score=92.0,
            security_score=100.0,
            maintainability_score=85.0,
        )

        updated = assert_result_success_with_data(result)
        assert updated.coverage_score == 95.0
        assert updated.complexity_score == 88.0
        assert updated.duplication_score == 92.0
        assert updated.security_score == 100.0
        assert updated.maintainability_score == 85.0

    async def test_update_issue_counts_success(self, service: QualityAnalysisService) -> None:
        """Test successful issue counts update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update issue counts
        result = await service.update_issue_counts(
            analysis_id=analysis.id,
            critical=2,
            high=5,
            medium=10,
            low=15,
        )

        updated = assert_result_success_with_data(result)
        assert updated.critical_issues == 2
        assert updated.high_issues == 5
        assert updated.medium_issues == 10
        assert updated.low_issues == 15

    async def test_complete_analysis_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis completion."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Complete it
        result = await service.complete_analysis(analysis.id)

        completed = assert_result_success_with_data(result)
        assert completed.status == AnalysisStatus.COMPLETED
        assert completed.completed_at is not None

    async def test_fail_analysis_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis failure marking."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = await service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Mark as failed
        error_message = "Analysis failed due to timeout"
        result = await service.fail_analysis(analysis.id, error_message)

        failed = assert_result_success_with_data(result)
        assert failed.status == AnalysisStatus.FAILED
        assert failed.error_message == error_message
        assert failed.completed_at is not None


class TestQualityIssueServiceComprehensive:
    """Comprehensive functional tests for QualityIssueService."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create service instance."""
        return QualityIssueService()

    async def test_create_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue creation."""
        analysis_id = str(uuid.uuid4())

        result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="security",
            severity="high",
            rule_id="S100",
            file_path="src/test.py",
            line_number=42,
            column_number=10,
            message="Potential security vulnerability",
            description="Detailed description of the issue",
        )

        issue = assert_result_success_with_data(result)

        assert isinstance(issue, QualityIssue)
        assert issue.analysis_id == analysis_id
        assert issue.issue_type == "security"
        assert issue.severity == "high"
        assert issue.rule_id == "S100"
        assert issue.file_path == "src/test.py"
        assert issue.line_number == 42
        assert issue.column_number == 10
        assert issue.message == "Potential security vulnerability"
        assert issue.description == "Detailed description of the issue"
        assert not issue.is_suppressed
        assert issue.id is not None

    async def test_create_issue_minimal_params(self, service: QualityIssueService) -> None:
        """Test issue creation with minimal parameters."""
        analysis_id = str(uuid.uuid4())

        result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="style",
            severity="low",
            rule_id="E302",
            file_path="src/style.py",
            message="Expected 2 blank lines",
        )

        issue = assert_result_success_with_data(result)

        assert issue.analysis_id == analysis_id
        assert issue.issue_type == "style"
        assert issue.severity == "low"
        assert issue.line_number is None  # Optional parameter
        assert issue.column_number is None  # Optional parameter
        assert issue.description is None  # Optional parameter

    async def test_get_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue retrieval."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="quality",
            severity="medium",
            rule_id="Q100",
            file_path="src/quality.py",
            message="Quality issue detected",
        )
        issue = assert_result_success_with_data(create_result)

        # Retrieve it
        result = await service.get_issue(issue.id)

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == issue.id
        assert retrieved.analysis_id == analysis_id

    async def test_list_issues_by_analysis(self, service: QualityIssueService) -> None:
        """Test listing issues by analysis ID."""
        analysis_id = str(uuid.uuid4())

        # Create multiple issues
        await service.create_issue(
            analysis_id=analysis_id,
            issue_type="security",
            severity="high",
            rule_id="S1",
            file_path="file1.py",
            message="Issue 1",
        )
        await service.create_issue(
            analysis_id=analysis_id,
            issue_type="complexity",
            severity="medium",
            rule_id="C1",
            file_path="file2.py",
            message="Issue 2",
        )

        result = await service.list_issues(analysis_id)

        issues = assert_result_success_with_data(result)
        assert isinstance(issues, list)
        assert len(issues) == 2

        # All should belong to the same analysis
        for issue in issues:
            assert issue.analysis_id == analysis_id

    async def test_mark_fixed_success(self, service: QualityIssueService) -> None:
        """Test successful issue marking as fixed."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="bug",
            severity="high",
            rule_id="B100",
            file_path="src/bug.py",
            message="Bug detected",
        )
        issue = assert_result_success_with_data(create_result)

        # Mark as fixed
        result = await service.mark_fixed(issue.id)

        fixed_issue = assert_result_success_with_data(result)
        assert fixed_issue.is_fixed

    async def test_suppress_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue suppression."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="false_positive",
            severity="low",
            rule_id="FP100",
            file_path="src/fp.py",
            message="False positive",
        )
        issue = assert_result_success_with_data(create_result)

        # Suppress it
        reason = "This is a false positive"
        result = await service.suppress_issue(issue.id, reason)

        suppressed = assert_result_success_with_data(result)
        assert suppressed.is_suppressed
        assert suppressed.suppression_reason == reason

    async def test_unsuppress_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue unsuppression."""
        # Create and suppress an issue
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_issue(
            analysis_id=analysis_id,
            issue_type="review",
            severity="medium",
            rule_id="R100",
            file_path="src/review.py",
            message="Needs review",
        )
        issue = assert_result_success_with_data(create_result)

        await service.suppress_issue(issue.id, "Initially suppressed")

        # Unsuppress it
        result = await service.unsuppress_issue(issue.id)

        unsuppressed = assert_result_success_with_data(result)
        assert not unsuppressed.is_suppressed
        assert unsuppressed.suppression_reason is None


class TestQualityReportServiceComprehensive:
    """Comprehensive functional tests for QualityReportService."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create service instance."""
        return QualityReportService()

    async def test_create_report_success(self, service: QualityReportService) -> None:
        """Test successful report creation."""
        analysis_id = str(uuid.uuid4())

        result = await service.create_report(
            analysis_id=analysis_id,
            report_type="html",
            report_type="html",
        )

        report = assert_result_success_with_data(result)

        assert isinstance(report, QualityReport)
        assert report.analysis_id == analysis_id
        assert report.report_type == "html"
        assert report.report_type == "html"
        assert report.id is not None

    async def test_create_report_minimal_params(self, service: QualityReportService) -> None:
        """Test report creation with minimal parameters."""
        analysis_id = str(uuid.uuid4())

        result = await service.create_report(
            analysis_id=analysis_id,
            report_type="json",
        )

        report = assert_result_success_with_data(result)
        assert report.analysis_id == analysis_id
        assert report.report_type == "json"
        assert report.report_type == "json"

    async def test_get_report_success(self, service: QualityReportService) -> None:
        """Test successful report retrieval."""
        # Create a report
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_report(
            analysis_id=analysis_id,
            report_type="pdf",
            report_type="pdf",
        )
        report = assert_result_success_with_data(create_result)

        # Retrieve it
        result = await service.get_report(report.id)

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == report.id
        assert retrieved.analysis_id == analysis_id
        assert retrieved.report_type == "pdf"

    async def test_list_reports_by_analysis(self, service: QualityReportService) -> None:
        """Test listing reports by analysis ID."""
        analysis_id = str(uuid.uuid4())

        # Create multiple reports
        await service.create_report(analysis_id=analysis_id, report_type="html")
        await service.create_report(analysis_id=analysis_id, report_type="json")
        await service.create_report(analysis_id=analysis_id, report_type="pdf")

        result = await service.list_reports(analysis_id)

        reports = assert_result_success_with_data(result)
        assert isinstance(reports, list)
        assert len(reports) == 3

        # All should belong to the same analysis
        for report in reports:
            assert report.analysis_id == analysis_id

        # Different types should be present
        types = {r.report_type for r in reports}
        assert types == {"html", "json", "pdf"}

    async def test_delete_report_success(self, service: QualityReportService) -> None:
        """Test successful report deletion."""
        # Create a report
        analysis_id = str(uuid.uuid4())
        create_result = await service.create_report(
            analysis_id=analysis_id,
            report_type="temp",
            report_type="temp",
        )
        report = assert_result_success_with_data(create_result)

        # Delete it
        result = await service.delete_report(report.id)

        assert_result_success_with_data(result)

        # Verify it's gone
        get_result = await service.get_report(report.id)
        assert get_result.is_failure

    async def test_delete_report_not_found(self, service: QualityReportService) -> None:
        """Test delete_report with non-existent ID."""
        result = await service.delete_report("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Report not found" in error
