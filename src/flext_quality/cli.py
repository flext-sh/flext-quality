"""FLEXT Quality CLI interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path
from typing import cast, override

from flext_cli import (
    FlextCli,
    FlextCliContext,
)

# Console import removed - using flext-cli exclusively
from flext_core import FlextCore

from .analyzer import CodeAnalyzer
from .config import FlextQualityConfig
from .reports import QualityReport
from .typings import FlextQualityTypes
from .web import FlextQualityWeb

# Quality score thresholds
MIN_ACCEPTABLE_QUALITY_SCORE = 70


class FlextQualityCliService(FlextCore.Service[int]):
    """Unified FLEXT Quality CLI service following enterprise patterns.

    Single responsibility class that handles all CLI operations with
    nested helper classes and explicit FlextCore.Result error handling.
    """

    @override
    def __init__(self, **_data: object) -> None:
        """Initialize CLI service with complete FLEXT ecosystem integration."""
        super().__init__()

        # Complete FLEXT ecosystem integration
        self._container = FlextCore.Container.get_global()
        self._context = FlextCore.Context()
        self._bus = FlextCore.Bus()
        self._dispatcher = FlextCore.Dispatcher()
        self._processors = FlextCore.Processors()
        self._registry = FlextCore.Registry(dispatcher=self._dispatcher)
        self._logger = FlextCore.Logger(__name__)

    @override
    def execute(self) -> FlextCore.Result[int]:
        """Execute CLI service - required abstract method implementation."""
        self._logger.info("CLI service execute called - this is a placeholder")
        return FlextCore.Result[int].ok(0)

    class _CliContextHelper:
        """Nested helper for CLI context management."""

        @staticmethod
        def get_cli_context() -> FlextCore.Result[FlextCliContext]:
            """Get CLI context using flext-cli exclusively."""
            context = FlextCliContext()
            return FlextCore.Result[FlextCliContext].ok(context)

    class _ProjectAnalysisHelper:
        """Nested helper for project analysis operations."""

        @override
        def __init__(self, logger: FlextCore.Logger) -> None:
            self.logger = logger

        def analyze_project_workflow(
            self,
            args: argparse.Namespace,
        ) -> FlextCore.Result[int]:
            """Execute complete project analysis workflow."""
            cli_context_result = (
                FlextQualityCliService._CliContextHelper.get_cli_context()
            )
            if cli_context_result.is_failure:
                return FlextCore.Result[int].fail(
                    cli_context_result.error or "CLI context creation failed",
                )

            cli_context = cli_context_result.value
            FlextCli()

            # Enable quiet mode for JSON/HTML output to prevent log contamination
            # Use FlextQualityConfig instead of direct environment manipulation

            quality_config = FlextQualityConfig()

            if args.format in {"json", "html"} and not args.verbose:
                quality_config.observability_quiet = True

            project_path = Path(args.path).resolve()
            if not project_path.exists():
                self._logger.error(f"Path does not exist: {project_path}")
                return FlextCore.Result[int].ok(1)

            self._logger.info(f"Analyzing project: {project_path}")

            # Create analyzer
            analyzer = CodeAnalyzer(project_path)

            # Run analysis
            analysis_result = analyzer.analyze_project(
                include_security=args.include_security,
                include_complexity=args.include_complexity,
                include_dead_code=args.include_dead_code,
                include_duplicates=args.include_duplicates,
            )

            # analysis_result is now AnalysisResults directly, not FlextCore.Result
            results = analysis_result

            # Check if any files were analyzed
            files_analyzed = getattr(results.overall_metrics, "files_analyzed", 0)
            if files_analyzed == 0:
                self._logger.error("No files to analyze")
                return FlextCore.Result[int].ok(1)

            # Generate report
            report = QualityReport(results)

            # Handle output based on format
            output_result: FlextCore.Result[None] = self._handle_output(
                args, report, cli_context
            )
            if output_result.is_failure:
                self._logger.error(
                    output_result.error or "Output processing failed",
                )
                return FlextCore.Result[int].ok(1)

            # Quality thresholds
            good_quality_threshold = 80
            medium_quality_threshold = 60

            # Return appropriate exit code based on quality
            quality_score = analyzer.get_quality_score()
            if quality_score >= good_quality_threshold:
                self._logger.info(f"Good quality: {quality_score}%")
                return FlextCore.Result[int].ok(0)
            if quality_score >= medium_quality_threshold:
                self._logger.warning(f"Medium quality: {quality_score}%")
                return FlextCore.Result[int].ok(1)
            self._logger.error(f"Poor quality: {quality_score}%")
            return FlextCore.Result[int].ok(2)

        def _handle_output(
            self,
            args: argparse.Namespace,
            report: QualityReport,
            cli_context: FlextCliContext,
        ) -> FlextCore.Result[None]:
            """Handle report output to file or stdout."""
            if args.output:
                return self._save_to_file(args, report, cli_context)
            return self._output_to_stdout(args, report, cli_context)

        def _save_to_file(
            self,
            args: argparse.Namespace,
            report: QualityReport,
            cli_context: FlextCliContext,
        ) -> FlextCore.Result[None]:
            """Save report to file using FlextCli export."""
            output_path = Path(args.output)

            if FLEXT_CLI_AVAILABLE:
                if args.format == "json":
                    # Get dict[str, object] from JSON report
                    report_dict: FlextQualityTypes.Core.ReportDict = json.loads(
                        report.to_json()
                    )
                    # Export data directly to file
                    try:
                        with Path(output_path).open("w", encoding="utf-8") as f:
                            json.dump(report_dict, f, indent=2)
                        export_result = FlextCore.Result[object].ok(None)
                    except Exception as e:
                        export_result = FlextCore.Result[object].fail(
                            f"Failed to export data: {e}"
                        )
                elif args.format == "html":
                    # Write HTML directly since FlextCli doesn't handle HTML export
                    output_path.write_text(report.to_html(), encoding="utf-8")
                    self._logger.info(f"HTML report saved to {output_path}")
                    return FlextCore.Result[None].ok(None)
                else:
                    # Table format - export as JSON
                    report_dict: FlextQualityTypes.Core.ReportDict = json.loads(
                        report.to_json()
                    )
                    # Export data directly to file
                    try:
                        with Path(output_path).open("w", encoding="utf-8") as f:
                            json.dump(report_dict, f, indent=2)
                        export_result = FlextCore.Result[object].ok(None)
                    except Exception as e:
                        export_result = FlextCore.Result[object].fail(
                            f"Failed to export data: {e}"
                        )

                if export_result and export_result.is_failure:
                    return FlextCore.Result[None].fail(
                        f"Failed to save report: {export_result.error}",
                    )
                if export_result and export_result.is_success:
                    success_msg = (
                        str(export_result.value)
                        if export_result.value
                        else "Report saved successfully"
                    )
                    self._logger.info(success_msg)
            else:
                # Fallback without FlextCli
                if args.format == "json":
                    output_path.write_text(report.to_json(), encoding="utf-8")
                elif args.format == "html":
                    output_path.write_text(report.to_html(), encoding="utf-8")
                else:
                    output_path.write_text(report.to_json(), encoding="utf-8")
                self._logger.info(f"Report saved to {output_path}")

            return FlextCore.Result[None].ok(None)

        def _output_to_stdout(
            self,
            args: argparse.Namespace,
            report: QualityReport,
            cli_context: FlextCliContext,
        ) -> FlextCore.Result[None]:
            """Output report to stdout."""
            if args.format == "json":
                if FLEXT_CLI_AVAILABLE:
                    # Get dict[str, object] from JSON report
                    report_dict: FlextQualityTypes.Core.ReportDict = json.loads(
                        report.to_json()
                    )
                    # Format data as JSON
                    try:
                        formatted_data = json.dumps(report_dict, indent=2)
                        format_result = FlextCore.Result[str].ok(formatted_data)
                    except Exception as e:
                        format_result = FlextCore.Result[str].fail(
                            f"Failed to format data: {e}"
                        )
                    if format_result.is_success:
                        sys.stdout.write(format_result.value + "\\n")
                    else:
                        return FlextCore.Result[None].fail(
                            f"Failed to format as JSON: {format_result.error}",
                        )
                else:
                    sys.stdout.write(report.to_json() + "\\n")
            elif args.format == "html":
                sys.stdout.write(report.to_html() + "\\n")
            else:
                # Get dict[str, object] from JSON report
                report_dict: FlextQualityTypes.Core.ReportDict = json.loads(
                    report.to_json()
                )
                cli_api = self._get_cli_api()
                # Display data as table using FlextCli
                cli_api.display_data(
                    cast("FlextCore.Types.Dict", report_dict), format_type="table"
                )

            return FlextCore.Result[None].ok(None)

    class _ProjectScoringHelper:
        """Nested helper for project scoring operations."""

        @override
        def __init__(self, logger: FlextCore.Logger) -> None:
            self.logger = logger

        def score_project_workflow(
            self, args: argparse.Namespace
        ) -> FlextCore.Result[int]:
            """Execute project scoring workflow."""
            cli_context_result = (
                FlextQualityCliService._CliContextHelper.get_cli_context()
            )
            if cli_context_result.is_failure:
                return FlextCore.Result[int].fail(
                    cli_context_result.error or "CLI context creation failed",
                )

            cli_api = self._get_cli_api()

            project_path = Path(args.path).resolve()
            self._logger.info(f"Calculating quality score for: {project_path}")

            # Quick analysis
            analyzer = CodeAnalyzer(project_path)
            analysis_result = analyzer.analyze_project(
                include_security=True,
                include_complexity=True,
                include_dead_code=False,  # Skip for speed
                include_duplicates=False,  # Skip for speed
            )

            # Unwrap FlextCore.Result
            if analysis_result.is_failure:
                self._logger.error(f"Analysis failed: {analysis_result.error}")
                return FlextCore.Result[int].ok(1)

            score_value = analyzer.get_quality_score()
            grade = analyzer.get_quality_grade()

            # Create score data for display
            score_data = {
                "score": score_value,
                "grade": grade,
                "project": str(project_path),
            }

            # Format and display using FlextCli or fallback
            # Display score data as table using FlextCli
            cli_api.display_data(
                cast("FlextCore.Types.Dict", score_data), format_type="table"
            )

            # Exit based on score
            if score_value >= MIN_ACCEPTABLE_QUALITY_SCORE:
                self._logger.info(f"Quality acceptable: {score_value}%")
                return FlextCore.Result[int].ok(0)
            self._logger.warning(f"Quality needs improvement: {score_value}%")
            return FlextCore.Result[int].ok(1)

    class _WebServerHelper:
        """Nested helper for web server operations."""

        @override
        def __init__(self, logger: FlextCore.Logger) -> None:
            self.logger = logger

        def run_web_server_workflow(
            self, args: argparse.Namespace
        ) -> FlextCore.Result[int]:
            """Execute web server startup workflow."""
            cli_context_result = (
                FlextQualityCliService._CliContextHelper.get_cli_context()
            )
            if cli_context_result.is_failure:
                return FlextCore.Result[int].fail(
                    cli_context_result.error or "CLI context creation failed",
                )

            self._logger.info(f"Starting web server on {args.host}:{args.port}")

            interface = FlextQualityWeb()
            interface.run(host=args.host, port=args.port, debug=args.debug)
            return FlextCore.Result[int].ok(0)

    def analyze_project(self, args: argparse.Namespace) -> FlextCore.Result[int]:
        """Analyze project quality using unified service pattern."""
        if self.logger is None:
            msg = "Logger must be initialized"
            raise RuntimeError(msg)
        analysis_helper = self._ProjectAnalysisHelper(self.logger)

        analysis_result: FlextCore.Result[int] = (
            analysis_helper.analyze_project_workflow(args)
        )
        if analysis_result.is_failure:
            self.logger.error("Quality analysis failed")
            return FlextCore.Result[int].fail(
                f"Analysis failed: {analysis_result.error}"
            )

        return analysis_result

    def score_project(self, args: argparse.Namespace) -> FlextCore.Result[int]:
        """Get quick quality score for project using unified service pattern."""
        if self.logger is None:
            msg = "Logger must be initialized"
            raise RuntimeError(msg)
        scoring_helper = self._ProjectScoringHelper(self.logger)

        scoring_result: FlextCore.Result[int] = scoring_helper.score_project_workflow(
            args
        )
        if scoring_result.is_failure:
            self.logger.error("Quality score calculation failed")
            return FlextCore.Result[int].fail(
                f"Score calculation failed: {scoring_result.error}",
            )

        return scoring_result

    def run_web_server(self, args: argparse.Namespace) -> FlextCore.Result[int]:
        """Run quality web interface server using unified service pattern."""
        if self.logger is None:
            msg = "Logger must be initialized"
            raise RuntimeError(msg)
        web_helper = self._WebServerHelper(self.logger)

        web_result: FlextCore.Result[int] = web_helper.run_web_server_workflow(args)
        if web_result.is_failure:
            self.logger.error("Web server failed")
            return FlextCore.Result[int].fail(f"Web server failed: {web_result.error}")

        return web_result

    def get_cli_context(self) -> FlextCore.Result[FlextCliContext]:
        """Public method to get CLI context."""
        return self._CliContextHelper.get_cli_context()

    # Legacy compatibility functions (required by __init__.py exports)
    def get_cli_context(self) -> FlextCliContext:
        """Get CLI context using flext-cli exclusively."""
        return FlextCliContext()

    def analyze_project(self, args: argparse.Namespace) -> int:
        """Analyze project quality using FlextCli APIs."""
        logger = FlextCore.Logger(__name__)
        self._CliContextHelper.get_cli_context()
        cli_api = FlextCli()

        try:
            project_path = Path(args.path).resolve()
            self._logger.info(f"Analyzing project: {project_path}")

            # Use CodeAnalyzer for analysis
            analyzer = CodeAnalyzer(project_path)
            analysis_result = analyzer.analyze_project(
                include_security=getattr(args, "include_security", True),
                include_complexity=getattr(args, "include_complexity", True),
                include_dead_code=getattr(args, "include_dead_code", True),
                include_duplicates=getattr(args, "include_duplicates", True),
            )

            # Unwrap FlextCore.Result
            if analysis_result.is_failure:
                self._logger.error(f"Analysis failed: {analysis_result.error}")
                return 1

            results = analysis_result.value

            # Display results using FlextCli
            result_data: FlextCore.Types.Dict = {
                "files_analyzed": getattr(results.overall_metrics, "files_analyzed", 0),
                "total_lines": getattr(results.overall_metrics, "total_lines", 0),
                "quality_score": f"{getattr(results.overall_metrics, 'quality_score', 0):.1f}%",
                "security_issues": len(results.security_issues),
                "complexity_issues": len(results.complexity_issues),
            }
            cli_api.display_data(result_data, format_type="table")

            return 0

        except Exception as e:
            logger.exception("Quality analysis failed")
            self._logger.exception(f"Analysis failed: {e}")
            if getattr(args, "verbose", False):
                traceback.print_exc()
            return 1

    def score_project(self, args: argparse.Namespace) -> int:
        """Get quick quality score for project using FlextCli APIs."""
        logger = FlextCore.Logger(__name__)
        self._CliContextHelper.get_cli_context()
        cli_api = FlextCli()

        try:
            project_path = Path(args.path).resolve()
            self._logger.info(f"Calculating quality score for: {project_path}")

            # Quick analysis
            analyzer = CodeAnalyzer(project_path)
            analysis_result = analyzer.analyze_project(
                include_duplicates=False,  # Skip for speed
            )

            # Unwrap FlextCore.Result
            if analysis_result.is_failure:
                self._logger.error(f"Analysis failed: {analysis_result.error}")
                return 1

            score_value = analyzer.get_quality_score()
            grade = analyzer.get_quality_grade()

            # Create score data for display
            score_data: FlextCore.Types.Dict = {
                "score": score_value,
                "grade": grade,
                "project": str(project_path),
            }

            # Format and display using FlextCli or fallback
            cli_api.display_data(score_data, format_type="table")

            # Exit based on score
            if score_value >= MIN_ACCEPTABLE_QUALITY_SCORE:
                self._logger.info(f"Quality acceptable: {score_value}%")
                return 0
            self._logger.warning(f"Quality needs improvement: {score_value}%")
            return 1

        except Exception as e:
            logger.exception("Quality score calculation failed")
            self._logger.exception(f"Score calculation failed: {e}")
            return 1

    def run_web_server(self, args: argparse.Namespace) -> int:
        """Run quality web interface server."""
        logger = FlextCore.Logger(__name__)
        self._CliContextHelper.get_cli_context()

        try:
            self._logger.info(f"Starting web server on {args.host}:{args.port}")

            interface = FlextQualityWeb()
            interface.run(host=args.host, port=args.port, debug=args.debug)
            return 0
        except KeyboardInterrupt:
            self._logger.info("Web server stopped by user")
            return 0
        except Exception as e:
            logger.exception("Web server failed")
            self._logger.exception(f"Web server failed: {e}")
            if getattr(args, "verbose", False):
                traceback.print_exc()
            return 1

    def quality_main() -> int:
        """Legacy quality main function alias."""
        return main()


def main() -> int:
    """Main CLI entry point using argparse with FlextCli integration."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality - Enterprise Code Quality Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""

