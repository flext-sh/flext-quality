"""Test suite for domain entities."""

from __future__ import annotations

from datetime import datetime

import pytest
from flext_quality.domain.entities import (
    AnalysisStatus,
    IssueSeverity,
    IssueType,
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
    QualityRule,
)
from pydantic import ValidationError


class TestQualityProject:
    """Test QualityProject entity."""

    def test_project_creation(self, secure_temp_dir: str) -> None:
        """Test basic project creation."""
        project = QualityProject(
            id="test-project-id",
            project_path=secure_temp_dir,
            repository_url="https://github.com/test/repo",
            language="python",
        )

        assert project.id == "test-project-id"
        assert project.project_path == secure_temp_dir
        assert project.repository_url == "https://github.com/test/repo"
        assert project.language == "python"
        assert project.auto_analyze is True
        assert project.min_coverage == 95.0

    def test_project_validation_success(self, secure_temp_dir: str) -> None:
        """Test successful project validation."""
        project = QualityProject(
            id="test-id",
            project_path=secure_temp_dir,
        )

        result = project.validate_domain_rules()
        assert result.success

    def test_project_validation_failure(self) -> None:
        """Test project validation failure."""
        # Empty path should fail at Pydantic validation level
        with pytest.raises(ValidationError):
            QualityProject(
                id="test-id",
                project_path="",  # Empty path should fail
            )

    def test_update_last_analysis(self, secure_temp_dir: str) -> None:
        """Test updating last analysis timestamp."""
        project = QualityProject(
            id="test-id",
            project_path=secure_temp_dir,
        )

        initial_count = project.total_analyses
        assert project.last_analysis_at is None

        updated_project = project.update_last_analysis()

        assert updated_project.last_analysis_at is not None
        assert isinstance(updated_project.last_analysis_at, datetime)
        assert updated_project.total_analyses == initial_count + 1


class TestQualityAnalysis:
    """Test QualityAnalysis entity."""

    def test_analysis_creation(self) -> None:
        """Test basic analysis creation."""
        analysis = QualityAnalysis(
            id="test-analysis-id",
            project_id="test-project-id",
            commit_hash="abc123",
            branch="main",
        )

        assert analysis.id == "test-analysis-id"
        assert analysis.project_id == "test-project-id"
        assert analysis.commit_hash == "abc123"
        assert analysis.branch == "main"
        assert analysis.status == AnalysisStatus.QUEUED

    def test_analysis_validation_success(self) -> None:
        """Test successful analysis validation."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        result = analysis.validate_domain_rules()
        assert result.success

    def test_analysis_validation_failure(self) -> None:
        """Test analysis validation failure."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="",  # Empty project_id should fail
        )

        result = analysis.validate_domain_rules()
        assert result.is_failure
        assert result.error is not None
        assert "required" in result.error.lower()

    def test_start_analysis(self) -> None:
        """Test starting an analysis."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        assert analysis.status == AnalysisStatus.QUEUED

        updated_analysis = analysis.start_analysis()

        assert updated_analysis.status == AnalysisStatus.ANALYZING
        assert updated_analysis.started_at is not None

    def test_complete_analysis(self) -> None:
        """Test completing an analysis."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        started_analysis = analysis.start_analysis()
        completed_analysis = started_analysis.complete_analysis()

        assert completed_analysis.status == AnalysisStatus.COMPLETED
        assert completed_analysis.completed_at is not None
        assert completed_analysis.duration_seconds is not None
        assert completed_analysis.duration_seconds >= 0

    def test_fail_analysis(self) -> None:
        """Test failing an analysis."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        started_analysis = analysis.start_analysis()
        failed_analysis = started_analysis.fail_analysis("Test error")

        assert failed_analysis.status == AnalysisStatus.FAILED
        assert failed_analysis.completed_at is not None
        assert failed_analysis.duration_seconds is not None

    def test_calculate_overall_score(self) -> None:
        """Test calculating overall score."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
            coverage_score=90.0,
            complexity_score=85.0,
            duplication_score=95.0,
            security_score=100.0,
            maintainability_score=80.0,
        )

        updated_analysis = analysis.calculate_overall_score()

        expected_score = (90.0 + 85.0 + 95.0 + 100.0 + 80.0) / 5
        assert updated_analysis.overall_score == expected_score

    def test_is_completed_property(self) -> None:
        """Test is_completed property."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        assert not analysis.is_completed

        completed_analysis = analysis.complete_analysis()
        assert completed_analysis.is_completed

        failed_analysis = analysis.model_copy(update={"status": AnalysisStatus.FAILED})
        assert failed_analysis.is_completed

    def test_successful_property(self) -> None:
        """Test successful property."""
        analysis = QualityAnalysis(
            id="test-id",
            project_id="project-id",
        )

        assert not analysis.successful

        completed_analysis = analysis.complete_analysis()
        assert completed_analysis.successful

        failed_analysis = analysis.model_copy(update={"status": AnalysisStatus.FAILED})
        assert not failed_analysis.successful


class TestQualityIssue:
    """Test QualityIssue entity."""

    def test_issue_creation(self) -> None:
        """Test basic issue creation."""
        issue = QualityIssue(
            id="test-issue-id",
            analysis_id="test-analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.MEDIUM,
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
            line_number=10,
        )

        assert issue.id == "test-issue-id"
        assert issue.analysis_id == "test-analysis-id"
        assert issue.issue_type == IssueType.STYLE
        assert issue.severity == IssueSeverity.MEDIUM
        assert issue.rule_id == "E302"
        assert issue.file_path == "test.py"
        assert issue.message == "Missing blank line"
        assert issue.line_number == 10
        assert not issue.is_fixed
        assert not issue.is_suppressed

    def test_issue_validation_success(self) -> None:
        """Test successful issue validation."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        result = issue.validate_domain_rules()
        assert result.success

    def test_issue_validation_failure(self) -> None:
        """Test issue validation failure."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="",  # Empty analysis_id should fail
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        result = issue.validate_domain_rules()
        assert result.is_failure
        assert result.error is not None
        assert "required" in result.error.lower()

    def test_mark_fixed(self) -> None:
        """Test marking issue as fixed."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        assert not issue.is_fixed

        fixed_issue = issue.mark_fixed()

        assert fixed_issue.is_fixed

    def test_suppress_issue(self) -> None:
        """Test suppressing an issue."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        assert not issue.is_suppressed
        assert issue.suppression_reason is None

        reason = "False positive"
        suppressed_issue = issue.suppress(reason)

        assert suppressed_issue.is_suppressed
        assert suppressed_issue.suppression_reason == reason

    def test_unsuppress_issue(self) -> None:
        """Test unsuppressing an issue."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        # First suppress it
        suppressed_issue = issue.suppress("Test reason")
        assert suppressed_issue.is_suppressed

        # Then unsuppress it
        unsuppressed_issue = suppressed_issue.unsuppress()

        assert not unsuppressed_issue.is_suppressed
        assert unsuppressed_issue.suppression_reason is None

    def test_increment_occurrence(self) -> None:
        """Test incrementing occurrence count."""
        issue = QualityIssue(
            id="test-id",
            analysis_id="analysis-id",
            issue_type=IssueType.STYLE,
            severity=IssueSeverity.LOW,
            rule_id="E302",
            file_path="test.py",
            message="Test message",
        )

        initial_count = issue.occurrence_count
        initial_time = issue.last_seen_at

        updated_issue = issue.increment_occurrence()

        assert updated_issue.occurrence_count == initial_count + 1
        assert updated_issue.last_seen_at > initial_time


