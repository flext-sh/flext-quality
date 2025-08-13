"""Command-line interface for FLEXT Quality.

This module provides CLI commands for code quality analysis.
Uses flext-cli patterns for consistency.
"""

from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path

from flext_core import get_logger

from flext_quality.analyzer import CodeAnalyzer
from flext_quality.reports import QualityReport


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.

    Args:
        level: Logging level to set (default: INFO)

    """
    # Logging is now handled by flext-infrastructure.monitoring.flext-observability


def run_web_server(args: argparse.Namespace) -> int:
    """Run quality web interface server."""
    logger = get_logger(__name__)
    try:
        from flext_quality.web_interface import QualityWebInterface
    except Exception:
        # Optional dependency; when unavailable, return error unless verbose mode prints trace
        if args.verbose:
            traceback.print_exc()
        logger.warning("Quality web interface not available; install optional dependencies.")
        return 1

    try:
        interface = QualityWebInterface()
        interface.run(host=args.host, port=args.port, debug=args.debug)
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception:
        if args.verbose:
            traceback.print_exc()
        return 1


def analyze_project(args: argparse.Namespace) -> int:
    """Analyze project quality."""
    try:
        # Enable quiet mode for JSON/HTML output to prevent log contamination
        if (
            hasattr(args, "format")
            and args.format in {"json", "html"}
            and not getattr(args, "verbose", False)
        ):
            os.environ["FLEXT_OBSERVABILITY_QUIET"] = "1"

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
        # Check if any files were analyzed
        files_analyzed = results.get("files_analyzed", 0)
        if isinstance(files_analyzed, (int, float)) and files_analyzed == 0:
            return 1  # Error: no files to analyze

        # Generate report
        report = QualityReport(results)
        if args.output:
            # Save to file
            output_path = Path(args.output)
            report.save_report(output_path, args.format)
        elif args.format == "json":
            # Write JSON to stdout explicitly for CLI output
            sys.stdout.write(report.to_json() + "\n")
        elif args.format == "html":
            # Write HTML to stdout explicitly for CLI output
            sys.stdout.write(report.to_html() + "\n")
        # Constants for quality thresholds
        good_quality_threshold = 80
        medium_quality_threshold = 60

        # Return appropriate exit code based on quality
        quality_score = analyzer.get_quality_score()
        if quality_score >= good_quality_threshold:
            return 0  # Good quality
        if quality_score >= medium_quality_threshold:
            return 1  # Medium quality
        return 2  # Poor quality
    except (RuntimeError, ValueError, TypeError):
        logger = get_logger(__name__)
        # EXPLICIT TRANSPARENCY: CLI function must return exit code for process management
        logger.exception("Quality analysis failed with specific error")
        logger.exception("Returning exit code 3 to indicate analysis failure")
        if args.verbose:
            logger.info("Verbose mode enabled - showing full traceback")
            traceback.print_exc()
        # Return 3 to indicate analysis error (distinct from quality scores 0,1,2)
        return 3


def score_project(args: argparse.Namespace) -> int:
    """Get quick quality score for project."""
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
        analyzer.get_quality_grade()

        # Show results (print to stdout for CLI usage)

        # Show issue counts
        issues_obj = results.get("issues", {})
        if isinstance(issues_obj, dict):
            len(issues_obj.get("security", []))
            len(issues_obj.get("complexity", []))

        # Constants for quality thresholds
        acceptable_quality_threshold = 70

        return 0 if score >= acceptable_quality_threshold else 1
    except (RuntimeError, ValueError, TypeError):
        logger = get_logger(__name__)
        logger.exception("Quality score calculation failed")
        return 3


def another_function(args: argparse.Namespace) -> int:
    """Compatibility alias for the 'score' command expected by tests.

    Delegates to `score_project` to compute a quick project quality score.
    """
    return score_project(args)


def main() -> int:
    """Provide CLI entry point.

    Returns:
        Exit code: 0=success, 1=quality below threshold, 3=error

    """
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
    # Keep historical test contract: use another_function as entrypoint
    score_parser.set_defaults(func=another_function)

    # Web server command
    web_parser = subparsers.add_parser("web", help="Run quality web interface")
    web_parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost)",
    )
    web_parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind to (default: 8080)",
    )
    web_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    web_parser.set_defaults(func=run_web_server)

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
