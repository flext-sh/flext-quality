"""Functional tests for application services to achieve 53% → 90%+ coverage.

Tests success paths and missing functionality in services.py.
Covers lines not tested by error scenarios.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile

import pytest

from flext_quality import (
    FlextAnalysisStatus,
    IssueSeverity,
    IssueType,
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)


class TestQualityProjectServiceFunctional:
    """Functional tests for QualityProjectService success paths."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create service instance."""
        return QualityProjectService()

    def test_project_creation_success(self, service: QualityProjectService) -> None:
        """Test successful project creation - covers lines 42-56."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.create_project(
                name="Test Project",
                project_path=temp_dir,
                language="python",
            )

            assert result.success
            project = result.value
            assert project.project_path == temp_dir
            assert project.language == "python"
            assert project.auto_analyze is True
            assert len(service._projects) == 1

    def test_project_retrieval_success(self, service: QualityProjectService) -> None:
        """Test successful project retrieval - covers lines 61-66."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = service.create_project(
                name="Test Project",
                project_path=temp_dir,
            )
            project_id = create_result.value.id

            # Get project
            result = service.get_project(str(project_id))

            assert result.success
            project = result.value
            assert project.id == project_id
            assert project.project_path == temp_dir

    def test_project_retrieval_not_found(self, service: QualityProjectService) -> None:
        """Test get project when not found - covers line 75."""
        result = service.get_project("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Project not found" in result.error

    def test_project_listing_success(self, service: QualityProjectService) -> None:
        """Test successful project listing - covers line 76."""
        # Create multiple projects
        with (
            tempfile.TemporaryDirectory() as temp_dir1,
            tempfile.TemporaryDirectory() as temp_dir2,
        ):
            service.create_project(
                name="Project 1",
                project_path=temp_dir1,
                language="python",
            )
            service.create_project(
                name="Project 2",
                project_path=temp_dir2,
                language="go",
            )

            result = service.list_projects()

            assert result.success
            projects = result.value
            assert len(projects) == 2
            assert projects[0].project_path == temp_dir1
            assert projects[1].project_path == temp_dir2

    def test_project_update_success(self, service: QualityProjectService) -> None:
        """Test successful project update - covers lines 82-95."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = service.create_project(
                name="Test Project",
                project_path=temp_dir,
            )
            project_id = create_result.value.id

            # Update project
            result = service.update_project(
                str(project_id),
                {"language": "go", "auto_analyze": False},
            )

            assert result.success
            updated_project = result.value
            assert updated_project.language == "go"
            assert updated_project.auto_analyze is False

    def test_update_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test update project when not found - covers line 89."""
        result = service.update_project("non-existent", {"language": "go"})

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Project not found" in result.error

    def test_project_deletion_success(self, service: QualityProjectService) -> None:
        """Test successful project deletion - covers lines 101-104."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = service.create_project(
                name="Test Project",
                project_path=temp_dir,
            )
            project_id = create_result.value.id

            # Delete project
            result = service.delete_project(str(project_id))

            assert result.success
            assert len(service._projects) == 0

    def test_delete_project_not_found(
        self,
        service: QualityProjectService,
    ) -> None:
        """Test delete project when not found - covers lines 102-103."""
        result = service.delete_project("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Project not found" in result.error


class TestQualityAnalysisServiceFunctional:
    """Functional tests for QualityAnalysisService success paths."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create service instance."""
        return QualityAnalysisService()

    def test_analysis_creation_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis creation - covers lines 121-141."""
        result = service.create_analysis(
            project_id="test-project-id",
            commit_hash="abc123",
            branch="main",
        )

        assert result.success
        analysis = result.value
        assert analysis.project_id == "test-project-id"
        assert analysis.commit_hash == "abc123"
        assert analysis.branch == "main"
        assert analysis.status == FlextAnalysisStatus.QUEUED
        assert len(service._analyses) == 1

    def test_analysis_retrieval_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis retrieval - covers lines 283-286."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Get analysis
        result = service.get_analysis(str(analysis_id))

        assert result.success
        analysis = result.value
        assert analysis.id == analysis_id
        assert analysis.project_id == "test-project"

    def test_get_analysis_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test get analysis when not found - covers line 284."""
        result = service.get_analysis("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Analysis not found" in result.error

    def test_update_metrics_success(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful metrics update - covers lines 147-171."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Update metrics
        result = service.update_metrics(
            analysis_id=str(analysis_id),
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        assert result.success
        updated_analysis = result.value
        assert updated_analysis.total_files == 10
        assert updated_analysis.total_lines == 1000
        assert updated_analysis.code_lines == 800
        assert updated_analysis.comment_lines == 100
        assert updated_analysis.blank_lines == 100

    def test_update_metrics_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test update metrics when analysis not found - covers line 149."""
        result = service.update_metrics(
            analysis_id="non-existent",
            total_files=5,
            total_lines=100,
            code_lines=80,
            comment_lines=10,
            blank_lines=10,
        )

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Analysis not found" in result.error

    def test_analysis_scores_update_success(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful scores update - covers lines 177-204."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Update scores
        result = service.update_scores(
            analysis_id=str(analysis_id),
            coverage_score=85.0,
            complexity_score=78.0,
            maintainability_score=80.0,
            security_score=95.0,
            overall_score=84.0,
        )

        assert result.success
        updated_analysis = result.value
        assert updated_analysis.coverage_score == 85.0
        assert updated_analysis.complexity_score == 78.0
        assert updated_analysis.duplication_score == 92.0
        assert updated_analysis.security_score == 95.0
        assert updated_analysis.maintainability_score == 80.0

    def test_update_scores_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test update scores when analysis not found - covers line 179."""
        result = service.update_scores(
            analysis_id="non-existent",
            coverage_score=85.0,
            complexity_score=78.0,
            maintainability_score=80.0,
            security_score=95.0,
            overall_score=84.0,
        )

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Analysis not found" in result.error

    def test_update_issue_counts_success(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful issue counts update - covers lines 212-226."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Update issue counts
        result = service.update_issue_counts(
            analysis_id=str(analysis_id),
            total_issues=10,
            critical_issues=1,
            high_issues=2,
            medium_issues=3,
            low_issues=4,
        )

        assert result.success
        updated_analysis = result.value
        assert updated_analysis.critical_issues == 1
        assert updated_analysis.high_issues == 2
        assert updated_analysis.medium_issues == 3
        assert updated_analysis.low_issues == 4
        assert updated_analysis.total_issues == 10  # Sum of all issues

    def test_complete_analyssuccess(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test successful analysis completion - covers lines 246-253."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Complete analysis
        result = service.complete_analysis(str(analysis_id))

        assert result.success
        completed_analysis = result.value
        assert completed_analysis.status == FlextAnalysisStatus.COMPLETED
        assert completed_analysis.completed_at is not None
        assert completed_analysis.duration_seconds is not None

    def test_complete_analysis_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test complete analysis when not found - covers line 248."""
        result = service.complete_analysis("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Analysis not found" in result.error

    def test_analysis_failure_success(self, service: QualityAnalysisService) -> None:
        """Test successful analysis failure - covers lines 263-271."""
        # Create analysis first
        create_result = service.create_analysis("test-project")
        analysis_id = create_result.value.id

        # Fail analysis
        result = service.fail_analysis(str(analysis_id), "Test error message")

        assert result.success
        failed_analysis = result.value
        assert failed_analysis.status == FlextAnalysisStatus.FAILED
        assert failed_analysis.completed_at is not None

    def test_fail_analysis_not_found(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test fail analysis when not found - covers line 265."""
        result = service.fail_analysis("non-existent-id", "Error")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Analysis not found" in result.error

    def test_analyses_listing_success(self, service: QualityAnalysisService) -> None:
        """Test successful analyses listing - covers lines 290-299."""
        # Create multiple analyses
        service.create_analysis("project-1")
        service.create_analysis("project-1")
        service.create_analysis("project-2")

        # List analyses for project-1
        result = service.list_analyses("project-1")

        assert result.success
        analyses = result.value
        assert len(analyses) == 2
        for analysis in analyses:
            assert analysis.project_id == "project-1"

    def test_analyses_listing_empty_result(
        self,
        service: QualityAnalysisService,
    ) -> None:
        """Test list analyses when none exist - covers empty filter case."""
        result = service.list_analyses("non-existent-project")

        assert result.success
        analyses = result.value
        assert len(analyses) == 0


class TestQualityIssueServiceFunctional:
    """Functional tests for QualityIssueService success paths."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create service instance."""
        return QualityIssueService()

    def test_issue_creation_success(self, service: QualityIssueService) -> None:
        """Test successful issue creation - covers lines 319-345."""
        result = service.create_issue(
            analysis_id="test-analysis",
            file_path="src/auth.py",
            line_number=42,
            column_number=1,
            severity=IssueSeverity.HIGH,
            issue_type=IssueType.SECURITY_VULNERABILITY,
            message="Potential security vulnerability",
            rule="S001",
        )

        assert result.success
        issue = result.value
        assert issue.analysis_id == "test-analysis"
        assert issue.issue_type == IssueType.SECURITY_VULNERABILITY
        assert issue.severity == IssueSeverity.HIGH
        assert issue.rule_id == "S001"
        assert issue.file_path == "src/auth.py"
        assert issue.line_number == 42
        assert issue.message == "Potential security vulnerability"
        assert len(service._issues) == 1

    def test_issue_retrieval_success(self, service: QualityIssueService) -> None:
        """Test successful issue retrieval - covers lines 350-355."""
        # Create issue first
        create_result = service.create_issue(
            analysis_id="test-analysis",
            file_path="test.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.LOW,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Style issue",
            rule="E301",
        )
        issue_id = create_result.value.id

        # Get issue
        result = service.get_issue(str(issue_id))

        assert result.success
        issue = result.value
        assert issue.id == issue_id
        assert issue.issue_type == IssueType.STYLE_VIOLATION

    def test_issue_retrieval_not_found(self, service: QualityIssueService) -> None:
        """Test get issue when not found - covers line 352."""
        result = service.get_issue("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Issue not found" in result.error

    def test_issues_listing_success(self, service: QualityIssueService) -> None:
        """Test successful issues listing - covers lines 361-377."""
        # Create multiple issues
        service.create_issue(
            analysis_id="analysis-1",
            file_path="file1.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.HIGH,
            issue_type=IssueType.SECURITY_VULNERABILITY,
            message="Issue 1",
            rule="S001",
        )
        service.create_issue(
            analysis_id="analysis-1",
            file_path="file2.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.LOW,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Issue 2",
            rule="E301",
        )
        service.create_issue(
            analysis_id="analysis-2",
            file_path="file3.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.MEDIUM,
            issue_type=IssueType.HIGH_COMPLEXITY,
            message="Issue 3",
            rule="C001",
        )

        # List issues for analysis-1
        result = service.list_issues("analysis-1")

        assert result.success
        issues = result.value
        assert len(issues) == 2
        for issue in issues:
            assert issue.analysis_id == "analysis-1"

    def test_issues_listing_empty_result(self, service: QualityIssueService) -> None:
        """Test list issues when none exist - covers empty filter case."""
        result = service.list_issues("non-existent-analysis")

        assert result.success
        issues = result.value
        assert len(issues) == 0

    def test_issue_mark_fixed_success(self, service: QualityIssueService) -> None:
        """Test successful issue marking as fixed - covers lines 383-390."""
        # Create issue first
        create_result = service.create_issue(
            analysis_id="test-analysis",
            file_path="test.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.LOW,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Style issue",
            rule="E301",
        )
        issue_id = create_result.value.id

        # Mark as fixed
        result = service.mark_fixed(str(issue_id))

        assert result.success
        fixed_issue = result.value
        assert fixed_issue.is_fixed is True

    def test_issue_mark_fixed_not_found(self, service: QualityIssueService) -> None:
        """Test mark fixed when issue not found - covers line 385."""
        result = service.mark_fixed("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Issue not found" in result.error

    def test_issue_suppression_success(self, service: QualityIssueService) -> None:
        """Test successful issue suppression - covers lines 399-406."""
        # Create issue first
        create_result = service.create_issue(
            analysis_id="test-analysis",
            file_path="test.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.LOW,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Style issue",
            rule="E301",
        )
        issue_id = create_result.value.id

        # Suppress issue
        result = service.suppress_issue(str(issue_id), "False positive")

        assert result.success
        suppressed_issue = result.value
        assert suppressed_issue.is_suppressed is True
        assert suppressed_issue.suppression_reason == "False positive"

    def test_issue_suppression_not_found(self, service: QualityIssueService) -> None:
        """Test suppress issue when not found - covers line 401."""
        result = service.suppress_issue("non-existent-id", "Reason")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Issue not found" in result.error

    def test_issue_unsuppression_success(self, service: QualityIssueService) -> None:
        """Test successful issue unsuppression - covers lines 411-418."""
        # Create and suppress issue first
        create_result = service.create_issue(
            analysis_id="test-analysis",
            file_path="test.py",
            line_number=1,
            column_number=1,
            severity=IssueSeverity.LOW,
            issue_type=IssueType.STYLE_VIOLATION,
            message="Style issue",
            rule="E301",
        )
        issue_id = create_result.value.id
        service.suppress_issue(str(issue_id), "False positive")

        # Unsuppress issue
        result = service.unsuppress_issue(str(issue_id))

        assert result.success
        unsuppressed_issue = result.value
        assert unsuppressed_issue.is_suppressed is False
        assert unsuppressed_issue.suppression_reason is None

    def test_unsuppress_issue_not_found(
        self,
        service: QualityIssueService,
    ) -> None:
        """Test unsuppress issue when not found - covers line 413."""
        result = service.unsuppress_issue("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Issue not found" in result.error


class TestQualityReportServiceFunctional:
    """Functional tests for QualityReportService success paths."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create service instance."""
        return QualityReportService()

    def test_report_creation_success(self, service: QualityReportService) -> None:
        """Test successful report creation - covers lines 429-449."""
        result = service.create_report(
            analysis_id="test-analysis",
            format_type="html",
            content="<html>Test report content</html>",
        )

        assert result.success
        report = result.value
        assert report.analysis_id == "test-analysis"
        assert report.report_type == "html"
        assert report.report_format == "detailed"
        assert report.generated_at is not None
        assert len(service._reports) == 1

    def test_report_retrieval_success(self, service: QualityReportService) -> None:
        """Test successful report retrieval - covers lines 454-461."""
        # Create report first
        create_result = service.create_report(
            analysis_id="test-analysis",
            format_type="json",
            content='{"test": "content"}',
        )
        report_id = create_result.value.id

        # Get report
        result = service.get_report(str(report_id))

        assert result.success
        report = result.value
        assert report.id == report_id
        assert report.analysis_id == "test-analysis"

    def test_report_retrieval_not_found(self, service: QualityReportService) -> None:
        """Test get report when not found - covers line 456."""
        result = service.get_report("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Report not found" in result.error

    def test_reports_listing_success(self, service: QualityReportService) -> None:
        """Test successful reports listing - covers lines 466-473."""
        # Create multiple reports
        service.create_report(
            analysis_id="analysis-1",
            format_type="html",
            content="<html>Report 1</html>",
        )
        service.create_report(
            analysis_id="analysis-1",
            format_type="json",
            content='{"report": "1"}',
        )
        service.create_report(
            analysis_id="analysis-2",
            format_type="pdf",
            content="PDF content",
        )

        # List reports for analysis-1
        result = service.list_reports("analysis-1")

        assert result.success
        reports = result.value
        assert len(reports) == 2
        for report in reports:
            assert report.analysis_id == "analysis-1"

    def test_reports_listing_empty_result(self, service: QualityReportService) -> None:
        """Test list reports when none exist - covers empty filter case."""
        result = service.list_reports("non-existent-analysis")

        assert result.success
        reports = result.value
        assert len(reports) == 0

    def test_report_deletion_success(self, service: QualityReportService) -> None:
        """Test successful report deletion - covers lines 477-481."""
        # Create report first
        create_result = service.create_report(
            analysis_id="test-analysis",
            format_type="html",
            content="<html>Report to delete</html>",
        )
        report_id = create_result.value.id

        # Delete report
        result = service.delete_report(str(report_id))

        assert result.success
        assert len(service._reports) == 0

    def test_report_deletion_not_found(self, service: QualityReportService) -> None:
        """Test delete report when not found - covers line 479."""
        result = service.delete_report("non-existent-id")

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Report not found" in result.error


class TestServiceIntegration:
    """Integration tests across services."""

    def test_full_workflow_integration(self) -> None:
        """Test complete workflow across all services."""
        project_service = QualityProjectService()
        analysis_service = QualityAnalysisService()
        issue_service = QualityIssueService()
        report_service = QualityReportService()

        # 1. Create project
        with tempfile.TemporaryDirectory() as temp_dir:
            project_result = project_service.create_project(
                name="Integration Test",
                project_path=temp_dir,
            )
            assert project_result.success
            project = project_result.value

            # 2. Create analysis
            analysis_result = analysis_service.create_analysis(str(project.id))
            assert analysis_result.success
            analysis = analysis_result.value

            # 3. Update analysis metrics
            metrics_result = analysis_service.update_metrics(
                str(analysis.id),
                5,
                100,
                80,
                10,
                10,
            )
            assert metrics_result.success

            # 4. Create issues
            issue_result = issue_service.create_issue(
                analysis_id=str(analysis.id),
                file_path="auth.py",
                line_number=1,
                column_number=1,
                severity=IssueSeverity.HIGH,
                issue_type=IssueType.SECURITY_VULNERABILITY,
                message="Security issue",
                rule="S001",
            )
            assert issue_result.success

            # 5. Update issue counts
            counts_result = analysis_service.update_issue_counts(
                analysis_id=str(analysis.id),
                total_issues=1,
                critical_issues=0,
                high_issues=1,
                medium_issues=0,
                low_issues=0,
            )
            assert counts_result.success

            # 6. Complete analysis
            complete_result = analysis_service.complete_analysis(str(analysis.id))
            assert complete_result.success

            # 7. Create report
            report_result = report_service.create_report(
                analysis_id=str(analysis.id),
                format_type="html",
                content="<html>Integration test report</html>",
            )
            assert report_result.success

            # Verify final state
            final_project = project_service.get_project(str(project.id))
            final_analysis = analysis_service.get_analysis(str(analysis.id))
            final_issues = issue_service.list_issues(str(analysis.id))
            final_reports = report_service.list_reports(str(analysis.id))

            assert final_project.success
            assert final_analysis.success
            assert final_analysis.value.status == FlextAnalysisStatus.COMPLETED
            assert final_issues.success
            assert len(final_issues.value) == 1
            assert final_reports.success
            assert len(final_reports.value) == 1
