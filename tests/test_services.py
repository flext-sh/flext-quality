"""Comprehensive functional tests for application services to achieve 100% coverage.

Real functional tests covering all service functionality following flext-core patterns.
Tests all success paths, error handling, and business logic for production-grade coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid

import pytest

from flext_core import FlextTypes
from flext_quality import (
    AnalysisStatus,
    IssueSeverity,
    IssueType,
    QualityAnalysis,
    QualityAnalysisService,
    QualityIssue,
    QualityIssueService,
    QualityProject,
    QualityProjectService,
    QualityReport,
    QualityReportService,
)

from .conftest import (
    assert_result_failure_with_error,
    assert_result_success_with_data,
)


class TestQualityProjectServiceComprehensive:
    """Comprehensive functional tests for QualityProjectService."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create service instance."""
        return QualityProjectService()

    def test_create_project_success_minimal_params(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project creation with minimal parameters."""
        result = service.create_project(
            name="minimal_project",
            project_path=secure_temp_dir,
        )

        project = assert_result_success_with_data(result)

        assert isinstance(project, QualityProject)
        assert project.project_path == secure_temp_dir
        assert project.language == "python"  # default
        assert project.repository_url is None
        assert project.id is not None

    def test_create_project_success_full_params(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project creation with all parameters."""
        result = service.create_project(
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

    def test_get_project_success(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project retrieval."""
        # First create a project
        create_result = service.create_project(
            name="test_project",
            project_path=secure_temp_dir,
        )
        created_project = assert_result_success_with_data(create_result)

        # Then retrieve it
        result = service.get_project(str(created_project.id))

        project = assert_result_success_with_data(result)
        assert project.id == created_project.id
        assert project.project_path == secure_temp_dir

    def test_project_get_not_found(self, service: QualityProjectService) -> None:
        """Test get_project with non-existent ID."""
        result = service.get_project("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error

    def test_project_list_empty(self, service: QualityProjectService) -> None:
        """Test list_projects when no projects exist."""
        result = service.list_projects()

        projects = assert_result_success_with_data(result)
        assert isinstance(projects, list)
        assert len(projects) == 0

    def test_list_projects_with_data(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test list_projects with existing projects."""
        # Create multiple projects
        service.create_project("project1", secure_temp_dir)
        service.create_project("project2", secure_temp_dir)

        result = service.list_projects()

        projects = assert_result_success_with_data(result)
        assert isinstance(projects, list)
        assert len(projects) == 2

        paths = [p.project_path for p in projects]
        assert secure_temp_dir in paths

    def test_update_project_success(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project update."""
        # Create a project
        create_result = service.create_project("original_name", secure_temp_dir)
        project = assert_result_success_with_data(create_result)

        # Update it
        updates: FlextTypes.Dict = {
            "language": "javascript",
        }
        result = service.update_project(str(project.id), updates)

        updated_project = assert_result_success_with_data(result)
        assert updated_project.language == "javascript"
        assert updated_project.id == project.id  # ID should remain the same

    def test_update_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test update_project with non-existent ID."""
        result = service.update_project(
            "non-existent-id",
            {"language": "new_language"},
        )

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error

    def test_delete_project_success(
        self,
        service: QualityProjectService,
        secure_temp_dir: str,
    ) -> None:
        """Test successful project deletion."""
        # Create a project
        create_result = service.create_project("to_delete", secure_temp_dir)
        project = assert_result_success_with_data(create_result)

        # Delete it
        result = service.delete_project(str(project.id))

        assert_result_success_with_data(result)

        # Verify it's gone
        get_result = service.get_project(str(project.id))
        assert get_result.is_failure

    def test_delete_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test delete_project with non-existent ID."""
        result = service.delete_project("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Project not found" in error


class TestQualityAnalysisServiceComprehensive:
    """Comprehensive functional tests for QualityAnalysisService."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create service instance."""
        return QualityAnalysisService()

    def test_create_analyssuccess(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful analysis creation."""
        project_id = str(uuid.uuid4())

        result = service.create_analysis(project_id=project_id)

        analysis = assert_result_success_with_data(result)

        assert isinstance(analysis, QualityAnalysis)
        assert analysis.project_id == project_id
        assert analysis.status == AnalysisStatus.QUEUED
        assert analysis.id is not None

    def test_analysis_retrieval_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis retrieval."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Retrieve it
        result = service.get_analysis(str(analysis.id))

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == analysis.id
        assert retrieved.project_id == project_id

    def test_get_analysis_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test get_analysis with non-existent ID."""
        result = service.get_analysis("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Analysis not found" in error

    def test_analysis_listing_success(self, service: QualityAnalysisService) -> None:
        """Test successful analyses listing."""
        project_id = str(uuid.uuid4())

        # Create multiple analyses
        service.create_analysis(project_id=project_id)
        service.create_analysis(project_id=project_id)

        result = service.list_analyses(project_id)

        analyses = assert_result_success_with_data(result)
        assert isinstance(analyses, list)
        assert len(analyses) == 2

        # All should belong to the same project
        for analysis in analyses:
            assert analysis.project_id == project_id

    def test_update_metrics_success(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful metrics update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update metrics
        result = service.update_metrics(
            analysis_id=str(analysis.id),
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

    def test_update_metrics_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test update_metrics with non-existent analysis."""
        result = service.update_metrics(
            analysis_id="non-existent",
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        error = assert_result_failure_with_error(result)
        assert "Analysis not found" in error

    def test_analysis_scores_update_success(
        self, service: QualityAnalysisService
    ) -> None:
        """Test successful scores update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update scores
        result = service.update_scores(
            analysis_id=str(analysis.id),
            coverage_score=95.0,
            complexity_score=88.0,
            overall_score=92.0,
            security_score=100.0,
            maintainability_score=85.0,
        )

        updated = assert_result_success_with_data(result)
        assert updated.coverage_score == 95.0
        assert updated.complexity_score == 88.0
        assert updated.duplication_score == 92.0
        assert updated.security_score == 100.0
        assert updated.maintainability_score == 85.0

    def test_update_issue_counts_success(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful issue counts update."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Update issue counts
        result = service.update_issue_counts(
            analysis_id=str(analysis.id),
            total_issues=32,
            critical_issues=2,
            high_issues=5,
            medium_issues=10,
            low_issues=15,
        )

        updated = assert_result_success_with_data(result)
        assert updated.critical_issues == 2
        assert updated.high_issues == 5
        assert updated.medium_issues == 10
        assert updated.low_issues == 15

    def test_complete_analyssuccess(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful analysis completion."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Complete it
        result = service.complete_analysis(str(analysis.id))

        completed = assert_result_success_with_data(result)
        assert completed.status == AnalysisStatus.COMPLETED
        assert completed.completed_at is not None

    def test_analysis_failure_marking_success(
        self, service: QualityAnalysisService
    ) -> None:
        """Test successful analysis failure marking."""
        # Create an analysis
        project_id = str(uuid.uuid4())
        create_result = service.create_analysis(project_id=project_id)
        analysis = assert_result_success_with_data(create_result)

        # Mark as failed
        error_message = "Analysis failed due to timeout"
        result = service.fail_analysis(str(analysis.id), error_message)

        failed = assert_result_success_with_data(result)
        assert failed.status == AnalysisStatus.FAILED
        assert failed.completed_at is not None


class TestQualityIssueServiceComprehensive:
    """Comprehensive functional tests for QualityIssueService."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create service instance."""
        return QualityIssueService()

    def test_issue_creation_success(self, service: QualityIssueService) -> None:
        """Test successful issue creation."""
        analysis_id = str(uuid.uuid4())

        result = service.create_issue(
            analysis_id=analysis_id,
            file_path="src/test.py",
            line_number=42,
            column_number=10,
            severity=IssueSeverity.HIGH,
            issue_type=IssueType.SECURITY_VULNERABILITY,
            message="Potential security vulnerability",
            rule="S100",
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
        assert not issue.is_suppressed
        assert issue.id is not None

    def test_create_issue_minimal_params(
        self,
        service: QualityIssueService,
    ) -> None:
        """Test issue creation with minimal parameters."""
        analysis_id = str(uuid.uuid4())

        result = service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.STYLE_VIOLATION,
            severity=IssueSeverity.LOW,
            rule="E302",
            file_path="src/style.py",
            line_number=1,
            column_number=1,
            message="Expected 2 blank lines",
        )

        issue = assert_result_success_with_data(result)

        assert issue.analysis_id == analysis_id
        assert issue.issue_type == "style"
        assert issue.severity == "low"
        assert issue.line_number is None  # Optional parameter
        assert issue.column_number is None  # Optional parameter

    def test_issue_retrieval_success(self, service: QualityIssueService) -> None:
        """Test successful issue retrieval."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.HIGH_COMPLEXITY,
            severity=IssueSeverity.MEDIUM,
            rule="Q100",
            file_path="src/quality.py",
            line_number=1,
            column_number=1,
            message="Quality issue detected",
        )
        issue = assert_result_success_with_data(create_result)

        # Retrieve it
        result = service.get_issue(str(issue.id))

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == issue.id
        assert retrieved.analysis_id == analysis_id

    def test_issue_listing_by_analysis(self, service: QualityIssueService) -> None:
        """Test listing issues by analysis ID."""
        analysis_id = str(uuid.uuid4())

        # Create multiple issues
        service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.SECURITY_VULNERABILITY,
            severity=IssueSeverity.HIGH,
            rule="S1",
            file_path="file1.py",
            line_number=1,
            column_number=1,
            message="Issue 1",
        )
        service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.HIGH_COMPLEXITY,
            severity=IssueSeverity.MEDIUM,
            rule="C1",
            file_path="file2.py",
            line_number=1,
            column_number=1,
            message="Issue 2",
        )

        result = service.list_issues(analysis_id)

        issues = assert_result_success_with_data(result)
        assert isinstance(issues, list)
        assert len(issues) == 2

        # All should belong to the same analysis
        for issue in issues:
            assert issue.analysis_id == analysis_id

    def test_issue_mark_fixed_success(self, service: QualityIssueService) -> None:
        """Test successful issue marking as fixed."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.SYNTAX_ERROR,
            severity=IssueSeverity.HIGH,
            rule="B100",
            file_path="src/bug.py",
            line_number=1,
            column_number=1,
            message="Bug detected",
        )
        issue = assert_result_success_with_data(create_result)

        # Mark as fixed
        result = service.mark_fixed(str(issue.id))

        fixed_issue = assert_result_success_with_data(result)
        assert fixed_issue.is_fixed

    def test_issue_suppression_success(self, service: QualityIssueService) -> None:
        """Test successful issue suppression."""
        # Create an issue
        analysis_id = str(uuid.uuid4())
        create_result = service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.STYLE_VIOLATION,
            severity=IssueSeverity.LOW,
            rule="FP100",
            file_path="src/fp.py",
            line_number=1,
            column_number=1,
            message="False positive",
        )
        issue = assert_result_success_with_data(create_result)

        # Suppress it
        reason = "This is a false positive"
        result = service.suppress_issue(str(issue.id), reason)

        suppressed = assert_result_success_with_data(result)
        assert suppressed.is_suppressed
        assert suppressed.suppression_reason == reason

    def test_issue_unsuppression_success(self, service: QualityIssueService) -> None:
        """Test successful issue unsuppression."""
        # Create and suppress an issue
        analysis_id = str(uuid.uuid4())
        create_result = service.create_issue(
            analysis_id=analysis_id,
            issue_type=IssueType.DUPLICATE_CODE,
            severity=IssueSeverity.MEDIUM,
            rule="R100",
            file_path="src/review.py",
            line_number=1,
            column_number=1,
            message="Needs review",
        )
        issue = assert_result_success_with_data(create_result)

        service.suppress_issue(str(issue.id), "Initially suppressed")

        # Unsuppress it
        result = service.unsuppress_issue(str(issue.id))

        unsuppressed = assert_result_success_with_data(result)
        assert not unsuppressed.is_suppressed
        assert unsuppressed.suppression_reason is None


class TestQualityReportServiceComprehensive:
    """Comprehensive functional tests for QualityReportService."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create service instance."""
        return QualityReportService()

    def test_report_creation_success(self, service: QualityReportService) -> None:
        """Test successful report creation."""
        analysis_id = str(uuid.uuid4())

        result = service.create_report(
            analysis_id=analysis_id,
            format_type="html",
            content="<html>Test report</html>",
        )

        report = assert_result_success_with_data(result)

        assert isinstance(report, QualityReport)
        assert report.analysis_id == analysis_id
        assert report.report_type == "html"
        assert report.report_type == "html"
        assert report.id is not None

    def test_create_report_minimal_params(
        self,
        service: QualityReportService,
    ) -> None:
        """Test report creation with minimal parameters."""
        analysis_id = str(uuid.uuid4())

        result = service.create_report(
            analysis_id=analysis_id,
            format_type="json",
            content='{"test": "report"}',
        )

        report = assert_result_success_with_data(result)
        assert report.analysis_id == analysis_id
        assert report.report_type == "json"
        assert report.report_type == "json"

    def test_report_retrieval_success(self, service: QualityReportService) -> None:
        """Test successful report retrieval."""
        # Create a report
        analysis_id = str(uuid.uuid4())
        create_result = service.create_report(
            analysis_id=analysis_id,
            format_type="pdf",
            content="PDF content",
        )
        report = assert_result_success_with_data(create_result)

        # Retrieve it
        result = service.get_report(str(report.id))

        retrieved = assert_result_success_with_data(result)
        assert retrieved.id == report.id
        assert retrieved.analysis_id == analysis_id
        assert retrieved.report_type == "pdf"

    def test_list_reports_by_analysis(
        self,
        service: QualityReportService,
    ) -> None:
        """Test listing reports by analysis ID."""
        analysis_id = str(uuid.uuid4())

        # Create multiple reports
        service.create_report(
            analysis_id=analysis_id,
            format_type="html",
            content="<html>HTML Report</html>",
        )
        service.create_report(
            analysis_id=analysis_id,
            format_type="json",
            content='{"report": "1"}',
        )
        service.create_report(
            analysis_id=analysis_id,
            format_type="pdf",
            content="PDF report",
        )

        result = service.list_reports(analysis_id)

        reports = assert_result_success_with_data(result)
        assert isinstance(reports, list)
        assert len(reports) == 3

        # All should belong to the same analysis
        for report in reports:
            assert report.analysis_id == analysis_id

        # Different types should be present
        types = {r.report_type for r in reports}
        assert types == {"html", "json", "pdf"}

    def test_report_deletion_success(self, service: QualityReportService) -> None:
        """Test successful report deletion."""
        # Create a report
        analysis_id = str(uuid.uuid4())
        create_result = service.create_report(
            analysis_id=analysis_id,
            format_type="temp",
            content="Temporary report",
        )
        report = assert_result_success_with_data(create_result)

        # Delete it
        result = service.delete_report(str(report.id))

        assert_result_success_with_data(result)

        # Verify it's gone
        get_result = service.get_report(str(report.id))
        assert get_result.is_failure

    def test_report_deletion_not_found(self, service: QualityReportService) -> None:
        """Test delete_report with non-existent ID."""
        result = service.delete_report("non-existent-id")

        error = assert_result_failure_with_error(result)
        assert "Report not found" in error
