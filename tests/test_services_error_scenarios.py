"""Error scenario tests for application services.

Real functional tests covering all error paths and exception handling
following flext-core patterns. Tests uncovered lines in services.py.
"""

from __future__ import annotations

from typing import Never, TypeVar
from unittest.mock import patch

import pytest

from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.domain.entities import AnalysisStatus, QualityAnalysis
from tests.conftest import (
    assert_result_failure_with_error,
    assert_result_success_with_data,
)

# Type variable for generic dictionary values
T = TypeVar("T")

# DRY pattern: Factory for exception-throwing dict classes with proper generics
def create_exception_dict(exception: Exception) -> type[dict[str, object]]:
    """SOLID factory: Creates exception-throwing dict classes.

    Single Responsibility: Creates mock dict that raises specific exceptions
    DRY principle: Eliminates duplicated ExceptionDict classes across tests
    Open/Closed: Extensible for different exception types without modification
    """
    class ExceptionDict(dict[str, object]):
        def get(self, key: str, default: object = None) -> Never:
            raise exception

        def values(self) -> Never:
            raise exception

        def __contains__(self, key: object) -> bool:
            raise exception

    return ExceptionDict


class TestQualityProjectServiceErrorScenarios:
    """Test error scenarios in QualityProjectService to improve coverage."""

    @pytest.fixture
    def service(self) -> QualityProjectService:
        """Create service instance."""
        return QualityProjectService()

    async def test_create_project_exception_handling(self, service: QualityProjectService) -> None:
        """Test exception handling in create_project - covers lines 58-59."""
        # Force exception by patching uuid4
        with patch("uuid.uuid4", side_effect=RuntimeError("UUID generation failed")):
            result = await service.create_project(
                name="test_project",
                project_path="/opt/test_secure",
            )

            error = assert_result_failure_with_error(result)
            assert "Failed to create project" in error
            assert "UUID generation failed" in error

    async def test_get_project_exception_handling(self, service: QualityProjectService) -> None:
        """Test exception handling in get_project - covers lines 70-71."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("Storage corrupted"))
        service._projects = exception_dict_class()  # type: ignore[assignment]  # Test mock

        result = await service.get_project("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to get project" in error
        assert "Storage corrupted" in error

    async def test_list_projects_exception_handling(self, service: QualityProjectService) -> None:
        """Test exception handling in list_projects - covers lines 77-78."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(TypeError("Invalid storage"))
        service._projects = exception_dict_class()  # type: ignore[assignment]  # Test mock

        result = await service.list_projects()

        error = assert_result_failure_with_error(result)
        assert "Failed to list projects" in error
        assert "Invalid storage" in error

    async def test_update_project_exception_handling(self, service: QualityProjectService) -> None:
        """Test exception handling in update_project - covers lines 97-98."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Model copy failed"))
        service._projects = exception_dict_class()  # type: ignore[assignment]  # Test mock

        result = await service.update_project("test-id", {"language": "go"})

        error = assert_result_failure_with_error(result)
        assert "Failed to update project" in error
        assert "Model copy failed" in error

    async def test_delete_project_exception_handling(self, service: QualityProjectService) -> None:
        """Test exception handling in delete_project - covers lines 106-107."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("Storage error"))
        service._projects = exception_dict_class()  # type: ignore[assignment]  # Test mock

        result = await service.delete_project("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to delete project" in error
        assert "Storage error" in error


class TestQualityAnalysisServiceErrorScenarios:
    """Test error scenarios in QualityAnalysisService to improve coverage."""

    @pytest.fixture
    def service(self) -> QualityAnalysisService:
        """Create service instance."""
        return QualityAnalysisService()

    async def test_create_analysis_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in create_analysis - covers lines 143-144."""
        # Force exception during uuid4 call
        with patch("uuid.uuid4", side_effect=TypeError("Invalid parameters")):
            result = await service.create_analysis(project_id="test-project")

            error = assert_result_failure_with_error(result)
            assert "Failed to create analysis" in error
            assert "Invalid parameters" in error

    async def test_update_metrics_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in update_metrics - covers lines 173-174."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Update failed"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.update_metrics(
            analysis_id="test-id",
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )

        error = assert_result_failure_with_error(result)
        assert "Failed to update metrics" in error
        assert "Update failed" in error

    async def test_update_scores_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in update_scores - covers lines 206-207."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("Calculation error"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.update_scores(
            analysis_id="test-id",
            coverage_score=95.0,
            complexity_score=90.0,
            duplication_score=85.0,
            security_score=100.0,
            maintainability_score=88.0,
        )

        error = assert_result_failure_with_error(result)
        assert "Failed to update scores" in error
        assert "Calculation error" in error

    async def test_update_issue_counts_analysis_not_found(self, service: QualityAnalysisService) -> None:
        """Test update_issue_counts when analysis not found - covers line 220."""
        result = await service.update_issue_counts(
            analysis_id="non-existent",
            critical=1,
            high=2,
            medium=3,
            low=4,
        )

        error = assert_result_failure_with_error(result)
        assert "Analysis not found" in error

    async def test_complete_analysis_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in complete_analysis - covers lines 255-256."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Cannot complete"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.complete_analysis("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to complete analysis" in error
        assert "Cannot complete" in error

    async def test_fail_analysis_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in fail_analysis - covers lines 275-276."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("Cannot fail"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.fail_analysis("test-id", "Test error")

        error = assert_result_failure_with_error(result)
        assert "Failed to fail analysis" in error
        assert "Cannot fail" in error

    async def test_get_analysis_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in get_analysis - covers lines 287-288."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(TypeError("Storage corrupted"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.get_analysis("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to get analysis" in error
        assert "Storage corrupted" in error

    async def test_list_analyses_exception_handling(self, service: QualityAnalysisService) -> None:
        """Test exception handling in list_analyses - covers lines 301-302."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("List error"))
        service._analyses = exception_dict_class()  # type: ignore[assignment]

        result = await service.list_analyses("test-project")

        error = assert_result_failure_with_error(result)
        assert "Failed to list analyses" in error
        assert "List error" in error


class TestQualityIssueServiceErrorScenarios:
    """Test error scenarios in QualityIssueService to improve coverage."""

    @pytest.fixture
    def service(self) -> QualityIssueService:
        """Create service instance."""
        return QualityIssueService()

    async def test_create_issue_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in create_issue - covers lines 347-348."""
        # Force exception during uuid4 call
        with patch("uuid.uuid4", side_effect=ValueError("Invalid issue type")):
            result = await service.create_issue(
                analysis_id="test-analysis",
                issue_type="style",
                severity="medium",
                rule_id="E302",
                file_path="test.py",
                message="Test issue",
            )

            error = assert_result_failure_with_error(result)
            assert "Failed to create issue" in error
            assert "Invalid issue type" in error

    async def test_get_issue_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in get_issue - covers line 356-357."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Storage failure"))
        service._issues = exception_dict_class()  # type: ignore[assignment]

        result = await service.get_issue("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to get issue" in error
        assert "Storage failure" in error

    async def test_list_issues_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in list_issues - covers lines 379-380."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(TypeError("Filter error"))
        service._issues = exception_dict_class()  # type: ignore[assignment]

        result = await service.list_issues("test-analysis")

        error = assert_result_failure_with_error(result)
        assert "Failed to list issues" in error
        assert "Filter error" in error

    async def test_mark_fixed_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in mark_fixed - covers lines 391-392."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Cannot mark fixed"))
        service._issues = exception_dict_class()  # type: ignore[assignment]

        result = await service.mark_fixed("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to mark issue as fixed" in error
        assert "Cannot mark fixed" in error

    async def test_suppress_issue_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in suppress_issue - covers lines 407-408."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("Cannot suppress"))
        service._issues = exception_dict_class()  # type: ignore[assignment]

        result = await service.suppress_issue("test-id", "False positive")

        error = assert_result_failure_with_error(result)
        assert "Failed to suppress issue" in error
        assert "Cannot suppress" in error

    async def test_unsuppress_issue_exception_handling(self, service: QualityIssueService) -> None:
        """Test exception handling in unsuppress_issue - covers lines 419-420."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Cannot unsuppress"))
        service._issues = exception_dict_class()  # type: ignore[assignment]

        result = await service.unsuppress_issue("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to unsuppress issue" in error
        assert "Cannot unsuppress" in error


class TestQualityReportServiceErrorScenarios:
    """Test error scenarios in QualityReportService to improve coverage."""

    @pytest.fixture
    def service(self) -> QualityReportService:
        """Create service instance."""
        return QualityReportService()

    async def test_create_report_exception_handling(self, service: QualityReportService) -> None:
        """Test exception handling in create_report - covers lines 451-452."""
        # Force exception during uuid4 call
        with patch("uuid.uuid4", side_effect=TypeError("Invalid parameters")):
            result = await service.create_report(
                analysis_id="test-analysis",
                report_type="html",
            )

            error = assert_result_failure_with_error(result)
            assert "Failed to create report" in error
            assert "Invalid parameters" in error

    async def test_get_report_exception_handling(self, service: QualityReportService) -> None:
        """Test exception handling in get_report - covers lines 462-463."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Access error"))
        service._reports = exception_dict_class()  # type: ignore[assignment]

        result = await service.get_report("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to get report" in error
        assert "Access error" in error

    async def test_list_reports_exception_handling(self, service: QualityReportService) -> None:
        """Test exception handling in list_reports - covers lines 474-475."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(ValueError("List error"))
        service._reports = exception_dict_class()  # type: ignore[assignment]

        result = await service.list_reports("test-analysis")

        error = assert_result_failure_with_error(result)
        assert "Failed to list reports" in error
        assert "List error" in error

    async def test_delete_report_exception_handling(self, service: QualityReportService) -> None:
        """Test exception handling in delete_report - covers lines 483-484."""
        # DRY: Use factory to create exception-throwing dict
        exception_dict_class = create_exception_dict(RuntimeError("Delete error"))
        service._reports = exception_dict_class()  # type: ignore[assignment]

        result = await service.delete_report("test-id")

        error = assert_result_failure_with_error(result)
        assert "Failed to delete report" in error
        assert "Delete error" in error
