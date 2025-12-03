"""Quality domain protocols following FLEXT_REFACTORING_PROMPT.md patterns.

Follows FLEXT_REFACTORING_PROMPT.md by eliminating duplication and using centralized protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import p

# Use p from flext-core instead of local definitions
# Following FLEXT_REFACTORING_PROMPT.md to eliminate duplication

# Analysis services use Domain.Service protocol
AnalysisService = p.Service
SecurityAnalyzerService = p.Service
LintingService = p.Service
ComplexityAnalyzerService = p.Service
DeadCodeDetectorService = p.Service
DuplicateDetectorService = p.Service
MetricsCollectorService = p.Service

# Report generation uses Application.Handler protocol
ReportGeneratorService = p.Handler[object]


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
