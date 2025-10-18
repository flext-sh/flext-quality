"""FLEXT Quality Services - Application services orchestration following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextContainer,
    FlextContext,
    FlextLogger,
    FlextResult,
    FlextService,
)

from .analysis_service import FlextQualityAnalysisService
from .issue_service import FlextQualityIssueService
from .project_service import FlextQualityProjectService
from .report_service import FlextQualityReportService


class FlextQualityServices(FlextService[None]):
    """Unified quality services orchestration following FLEXT patterns.

    Single responsibility: Quality domain services coordination
    Uses composition of focused service modules.
    """

    def __init__(self) -> None:
        """Initialize quality services with flext-core integration."""
        super().__init__()
        # Complete flext-core integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self.logger = FlextLogger(__name__)

        # Initialize focused service modules
        self._project_service = FlextQualityProjectService()
        self._issue_service = FlextQualityIssueService()
        self._analysis_service = FlextQualityAnalysisService()
        self._report_service = FlextQualityReportService()

    def execute(self, data: object) -> FlextResult[None]:
        """Execute services orchestration."""
        return FlextResult[None].ok(None)

    # =============================================================================
    # SERVICE ACCESSORS - Clean delegation to focused services
    # =============================================================================

    def get_project_service(self) -> FlextQualityProjectService:
        """Get project service instance."""
        return self._project_service

    def get_issue_service(self) -> FlextQualityIssueService:
        """Get issue service instance."""
        return self._issue_service

    def get_analysis_service(self) -> FlextQualityAnalysisService:
        """Get analysis service instance."""
        return self._analysis_service

    def get_report_service(self) -> FlextQualityReportService:
        """Get report service instance."""
        return self._report_service


# Export all classes via __all__
__all__ = [
    # Unified services class - main entry point
    "FlextQualityServices",
]
