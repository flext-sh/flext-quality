"""Documentation assistance helper - Docstring quality analysis.

Pragmatic utilities for:
- Checking docstring coverage
- Validating docstring format (Google style)
- Suggesting documentation improvements

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
from pathlib import Path

from flext_core import FlextResult

# Coverage grade thresholds
COVERAGE_GRADE_A_THRESHOLD = 90
COVERAGE_GRADE_B_THRESHOLD = 80
COVERAGE_GRADE_C_THRESHOLD = 70
COVERAGE_GRADE_D_THRESHOLD = 50
COVERAGE_RECOMMENDATION_THRESHOLD = 80


def check_docstring_coverage(
    module_path: Path,
) -> FlextResult[dict[str, object]]:
    """Check percentage of functions/classes with docstrings.

    Args:
        module_path: Python module to analyze

    Returns:
        FlextResult with coverage statistics

    """
    try:
        with Path(module_path).open(encoding="utf-8") as f:
            tree = ast.parse(f.read())

        total_items = 0
        documented_items = 0
        missing_docs = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total_items += 1
                has_docstring = ast.get_docstring(node) is not None

                if has_docstring:
                    documented_items += 1
                else:
                    missing_docs.append(f"{node.name} (line {node.lineno})")

        coverage_pct = (documented_items / total_items * 100) if total_items > 0 else 0

        return FlextResult.ok({
            "file": str(module_path),
            "total_items": total_items,
            "documented_items": documented_items,
            "undocumented_items": total_items - documented_items,
            "coverage_percent": coverage_pct,
            "coverage_grade": (
                "A"
                if coverage_pct >= COVERAGE_GRADE_A_THRESHOLD
                else "B"
                if coverage_pct >= COVERAGE_GRADE_B_THRESHOLD
                else "C"
                if coverage_pct >= COVERAGE_GRADE_C_THRESHOLD
                else "D"
                if coverage_pct >= COVERAGE_GRADE_D_THRESHOLD
                else "F"
            ),
            "missing_docs": missing_docs[:10],  # First 10
        })

    except SyntaxError as e:
        return FlextResult.fail(f"Syntax error in {module_path}: {e}")
    except Exception as e:
        return FlextResult.fail(f"Docstring analysis failed: {e}")


def validate_google_style_docstrings(
    module_path: Path,
) -> FlextResult[dict[str, object]]:
    """Validate docstrings follow Google style format.

    Args:
        module_path: Python module to check

    Returns:
        FlextResult with validation results

    """
    try:
        with Path(module_path).open(encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content)

        issues = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Check for Google style markers
                    has_args = "Args:" in docstring

                    # For functions with params, should have Args:
                    if (
                        isinstance(node, ast.FunctionDef)
                        and node.args.args
                        and not has_args
                    ):
                        issues.append(
                            f"{node.name} has parameters but no Args: section"
                        )

                    # Check for proper formatting
                    if docstring.startswith(" "):
                        issues.append(f"{node.name}: Docstring indentation issue")

        return FlextResult.ok({
            "file": str(module_path),
            "issues_found": len(issues),
            "issues": issues[:10],  # First 10
            "status": "compliant" if len(issues) == 0 else "needs_fixes",
        })

    except Exception as e:
        return FlextResult.fail(f"Google style validation failed: {e}")


def suggest_docstring_improvements(
    module_path: Path,
) -> FlextResult[list[str]]:
    """Suggest docstring improvements.

    Args:
        module_path: Python module to analyze

    Returns:
        FlextResult with list of suggestions

    """
    try:
        with Path(module_path).open(encoding="utf-8") as f:
            tree = ast.parse(f.read())

        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)

                # Check for short one-liners that need more detail
                if docstring and len(docstring.splitlines()) == 1:
                    if len(node.args.args) > 0:
                        suggestions.append(
                            f"{node.name}: Add Args section to docstring"
                        )
                    if node.returns:
                        suggestions.append(
                            f"{node.name}: Add Returns section to docstring"
                        )

                # Check for functions without docstrings
                if not docstring:
                    suggestions.append(f"{node.name}: Missing docstring")

        return FlextResult.ok(
            suggestions[:15] if suggestions else ["Docstrings look good!"]
        )

    except Exception as e:
        return FlextResult.fail(f"Suggestion generation failed: {e}")


def analyze_api_documentation(
    module_path: Path,
) -> FlextResult[dict[str, object]]:
    """Analyze API documentation completeness.

    Args:
        module_path: Module to analyze

    Returns:
        FlextResult with API documentation analysis

    """
    try:
        with Path(module_path).open(encoding="utf-8") as f:
            tree = ast.parse(f.read())

        public_items = []
        documented_items = 0

        for node in ast.walk(tree):
            # Only check top-level definitions (first level)
            if isinstance(
                node, (ast.FunctionDef, ast.ClassDef)
            ) and not node.name.startswith("_"):
                public_items.append(node.name)
                if ast.get_docstring(node):
                    documented_items += 1

        coverage = (documented_items / len(public_items) * 100) if public_items else 0

        return FlextResult.ok({
            "file": str(module_path),
            "public_items": len(public_items),
            "documented_items": documented_items,
            "coverage_percent": coverage,
            "public_names": public_items[:20],
            "recommendation": (
                "Good API documentation coverage"
                if coverage >= COVERAGE_RECOMMENDATION_THRESHOLD
                else "Enhance API documentation"
            ),
        })

    except Exception as e:
        return FlextResult.fail(f"API documentation analysis failed: {e}")
