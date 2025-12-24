"""FLEXT Quality CLI interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import argparse
import logging
import os
import traceback
from pathlib import Path
from typing import Self, override

from flext_cli import FlextCli, FlextCliFileTools
from pydantic import BaseModel, Field

from flext import FlextContainer, FlextLogger, FlextResult, FlextService

from .analyzer import FlextQualityAnalyzer
from .docs_maintenance.cli import run_comprehensive
from .reports import FlextQualityReportGenerator, ReportFormat
from .settings import FlextQualitySettings
from .subprocess_utils import SubprocessUtils
from .web import FlextQualityWeb

# =====================================================================
# Configuration Models - Data-Driven Approach (Pydantic 2)
# =====================================================================


class CliQualityThresholds(BaseModel):
    """Quality score thresholds as data."""

    good_threshold: float = Field(default=80.0, ge=0, le=100)
    medium_threshold: float = Field(default=60.0, ge=0, le=100)
    minimum_acceptable: float = Field(default=70.0, ge=0, le=100)


class CliOutputFormats(BaseModel):
    """Supported output formats and their metadata."""

    supported_formats: dict[str, str] = Field(
        default_factory=lambda: {
            "json": "JSON format output",
            "html": "HTML format output",
            "table": "Table format output",
        },
    )


class CliConfig(BaseModel):
    """CLI configuration as data - replaces hardcoded values."""

    thresholds: CliQualityThresholds = Field(default_factory=CliQualityThresholds)
    formats: CliOutputFormats = Field(default_factory=CliOutputFormats)
    default_host: str = Field(default="127.0.0.1")
    default_port: int = Field(default=8000)


# =====================================================================
# Focused Utility Classes - Single Responsibility Principle
# =====================================================================


class CliArgumentValidator:
    """Validates and normalizes CLI arguments."""

    @staticmethod
    def validate_project_path(path: Path) -> FlextResult[Path]:
        """Validate project path exists."""
        resolved_path = path.resolve()
        if not resolved_path.exists():
            return FlextResult[Path].fail(f"Path does not exist: {resolved_path}")
        return FlextResult[Path].ok(resolved_path)

    @staticmethod
    def validate_output_format(fmt: str, supported: list[str]) -> FlextResult[str]:
        """Validate output format is supported."""
        if fmt not in supported:
            return FlextResult[str].fail(
                f"Unsupported format: {fmt}. Choose from: {', '.join(supported)}",
            )
        return FlextResult[str].ok(fmt)


class QualityReportFormatter:
    """Formats and outputs quality reports using FlextCli."""

    def __init__(self, logger: FlextLogger) -> None:
        """Initialize formatter with logger and FlextCli."""
        super().__init__()
        self.logger = logger
        self._cli = FlextCli()
        self._file_tools = FlextCliFileTools()

    def output_report(
        self,
        report: FlextQualityReportGenerator,
        fmt: str,
        output_path: Path | None = None,
    ) -> FlextResult[bool]:
        """Output report to file or stdout using FlextCli."""
        if output_path:
            return self._save_to_file(report, fmt, output_path)
        return self._output_to_stdout(report, fmt)

    def _save_to_file(
        self,
        report: FlextQualityReportGenerator,
        fmt: str,
        output_path: Path,
    ) -> FlextResult[bool]:
        """Save report to file with proper directory creation and error handling."""
        # Determine report format
        format_type = ReportFormat.JSON
        if fmt == "html":
            format_type = ReportFormat.HTML
        elif fmt == "csv":
            format_type = ReportFormat.TEXT  # Default to text for unsupported formats

        # Create parent directories if they don't exist
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return FlextResult[bool].fail(f"Failed to create output directory: {e}")

        # Save report using proper API
        save_result = report.save_report(output_path, format_type)

        if save_result.is_success:
            self.logger.info("Report saved to %s", output_path)
            return FlextResult[bool].ok(True)
        return save_result

    def _output_to_stdout(
        self,
        report: FlextQualityReportGenerator,
        fmt: str,
    ) -> FlextResult[bool]:
        """Output report to stdout using proper report generation methods."""
        # Determine report format
        if fmt == "html":
            report_result = report.generate_html_report()
        elif fmt == "json":
            report_result = report.generate_json_report()
        else:
            report_result = report.generate_text_report()

        if report_result.is_failure:
            return FlextResult[bool].fail(
                f"Failed to generate report: {report_result.error}",
            )

        # Output to stdout
        try:
            self._cli.formatters.print(report_result.value)
            return FlextResult[bool].ok(True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to output report: {e}")


class AnalysisOptions(BaseModel):
    """Analysis options configuration."""

    include_security: bool = Field(default=True)
    include_complexity: bool = Field(default=True)
    include_dead_code: bool = Field(default=True)
    include_duplicates: bool = Field(default=True)


class ProjectQualityAnalyzer:
    """Wraps code analyzer with CLI-specific logic."""

    def __init__(self, logger: FlextLogger, config: CliConfig) -> None:
        """Initialize analyzer wrapper with logger and config."""
        super().__init__()
        self.logger = logger
        self.config = config

    def analyze(
        self,
        project_path: Path,
        options: AnalysisOptions | None = None,
    ) -> FlextResult[FlextQualityAnalyzer]:
        """Execute project analysis."""
        try:
            opts = options if options is not None else AnalysisOptions()
            analyzer = FlextQualityAnalyzer(project_path=project_path)
            result = analyzer.analyze_project(
                include_security=opts.include_security,
                include_complexity=opts.include_complexity,
                include_dead_code=opts.include_dead_code,
                include_duplicates=opts.include_duplicates,
            )
            if result.is_failure:
                return FlextResult[FlextQualityAnalyzer].fail(
                    f"Analysis failed: {result.error}",
                )
            return FlextResult[FlextQualityAnalyzer].ok(analyzer)
        except Exception as e:
            return FlextResult[FlextQualityAnalyzer].fail(f"Analysis error: {e}")

    def get_exit_code(self, quality_score: float) -> int:
        """Determine exit code based on quality score."""
        thresholds = self.config.thresholds
        if quality_score >= thresholds.good_threshold:
            return 0
        if quality_score >= thresholds.medium_threshold:
            return 1
        return 2


class CliCommandRouter:
    """Routes CLI commands to appropriate handlers."""

    def __init__(self, logger: FlextLogger, config: CliConfig) -> None:
        """Initialize router with logger and config."""
        super().__init__()
        self.logger = logger
        self.config = config
        self.formatter = QualityReportFormatter(logger)
        self.analyzer_wrapper = ProjectQualityAnalyzer(logger, config)

    def route_analyze(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route analyze command."""
        # Validate project path
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            error_msg = path_result.error or "Unknown error in path validation"
            self.logger.error(error_msg)
            return FlextResult[int].ok(1)

        project_path = path_result.value

        # Analyze project with options
        options = AnalysisOptions(
            include_security=args.include_security,
            include_complexity=args.include_complexity,
            include_dead_code=args.include_dead_code,
            include_duplicates=args.include_duplicates,
        )
        analyzer_result = self.analyzer_wrapper.analyze(project_path, options)

        if analyzer_result.is_failure:
            if analyzer_result.is_failure:
                self.logger.error(analyzer_result.error or "Unknown error")
            else:
                self.logger.error("Unknown error in analyzer")
            return FlextResult[int].ok(1)

        analyzer = analyzer_result.value

        # Generate and output report
        analysis_results = analyzer.get_last_analysis_result()
        if analysis_results is None:
            self.logger.error("No analysis results available")
            return FlextResult[int].ok(1)

        report = FlextQualityReportGenerator(analysis_results)
        output_result = self.formatter.output_report(
            report,
            args.format,
            Path(args.output) if args.output else None,
        )

        if output_result.is_failure:
            if output_result.is_failure:
                self.logger.error(output_result.error or "Unknown error")
            else:
                self.logger.error("Unknown error in output")
            return FlextResult[int].ok(1)

        # Return appropriate exit code
        quality_score = analyzer.get_quality_score()
        exit_code = self.analyzer_wrapper.get_exit_code(quality_score)
        if exit_code == 0:
            self.logger.info(f"Good quality: {quality_score:.1f}%")
        elif exit_code == 1:
            self.logger.warning(f"Medium quality: {quality_score:.1f}%")
        else:
            self.logger.error(f"Poor quality: {quality_score:.1f}%")

        return FlextResult[int].ok(exit_code)

    def route_score(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route score command."""
        # Validate project path
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            error_msg = path_result.error or "Unknown error in path validation"
            self.logger.error(error_msg)
            return FlextResult[int].ok(1)

        project_path = path_result.value

        # Quick analysis (skip dead code and duplicates for speed)
        options = AnalysisOptions(
            include_security=True,
            include_complexity=True,
            include_dead_code=False,
            include_duplicates=False,
        )
        analyzer_result = self.analyzer_wrapper.analyze(project_path, options)

        if analyzer_result.is_failure:
            if analyzer_result.is_failure:
                self.logger.error(analyzer_result.error or "Unknown error")
            else:
                self.logger.error("Unknown error in analyzer")
            return FlextResult[int].ok(1)

        analyzer = analyzer_result.value
        quality_score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()

        # Display score
        self.logger.info(f"Quality Score: {quality_score:.1f}% ({grade})")

        # Return exit code
        if quality_score >= self.config.thresholds.minimum_acceptable:
            self.logger.info("Quality acceptable")
            return FlextResult[int].ok(0)

        self.logger.warning("Quality needs improvement")
        return FlextResult[int].ok(1)

    def route_web(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route web command."""
        self.logger.info(f"Starting web server on {args.host}:{args.port}")
        try:
            interface = FlextQualityWeb()
            interface.run(host=args.host, port=args.port, debug=args.debug)
            return FlextResult[int].ok(0)
        except KeyboardInterrupt:
            self.logger.info("Web server stopped by user")
            return FlextResult[int].ok(0)
        except Exception:
            self.logger.exception("Web server failed")
            return FlextResult[int].ok(1)


# =====================================================================
# Main Service Class - Delegates to Utilities
# =====================================================================


class FlextQualityCliService(FlextService[int]):
    """Main CLI service with SOLID delegation."""

    # Type hints for private attributes
    _cli_logger: FlextLogger
    _cli_config: CliConfig
    _cli_container: FlextContainer

    def __new__(
        cls,
        _config: CliConfig | None = None,
        **_data: object,
    ) -> Self:
        """Create new CLI service instance.

        Args:
            _config: Configuration (ignored in __new__, used in __init__).
            **_data: Additional keyword arguments.

        Returns:
            New FlextQualityCliService instance.

        """
        return super().__new__(cls)

    def __init__(self, config: CliConfig | None = None, **_data: object) -> None:
        """Initialize CLI service with optional config."""
        super().__init__()
        # Use object.__setattr__ to bypass Pydantic's custom __setattr__ for private attributes
        # Use unique names (_cli_*) to avoid overriding parent attributes
        object.__setattr__(
            self,
            "_cli_config",
            config if config is not None else CliConfig(),
        )
        object.__setattr__(self, "_cli_logger", FlextLogger(__name__))
        self._router = CliCommandRouter(self._cli_logger, self._cli_config)

    @property
    def cli_config(self) -> CliConfig:
        """Access CLI configuration (read-only)."""
        return self._cli_config

    @property
    def cli_logger(self) -> FlextLogger:
        """Access CLI logger (read-only)."""
        return self._cli_logger

    def get_router(self) -> CliCommandRouter:
        """Get command router for dispatching CLI commands."""
        return self._router

    @override
    def execute(self, **_kwargs: object) -> FlextResult[int]:
        """Execute CLI service - required abstract method."""
        self.logger.info("CLI service running")
        return FlextResult[int].ok(0)


# =====================================================================
# Main Entry Point - Simple Command Dispatch
# =====================================================================


# =====================================================================
# CLI Command Wrappers for Testing and Direct Use
# =====================================================================


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration for the CLI.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)

    """
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def analyze_project(args: argparse.Namespace) -> int:
    """Analyze a project and return exit code.

    This is a convenience wrapper for the analyze command, allowing direct
    function calls with argparse.Namespace arguments instead of parsing CLI.

    Args:
        args: argparse.Namespace with fields:
            - path: Project path (str or Path)
            - output: Optional output file path
            - format: Output format (json, html, text, table)
            - verbose: Enable verbose output (bool)
            - include_security: Include security analysis (bool)
            - include_complexity: Include complexity analysis (bool)
            - include_dead_code: Include dead code analysis (bool)
            - include_duplicates: Include duplication analysis (bool)

    Returns:
        Exit code (0 for success, 1+ for errors)

    """
    try:
        # Setup logging if verbose
        if getattr(args, "verbose", False):
            setup_logging("DEBUG")
        else:
            setup_logging("INFO")

        # Validate and convert path
        path = args.path if isinstance(args.path, Path) else Path(args.path)
        if not path.exists():
            return 1
        if not path.is_dir():
            return 1

        # Create config
        config = CliConfig()
        FlextQualitySettings()

        # Create service and router
        service = FlextQualityCliService(config)
        router = service.get_router()

        # Create modified args with path as Path object
        analyze_args = argparse.Namespace(
            path=path,
            output=getattr(args, "output", None),
            format=getattr(args, "format", "table"),
            include_security=getattr(args, "include_security", True),
            include_complexity=getattr(args, "include_complexity", True),
            include_dead_code=getattr(args, "include_dead_code", True),
            include_duplicates=getattr(args, "include_duplicates", True),
        )

        # Execute analyze command
        result = router.route_analyze(analyze_args)
        return result.value if result.is_success else 1

    except Exception:
        if getattr(args, "verbose", False):
            traceback.print_exc()
        return 1


def another_function() -> str:
    """Placeholder function for test compatibility.

    This function exists for test compatibility and may be removed
    in future versions when test imports are updated.

    Returns:
        A simple string for testing.

    """
    return "placeholder"


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality - Enterprise Code Quality Analysis & Documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
 flext-quality analyze ./my-project
 flext-quality analyze ./my-project --output report.html --format html
 flext-quality score ./my-project
 flext-quality web --port 8080
 flext-quality doc comprehensive --project-root ./my-project
 flext-quality doc --help
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
    analyze_parser.add_argument("path", type=Path, help="Path to project")
    analyze_parser.add_argument("--output", "-o", type=Path, help="Output file path")
    analyze_parser.add_argument(
        "--format",
        "-f",
        default="table",
        choices=["table", "json", "html"],
    )
    analyze_parser.add_argument("--include-security", action="store_true", default=True)
    analyze_parser.add_argument(
        "--no-security",
        dest="include_security",
        action="store_false",
    )
    analyze_parser.add_argument(
        "--include-complexity",
        action="store_true",
        default=True,
    )
    analyze_parser.add_argument(
        "--no-complexity",
        dest="include_complexity",
        action="store_false",
    )
    analyze_parser.add_argument(
        "--include-dead-code",
        action="store_true",
        default=True,
    )
    analyze_parser.add_argument(
        "--no-dead-code",
        dest="include_dead_code",
        action="store_false",
    )
    analyze_parser.add_argument(
        "--include-duplicates",
        action="store_true",
        default=True,
    )
    analyze_parser.add_argument(
        "--no-duplicates",
        dest="include_duplicates",
        action="store_false",
    )

    # Score command
    score_parser = subparsers.add_parser("score", help="Get quick quality score")
    score_parser.add_argument("path", type=Path, help="Path to project")

    # Web command
    web_parser = subparsers.add_parser("web", help="Run web interface server")
    web_parser.add_argument("--host", default="127.0.0.1")
    web_parser.add_argument("--port", type=int, default=8000)
    web_parser.add_argument("--debug", action="store_true")

    # Make command - execute Makefile targets
    make_parser = subparsers.add_parser(
        "make",
        help="Execute project Makefile targets",
        description="Run make targets across FLEXT projects",
    )
    make_parser.add_argument(
        "target",
        help="Makefile target to execute (e.g., docs, fix, validate)",
    )
    make_parser.add_argument(
        "--project-path",
        type=Path,
        default=Path.cwd(),
        help="Path to the project (defaults to current directory)",
    )
    make_parser.add_argument(
        "--env",
        action="append",
        nargs="?",
        help="Environment variables (format: KEY=VALUE)",
    )

    # Doc command - delegates to documentation maintenance CLI
    doc_parser = subparsers.add_parser(
        "doc",
        help="Manage project documentation",
        description="Documentation maintenance and validation commands",
    )
    doc_parser.add_argument(
        "subcommand",
        nargs="?",
        default="comprehensive",
        help="Documentation subcommand (comprehensive, validate, etc.)",
    )
    doc_parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Path to the project root (defaults to current directory)",
    )
    doc_parser.add_argument(
        "--profile",
        default="advanced",
        help="Maintenance profile slug to use",
    )
    doc_parser.add_argument(
        "--config",
        type=Path,
        help="Optional path to a maintenance configuration file",
    )
    doc_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without applying changes",
    )
    doc_parser.add_argument(
        "--verbose-docs",
        action="store_true",
        help="Show detailed logging for documentation operations",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Handle make command (execute Makefile targets)
    if args.command == "make":
        return _run_make_target(args)

    # Handle doc command (delegates to documentation maintenance module)
    if args.command == "doc":
        return _route_doc_command(args)

    # Configure logging for quality commands
    config = CliConfig()
    quality_config = FlextQualitySettings()
    if args.verbose:
        quality_config.observability_log_level = "DEBUG"

    # Create service and route quality command
    service = FlextQualityCliService(config)
    router = service.get_router()

    if args.command == "analyze":
        result = router.route_analyze(args)
        return result.value if result.is_success else 1
    if args.command == "score":
        result = router.route_score(args)
        return result.value if result.is_success else 1
    if args.command == "web":
        result = router.route_web(args)
        return result.value if result.is_success else 1

    parser.print_help()
    return 1


def _run_make_target(args: object) -> int:
    """Execute a Makefile target using flext-core utilities."""
    cli = FlextCli()
    args_dict = vars(args)

    project_path = Path(args_dict.get("project_path", Path.cwd()))
    target = args_dict.get("target")

    # Validate target
    if not target or not isinstance(target, str):
        cli.formatters.print("Invalid target specified", style="red")
        return 1

    # Validate project path
    if not project_path.exists():
        cli.formatters.print(
            f"Project path does not exist: {project_path}",
            style="red",
        )
        return 1

    # Build environment with custom variables
    env = os.environ.copy()
    if args_dict.get("env"):
        for env_var in args_dict["env"]:
            if env_var and "=" in env_var:
                key, value = env_var.split("=", 1)
                env[key.strip()] = value.strip()

    # Execute make target using flext-core utilities (no code duplication)
    cli.formatters.print(f"Running: make {target}", style="cyan")
    result = SubprocessUtils.run_external_command(
        ["make", target],
        cwd=project_path,
        env=env,
        capture_output=False,
        check=False,
    )

    if result.is_success:
        process = result.value
        if process.returncode == 0:
            cli.formatters.print(
                f"✓ make {target} completed successfully",
                style="green",
            )
            return 0
        cli.formatters.print(
            f"✗ make {target} failed with code {process.returncode}",
            style="red",
        )
        return process.returncode

    # Error executing command
    error = result.error
    cli.formatters.print(f"Make execution error: {error}", style="red")
    return 1


def _route_doc_command(args: object) -> int:
    """Route documentation commands to the docs_maintenance module."""
    try:
        cli = FlextCli()

        # Convert argparse namespace to function arguments
        args_dict = vars(args)

        if args_dict.get("subcommand") == "comprehensive":
            run_comprehensive(
                project_root=args_dict.get("project_root", Path.cwd()),
                profile=args_dict.get("profile", "advanced"),
                config=args_dict.get("config"),
                dry_run=args_dict.get("dry_run", False),
                verbose=args_dict.get("verbose_docs", False),
            )
            return 0
        cli.formatters.print(
            f"Documentation subcommand '{args_dict.get('subcommand')}' "
            "not yet implemented. Use 'comprehensive'.",
            style="yellow",
        )
        return 1

    except Exception as e:
        cli = FlextCli()
        cli.formatters.print(f"Documentation command error: {e}", style="red")
        return 1


if __name__ == "__main__":
    main()
