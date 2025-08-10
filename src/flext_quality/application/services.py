"""Application services for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core service patterns - NO duplication.
    Clean architecture with dependency injection and FlextResult pattern.
"""

from __future__ import annotations

from flext_core import FlextResult, TConfigDict

from flext_quality.domain.entities import (
    AnalysisStatus,
    IssueSeverity,
    IssueType,
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
)


# Simplified DI - removed decorator
class QualityProjectService:
    """Service for managing quality projects."""

    def __init__(self) -> None:
        self._projects: dict[str, QualityProject] = {}

    async def create_project(
        self,
        name: str,
        project_path: str,
        repository_url: str | None = None,
        config_path: str | None = None,
        language: str = "python",
        auto_analyze: bool = True,
        min_coverage: float = 95.0,
        max_complexity: int = 10,
        max_duplication: float = 5.0,
    ) -> FlextResult[QualityProject]:
        """Create a new quality project.

        Args:
            name: Project name
            project_path: Path to the project directory
            repository_url: Optional repository URL
            config_path: Optional configuration file path
            language: Project language (default: python)
            auto_analyze: Whether to auto-analyze on changes
            min_coverage: Minimum coverage threshold
            max_complexity: Maximum complexity threshold
            max_duplication: Maximum duplication threshold

        Returns:
            FlextResult containing the created project or error

        """
        try:
            from uuid import uuid4

            project = QualityProject(
                id=str(uuid4()),
                name=name,  # Use the name parameter
                project_path=project_path,
                repository_url=repository_url,
                config_path=config_path,
                language=language,
                auto_analyze=auto_analyze,
                min_coverage=min_coverage,
                max_complexity=max_complexity,
                max_duplication=max_duplication,
            )

            self._projects[project.id] = project
            return FlextResult.ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create project {e}")

    async def get_project(
        self,
        project_id: str,
    ) -> FlextResult[QualityProject]:
        """Get a project by ID.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing the project or error

        """
        try:
            project = self._projects.get(project_id)
            if project is None:
                return FlextResult.fail(f"Project not found: {project_id}")
            return FlextResult.ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get project {e}")

    async def list_projects(self) -> FlextResult[list[QualityProject]]:
        """List all projects.

        Returns:
            FlextResult containing list of projects or error

        """
        try:
            projects = list(self._projects.values())
            return FlextResult.ok(projects)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to list projects {e}")

    async def update_project(
        self,
        project_id: str,
        updates: dict[str, object],
    ) -> FlextResult[QualityProject]:
        """Update an existing project.

        Args:
            project_id: Project unique identifier
            updates: Dictionary of fields to update

        Returns:
            FlextResult containing the updated project or error

        """
        try:
            project = self._projects.get(project_id)
            if not project:
                return FlextResult.fail("Project not found")

            # Use model_copy to create updated version (immutable pattern)
            updated_project = project.model_copy(update=updates)

            # Store the updated project
            self._projects[project_id] = updated_project

            return FlextResult.ok(updated_project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to update project: {e}")

    async def delete_project(self, project_id: str) -> FlextResult[bool]:
        """Delete a project.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing success status or error

        """
        try:
            if project_id in self._projects:
                del self._projects[project_id]
                return FlextResult.ok(True)
            return FlextResult.fail("Project not found")
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to delete project: {e}")


# Simplified DI - removed decorator
class QualityAnalysisService:
    """Service for managing quality analyses."""

    def __init__(self) -> None:
        self._analyses: dict[str, QualityAnalysis] = {}

    async def create_analysis(
        self,
        project_id: str,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: TConfigDict | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Create a new quality analysis.

        Args:
            project_id: Project unique identifier
            commit_hash: Optional commit hash
            branch: Optional branch name
            pull_request_id: Optional pull request ID
            analysis_config: Optional analysis configuration

        Returns:
            FlextResult containing the created analysis or error

        """
        try:
            from uuid import uuid4

            # Create real QualityAnalysis entity following flext-core patterns
            analysis = QualityAnalysis(
                id=str(uuid4()),
                project_id=project_id,
                commit_hash=commit_hash,
                branch=branch,
                pull_request_id=pull_request_id,
                analysis_config=analysis_config or {},
                status=AnalysisStatus.QUEUED,
            )

            # Store in repository
            self._analyses[analysis.id] = analysis

            return FlextResult.ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create analysis: {e}")

    async def update_metrics(
        self,
        analysis_id: str,
        total_files: int,
        total_lines: int,
        code_lines: int,
        comment_lines: int,
        blank_lines: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis metrics.

        Args:
            analysis_id: Analysis unique identifier
            total_files: Total number of files
            total_lines: Total number of lines
            code_lines: Number of code lines
            comment_lines: Number of comment lines
            blank_lines: Number of blank lines

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            # Use immutable update pattern following flext-core guidelines
            updated_analysis = analysis.model_copy(
                update={
                    "total_files": total_files,
                    "total_lines": total_lines,
                    "code_lines": code_lines,
                    "comment_lines": comment_lines,
                    "blank_lines": blank_lines,
                },
            )

            # Store updated analysis
            self._analyses[analysis_id] = updated_analysis

            return FlextResult.ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to update metrics: {e}")

    async def update_scores(
        self,
        analysis_id: str,
        coverage_score: float,
        complexity_score: float,
        duplication_score: float,
        security_score: float,
        maintainability_score: float,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis quality scores.

        Args:
            analysis_id: Analysis unique identifier
            coverage_score: Code coverage score
            complexity_score: Code complexity score
            duplication_score: Code duplication score
            security_score: Security vulnerability score
            maintainability_score: Code maintainability score

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            # Use immutable update pattern following flext-core guidelines
            updated_analysis = analysis.model_copy(
                update={
                    "coverage_score": coverage_score,
                    "complexity_score": complexity_score,
                    "duplication_score": duplication_score,
                    "security_score": security_score,
                    "maintainability_score": maintainability_score,
                },
            )

            # Calculate overall score using domain method
            final_analysis = updated_analysis.calculate_overall_score()

            # Store updated analysis
            self._analyses[analysis_id] = final_analysis

            return FlextResult.ok(final_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to update scores: {e}")

    async def update_issue_counts(
        self,
        analysis_id: str,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis issue counts.

        Args:
            analysis_id: Analysis unique identifier
            critical: Number of critical issues
            high: Number of high priority issues
            medium: Number of medium priority issues
            low: Number of low priority issues

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            # Use immutable update pattern following flext-core guidelines
            total_issues = critical + high + medium + low
            updated_analysis = analysis.model_copy(
                update={
                    "critical_issues": critical,
                    "high_issues": high,
                    "medium_issues": medium,
                    "low_issues": low,
                    "total_issues": total_issues,
                },
            )

            # Store updated analysis
            self._analyses[analysis_id] = updated_analysis

            return FlextResult.ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to update issue counts: {e}")

    async def complete_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as completed.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing the completed analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            # Use immutable update pattern following flext-core guidelines
            completed_analysis = analysis.complete_analysis()

            # Store updated analysis
            self._analyses[analysis_id] = completed_analysis

            return FlextResult.ok(completed_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to complete analysis: {e}")

    async def fail_analysis(
        self,
        analysis_id: str,
        error: str,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as failed.

        Args:
            analysis_id: Analysis unique identifier
            error: Error message describing the failure

        Returns:
            FlextResult containing the failed analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            # Use immutable update pattern following flext-core guidelines
            failed_analysis = analysis.fail_analysis(error)

            # Store updated analysis
            self._analyses[analysis_id] = failed_analysis

            return FlextResult.ok(failed_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to fail analysis: {e}")

    async def get_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[QualityAnalysis]:
        """Get an analysis by ID.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing the analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if analysis is None:
                return FlextResult.fail(f"Analysis not found: {analysis_id}")
            return FlextResult.ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get analysis: {e}")

    async def list_analyses(
        self,
        project_id: str,
    ) -> FlextResult[list[QualityAnalysis]]:
        """List analyses for a project.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing list of analyses or error

        """
        try:
            analyses = [
                a for a in self._analyses.values() if a.project_id == project_id
            ]
            # Sort by started_at descending
            analyses.sort(key=lambda a: a.started_at, reverse=True)
            return FlextResult.ok(analyses)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to list analyses: {e}")


# Simplified DI - removed decorator
class QualityIssueService:
    """Service for managing quality issues."""

    def __init__(self) -> None:
        self._issues: dict[str, QualityIssue] = {}

    async def create_issue(
        self,
        analysis_id: str,
        issue_type: str,
        severity: str,
        rule_id: str,
        file_path: str,
        message: str,
        line_number: int | None = None,
        column_number: int | None = None,
        end_line_number: int | None = None,
        end_column_number: int | None = None,
        code_snippet: str | None = None,
        suggestion: str | None = None,
    ) -> FlextResult[QualityIssue]:
        """Create a new quality issue.

        Args:
            analysis_id: Analysis unique identifier
            issue_type: Type of the issue
            severity: Severity level
            rule_id: Rule identifier that triggered the issue
            file_path: File path where issue was found
            message: Issue description message
            line_number: Optional line number
            column_number: Optional column number
            end_line_number: Optional end line number
            end_column_number: Optional end column number
            code_snippet: Optional code snippet
            suggestion: Optional suggestion for fix

        Returns:
            FlextResult containing the created issue or error

        """
        try:
            from uuid import uuid4

            issue = QualityIssue(
                id=str(uuid4()),
                analysis_id=analysis_id,
                issue_type=IssueType(issue_type),
                severity=IssueSeverity(severity),
                rule_id=rule_id,
                file_path=file_path,
                message=message,
                line_number=line_number,
                column_number=column_number,
                end_line_number=end_line_number,
                end_column_number=end_column_number,
                code_snippet=code_snippet,
                suggestion=suggestion,
            )

            self._issues[issue.id] = issue
            return FlextResult.ok(issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create issue: {e}")

    async def get_issue(self, issue_id: str) -> FlextResult[QualityIssue]:
        """Get an issue by ID.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if issue is None:
                return FlextResult.fail(f"Issue not found: {issue_id}")
            return FlextResult.ok(issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get issue {e}")

    async def list_issues(
        self,
        analysis_id: str,
        severity: str | None = None,
        issue_type: str | None = None,
        file_path: str | None = None,
    ) -> FlextResult[list[QualityIssue]]:
        """List issues for an analysis with optional filters.

        Args:
            analysis_id: Analysis unique identifier
            severity: Optional severity filter
            issue_type: Optional issue type filter
            file_path: Optional file path filter

        Returns:
            FlextResult containing list of issues or error

        """
        try:
            issues = [i for i in self._issues.values() if i.analysis_id == analysis_id]

            if severity:
                issues = [i for i in issues if i.severity == severity]

            if issue_type:
                issues = [i for i in issues if i.issue_type == issue_type]

            if file_path:
                issues = [i for i in issues if i.file_path == file_path]

            return FlextResult.ok(issues)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to list issues: {e}")

    async def mark_fixed(self, issue_id: str) -> FlextResult[QualityIssue]:
        """Mark issue as fixed.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the fixed issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            fixed_issue = issue.mark_fixed()
            self._issues[issue_id] = fixed_issue
            return FlextResult.ok(fixed_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to mark issue as fixed: {e}")

    async def suppress_issue(
        self,
        issue_id: str,
        reason: str,
    ) -> FlextResult[QualityIssue]:
        """Suppress an issue.

        Args:
            issue_id: Issue unique identifier
            reason: Reason for suppressing the issue

        Returns:
            FlextResult containing the suppressed issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            suppressed_issue = issue.suppress(reason)
            self._issues[issue_id] = suppressed_issue
            return FlextResult.ok(suppressed_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to suppress issue: {e}")

    async def unsuppress_issue(self, issue_id: str) -> FlextResult[QualityIssue]:
        """Remove suppression from an issue.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the unsuppressed issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            unsuppressed_issue = issue.unsuppress()
            self._issues[issue_id] = unsuppressed_issue
            return FlextResult.ok(unsuppressed_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to unsuppress issue: {e}")


# Simplified DI - removed decorator
class QualityReportService:
    """Service for managing quality reports."""

    def __init__(self) -> None:
        self._reports: dict[str, QualityReport] = {}

    async def create_report(
        self,
        analysis_id: str,
        report_type: str,
        report_format: str = "summary",
        report_path: str | None = None,
        report_size_bytes: int = 0,
    ) -> FlextResult[QualityReport]:
        """Create a new quality report.

        Args:
            analysis_id: Analysis unique identifier
            report_type: Type of report to generate
            report_format: Format of the report (default: summary)
            report_path: Optional path to save the report
            report_size_bytes: Size of the report in bytes

        Returns:
            FlextResult containing the created report or error

        """
        try:
            from uuid import uuid4

            report = QualityReport(
                id=str(uuid4()),
                analysis_id=analysis_id,
                report_type=report_type,
                report_format=report_format,
                report_path=report_path,
                report_size_bytes=report_size_bytes,
            )

            self._reports[report.id] = report
            return FlextResult.ok(report)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create report: {e}")

    async def get_report(self, report_id: str) -> FlextResult[QualityReport]:
        """Get a report by ID.

        Args:
            report_id: Report unique identifier

        Returns:
            FlextResult containing the report or error

        """
        try:
            report = self._reports.get(report_id)
            if report is None:
                return FlextResult.fail(f"Report not found: {report_id}")
            updated_report = report.increment_access()
            self._reports[report_id] = updated_report
            return FlextResult.ok(updated_report)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get report: {e}")

    async def list_reports(
        self,
        analysis_id: str,
    ) -> FlextResult[list[QualityReport]]:
        """List reports for an analysis.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of reports or error

        """
        try:
            reports = [
                r for r in self._reports.values() if r.analysis_id == analysis_id
            ]
            return FlextResult.ok(reports)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to list reports {e}")

    async def delete_report(self, report_id: str) -> FlextResult[bool]:
        """Delete a report.

        Args:
            report_id: Report unique identifier

        Returns:
            FlextResult containing success status or error

        """
        try:
            if report_id in self._reports:
                del self._reports[report_id]
                return FlextResult.ok(True)
            return FlextResult.fail("Report not found")
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to delete report: {e}")


# Implementation classes for dependency injection containers
# These wrap the main services with specific interface implementations


# Base implementation for services with common DI pattern - DRY principle
class BasePortService:
    """Base service with port and repository injection.

    DRY: Eliminates duplicate constructor pattern across services.
    SOLID: Dependency inversion principle.
    """

    def __init__(
        self,
        port: object | None = None,
        repository: object | None = None,
    ) -> None:
        self._port = port
        self._repository = repository


class AnalysisServiceImpl:
    """Implementation of analysis service for DI container."""

    def __init__(self) -> None:
        self._analysis_service = QualityAnalysisService()

    async def analyze_project(self, project_id: str) -> FlextResult[QualityAnalysis]:
        """Analyze project by ID."""
        return await self._analysis_service.create_analysis(
            project_id=project_id,
        )


class SecurityAnalyzerServiceImpl(BasePortService):
    """Implementation of security analyzer service for DI container."""

    async def analyze_security(
        self,
        project_path: str,
    ) -> FlextResult[dict[str, object]]:
        """Analyze security issues in project."""
        try:
            from pathlib import Path

            from flext_quality.backends.external_backend import ExternalBackend

            # Use the generic external backend for security analysis
            backend = ExternalBackend()

            # Read project files and analyze with bandit
            project_path_obj = Path(project_path)
            security_issues = []

            if project_path_obj.exists():
                # For each Python file, run security analysis
                for py_file in project_path_obj.rglob("*.py"):
                    try:
                        code = py_file.read_text(encoding="utf-8")
                        result = backend.analyze(code, py_file, tool="bandit")
                        if "issues" in result:
                            security_issues.extend(result["issues"])
                    except (OSError, UnicodeDecodeError):
                        # Skip files that can't be read
                        continue

            return FlextResult.ok({
                "security_issues": security_issues,
                "project_path": project_path,
                "tool": "bandit",
                "total_issues": len(security_issues),
            })
        except Exception as e:
            return FlextResult.fail(f"Security analysis failed: {e}")


class LintingServiceImpl(BasePortService):
    """Implementation of linting service for DI container."""

    async def run_linting(self, project_path: str) -> FlextResult[dict[str, object]]:
        """Run linting analysis on project."""
        try:
            from pathlib import Path

            from flext_quality.backends.external_backend import ExternalBackend

            # Use the generic external backend for linting analysis
            backend = ExternalBackend()

            # Read project files and analyze with ruff
            project_path_obj = Path(project_path)
            linting_issues = []

            if project_path_obj.exists():
                # For each Python file, run linting analysis
                for py_file in project_path_obj.rglob("*.py"):
                    try:
                        code = py_file.read_text(encoding="utf-8")
                        result = backend.analyze(code, py_file, tool="ruff")
                        if "issues" in result:
                            linting_issues.extend(result["issues"])
                    except (OSError, UnicodeDecodeError):
                        # Skip files that can't be read
                        continue

            return FlextResult.ok({
                "linting_issues": linting_issues,
                "project_path": project_path,
                "tool": "ruff",
                "total_issues": len(linting_issues),
            })
        except Exception as e:
            return FlextResult.fail(f"Linting analysis failed: {e}")


class ReportGeneratorServiceImpl:
    """Implementation of report generator service for DI container."""

    def __init__(self) -> None:
        self._report_service = QualityReportService()

    async def generate_report(
        self,
        analysis_id: str,
        report_type: str,
    ) -> FlextResult[QualityReport]:
        """Generate report for analysis."""
        return await self._report_service.create_report(
            analysis_id=analysis_id,
            report_type=report_type,
        )
