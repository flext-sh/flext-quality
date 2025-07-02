"""Command-line interface for FLEXT Quality."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

from .analyzer import CodeAnalyzer
from .reports import QualityReport


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def analyze_command(args: Any) -> int:
    """Execute analysis command."""
    try:
        project_path = Path(args.path).resolve()

        if not project_path.exists():
            print(f"❌ Error: Path '{project_path}' does not exist")
            return 1

        print(f"🔍 Analyzing project: {project_path}")

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
            print(f"📄 Report saved to: {output_path}")
        # Print to console
        elif args.format == "json":
            print(report.generate_json_report())
        elif args.format == "html":
            print(report.generate_html_report())
        else:
            print(report.generate_text_report())

        # Return appropriate exit code based on quality
        quality_score = analyzer.get_quality_score()
        if quality_score >= 80:
            return 0  # Good quality
        if quality_score >= 60:
            return 1  # Medium quality
        return 2  # Poor quality

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 3


def score_command(args: Any) -> int:
    """Execute quick score command."""
    try:
        project_path = Path(args.path).resolve()

        if not project_path.exists():
            print(f"❌ Error: Path '{project_path}' does not exist")
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

        print(f"📊 Quality Score: {score:.1f}/100 (Grade: {grade})")
        print(f"📁 Files: {results['files_analyzed']}")
        print(f"📄 Lines: {results['total_lines']:,}")

        # Show issue counts
        issues = results.get("issues", {})
        security_count = len(issues.get("security", []))
        complexity_count = len(issues.get("complexity", []))

        if security_count > 0:
            print(f"🔒 Security Issues: {security_count}")
        if complexity_count > 0:
            print(f"🧩 Complexity Issues: {complexity_count}")

        return 0 if score >= 70 else 1

    except Exception as e:
        print(f"❌ Score calculation failed: {e}")
        return 3


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality - Enterprise Code Quality Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flext-quality analyze ./my-project
  flext-quality analyze ./my-project --output report.html --format html
  flext-quality score ./my-project
  flext-quality analyze ./my-project --no-security --no-duplicates
        """,
    )

    # Global options
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
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
        "analyze", help="Run comprehensive code analysis"
    )
    analyze_parser.add_argument("path", help="Path to the project to analyze")
    analyze_parser.add_argument(
        "--output", "-o", help="Output file path (default: print to console)"
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
    analyze_parser.set_defaults(func=analyze_command)

    # Score command
    score_parser = subparsers.add_parser("score", help="Get quick quality score")
    score_parser.add_argument("path", help="Path to the project to analyze")
    score_parser.set_defaults(func=score_command)

    # Parse arguments
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)

    # Execute command
    if hasattr(args, "func"):
        return args.func(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