Examples:
    flext-quality analyze ./my-project
    flext-quality analyze ./my-project --output report.html --format html
    flext-quality score ./my-project
    flext-quality web --port 8080
        """,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze project quality")
    analyze_parser.add_argument("path", type=Path, help="Path to project to analyze")
    analyze_parser.add_argument("--output", "-o", type=Path, help="Output file path")
    analyze_parser.add_argument(
        "--format",
        "-f",
        default="table",
        choices=["table", "json", "html"],
        help="Output format",
    )
    analyze_parser.add_argument(
        "--include-security",
        action="store_true",
        default=True,
        help="Include security analysis",
    )
    analyze_parser.add_argument(
        "--no-security",
        dest="include_security",
        action="store_false",
        help="Skip security analysis",
    )
    analyze_parser.add_argument(
        "--include-complexity",
        action="store_true",
        default=True,
        help="Include complexity analysis",
    )
    analyze_parser.add_argument(
        "--no-complexity",
        dest="include_complexity",
        action="store_false",
        help="Skip complexity analysis",
    )
    analyze_parser.add_argument(
        "--include-dead-code",
        action="store_true",
        default=True,
        help="Include dead code detection",
    )
    analyze_parser.add_argument(
        "--no-dead-code",
        dest="include_dead_code",
        action="store_false",
        help="Skip dead code detection",
    )
    analyze_parser.add_argument(
        "--include-duplicates",
        action="store_true",
        default=True,
        help="Include duplicate code detection",
    )
    analyze_parser.add_argument(
        "--no-duplicates",
        dest="include_duplicates",
        action="store_false",
        help="Skip duplicate code detection",
    )

    # Score command
    score_parser = subparsers.add_parser("score", help="Get quick quality score")
    score_parser.add_argument("path", type=Path, help="Path to project to score")

    # Web command
    web_parser = subparsers.add_parser("web", help="Run web interface server")
    web_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address to bind to",
    )
    web_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number to bind to",
    )
    web_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Setup logging level using FlextQualityConfig

    quality_config = FlextQualityConfig()

    if args.verbose:
        quality_config.observability_log_level = "DEBUG"

    # Route to appropriate handler
    if args.command == "analyze":
        return FlextQualityCliService.analyze_project(args)
    if args.command == "score":
        return FlextQualityCliService.score_project(args)
    if args.command == "web":
        return FlextQualityCliService.run_web_server(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    main()
