"""Utility classes and functions for FLEXT Quality project.

This module provides reusable utility classes with static methods for common
operations across the quality analysis system, following FLEXT patterns.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

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
    IssueType = SecurityIssue | ComplexityIssue | DeadCodeIssue | DuplicationIssue
    IssueList = list[IssueType]
else:
    IssueType = object
    IssueList = list[object]


class FlextQualityUtilities:
    """Utility class for FLEXT Quality operations."""

    @staticmethod
    def is_issue_list(value: object) -> bool:
        """Type guard to check if value is a list of quality issues."""
        if not isinstance(value, list):
            return False
        # For empty lists, assume they are valid issue lists
        if not value:
            return True
        # Check first item to determine if it's likely an issue list
        first_item = value[0]
        return hasattr(first_item, "file_path") and hasattr(first_item, "message")

    @staticmethod
    def safe_issue_list(value: object) -> list[object]:
        """Safely convert value to typed issue list."""
        if FlextQualityUtilities.is_issue_list(value):
            return value  # type: ignore[return-value]
        return []

    @staticmethod
    def get_issue_summary(issue: object) -> str:
        """Get a formatted summary string for any issue type."""
        # Check if it's a DuplicationIssue by checking for 'files' attribute
        if hasattr(issue, "files") and hasattr(issue, "similarity"):
            files = getattr(issue, "files", [])
            files_str = ", ".join(files[:2]) if files else "unknown"
            return f"Duplicated in: {files_str}"

        # For all other issue types (SecurityIssue, ComplexityIssue, DeadCodeIssue)
        if hasattr(issue, "file_path") and hasattr(issue, "line_number"):
            file_path = getattr(issue, "file_path", "unknown")
            line_number = getattr(issue, "line_number", "?")
            return f"{file_path}:{line_number}"

        return "Unknown location"


class FlextReportUtilities:
    """Utility class for report generation operations."""

    @staticmethod
    def format_issue_categories(results: object) -> dict[str, list[object]]:
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
    def create_report_lines() -> list[str]:
        """Create a new report lines list with proper typing."""
        return []

    @staticmethod
    def safe_extend_lines(target: list[str], source: object) -> None:
        """Safely extend target list with source items."""
        if isinstance(source, list):
            str_items = [str(item) for item in source]
            target.extend(str_items)


class FlextTestUtilities:
    """Utility class for testing with real code execution."""

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
                "def broken_function(\n  # Missing closing parenthesis", encoding="utf-8"
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
    """Utility class for analysis operations."""

    @staticmethod
    def calculate_real_score(analysis_results: AnalysisResults | object) -> float:
        """Calculate quality score from real analysis results."""
        if not hasattr(analysis_results, "overall_metrics"):
            return 0.0

        metrics = getattr(analysis_results, "overall_metrics", None)
        if metrics is None:
            return 0.0
        return getattr(metrics, "quality_score", 0.0)

    @staticmethod
    def count_real_issues(analysis_results: AnalysisResults | object) -> int:
        """Count total issues from real analysis results."""
        if hasattr(analysis_results, "total_issues"):
            total_issues_attr = getattr(analysis_results, "total_issues", 0)
            return (
                int(total_issues_attr)
                if isinstance(total_issues_attr, (int, float))
                else 0
            )
        return 0


__all__ = [
    "FlextAnalysisUtilities",
    "FlextQualityUtilities",
    "FlextReportUtilities",
    "FlextTestUtilities",
    "IssueList",
    "IssueType",
]