class TestQualityRule:
    """Test QualityRule entity."""

    def test_rule_creation(self) -> None:
        """Test basic rule creation."""
        rule = QualityRule(
            id="test-rule-id",
            rule_id="E302",
            category=IssueType.STYLE,
            enabled=True,
            severity=IssueSeverity.MEDIUM,
        )

        assert rule.id == "test-rule-id"
        assert rule.rule_id == "E302"
        assert rule.category == IssueType.STYLE
        assert rule.enabled is True
        assert rule.severity == IssueSeverity.MEDIUM

    def test_rule_validation_success(self) -> None:
        """Test successful rule validation."""
        rule = QualityRule(
            id="test-id",
            rule_id="E302",
            category=IssueType.STYLE,
        )

        result = rule.validate_domain_rules()
        assert result.success

    def test_rule_validation_failure(self) -> None:
        """Test rule validation failure."""
        # Use model_copy to create an invalid state for testing
        rule = QualityRule(
            id="test-id",
            rule_id="E302",
            category=IssueType.STYLE,
        )

        # Create an invalid instance for testing validation
        invalid_rule = rule.model_copy(update={"rule_id": ""})

        result = invalid_rule.validate_domain_rules()
        assert result.is_failure
        assert result.error is not None
        assert "required" in result.error.lower()

    def test_enable_disable_rule(self) -> None:
        """Test enabling and disabling a rule."""
        rule = QualityRule(
            id="test-id",
            rule_id="E302",
            category=IssueType.STYLE,
            enabled=False,
        )

        assert not rule.enabled

        enabled_rule = rule.enable()
        assert enabled_rule.enabled

        disabled_rule = enabled_rule.disable()
        assert not disabled_rule.enabled

    def test_update_severity(self) -> None:
        """Test updating rule severity."""
        rule = QualityRule(
            id="test-id",
            rule_id="E302",
            category=IssueType.STYLE,
            severity=IssueSeverity.LOW,
        )

        assert rule.severity == IssueSeverity.LOW

        updated_rule = rule.update_severity(IssueSeverity.HIGH)

        assert updated_rule.severity == IssueSeverity.HIGH

    def test_set_parameter(self) -> None:
        """Test setting rule parameters."""
        rule = QualityRule(
            id="test-id",
            rule_id="E302",
            category=IssueType.STYLE,
        )

        assert len(rule.parameters) == 0

        updated_rule = rule.set_parameter("max_line_length", 120)

        assert updated_rule.parameters["max_line_length"] == 120


class TestQualityReport:
    """Test QualityReport entity."""

    def test_report_creation(self) -> None:
        """Test basic report creation."""
        report = QualityReport(
            id="test-report-id",
            analysis_id="test-analysis-id",
            report_type="html",
            report_format="detailed",
        )

        assert report.id == "test-report-id"
        assert report.analysis_id == "test-analysis-id"
        assert report.report_type == "html"
        assert report.report_format == "detailed"
        assert report.access_count == 0

    def test_report_validation_success(self) -> None:
        """Test successful report validation."""
        report = QualityReport(
            id="test-id",
            analysis_id="analysis-id",
            report_type="json",
        )

        result = report.validate_domain_rules()
        assert result.success

    def test_report_validation_failure(self) -> None:
        """Test report validation failure."""
        report = QualityReport(
            id="test-id",
            analysis_id="",  # Empty analysis_id should fail
            report_type="json",
        )

        result = report.validate_domain_rules()
        assert result.is_failure
        assert result.error is not None
        assert "required" in result.error.lower()

    def test_increment_access(self) -> None:
        """Test incrementing access count."""
        report = QualityReport(
            id="test-id",
            analysis_id="analysis-id",
            report_type="json",
        )

        assert report.access_count == 0
        assert report.last_accessed_at is None

        updated_report = report.increment_access()

        assert updated_report.access_count == 1
        assert updated_report.last_accessed_at is not None
