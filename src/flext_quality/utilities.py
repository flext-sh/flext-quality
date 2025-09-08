"""Quality-specific utility classes extending flext-core FlextUtilities.

Uses flext-core FlextUtilities as base and adds only quality-specific utilities.
Follows FLEXT patterns: Multiple classes per module, extending core functionality.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, cast

from flext_core.utilities import FlextUtilities  # Use flext-core utilities as base

if TYPE_CHECKING:
    from flext_quality.analysis_types import (
        AnalysisResults,
        ComplexityIssue,
        DeadCodeIssue,
        DuplicationIssue,
        SecurityIssue,
    )

# Type aliases for better readability
if TYPE_CHECKING:
    QualityIssueType = (
        SecurityIssue | ComplexityIssue | DeadCodeIssue | DuplicationIssue
    )
    QualityIssueList = list[QualityIssueType]
else:
    QualityIssueType = object
    QualityIssueList = FlextTypes.Core.List


class FlextQualityUtilities:
    """Quality-specific utilities using FlextUtilities composition.

    Uses composition with all FlextUtilities functionalities while adding
    quality-specific functionality. Eliminates inheritance complexity.
    """

    @staticmethod
    def is_quality_issue_list(value: object) -> bool:
        """Type guard to check if value is a list of quality issues."""
        # Use native Python type checking since FlextUtilities doesn't have is_list
        if not isinstance(value, list):
            return False
        if not value:  # Empty list is valid
            return True
        # Quality-specific check: issues have file_path and message
        # Cast to list for safe access after isinstance check
        value_list = cast("FlextTypes.Core.List", value)
        first_item = value_list[0]
        return hasattr(first_item, "file_path") and hasattr(first_item, "message")

    @staticmethod
    def safe_issue_list(value: object) -> FlextTypes.Core.List:
        """Safely convert value to typed issue list."""
        if FlextQualityUtilities.is_quality_issue_list(value):
            return value
        return []

    @staticmethod
    def get_issue_summary(issue: object) -> str:
        """Get a formatted summary string for any issue type."""
        # Use FlextUtilities safe conversions instead of raw getattr
        if hasattr(issue, "files") and hasattr(issue, "similarity"):
            files = getattr(issue, "files", [])
            if files and isinstance(files, list):
                files_str = ", ".join(str(f) for f in files[:2])
                return f"Duplicated in: {files_str}"

        # For all other issue types - use safe string conversion
        if hasattr(issue, "file_path") and hasattr(issue, "line_number"):
            file_path = FlextUtilities.TextProcessor.safe_string(
                getattr(issue, "file_path", ""), "unknown"
            )
            line_number = FlextUtilities.TextProcessor.safe_string(
                getattr(issue, "line_number", ""), "?"
            )
            return f"{file_path}:{line_number}"

        return "Unknown location"


class FlextReportUtilities:
    """Report generation utilities using FlextUtilities composition.

    Uses composition with all FlextUtilities functionalities for
    quality-specific report formatting.
    """

    @staticmethod
    def format_issue_categories(results: object) -> dict[str, FlextTypes.Core.List]:
        """Format issue categories with proper typing."""
        return {
            "SECURITY": FlextQualityUtilities.safe_issue_list(
                getattr(results, "security_issues", [])
            ),
            "COMPLEXITY": FlextQualityUtilities.safe_issue_list(
                getattr(results, "complexity_issues", [])
            ),
            "DEAD CODE": FlextQualityUtilities.safe_issue_list(
                getattr(results, "dead_code_issues", [])
            ),
            "DUPLICATION": FlextQualityUtilities.safe_issue_list(
                getattr(results, "duplication_issues", [])
            ),
        }

    @staticmethod
    def create_report_lines() -> FlextTypes.Core.StringList:
        """Create a new report lines list with proper typing."""
        return []

    @staticmethod
    def safe_extend_lines(target: FlextTypes.Core.StringList, source: object) -> None:
        """Safely extend target list with source items."""
        # Use native Python type checking since FlextUtilities doesn't have is_list
        if isinstance(source, list):
            str_items = [
                FlextUtilities.TextProcessor.safe_string(item, "") for item in source
            ]
            target.extend(str_items)


class FlextTestUtilities:
    """Testing utilities using FlextUtilities composition.

    Uses composition with all FlextUtilities functionalities for
    quality-specific testing utilities.
    """

    @staticmethod
    def create_test_file_with_issues(file_path: Path, issue_type: str) -> None:
        """Create test files with specific types of real issues."""
        content_map = {
            "complexity": '''
def complex_function(x):
    """Function with high complexity - real code."""
    if x > 10:
        if x > 20:
            if x > 30:
                if x > 40:
                    if x > 50:
                        return "very high"
                    else:
                        return "high"
                else:
                    return "medium-high"
            else:
                return "medium"
        else:
            return "low-medium"
    else:
        return "low"
''',
            "security": '''
import os
import subprocess

def unsafe_function(user_input):
    """Function with real security issues."""
    # SQL injection vulnerability (real)
    query = f"SELECT * FROM users WHERE name = '{user_input}'"

    # Command injection vulnerability (real)
    os.system(f"ls {user_input}")

    # Another command injection (real)
    subprocess.call(f"echo {user_input}", shell=True)

    return query
''',
            "dead_code": '''
def used_function():
    """This function is used."""
    return "active"

def unused_function():
    """This function is never called - dead code."""
    unused_variable = "this is dead code"
    return unused_variable

def another_unused():
    """Another unused function."""
    pass

# This is the only function that gets called
result = used_function()
''',
            "duplication": '''
def process_data_type_a(data):
    """Process data type A."""
    if not data:
        return None
    processed = []
    for item in data:
        if item > 0:
            processed.append(item * 2)
    return processed

def process_data_type_b(data):
    """Process data type B - duplicated logic."""
    if not data:
        return None
    processed = []
    for item in data:
        if item > 0:
            processed.append(item * 2)
    return processed
''',
        }

        content = content_map.get(issue_type, "# Basic test file")
        file_path.write_text(dedent(content).strip(), encoding="utf-8")

    @staticmethod
    def create_failing_file(file_path: Path, error_type: str) -> None:
        """Create files that will cause real analysis failures."""
        if error_type == "syntax_error":
            file_path.write_text(
                "def broken_function(\n  # Missing closing parenthesis",
                encoding="utf-8",
            )
        elif error_type == "encoding_error":
            # Create a file with invalid UTF-8
            file_path.write_bytes(b"# Invalid UTF-8: \xff\xfe")
        elif error_type == "permission_error":
            file_path.write_text("# Normal content", encoding="utf-8")
            file_path.chmod(0o000)  # Remove all permissions
        else:
            file_path.write_text("# Test file", encoding="utf-8")


class FlextAnalysisUtilities:
    """Analysis utilities using FlextUtilities composition.

    Uses composition with all FlextUtilities functionalities for
    quality-specific analysis utilities.
    """

    @staticmethod
    def calculate_real_score(analysis_results: AnalysisResults | object) -> float:
        """Calculate quality score from real analysis results."""
        # Use FlextUtilities for safe attribute access
        if not hasattr(analysis_results, "overall_metrics"):
            return 0.0

        metrics = getattr(analysis_results, "overall_metrics", None)
        if metrics is None:
            return 0.0

        # Use safe float conversion from FlextUtilities
        score = getattr(metrics, "quality_score", 0.0)
        return FlextUtilities.Conversions.safe_float(score, 0.0)

    @staticmethod
    def count_real_issues(analysis_results: AnalysisResults | object) -> int:
        """Count total issues from real analysis results."""
        # Use FlextUtilities for safe type conversion
        if hasattr(analysis_results, "total_issues"):
            total_issues_attr = getattr(analysis_results, "total_issues", 0)
            return FlextUtilities.Conversions.safe_int(total_issues_attr, 0)
        return 0


# Backward compatibility aliases - classes are now separate (correct FLEXT pattern)
# No aliases needed since classes exist independently

# Legacy compatibility aliases
IssueType = QualityIssueType
IssueList = QualityIssueList

# Export CONSOLIDATED class and aliases
__all__ = [
    # Backward compatibility
    "FlextAnalysisUtilities",
    "FlextQualityUtilities",
    "FlextReportUtilities",
    "FlextTestUtilities",
    # Legacy compatibility
    "IssueList",
    "IssueType",
    "QualityIssueList",
    "QualityIssueType",
]
