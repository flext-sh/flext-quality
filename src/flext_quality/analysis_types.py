"""FLEXT Quality Analysis Types - Re-exports from models using proper inheritance.

This module provides backward compatibility imports for analysis result types
using proper class inheritance instead of aliases.
All models are now defined in FlextQualityModels to follow FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from .models import FlextQualityModels


# Re-export classes from FlextQualityModels using proper inheritance
# Note: Many classes consolidated into fewer using mixins and composition
class FileAnalysisResult(FlextQualityModels.AnalysisResults):
    """File analysis result model - inherits from FlextQualityModels.AnalysisResults."""


class CodeIssue(FlextQualityModels.IssueModel):
    """Code issue model - inherits from FlextQualityModels.IssueModel."""


class ComplexityIssue(FlextQualityModels.IssueModel):
    """Complexity issue model - inherits from FlextQualityModels.IssueModel."""


class SecurityIssue(FlextQualityModels.IssueModel):
    """Security issue model - inherits from FlextQualityModels.IssueModel."""


class DeadCodeIssue(FlextQualityModels.IssueModel):
    """Dead code issue model - inherits from FlextQualityModels.IssueModel."""


class DuplicationIssue(FlextQualityModels.IssueModel):
    """Duplication issue model - inherits from FlextQualityModels.IssueModel."""


class Dependency(FlextQualityModels.Dependency):
    """Dependency model - inherits from FlextQualityModels.Dependency."""


class TestResults(FlextQualityModels.TestResults):
    """Test results model - inherits from FlextQualityModels.TestResults."""


class OverallMetrics(FlextQualityModels.OverallMetrics):
    """Overall metrics model - inherits from FlextQualityModels.OverallMetrics."""


class AnalysisResults(FlextQualityModels.AnalysisResults):
    """Analysis results model - inherits from FlextQualityModels.AnalysisResults."""


# For backward compatibility, create a class with nested classes using inheritance
class FlextQualityAnalysisTypes:
    """Backward compatibility class - all models moved to FlextQualityModels."""

    # Consolidated models for backward compatibility using inheritance
    class FileAnalysisResult(FlextQualityModels.AnalysisResults):
        """File analysis result model."""

    class CodeIssue(FlextQualityModels.IssueModel):
        """Code issue model."""

    class ComplexityIssue(FlextQualityModels.IssueModel):
        """Complexity issue model."""

    class SecurityIssue(FlextQualityModels.IssueModel):
        """Security issue model."""

    class DeadCodeIssue(FlextQualityModels.IssueModel):
        """Dead code issue model."""

    class DuplicationIssue(FlextQualityModels.IssueModel):
        """Duplication issue model."""

    class Dependency(FlextQualityModels.Dependency):
        """Dependency model."""

    class TestResults(FlextQualityModels.TestResults):
        """Test results model."""

    class OverallMetrics(FlextQualityModels.OverallMetrics):
        """Overall metrics model."""

    class AnalysisResults(FlextQualityModels.AnalysisResults):
        """Analysis results model."""


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
