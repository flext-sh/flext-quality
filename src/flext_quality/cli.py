"""Command-line interface for FLEXT Quality.

This module provides CLI commands for code quality analysis.
Uses flext-cli patterns for consistency.
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

from flext_quality.analyzer import CodeAnalyzer
from flext_quality.reports import QualityReport


def setup_logging(level: str = "INFO") -> None:
    # Logging is now handled by flext-infrastructure.monitoring.flext-observability
    pass


def analyze_project(args: argparse.Namespace) -> int:
    """Analyze project quality."""
    try:
        project_path = Path(args.path).resolve()

        if not project_path.exists():
            return 1

        # Create analyzer
        analyzer = CodeAnalyzer(project_path)

        # Run analysis
        results = analyzer.analyze_project(
            include_security=args.include_security,
            include_complexity=args.include_complexity,
            include_dead_code=args.include_dead_code,
            include_duplicates=args.include_duplicates,
        )

        # Generate report
        report = QualityReport(results)

        if args.output:
            # Save to file
            output_path = Path(args.output)
            report.save_report(output_path, args.format)
            print(f"Report saved to: {output_path}")  # noqa: T201
        elif args.format == "json":
            print(report.generate_json_report())  # noqa: T201
        elif args.format == "html":
            print(report.generate_html_report())  # noqa: T201
        else:
            print(report.generate_text_report())  # noqa: T201

        # Return appropriate exit code based on quality
        quality_score = analyzer.get_quality_score()
        if quality_score >= 80:
            return 0  # Good quality
        if quality_score >= 60:
            return 1  # Medium quality
        return 2  # Poor quality

    except Exception:
        if args.verbose:
            traceback.print_exc()
        return 3


def another_function(args: argparse.Namespace) -> int:
    """Another function."""
    try:
        project_path = Path(args.path).resolve()

        if not project_path.exists():
            return 1

        # Quick analysis
        analyzer = CodeAnalyzer(project_path)
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=False,  # Skip for speed
            include_duplicates=False,  # Skip for speed
        )

        score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()

        # Show results
        print(f"Quality Score: {score:.1f}/100.0")  # noqa: T201
        print(f"Quality Grade: {grade}")  # noqa: T201

        # Show issue counts
        issues = results.get("issues", {})
        security_count = len(issues.get("security", []))
        complexity_count = len(issues.get("complexity", []))

        print(f"Security Issues: {security_count}")  # noqa: T201
        print(f"Complexity Issues: {complexity_count}")  # noqa: T201

        return 0 if score >= 70 else 1

    except Exception:
        return 3


def main() -> int:
    parser = argparse.ArgumentParser(
        description="FLEXT Quality - Enterprise Code Quality Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    flext-infrastructure.monitoring.flext-quality analyze ./my-project
    flext-infrastructure.monitoring.flext-quality analyze ./my-project --output report.html --format html
    flext-infrastructure.monitoring.flext-quality score ./my-project
    flext-infrastructure.monitoring.flext-quality analyze ./my-project --no-security --no-duplicates
        """,
    )

    # Global options
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Run comprehensive code analysis",
    )
    analyze_parser.add_argument("path", help="Path to the project to analyze")
    analyze_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: print to console)",
    )
    analyze_parser.add_argument(
        "--format",
        "-f",
        choices=["text", "json", "html"],
        default="text",
        help="Report format",
    )
    analyze_parser.add_argument(
        "--no-security",
        action="store_false",
        dest="include_security",
        help="Skip security analysis",
    )
    analyze_parser.add_argument(
        "--no-complexity",
        action="store_false",
        dest="include_complexity",
        help="Skip complexity analysis",
    )
    analyze_parser.add_argument(
        "--no-dead-code",
        action="store_false",
        dest="include_dead_code",
        help="Skip dead code detection",
    )
    analyze_parser.add_argument(
        "--no-duplicates",
        action="store_false",
        dest="include_duplicates",
        help="Skip duplicate code detection",
    )
    analyze_parser.set_defaults(func=analyze_project)

    # Score command
    score_parser = subparsers.add_parser("score", help="Get quick quality score")
    score_parser.add_argument("path", help="Path to the project to analyze")
    score_parser.set_defaults(func=another_function)

    # Parse arguments
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)

    # Execute command
    if hasattr(args, "func"):
        result = args.func(args)
        return int(result) if result is not None else 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
