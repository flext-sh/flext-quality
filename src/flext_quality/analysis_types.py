"""FLEXT Quality Analysis Types - Re-exports from models for backward compatibility.

This module provides backward compatibility imports for analysis result types.
All models are now defined in FlextQualityModels to follow FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from .models import FlextQualityModels

# Re-export classes from FlextQualityModels for backward compatibility
# Note: Many classes consolidated into fewer using mixins and composition
FileAnalysisResult = FlextQualityModels.AnalysisResults  # Consolidated
CodeIssue = FlextQualityModels.IssueModel  # Consolidated
ComplexityIssue = FlextQualityModels.IssueModel  # Consolidated
SecurityIssue = FlextQualityModels.IssueModel  # Consolidated
DeadCodeIssue = FlextQualityModels.IssueModel  # Consolidated
DuplicationIssue = FlextQualityModels.IssueModel  # Consolidated
Dependency = FlextQualityModels.Dependency
TestResults = FlextQualityModels.TestResults
OverallMetrics = FlextQualityModels.OverallMetrics
AnalysisResults = FlextQualityModels.AnalysisResults


# For backward compatibility, create a dummy class with nested classes
class FlextQualityAnalysisTypes:
    """Backward compatibility class - all models moved to FlextQualityModels."""

    # Consolidated models for backward compatibility
    FileAnalysisResult = FlextQualityModels.AnalysisResults
    CodeIssue = FlextQualityModels.IssueModel
    ComplexityIssue = FlextQualityModels.IssueModel
    SecurityIssue = FlextQualityModels.IssueModel
    DeadCodeIssue = FlextQualityModels.IssueModel
    DuplicationIssue = FlextQualityModels.IssueModel
    Dependency = FlextQualityModels.Dependency
    TestResults = FlextQualityModels.TestResults
    OverallMetrics = FlextQualityModels.OverallMetrics
    AnalysisResults = FlextQualityModels.AnalysisResults


# Export all classes
__all__ = [
    "AnalysisResults",
    "CodeIssue",
    "ComplexityIssue",
    "DeadCodeIssue",
    "Dependency",
    "DuplicationIssue",
    "FileAnalysisResult",
    "FlextQualityAnalysisTypes",
    "OverallMetrics",
    "SecurityIssue",
    "TestResults",
]
