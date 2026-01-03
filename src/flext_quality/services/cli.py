"""CLI entry point for flext-quality.

Provides Typer-based command-line interface for quality operations including:
- Code quality checks (lint, type, security, test)
- Memory search via claude-mem
- Code search via claude-context
- Hook execution
- Rules validation
- Code execution command building

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import typer

# Main application
app = typer.Typer(
    name="flext-quality",
    help="FLEXT Quality - Code quality analysis and Claude Code integration",
    no_args_is_help=True,
)

# Subcommands
memory_app = typer.Typer(help="Cross-session memory operations via claude-mem")
code_app = typer.Typer(help="Semantic code search via claude-context")
hook_app = typer.Typer(help="Hook execution and management")
rules_app = typer.Typer(help="YAML rules validation")
exec_app = typer.Typer(help="Code execution command building")

app.add_typer(memory_app, name="memory")
app.add_typer(code_app, name="code")
app.add_typer(hook_app, name="hook")
app.add_typer(rules_app, name="rules")
app.add_typer(exec_app, name="exec")


def _run_lint(path: Path) -> int:
    """Run ruff linting on path."""
    result = subprocess.run(
        ["ruff", "check", str(path)],  # noqa: S607 - CLI tool execution
        check=False,
    )
    return result.returncode


def _run_type_check(path: Path) -> int:
    """Run type checking on path."""
    src_path = path / "src"
    if not src_path.exists():
        src_path = path
    result = subprocess.run(
        ["pyrefly", "check", str(src_path)],  # noqa: S607 - CLI tool execution
        check=False,
    )
    return result.returncode


def _run_tests(path: Path, min_coverage: int = 80) -> int:
    """Run tests with coverage."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(path / "src")
    result = subprocess.run(
        [  # noqa: S607 - CLI tool execution
            "pytest",
            str(path / "tests"),
            f"--cov={path / 'src'}",
            f"--cov-fail-under={min_coverage}",
            "--cov-report=term-missing",
        ],
        check=False,
        env=env,
    )
    return result.returncode


def _run_security(path: Path) -> int:
    """Run security scanning."""
    src_path = path / "src"
    if not src_path.exists():
        src_path = path
    result = subprocess.run(
        ["bandit", "-r", str(src_path), "-c", "pyproject.toml"],  # noqa: S607 - CLI tool execution
        check=False,
    )
    return result.returncode


def main() -> int:
    """Main CLI entry point for flext-quality.

    Returns:
        int: Exit code (0 for success, 1 for error)

    """
    args = sys.argv[1:]

    # No arguments - show status
    if not args:
        sys.stdout.write("flext-quality v0.9.0\n")
        sys.stdout.write("Usage: flext-quality <command> <path>\n")
        sys.stdout.write("Commands: check, validate\n")
        return 0

    command = args[0]
    path = Path(args[1]) if len(args) > 1 else Path()

    if command == "check":
        # Quick check: lint + type
        sys.stdout.write(f"Running check on {path}...\n")
        lint_result = _run_lint(path)
        if lint_result != 0:
            sys.stderr.write("Lint check failed\n")
            return lint_result
        type_result = _run_type_check(path)
        if type_result != 0:
            sys.stderr.write("Type check failed\n")
            return type_result
        sys.stdout.write("All checks passed!\n")
        return 0

    if command == "validate":
        # Full validation: lint + type + security + test
        sys.stdout.write(f"Running validation on {path}...\n")

        # Parse --min-coverage if provided
        min_coverage = 80
        for i, arg in enumerate(args):
            if arg == "--min-coverage" and i + 1 < len(args):
                min_coverage = int(args[i + 1])

        lint_result = _run_lint(path)
        if lint_result != 0:
            return lint_result

        type_result = _run_type_check(path)
        if type_result != 0:
            return type_result

        security_result = _run_security(path)
        if security_result != 0:
            return security_result

        test_result = _run_tests(path, min_coverage)
        if test_result != 0:
            return test_result

        sys.stdout.write("All validations passed!\n")
        return 0

    sys.stderr.write(f"Unknown command: {command}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
