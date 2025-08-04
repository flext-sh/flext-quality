"""Functional tests for application services to achieve 53% → 90%+ coverage.

Tests success paths and missing functionality in services.py.
Covers lines not tested by error scenarios.
"""

from __future__ import annotations

import tempfile

import pytest

from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.domain.entities import AnalysisStatus, IssueSeverity, IssueType


class TestQualityProjectServiceFunctional:
    """Functional tests for QualityProjectService success paths."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create service instance."""
        return QualityProjectService()

    async def test_create_project_success(self, service: QualityProjectService) -> None:
        """Test successful project creation - covers lines 42-56."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = await service.create_project(
                name="Test Project", project_path=temp_dir, language="python",
            )

            assert result.success
            project = result.data
            assert project.project_path == temp_dir
            assert project.language == "python"
            assert project.auto_analyze is True
            assert len(service._projects) == 1

    async def test_get_project_success(self, service: QualityProjectService) -> None:
        """Test successful project retrieval - covers lines 61-66."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = await service.create_project(
                name="Test Project", project_path=temp_dir,
            )
            project_id = create_result.data.id

            # Get project
            result = await service.get_project(project_id)

            assert result.success
            project = result.data
            assert project.id == project_id
            assert project.project_path == temp_dir

    async def test_get_project_not_found(self, service: QualityProjectService) -> None:
        """Test get project when not found - covers line 75."""
        result = await service.get_project("non-existent-id")

        assert result.is_failure
        assert "Project not found" in result.error

    async def test_list_projects_success(self, service: QualityProjectService) -> None:
        """Test successful project listing - covers line 76."""
        # Create multiple projects
        with (
            tempfile.TemporaryDirectory() as temp_dir1,
            tempfile.TemporaryDirectory() as temp_dir2,
        ):
            await service.create_project(
                name="Project 1", project_path=temp_dir1, language="python",
            )
            await service.create_project(
                name="Project 2", project_path=temp_dir2, language="go",
            )

            result = await service.list_projects()

            assert result.success
            projects = result.data
            assert len(projects) == 2
            assert projects[0].project_path == temp_dir1
            assert projects[1].project_path == temp_dir2

    async def test_update_project_success(self, service: QualityProjectService) -> None:
        """Test successful project update - covers lines 82-95."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = await service.create_project(
                name="Test Project", project_path=temp_dir,
            )
            project_id = create_result.data.id

            # Update project
            result = await service.update_project(
                project_id, {"language": "go", "auto_analyze": False},
            )

            assert result.success
            updated_project = result.data
            assert updated_project.language == "go"
            assert updated_project.auto_analyze is False

    async def test_update_project_not_found(
        self, service: QualityProjectService,
    ) -> None:
        """Test update project when not found - covers line 89."""
        result = await service.update_project("non-existent", {"language": "go"})

        assert result.is_failure
        assert "Project not found" in result.error

    async def test_delete_project_success(self, service: QualityProjectService) -> None:
        """Test successful project deletion - covers lines 101-104."""
        # Create project first
        with tempfile.TemporaryDirectory() as temp_dir:
            create_result = await service.create_project(
                name="Test Project", project_path=temp_dir,
            )
            project_id = create_result.data.id

            # Delete project
            result = await service.delete_project(project_id)

            assert result.success
            assert len(service._projects) == 0

    async def test_delete_project_not_found(
        self, service: QualityProjectService,
    ) -> None:
        """Test delete project when not found - covers lines 102-103."""
        result = await service.delete_project("non-existent-id")

        assert result.is_failure
        assert "Project not found" in result.error


class TestQualityAnalysisServiceFunctional:
    """Functional tests for QualityAnalysisService success paths."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create service instance."""
        return QualityAnalysisService()

    async def test_create_analyssuccess(self, service: QualityAnalysisService) -> None:
        """Test successful analysis creation - covers lines 121-141."""
        result = await service.create_analysis(
            project_id="test-project-id", commit_hash="abc123", branch="main",
        )

        assert result.success
        analysis = result.data
        assert analysis.project_id == "test-project-id"
        assert analysis.commit_hash == "abc123"
        assert analysis.branch == "main"
        assert analysis.status == AnalysisStatus.QUEUED
        assert len(service._analyses) == 1

    async def test_get_analyssuccess(self, service: QualityAnalysisService) -> None:
        """Test successful analysis retrieval - covers lines 283-286."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Get analysis
        result = await service.get_analysis(analysis_id)

        assert result.success
        analysis = result.data
        assert analysis.id == analysis_id
        assert analysis.project_id == "test-project"

    async def test_get_analysis_not_found(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test get analysis when not found - covers line 284."""
        result = await service.get_analysis("non-existent-id")

        assert result.is_failure
        assert "Analysis not found" in result.error

    async def test_update_metrics_success(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test successful metrics update - covers lines 147-171."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Update metrics
        result = await service.update_metrics(
            analysis_id=analysis_id,
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        assert result.success
        updated_analysis = result.data
        assert updated_analysis.total_files == 10
        assert updated_analysis.total_lines == 1000
        assert updated_analysis.code_lines == 800
        assert updated_analysis.comment_lines == 100
        assert updated_analysis.blank_lines == 100

    async def test_update_metrics_not_found(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test update metrics when analysis not found - covers line 149."""
        result = await service.update_metrics(
            analysis_id="non-existent",
            total_files=5,
            total_lines=100,
            code_lines=80,
            comment_lines=10,
            blank_lines=10,
        )

        assert result.is_failure
        assert "Analysis not found" in result.error

    async def test_update_scores_success(self, service: QualityAnalysisService) -> None:
        """Test successful scores update - covers lines 177-204."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Update scores
        result = await service.update_scores(
            analysis_id=analysis_id,
            coverage_score=85.0,
            complexity_score=78.0,
            duplication_score=92.0,
            security_score=95.0,
            maintainability_score=80.0,
        )

        assert result.success
        updated_analysis = result.data
        assert updated_analysis.coverage_score == 85.0
        assert updated_analysis.complexity_score == 78.0
        assert updated_analysis.duplication_score == 92.0
        assert updated_analysis.security_score == 95.0
        assert updated_analysis.maintainability_score == 80.0

    async def test_update_scores_not_found(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test update scores when analysis not found - covers line 179."""
        result = await service.update_scores(
            analysis_id="non-existent",
            coverage_score=85.0,
            complexity_score=78.0,
            duplication_score=92.0,
            security_score=95.0,
            maintainability_score=80.0,
        )

        assert result.is_failure
        assert "Analysis not found" in result.error

    async def test_update_issue_counts_success(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test successful issue counts update - covers lines 212-226."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Update issue counts
        result = await service.update_issue_counts(
            analysis_id=analysis_id, critical=1, high=2, medium=3, low=4,
        )

        assert result.success
        updated_analysis = result.data
        assert updated_analysis.critical_issues == 1
        assert updated_analysis.high_issues == 2
        assert updated_analysis.medium_issues == 3
        assert updated_analysis.low_issues == 4
        assert updated_analysis.total_issues == 10  # Sum of all issues

    async def test_complete_analyssuccess(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test successful analysis completion - covers lines 246-253."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Complete analysis
        result = await service.complete_analysis(analysis_id)

        assert result.success
        completed_analysis = result.data
        assert completed_analysis.status == AnalysisStatus.COMPLETED
        assert completed_analysis.completed_at is not None
        assert completed_analysis.duration_seconds is not None

    async def test_complete_analysis_not_found(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test complete analysis when not found - covers line 248."""
        result = await service.complete_analysis("non-existent-id")

        assert result.is_failure
        assert "Analysis not found" in result.error

    async def test_fail_analyssuccess(self, service: QualityAnalysisService) -> None:
        """Test successful analysis failure - covers lines 263-271."""
        # Create analysis first
        create_result = await service.create_analysis("test-project")
        analysis_id = create_result.data.id

        # Fail analysis
        result = await service.fail_analysis(analysis_id, "Test error message")

        assert result.success
        failed_analysis = result.data
        assert failed_analysis.status == AnalysisStatus.FAILED
        assert failed_analysis.completed_at is not None

    async def test_fail_analysis_not_found(
        self, service: QualityAnalysisService,
    ) -> None:
        """Test fail analysis when not found - covers line 265."""
        result = await service.fail_analysis("non-existent-id", "Error")

        assert result.is_failure
        assert "Analysis not found" in result.error

    async def test_list_analyses_success(self, service: QualityAnalysisService) -> None:
        """Test successful analyses listing - covers lines 290-299."""
        # Create multiple analyses
        await service.create_analysis("project-1")
        await service.create_analysis("project-1")
        await service.create_analysis("project-2")

        # List analyses for project-1
        result = await service.list_analyses("project-1")

        assert result.success
        analyses = result.data
        assert len(analyses) == 2
        for analysis in analyses:
            assert analysis.project_id == "project-1"

    async def test_list_analyses_empty(self, service: QualityAnalysisService) -> None:
        """Test list analyses when none exist - covers empty filter case."""
        result = await service.list_analyses("non-existent-project")

        assert result.success
        analyses = result.data
        assert len(analyses) == 0


class TestQualityIssueServiceFunctional:
    """Functional tests for QualityIssueService success paths."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create service instance."""
        return QualityIssueService()

    async def test_create_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue creation - covers lines 319-345."""
        result = await service.create_issue(
            analysis_id="test-analysis",
            issue_type="security",
            severity="high",
            rule_id="S001",
            file_path="src/auth.py",
            line_number=42,
            message="Potential security vulnerability",
        )

        assert result.success
        issue = result.data
        assert issue.analysis_id == "test-analysis"
        assert issue.issue_type == IssueType.SECURITY
        assert issue.severity == IssueSeverity.HIGH
        assert issue.rule_id == "S001"
        assert issue.file_path == "src/auth.py"
        assert issue.line_number == 42
        assert issue.message == "Potential security vulnerability"
        assert len(service._issues) == 1

    async def test_get_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue retrieval - covers lines 350-355."""
        # Create issue first
        create_result = await service.create_issue(
            analysis_id="test-analysis",
            issue_type="style",
            severity="low",
            rule_id="E301",
            file_path="test.py",
            message="Style issue",
        )
        issue_id = create_result.data.id

        # Get issue
        result = await service.get_issue(issue_id)

        assert result.success
        issue = result.data
        assert issue.id == issue_id
        assert issue.issue_type == IssueType.STYLE

    async def test_get_issue_not_found(self, service: QualityIssueService) -> None:
        """Test get issue when not found - covers line 352."""
        result = await service.get_issue("non-existent-id")

        assert result.is_failure
        assert "Issue not found" in result.error

    async def test_list_issues_success(self, service: QualityIssueService) -> None:
        """Test successful issues listing - covers lines 361-377."""
        # Create multiple issues
        await service.create_issue(
            "analysis-1", "security", "high", "S001", "file1.py", message="Issue 1",
        )
        await service.create_issue(
            "analysis-1", "style", "low", "E301", "file2.py", message="Issue 2",
        )
        await service.create_issue(
            "analysis-2", "complexity", "medium", "C001", "file3.py", message="Issue 3",
        )

        # List issues for analysis-1
        result = await service.list_issues("analysis-1")

        assert result.success
        issues = result.data
        assert len(issues) == 2
        for issue in issues:
            assert issue.analysis_id == "analysis-1"

    async def test_list_issues_empty(self, service: QualityIssueService) -> None:
        """Test list issues when none exist - covers empty filter case."""
        result = await service.list_issues("non-existent-analysis")

        assert result.success
        issues = result.data
        assert len(issues) == 0

    async def test_mark_fixed_success(self, service: QualityIssueService) -> None:
        """Test successful issue marking as fixed - covers lines 383-390."""
        # Create issue first
        create_result = await service.create_issue(
            "test-analysis", "style", "low", "E301", "test.py", message="Style issue",
        )
        issue_id = create_result.data.id

        # Mark as fixed
        result = await service.mark_fixed(issue_id)

        assert result.success
        fixed_issue = result.data
        assert fixed_issue.is_fixed is True

    async def test_mark_fixed_not_found(self, service: QualityIssueService) -> None:
        """Test mark fixed when issue not found - covers line 385."""
        result = await service.mark_fixed("non-existent-id")

        assert result.is_failure
        assert "Issue not found" in result.error

    async def test_suppress_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue suppression - covers lines 399-406."""
        # Create issue first
        create_result = await service.create_issue(
            "test-analysis", "style", "low", "E301", "test.py", message="Style issue",
        )
        issue_id = create_result.data.id

        # Suppress issue
        result = await service.suppress_issue(issue_id, "False positive")

        assert result.success
        suppressed_issue = result.data
        assert suppressed_issue.is_suppressed is True
        assert suppressed_issue.suppression_reason == "False positive"

    async def test_suppress_issue_not_found(self, service: QualityIssueService) -> None:
        """Test suppress issue when not found - covers line 401."""
        result = await service.suppress_issue("non-existent-id", "Reason")

        assert result.is_failure
        assert "Issue not found" in result.error

    async def test_unsuppress_issue_success(self, service: QualityIssueService) -> None:
        """Test successful issue unsuppression - covers lines 411-418."""
        # Create and suppress issue first
        create_result = await service.create_issue(
            "test-analysis", "style", "low", "E301", "test.py", message="Style issue",
        )
        issue_id = create_result.data.id
        await service.suppress_issue(issue_id, "False positive")

        # Unsuppress issue
        result = await service.unsuppress_issue(issue_id)

        assert result.success
        unsuppressed_issue = result.data
        assert unsuppressed_issue.is_suppressed is False
        assert unsuppressed_issue.suppression_reason is None

    async def test_unsuppress_issue_not_found(
        self, service: QualityIssueService,
    ) -> None:
        """Test unsuppress issue when not found - covers line 413."""
        result = await service.unsuppress_issue("non-existent-id")

        assert result.is_failure
        assert "Issue not found" in result.error


class TestQualityReportServiceFunctional:
    """Functional tests for QualityReportService success paths."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create service instance."""
        return QualityReportService()

    async def test_create_report_success(self, service: QualityReportService) -> None:
        """Test successful report creation - covers lines 429-449."""
        result = await service.create_report(
            analysis_id="test-analysis", report_type="html", report_format="detailed",
        )

        assert result.success
        report = result.data
        assert report.analysis_id == "test-analysis"
        assert report.report_type == "html"
        assert report.report_format == "detailed"
        assert report.generated_at is not None
        assert len(service._reports) == 1

    async def test_get_report_success(self, service: QualityReportService) -> None:
        """Test successful report retrieval - covers lines 454-461."""
        # Create report first
        create_result = await service.create_report("test-analysis", "json")
        report_id = create_result.data.id

        # Get report
        result = await service.get_report(report_id)

        assert result.success
        report = result.data
        assert report.id == report_id
        assert report.analysis_id == "test-analysis"

    async def test_get_report_not_found(self, service: QualityReportService) -> None:
        """Test get report when not found - covers line 456."""
        result = await service.get_report("non-existent-id")

        assert result.is_failure
        assert "Report not found" in result.error

    async def test_list_reports_success(self, service: QualityReportService) -> None:
        """Test successful reports listing - covers lines 466-473."""
        # Create multiple reports
        await service.create_report("analysis-1", "html")
        await service.create_report("analysis-1", "json")
        await service.create_report("analysis-2", "pdf")

        # List reports for analysis-1
        result = await service.list_reports("analysis-1")

        assert result.success
        reports = result.data
        assert len(reports) == 2
        for report in reports:
            assert report.analysis_id == "analysis-1"

    async def test_list_reports_empty(self, service: QualityReportService) -> None:
        """Test list reports when none exist - covers empty filter case."""
        result = await service.list_reports("non-existent-analysis")

        assert result.success
        reports = result.data
        assert len(reports) == 0

    async def test_delete_report_success(self, service: QualityReportService) -> None:
        """Test successful report deletion - covers lines 477-481."""
        # Create report first
        create_result = await service.create_report("test-analysis", "html")
        report_id = create_result.data.id

        # Delete report
        result = await service.delete_report(report_id)

        assert result.success
        assert len(service._reports) == 0

    async def test_delete_report_not_found(self, service: QualityReportService) -> None:
        """Test delete report when not found - covers line 479."""
        result = await service.delete_report("non-existent-id")

        assert result.is_failure
        assert "Report not found" in result.error


class TestServiceIntegration:
    """Integration tests across services."""

    async def test_full_workflow_integration(self) -> None:
        """Test complete workflow across all services."""
        project_service = QualityProjectService()
        analysis_service = QualityAnalysisService()
        issue_service = QualityIssueService()
        report_service = QualityReportService()

        # 1. Create project
        with tempfile.TemporaryDirectory() as temp_dir:
            project_result = await project_service.create_project(
                name="Integration Test", project_path=temp_dir,
            )
            assert project_result.success
            project = project_result.data

            # 2. Create analysis
            analysis_result = await analysis_service.create_analysis(project.id)
            assert analysis_result.success
            analysis = analysis_result.data

            # 3. Update analysis metrics
            metrics_result = await analysis_service.update_metrics(
                analysis.id, 5, 100, 80, 10, 10,
            )
            assert metrics_result.success

            # 4. Create issues
            issue_result = await issue_service.create_issue(
                analysis.id,
                "security",
                "high",
                "S001",
                "auth.py",
                message="Security issue",
            )
            assert issue_result.success

            # 5. Update issue counts
            counts_result = await analysis_service.update_issue_counts(
                analysis.id, 0, 1, 0, 0,
            )
            assert counts_result.success

            # 6. Complete analysis
            complete_result = await analysis_service.complete_analysis(analysis.id)
            assert complete_result.success

            # 7. Create report
            report_result = await report_service.create_report(analysis.id, "html")
            assert report_result.success

            # Verify final state
            final_project = await project_service.get_project(project.id)
            final_analysis = await analysis_service.get_analysis(analysis.id)
            final_issues = await issue_service.list_issues(analysis.id)
            final_reports = await report_service.list_reports(analysis.id)

            assert final_project.success
            assert final_analysis.success
            assert final_analysis.data.status == AnalysisStatus.COMPLETED
            assert final_issues.success
            assert len(final_issues.data) == 1
            assert final_reports.success
            assert len(final_reports.data) == 1
