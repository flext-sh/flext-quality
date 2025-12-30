"""Progressive Reporter for Hook Violations and Messages.

Improves UX of error messages by:
1. Showing BLOCKING violations first (TOP 3)
2. Grouping violations by type
3. Supporting exit codes 0/1/2
3. Providing actionable guidance
4. Showing count of additional violations
5. JSON output formatting for hooks
6. Educational message generation

Usage:
    from flext_quality.hooks.reporter import ProgressiveReporter

    reporter = ProgressiveReporter()
    formatted = reporter.format(violations)
    print(formatted)

    # For hook output
    json_output = reporter.format_json(violations, "allow")
    print(json_output)
"""

from __future__ import annotations

import json
from typing import Any, NotRequired, TypedDict


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

    def format_json(
        self,
        violations: list[ViolationDict],
        decision: str = "allow",
        exit_code: int | None = None,
    ) -> str:
        """Format violations and decision as JSON for hook output.

        Args:
            violations: List of violation dicts
            decision: Hook decision ('allow', 'warn', 'block')
            exit_code: Optional exit code (0=allow, 1=warn, 2=block)

        Returns:
            JSON string with structured hook output

        """
        blocking_count = len([v for v in violations if v.get("blocking", False)])

        # CRITICAL: Override decision to "block" if blocking violations exist
        if blocking_count > 0 and decision != "block":
            decision = "block"

        if exit_code is None:
            # Infer exit code from decision (with blocking violations override)
            exit_code = {"allow": 0, "warn": 1, "block": 2}.get(decision, 0)
        elif blocking_count > 0:
            # Force exit_code=2 if blocking violations present
            exit_code = 2

        output: dict[str, Any] = {
            "decision": decision,
            "exit_code": exit_code,
            "reason": self._get_reason(decision, len(violations), blocking_count),
            "violations_count": len(violations),
            "blocking_count": blocking_count,
        }

        if violations:
            output["violations"] = violations

        return json.dumps(output)

    def format_educational_message(
        self,
        violations: list[ViolationDict],
        context: str = "code-quality",
    ) -> str:
        """Format educational message for learning from violations.

        Args:
            violations: List of violation dicts
            context: Context for message ('code-quality', 'security', 'testing')

        Returns:
            Educational message string

        """
        if not violations:
            return "✅ No violations found!\n\n"

        lines: list[str] = []

        # Header based on context
        headers = {
            "code-quality": "📚 Code Quality Learning",
            "security": "🔒 Security Patterns",
            "testing": "🧪 Testing Best Practices",
        }

        lines.extend([
            f"\n{headers.get(context, '📚 Learning')}",
            "=" * 50,
        ])

        # Group by code and provide education
        grouped = self.group_by_code(violations)

        for code, items in list(grouped.items())[:3]:  # Top 3 violation types
            lines.extend((
                f"\n📌 {code} ({len(items)} occurrence{'s' if len(items) > 1 else ''})",
                f"   Message: {items[0].get('message', 'N/A')}",
                "   How to fix: Review documentation and update code",
            ))

        if len(grouped) > 3:
            lines.append(f"\n... and {len(grouped) - 3} more violation types")

        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

    def _get_reason(
        self,
        decision: str,
        total_count: int,
        blocking_count: int,
    ) -> str:
        """Get human-readable reason for decision.

        Args:
            decision: Hook decision
            total_count: Total violations
            blocking_count: Blocking violations count

        Returns:
            Reason string

        """
        if decision == "block":
            return f"Execution blocked: {blocking_count} blocking violation(s) found"
        if decision == "warn":
            return f"Execution allowed with warnings: {total_count} violation(s) found"
        return "Execution allowed: no violations found"

    def format_summary(
        self,
        violations: list[ViolationDict],
        file_path: str | None = None,
    ) -> str:
        """Format concise summary of violations.

        Args:
            violations: List of violation dicts
            file_path: Optional file path for context

        Returns:
            Summary string

        """
        if not violations:
            return "✅ All checks passed"

        blocking_count = len([v for v in violations if v.get("blocking", False)])
        warning_count = len(violations) - blocking_count

        parts = []
        if file_path:
            parts.append(f"📄 {file_path}")

        if blocking_count > 0:
            parts.append(f"🚫 {blocking_count} blocking")

        if warning_count > 0:
            plural = "s" if warning_count > 1 else ""
            parts.append(f"⚠️  {warning_count} warning{plural}")

        return " | ".join(parts) if parts else "No violations"
