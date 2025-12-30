"""Progressive Reporter for Hook Violations.

Improves UX of error messages by:
1. Showing BLOCKING violations first (TOP 3)
2. Grouping violations by type
3. Providing actionable guidance
4. Showing count of additional violations

Usage:
    from flext_quality.hooks.reporter import ProgressiveReporter

    reporter = ProgressiveReporter()
    formatted = reporter.format(violations)
    print(formatted)
"""

from __future__ import annotations

from typing import NotRequired, TypedDict


class ViolationDict(TypedDict):
    """Violation information dict."""

    code: str
    message: str
    line: int | str
    blocking: NotRequired[bool]
    file: NotRequired[str]
    snippet: NotRequired[str]
    name: NotRequired[str]


class ProgressiveReporter:
    """Progressive violation reporter for hook validation.

    Shows violations in order of importance:
    1. BLOCKING violations (must fix first)
    2. Top 3 violations
    3. Summary of remaining violations
    """

    MAX_INITIAL_VIOLATIONS = 3

    def __init__(self) -> None:
        """Initialize reporter."""
        self.max_violations = self.MAX_INITIAL_VIOLATIONS

    def format(self, violations: list[ViolationDict]) -> str:
        """Format violations for user-friendly display.

        Args:
            violations: List of violation dicts with keys:
                - code: Violation code (e.g., "ARG002")
                - message: Violation message
                - line: Line number
                - file: File path (optional)
                - blocking: Whether violation blocks execution (optional)

        Returns:
            Formatted violation message for display

        """
        if not violations:
            return "✅ No violations found"

        lines: list[str] = []

        # Separate blocking from non-blocking
        blocking = [v for v in violations if v.get("blocking", False)]
        warnings = [v for v in violations if not v.get("blocking", False)]

        # Show blocking violations first (TOP 3)
        if blocking:
            lines.extend([
                f"🚫 BLOCKING VIOLATIONS ({len(blocking)} found):",
                "   Fix these FIRST - they prevent execution:\n",
            ])

            for v in blocking[: self.max_violations]:
                code = v.get("code", "UNKNOWN")
                msg = v.get("message", "No message")
                line_num = v.get("line", "?")
                lines.append(f"   [{code}] Line {line_num}: {msg}")

            if len(blocking) > self.max_violations:
                remaining = len(blocking) - self.max_violations
                lines.append(f"\n   ... +{remaining} more blocking violations")

        # Show warnings if no blocking violations
        if not blocking and warnings:
            lines.extend([
                f"⚠️  WARNING VIOLATIONS ({len(warnings)} found):",
                "   Consider fixing these:\n",
            ])

            for v in warnings[: self.max_violations]:
                code = v.get("code", "UNKNOWN")
                msg = v.get("message", "No message")
                line_num = v.get("line", "?")
                lines.append(f"   [{code}] Line {line_num}: {msg}")

            if len(warnings) > self.max_violations:
                remaining = len(warnings) - self.max_violations
                lines.append(f"\n   ... +{remaining} more warnings")

        # Add guidance
        lines.extend([
            "\n📚 For detailed information:",
            "   • Run: ./scripts/post_edit_validate.sh <backup_id> <file>",
            "   • See: ~/.claude/CLAUDE.md → Code Quality Standards",
        ])

        return "\n".join(lines)

    def format_compact(self, violations: list[ViolationDict]) -> str:
        """Format violations as single-line summary.

        Args:
            violations: List of violation dicts

        Returns:
            Single-line violation summary

        """
        if not violations:
            return "✅ No violations"

        blocking_count = len([v for v in violations if v.get("blocking", False)])
        warning_count = len(violations) - blocking_count

        if blocking_count:
            return f"🚫 {blocking_count} blocking + {warning_count} warnings"

        return f"⚠️  {warning_count} warnings"

    def group_by_code(
        self, violations: list[ViolationDict]
    ) -> dict[str, list[ViolationDict]]:
        """Group violations by violation code.

        Args:
            violations: List of violation dicts

        Returns:
            Dict mapping violation code -> list of violations

        """
        grouped: dict[str, list[ViolationDict]] = {}

        for v in violations:
            code = v.get("code", "UNKNOWN")
            if code not in grouped:
                grouped[code] = []
            grouped[code].append(v)

        return grouped
