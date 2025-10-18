"""FLEXT Quality Issue Service - Focused issue management service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)

from .entities import FlextQualityEntities

# Direct access to entities (no wrappers)
Issue = FlextQualityEntities.Issue


class FlextQualityIssueService(FlextService[None]):
    """Service for managing quality issues using flext-core patterns.

    Single responsibility: Issue lifecycle management
    """

    def __init__(self) -> None:
        """Initialize issue service."""
        super().__init__()
        self.logger = FlextLogger(__name__)

    @override
    def execute(self, data: object) -> FlextResult[None]:
        """Execute service operation - not used for this service type."""
        return FlextResult[None].fail("IssueService does not support execute operation")

    def create_issue(
        self,
        analysis_id: str,
        file_path: str,
        line_number: int,
        column_number: int | None,
        severity: str,
        issue_type: str,
        message: str,
        rule: str | None = None,
        _source: str = "ruff",
    ) -> FlextResult[Issue]:
        """Create a new quality issue."""
        try:
            # Create issue ID
            issue_id = f"{analysis_id}:{file_path}:{line_number}"

            # Create quality issue
            issue = Issue(
                id=issue_id,
                analysis_id=analysis_id,
                file_path=file_path,
                line_number=line_number,
                column_number=column_number,
                issue_type=issue_type,
                severity=severity,
                message=message,
                rule_id=rule or "unknown",
            )

            self.logger.debug(f"Created quality issue: {issue_id}")
            return FlextResult[Issue].ok(issue)
        except Exception as e:
            self.logger.exception("Failed to create issue")
            return FlextResult[Issue].fail(
                f"Failed to create issue: {e}",
            )

    def get_issues_by_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[Issue]]:
        """Get all issues for a specific analysis."""
        try:
            # Note: This would need access to an issue repository
            # For now, return empty list
            issues = []
            return FlextResult[list[Issue]].ok(issues)
        except Exception as e:
            self.logger.exception(
                "Failed to get issues for analysis %s",
                analysis_id,
            )
            return FlextResult[list[Issue]].fail(
                f"Failed to get issues: {e}",
            )

    def get_issue(
        self,
        issue_id: str,
    ) -> FlextResult[Issue | None]:
        """Get a specific issue by ID."""
        try:
            # Note: This would need access to an issue repository
            # For now, return None
            return FlextResult[Issue | None].ok(None)
        except Exception as e:
            self.logger.exception(f"Failed to get issue {issue_id}")
            return FlextResult[Issue | None].fail(
                f"Failed to get issue: {e}",
            )

    def mark_fixed(
        self,
        issue_id: str,
    ) -> FlextResult[Issue]:
        """Mark an issue as fixed."""
        try:
            # Note: This would need access to an issue repository
            # For now, return not found
            return FlextResult[Issue].fail(
                f"Issue not found: {issue_id}",
            )
        except Exception as e:
            self.logger.exception(f"Failed to mark issue as fixed {issue_id}")
            return FlextResult[Issue].fail(
                f"Failed to mark issue as fixed: {e}",
            )

    def suppress_issue(
        self,
        issue_id: str,
        reason: str,
    ) -> FlextResult[Issue]:
        """Suppress a specific issue."""
        try:
            # Note: This would need access to an issue repository
            # For now, return not found
            return FlextResult[Issue].fail(
                f"Issue not found: {issue_id}",
            )
        except Exception as e:
            self.logger.exception(f"Failed to suppress issue {issue_id}")
            return FlextResult[Issue].fail(
                f"Failed to suppress issue: {e}",
            )

    def unsuppress_issue(
        self,
        issue_id: str,
    ) -> FlextResult[Issue]:
        """Unsuppress a quality issue."""
        try:
            # Note: This would need access to an issue repository
            # For now, return not found
            return FlextResult[Issue].fail("Issue not found")
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to unsuppress issue")
            return FlextResult[Issue].fail(
                f"Failed to unsuppress issue: {e}",
            )
