"""Quality domain protocols following FLEXT_REFACTORING_PROMPT.md patterns.

Follows FLEXT_REFACTORING_PROMPT.md by eliminating duplication and using centralized protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextCore

# Use FlextCore.Protocols from flext-core instead of local definitions
# Following FLEXT_REFACTORING_PROMPT.md to eliminate duplication

# Analysis services use Domain.Service protocol
AnalysisService = FlextCore.Protocols.Domain.Service
SecurityAnalyzerService = FlextCore.Protocols.Domain.Service
LintingService = FlextCore.Protocols.Domain.Service
ComplexityAnalyzerService = FlextCore.Protocols.Domain.Service
DeadCodeDetectorService = FlextCore.Protocols.Domain.Service
DuplicateDetectorService = FlextCore.Protocols.Domain.Service
MetricsCollectorService = FlextCore.Protocols.Domain.Service

# Report generation uses Application.Handler protocol
ReportGeneratorService = FlextCore.Protocols.Application.Handler[object, str]


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
