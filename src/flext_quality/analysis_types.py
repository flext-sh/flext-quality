"""FLEXT Quality Analysis Types - Re-exports from models for backward compatibility.

This module provides backward compatibility imports for analysis result types.
All models are now defined in FlextQualityModels to follow FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from .models import FlextQualityModels

# Re-export classes from FlextQualityModels for backward compatibility
FileAnalysisResult = FlextQualityModels.FileAnalysisResult
CodeIssue = FlextQualityModels.CodeIssue
ComplexityIssue = FlextQualityModels.ComplexityIssue
SecurityIssue = FlextQualityModels.SecurityIssue
DeadCodeIssue = FlextQualityModels.DeadCodeIssue
DuplicationIssue = FlextQualityModels.DuplicationIssue
Dependency = FlextQualityModels.Dependency
TestResults = FlextQualityModels.TestResults
OverallMetrics = FlextQualityModels.OverallMetrics
AnalysisResults = FlextQualityModels.AnalysisResults


# For backward compatibility, create a dummy class with nested classes
class FlextQualityAnalysisTypes:
    """Backward compatibility class - all models moved to FlextQualityModels."""

    FileAnalysisResult = FileAnalysisResult
    CodeIssue = CodeIssue
    ComplexityIssue = ComplexityIssue
    SecurityIssue = SecurityIssue
    DeadCodeIssue = DeadCodeIssue
    DuplicationIssue = DuplicationIssue
    Dependency = Dependency
    TestResults = TestResults
    OverallMetrics = OverallMetrics
    AnalysisResults = AnalysisResults


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
