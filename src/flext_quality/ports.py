"""Quality domain protocols following FLEXT_REFACTORING_PROMPT.md patterns.

Follows FLEXT_REFACTORING_PROMPT.md by eliminating duplication and using centralized protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextProtocols

# Use FlextProtocols from flext-core instead of local definitions
# Following FLEXT_REFACTORING_PROMPT.md to eliminate duplication

# Analysis services use Domain.Service protocol
AnalysisService = FlextProtocols.Service
SecurityAnalyzerService = FlextProtocols.Service
LintingService = FlextProtocols.Service
ComplexityAnalyzerService = FlextProtocols.Service
DeadCodeDetectorService = FlextProtocols.Service
DuplicateDetectorService = FlextProtocols.Service
MetricsCollectorService = FlextProtocols.Service

# Report generation uses Application.Handler protocol
ReportGeneratorService = FlextProtocols.Handler[object]


# Export protocol aliases
__all__ = [
    "AnalysisService",
    "ComplexityAnalyzerService",
    "DeadCodeDetectorService",
    "DuplicateDetectorService",
    "LintingService",
    "MetricsCollectorService",
    "ReportGeneratorService",
    "SecurityAnalyzerService",
]
