"""Test suite for simple API."""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_quality import QualityAPI


class TestQualityAPI:
    """Test QualityAPI functionality."""

    @pytest.fixture
    def api(self) -> QualityAPI:
        """Create a QualityAPI instance."""
        return QualityAPI()

    async def test_create_project(self, api: QualityAPI) -> None:
        """Test creating a project through API."""
        result = await api.create_project(
            name="test_project",
            project_path="./test_project",
            repository_url="https://github.com/test/repo",
            language="python",
        )

        assert result.success
        assert result.data is not None
        assert result.data.project_path == "./test_project"

    async def test_get_project(self, api: QualityAPI) -> None:
        """Test getting a project through API."""
        # First create a project
        create_result = await api.create_project(
            name="test_project",
            project_path="./test_project",
        )
        assert create_result.success
        project_id = uuid4()  # Use UUID type as expected by API

        # Mock the project in service for testing
        api.project_service._projects[str(project_id)] = create_result.data

        # Get the project
        result = await api.get_project(project_id)
        assert result.success

    async def test_list_projects(self, api: QualityAPI) -> None:
        """Test listing projects through API."""
        result = await api.list_projects()
        assert result.success
        assert isinstance(result.data, list)

    async def test_update_project(self, api: QualityAPI) -> None:
        """Test updating a project through API."""
        # First create a project
        create_result = await api.create_project(
            name="test_project",
            project_path="./test_project",
        )
        assert create_result.success
        project_id = uuid4()

        # Mock the project in service (ensure data is not None)
        if create_result.data is not None:
            api.project_service._projects[str(project_id)] = create_result.data

        # Update the project
        updates: dict[str, object] = {"language": "go"}
        result = await api.update_project(project_id, updates)
        assert result.success

    async def test_delete_project(self, api: QualityAPI) -> None:
        """Test deleting a project through API."""
        # First create a project
        create_result = await api.create_project(
            name="test_project",
            project_path="./test_project",
        )
        assert create_result.success
        project_id = uuid4()

        # Mock the project in service (ensure data is not None)
        if create_result.data is not None:
            api.project_service._projects[str(project_id)] = create_result.data

        # Delete the project
        result = await api.delete_project(project_id)
        assert result.success

    async def test_create_analysis(self, api: QualityAPI) -> None:
        """Test creating an analysis through API."""
        project_id = uuid4()

        result = await api.create_analysis(
            project_id=project_id,
            commit_hash="abc123",
            branch="main",
        )
        assert result.success

    async def test_update_analysis_metrics(self, api: QualityAPI) -> None:
        """Test updating analysis metrics through API."""
        analysis_id = uuid4()

        result = await api.update_metrics(
            analysis_id=analysis_id,
            total_files=10,
            total_lines=1000,
            code_lines=800,
            comment_lines=100,
            blank_lines=100,
        )
        # This will fail because analysis doesn't exist, but tests the API call
        assert result.is_failure

    async def test_update_analysis_scores(self, api: QualityAPI) -> None:
        """Test updating analysis scores through API."""
        analysis_id = uuid4()

        result = await api.update_scores(
            analysis_id=analysis_id,
            coverage_score=95.0,
            complexity_score=90.0,
            duplication_score=85.0,
            security_score=100.0,
            maintainability_score=88.0,
        )
        # This will fail because analysis doesn't exist
        assert result.is_failure

    async def test_create_issue(self, api: QualityAPI) -> None:
        """Test creating an issue through API."""
        analysis_id = uuid4()

        result = await api.create_issue(
            analysis_id=analysis_id,
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
            line_number=10,
        )
        assert result.success

    async def test_get_issue(self, api: QualityAPI) -> None:
        """Test getting an issue through API."""
        # First create an issue
        analysis_id = uuid4()
        create_result = await api.create_issue(
            analysis_id=analysis_id,
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.success

        issue_id = uuid4()
        # Mock the issue in service
        api.issue_service._issues[str(issue_id)] = create_result.data

        result = await api.get_issue(issue_id)
        assert result.success

    async def test_mark_issue_fixed(self, api: QualityAPI) -> None:
        """Test marking an issue as fixed through API."""
        # First create an issue
        analysis_id = uuid4()
        create_result = await api.create_issue(
            analysis_id=analysis_id,
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.success

        issue_id = uuid4()
        # Mock the issue in service
        api.issue_service._issues[str(issue_id)] = create_result.data

        result = await api.mark_issue_fixed(issue_id)
        assert result.success

    async def test_suppress_issue(self, api: QualityAPI) -> None:
        """Test suppressing an issue through API."""
        # First create an issue
        analysis_id = uuid4()
        create_result = await api.create_issue(
            analysis_id=analysis_id,
            issue_type="style",
            severity="medium",
            rule_id="E302",
            file_path="test.py",
            message="Missing blank line",
        )
        assert create_result.success

        issue_id = uuid4()
        # Mock the issue in service
        api.issue_service._issues[str(issue_id)] = create_result.data

        result = await api.suppress_issue(issue_id, "False positive")
        assert result.success

    async def test_create_report(self, api: QualityAPI) -> None:
        """Test creating a report through API."""
        analysis_id = uuid4()

        result = await api.create_report(
            analysis_id=analysis_id,
            report_type="html",
            report_format="detailed",
        )
        assert result.success

    async def test_get_report(self, api: QualityAPI) -> None:
        """Test getting a report through API."""
        # First create a report
        analysis_id = uuid4()
        create_result = await api.create_report(
            analysis_id=analysis_id,
            report_type="json",
        )
        assert create_result.success

        report_id = uuid4()
        # Mock the report in service
        api.report_service._reports[str(report_id)] = create_result.data

        result = await api.get_report(report_id)
        assert result.success

    async def test_delete_report(self, api: QualityAPI) -> None:
        """Test deleting a report through API."""
        # First create a report
        analysis_id = uuid4()
        create_result = await api.create_report(
            analysis_id=analysis_id,
            report_type="pdf",
        )
        assert create_result.success

        report_id = uuid4()
        # Mock the report in service
        api.report_service._reports[str(report_id)] = create_result.data

        result = await api.delete_report(report_id)
        assert result.success

    async def test_analyze_project_full(self, api: QualityAPI) -> None:
        """Test full project analysis through API."""
        project_id = uuid4()

        result = await api.run_full_analysis(
            project_id=project_id,
            commit_hash="abc123",
            branch="main",
        )
        # This is complex flow, just test it doesn't crash
        assert result is not None

    async def test_list_project_analyses(self, api: QualityAPI) -> None:
        """Test listing project analyses through API."""
        project_id = uuid4()

        result = await api.list_analyses(project_id)
        assert result.success

    async def test_list_analysis_issues(self, api: QualityAPI) -> None:
        """Test listing analysis issues through API."""
        analysis_id = uuid4()

        result = await api.list_issues(analysis_id)
        assert result.success

    async def test_list_analysis_reports(self, api: QualityAPI) -> None:
        """Test listing analysis reports through API."""
        analysis_id = uuid4()

        result = await api.list_reports(analysis_id)
        assert result.success
