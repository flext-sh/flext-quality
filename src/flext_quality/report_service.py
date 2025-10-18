"""FLEXT Quality Report Service - Focused report management service.

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
Report = FlextQualityEntities.Report


class FlextQualityReportService(FlextService[None]):
    """Service for managing quality reports using flext-core patterns.

    Single responsibility: Report lifecycle management
    """

    def __init__(self) -> None:
        """Initialize report service."""
        super().__init__()
        self.logger = FlextLogger(__name__)

    @override
    def execute(self, data: object) -> FlextResult[None]:
        """Execute service operation - not used for this service type."""
        return FlextResult[None].fail(
            "ReportService does not support execute operation"
        )

    def create_report(
        self,
        analysis_id: str,
        format_type: str,
        content: str,
        file_path: str | None = None,
        _metadata: dict[str, object] | None = None,
    ) -> FlextResult[Report]:
        """Create a new quality report."""
        try:
            report = Report(
                id=f"{analysis_id}_report_{len(self._get_reports())}",
                analysis_id=analysis_id,
                format_type=format_type,
                report_format="summary",
                report_path=file_path,
                report_size_bytes=len(content.encode()) if content else 0,
            )

            self.logger.info("Created report: %s", report.id)
            return FlextResult[Report].ok(report)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to create report")
            return FlextResult[Report].fail(
                f"Failed to create report: {e}",
            )

    def get_reports_by_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[Report]]:
        """Get all reports for an analysis."""
        try:
            # Note: This would need access to a report repository
            # For now, return empty list
            reports = []
            return FlextResult[list[Report]].ok(reports)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to list reports")
            return FlextResult[list[Report]].fail(
                f"Failed to list reports: {e}",
            )

    def delete_report(self, report_id: str) -> FlextResult[bool]:
        """Delete a quality report."""
        try:
            # Note: This would need access to a report repository
            # For now, return not found
            return FlextResult[bool].fail("Report not found")
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to delete report")
            return FlextResult[bool].fail(f"Failed to delete report: {e}")

    def _get_reports(self) -> list[Report]:
        """Get all reports (internal helper)."""
        # Note: This would need access to a report repository
        # For now, return empty list
        return []
