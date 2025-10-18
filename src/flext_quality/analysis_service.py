"""FLEXT Quality Analysis Service - Focused analysis management service.

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
Analysis = FlextQualityEntities.Analysis


class FlextQualityAnalysisService(FlextService[None]):
    """Service for managing quality analyses using flext-core patterns.

    Single responsibility: Analysis lifecycle management
    """

    def __init__(self) -> None:
        """Initialize analysis service."""
        super().__init__()
        self.logger = FlextLogger(__name__)

    @override
    def execute(self, data: object) -> FlextResult[None]:
        """Execute service operation - not used for this service type."""
        return FlextResult[None].fail(
            "AnalysisService does not support execute operation"
        )

    def create_analysis(
        self,
        project_id: str,
        config: dict[str, object] | None = None,
    ) -> FlextResult[Analysis]:
        """Create a new quality analysis."""
        try:
            analysis = Analysis(
                id=f"{project_id}_analysis_{len(self._get_analyses())}",
                project_id=project_id,
                status="pending",
                analysis_config=config or {},
            )

            self.logger.info("Created analysis: %s", analysis.id)
            return FlextResult[Analysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to create analysis")
            return FlextResult[Analysis].fail(
                f"Failed to create analysis: {e}",
            )

    def get_analyses_by_project(
        self,
        project_id: str,
    ) -> FlextResult[list[Analysis]]:
        """Get all analyses for a project."""
        try:
            # Note: This would need access to an analysis repository
            # For now, return empty list
            analyses = []
            return FlextResult[list[Analysis]].ok(analyses)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Failed to list analyses")
            return FlextResult[list[Analysis]].fail(
                f"Failed to list analyses: {e}",
            )

    def _get_analyses(self) -> list[Analysis]:
        """Get all analyses (internal helper)."""
        # Note: This would need access to an analysis repository
        # For now, return empty list
        return []
