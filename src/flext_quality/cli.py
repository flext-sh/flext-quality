"""FLEXT Quality CLI interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import argparse
import json
import logging
import os
import traceback
from pathlib import Path
from typing import Self, override

from flext_cli import FlextCli, FlextCliFileTools
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextTypes as t,
)
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from .analyzer import FlextQualityAnalyzer
from .command_strategies import CommandStrategies as c
from .docs_maintenance.cli import run_comprehensive
from .plugins.code_quality_plugin import FlextCodeQualityPlugin
from .reports import FlextQualityReportGenerator, ReportFormat
from .settings import FlextQualitySettings
from .subprocess_utils import SubprocessUtils
from .tools.quality_operations import FlextQualityOperations
from .tools.test_operations import (
    FixtureConsolidateOperation,
    TestAntipatternOperation,
    TestInheritanceOperation,
    TestStructureOperation,
)
from .tools.workspace_discovery import FlextWorkspaceDiscovery
from .web import FlextQualityWeb

# Type alias for test quality operation results
TestQualityResult = dict[str, t.GeneralValueType]

# CLI Display Constants
MAX_ITEMS_TO_DISPLAY = 5  # Maximum items to show in tree/table output
COVERAGE_GOOD_THRESHOLD = 80  # Excellent coverage percentage
COVERAGE_ACCEPTABLE_THRESHOLD = 70  # Minimum acceptable coverage

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
    # Display configuration (Fase 4)
    max_display_items: int = Field(default=5, ge=1)
    coverage_good_threshold: float = Field(default=80.0, ge=0, le=100)
    coverage_acceptable_threshold: float = Field(default=70.0, ge=0, le=100)


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


class CliCommandRouter:
    """Routes CLI commands to appropriate handlers."""

    def __init__(self, logger: FlextLogger, config: CliConfig) -> None:
        """Initialize router with logger and config."""
        super().__init__()
        self.logger = logger
        self.config = config
        self.formatter = QualityReportFormatter(logger)
        self._cli = FlextCli()
        self._console = Console()
        self._quiet_mode = False

    def _configure_from_args(self, args: argparse.Namespace) -> None:
        """Configure CLI based on command arguments (quiet mode, etc)."""
        # Enable quiet mode if requested
        if (hasattr(args, "quiet") and args.quiet) or (
            hasattr(args, "no_color") and args.no_color
        ):
            self._quiet_mode = True

    def _maybe_print(self, message: str, style: str = "info") -> None:
        """Print message only if not in quiet mode."""
        if self._quiet_mode:
            return
        if style == "error":
            self.logger.error(message)
        elif style == "warning":
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def _format_and_display_result(
        self,
        result: t.GeneralValueType,
        fmt: str = "table",
    ) -> None:
        """Auto-dispatch result formatting based on type.

        Uses isinstance checks for type-safe routing without getattr().
        Respects quiet_mode and selected format.
        """
        if self._quiet_mode:
            return

        # Dispatch based on result type with explicit routing
        if isinstance(result, FlextCodeQualityPlugin.CheckResult):
            self._display_check_result(result, fmt)
        elif isinstance(result, FlextCodeQualityPlugin.WorkspaceCheckResult):
            self._display_workspace_result(result, fmt)
        elif isinstance(result, dict):
            self._display_analysis_result(result, fmt)

    def _display_check_result(
        self,
        result: FlextCodeQualityPlugin.CheckResult,
        fmt: str,
    ) -> None:
        """Display CheckResult as table or JSON."""
        if fmt == "json":
            data = {
                "total_violations": result.total_violations,
                "files_checked": result.files_checked,
                "violations_by_category": result.violations_by_category,
                "violations_by_severity": result.violations_by_severity,
            }
            self._cli.formatters.print(json.dumps(data, indent=2))
            return

        # Table format (default)
        summary_table = Table(title="📊 Check Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_row("Files Checked", str(result.files_checked))
        summary_table.add_row("Total Violations", str(result.total_violations))

        category_table = Table(title="By Category")
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Count", style="yellow")
        for category, count in result.violations_by_category.items():
            category_table.add_row(category, str(count))

        severity_table = Table(title="By Severity")
        severity_table.add_column("Severity", style="cyan")
        severity_table.add_column("Count", style="magenta")
        for severity, count in result.violations_by_severity.items():
            severity_table.add_row(severity, str(count))

        self._cli.formatters.print(summary_table)
        self._cli.formatters.print(category_table)
        self._cli.formatters.print(severity_table)

    def _display_workspace_result(
        self,
        result: FlextCodeQualityPlugin.WorkspaceCheckResult,
        fmt: str,
    ) -> None:
        """Display WorkspaceCheckResult as table or JSON."""
        if fmt == "json":
            data = {
                "total_projects": result.total_projects,
                "total_files": result.total_files,
                "total_violations": result.total_violations,
                "violations_by_project": result.violations_by_project,
                "violations_by_category": result.violations_by_category,
                "violations_by_severity": result.violations_by_severity,
            }
            self._cli.formatters.print(json.dumps(data, indent=2))
            return

        # Table format (default)
        summary_table = Table(title="📊 Workspace Check Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_row("Total Projects", str(result.total_projects))
        summary_table.add_row("Total Files", str(result.total_files))
        summary_table.add_row("Total Violations", str(result.total_violations))

        project_table = Table(title="By Project")
        project_table.add_column("Project", style="cyan")
        project_table.add_column("Violations", style="yellow")
        for project, violations in result.violations_by_project.items():
            project_table.add_row(project, str(violations))

        category_table = Table(title="By Category")
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Count", style="yellow")
        for category, count in result.violations_by_category.items():
            category_table.add_row(category, str(count))

        self._cli.formatters.print(summary_table)
        self._cli.formatters.print(project_table)
        self._cli.formatters.print(category_table)

    def _display_analysis_result(
        self,
        result: dict,
        fmt: str,
    ) -> None:
        """Display analysis result as table or JSON."""
        if fmt == "json":
            self._cli.formatters.print(json.dumps(result, indent=2))
            return

        # Table format (default)
        quality_table = Table(title="📊 Quality Analysis")
        quality_table.add_column("Metric", style="cyan")
        quality_table.add_column("Value", style="green")
        for key, value in result.items():
            quality_table.add_row(str(key), str(value))

        self._cli.formatters.print(quality_table)

    def route_analyze(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route analyze command."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

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
        analyzer_wrapper = ProjectQualityAnalyzer(self.logger, self.config)
        analyzer_result = analyzer_wrapper.analyze(project_path, options)

        if analyzer_result.is_failure:
            self.logger.error(analyzer_result.error or "Unknown error")
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
            self.logger.error(output_result.error or "Unknown error")
            return FlextResult[int].ok(1)

        # Determine exit code using strategy thresholds (strategy-driven)
        quality_score = analyzer.get_quality_score()
        if quality_score >= c.ANALYZE_SUCCESS_THRESHOLD:
            exit_code = 0
            self._maybe_print(f"✅ Good quality: {quality_score:.1f}%", "success")
        elif quality_score >= c.ANALYZE_WARNING_THRESHOLD:
            exit_code = 1
            self._maybe_print(f"⚠️  Medium quality: {quality_score:.1f}%", "warning")
        else:
            exit_code = 2
            self._maybe_print(f"❌ Poor quality: {quality_score:.1f}%", "error")

        return FlextResult[int].ok(exit_code)

    def route_score(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route score command."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

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
        analyzer_wrapper = ProjectQualityAnalyzer(self.logger, self.config)
        analyzer_result = analyzer_wrapper.analyze(project_path, options)

        if analyzer_result.is_failure:
            self.logger.error(analyzer_result.error or "Unknown error")
            return FlextResult[int].ok(1)

        analyzer = analyzer_result.value
        quality_score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()

        # Display score (respects quiet mode)
        self._maybe_print(f"📊 Quality Score: {quality_score:.1f}% ({grade})", "info")

        # Return exit code using strategy thresholds
        if quality_score >= c.SCORE_SUCCESS_THRESHOLD:
            self._maybe_print("✅ Quality acceptable", "success")
            return FlextResult[int].ok(0)
        if quality_score >= c.SCORE_WARNING_THRESHOLD:
            self._maybe_print("⚠️  Quality needs improvement", "warning")
            return FlextResult[int].ok(1)

        self._maybe_print("❌ Quality critically low", "error")
        return FlextResult[int].ok(2)

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
            return FlextResult[int].ok(2)

    def route_check(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route check command (lint + type)."""
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.check()

        if result.is_failure:
            self.logger.error(f"Check failed: {result.error}")
            return FlextResult[int].ok(2)

        report = result.value
        if report.passed:
            self.logger.info(
                f"Check PASSED - lint: {report.lint_errors}, type: {report.type_errors}",
            )
            return FlextResult[int].ok(0)

        self.logger.error(
            f"Check FAILED - lint: {report.lint_errors}, type: {report.type_errors}",
        )
        return FlextResult[int].ok(2)

    def route_validate(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route validate command (lint + type + security + test) with Rich UI."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.validate_project(min_coverage=args.min_coverage)

        if result.is_failure:
            self.logger.error(f"Validate failed: {result.error}")
            return FlextResult[int].ok(1)

        report = result.value
        if not self._quiet_mode:
            self._display_validation_report(report)

        # Use strategy-driven validation result (report.passed)
        if report.passed:
            self._maybe_print("✅ Validation PASSED", "success")
            return FlextResult[int].ok(0)

        self._maybe_print("❌ Validation FAILED", "error")
        return FlextResult[int].ok(2)

    def _display_validation_report(
        self,
        report: t.GeneralValueType,  # Would be ValidationReport type
    ) -> None:
        """Display validation report."""
        self.logger.info("🔍 Validation Report")
        self.logger.info(str(report))

    def route_lint(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route lint command."""
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.lint(fix=args.fix)

        if result.is_failure:
            self.logger.error(f"Lint failed: {result.error}")
            return FlextResult[int].ok(2)

        report = result.value
        if report.passed:
            self.logger.info(f"Lint PASSED - {report.files_checked} files checked")
            return FlextResult[int].ok(0)

        self.logger.error(f"Lint FAILED - {report.errors} errors")
        return FlextResult[int].ok(2)

    def route_type_check(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route type-check command."""
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.type_check(strict=args.strict)

        if result.is_failure:
            self.logger.error(f"Type check failed: {result.error}")
            return FlextResult[int].ok(2)

        report = result.value
        if report.passed:
            self.logger.info(
                f"Type check PASSED ({report.tool}) - {report.files_checked} files",
            )
            return FlextResult[int].ok(0)

        self.logger.error(f"Type check FAILED - {report.errors} errors")
        return FlextResult[int].ok(2)

    def route_security(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route security command."""
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.security()

        if result.is_failure:
            self.logger.error(f"Security scan failed: {result.error}")
            return FlextResult[int].ok(2)

        report = result.value
        if report.passed:
            self.logger.info("Security scan PASSED")
            return FlextResult[int].ok(0)

        self.logger.error(
            f"Security scan FAILED - high={report.high}, medium={report.medium}",
        )
        return FlextResult[int].ok(2)

    def route_test(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route test command."""
        path_result = CliArgumentValidator.validate_project_path(args.path)
        if path_result.is_failure:
            self.logger.error(path_result.error or "Invalid path")
            return FlextResult[int].ok(1)

        ops = FlextQualityOperations(path_result.value)
        result = ops.test(min_coverage=args.min_coverage)

        if result.is_failure:
            self.logger.error(f"Test execution failed: {result.error}")
            return FlextResult[int].ok(2)

        report = result.value
        if report.passed:
            self.logger.info(
                f"Tests PASSED - coverage={report.coverage_percent:.1f}%",
            )
            return FlextResult[int].ok(0)

        self.logger.error(f"Tests FAILED - {report.failed_count} failures")
        return FlextResult[int].ok(2)

    def route_test_antipatterns(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route test antipatterns subcommand."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        targets = self._resolve_test_quality_targets(args)
        if not targets:
            self.logger.error("No valid targets found")
            return FlextResult[int].ok(2)

        operation = TestAntipatternOperation()
        return self._execute_test_operation(operation, args, targets, "antipatterns")

    def route_test_inheritance(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route test inheritance subcommand."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        targets = self._resolve_test_quality_targets(args)
        if not targets:
            self.logger.error("No valid targets found")
            return FlextResult[int].ok(2)

        operation = TestInheritanceOperation()
        return self._execute_test_operation(operation, args, targets, "inheritance")

    def route_test_structure(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route test structure subcommand."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        targets = self._resolve_test_quality_targets(args)
        if not targets:
            self.logger.error("No valid targets found")
            return FlextResult[int].ok(2)

        operation = TestStructureOperation()
        return self._execute_test_operation(operation, args, targets, "structure")

    def route_test_fixtures(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route test fixtures subcommand."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        targets = self._resolve_test_quality_targets(args)
        if not targets:
            self.logger.error("No valid targets found")
            return FlextResult[int].ok(2)

        operation = FixtureConsolidateOperation()
        return self._execute_test_operation(operation, args, targets, "fixtures")

    def _execute_test_operation(
        self,
        operation: TestAntipatternOperation
        | TestInheritanceOperation
        | TestStructureOperation
        | FixtureConsolidateOperation,
        args: argparse.Namespace,
        targets: list[Path],
        name: str,
    ) -> FlextResult[int]:
        """Execute test quality operation with appropriate mode."""
        if args.dry_run:
            result = operation.dry_run(targets)
            if result.is_failure:
                self.logger.error(f"Dry run failed: {result.error}")
                return FlextResult[int].ok(2)
            if not self._quiet_mode:
                self._print_test_quality_result(result.value, name, "dry-run")
            return FlextResult[int].ok(0)

        if args.execute:
            result = operation.run(targets, None)
            if result.is_failure:
                self.logger.error(f"Execute failed: {result.error}")
                return FlextResult[int].ok(2)
            if not self._quiet_mode:
                self._print_test_quality_result(result.value, name, "execute")
            return FlextResult[int].ok(0)

        if args.rollback:
            backup_dir = Path.home() / ".flext" / "backups"
            result = operation.rollback(backup_dir)
            if result.is_failure:
                self.logger.error(f"Rollback failed: {result.error}")
                return FlextResult[int].ok(2)
            self._maybe_print("Rollback completed", "success")
            return FlextResult[int].ok(0)

        # Default: dry-run
        result = operation.dry_run(targets)
        if result.is_failure:
            self.logger.error(f"Analysis failed: {result.error}")
            return FlextResult[int].ok(2)
        if not self._quiet_mode:
            self._print_test_quality_result(result.value, name, "dry-run")
        return FlextResult[int].ok(0)

    def _resolve_test_quality_targets(self, args: argparse.Namespace) -> list[Path]:
        """Resolve target paths for test quality operations."""
        targets: list[Path] = []
        workspace_root = Path.home() / "flext"

        # Single target file
        if args.target:
            path = Path(args.target)
            if path.exists():
                targets.append(path)
            return targets

        # Single project
        if args.project:
            project_path = workspace_root / args.project
            if project_path.exists():
                targets.append(project_path)
            return targets

        # Workspace (all projects via discovery)
        if args.workspace:
            discovery = FlextWorkspaceDiscovery(workspace_root=workspace_root)
            result = discovery.get_ordered_projects()
            if result.is_success:
                targets.extend(
                    workspace_root / project_name
                    for project_name in result.value
                    if (workspace_root / project_name).exists()
                )
            return targets

        # Default: current directory
        targets.append(Path.cwd())
        return targets

    def _print_test_quality_result(
        self,
        result: TestQualityResult,
        subcommand: str,
        mode: str,
    ) -> None:
        """Print test quality operation result with Rich UI."""
        # Create root tree
        mode_symbol = "🔍" if mode == "dry-run" else "⚙️" if mode == "execute" else "↩️"
        tree = Tree(
            f"{mode_symbol} Test Quality: {subcommand.upper()} ({mode.upper()})"
        )

        # Process results
        for key, value in result.items():
            if key == "duplicates" and isinstance(value, list):
                dup_branch = tree.add(f"📋 Duplicates: {len(value)} groups")
                for dup in value[:MAX_ITEMS_TO_DISPLAY]:
                    if isinstance(dup, dict):
                        name = dup.get("name", "unknown")
                        dup_branch.add(f"[yellow]{name}[/yellow]")
                if len(value) > MAX_ITEMS_TO_DISPLAY:
                    dup_branch.add(
                        f"[dim]... and {len(value) - MAX_ITEMS_TO_DISPLAY} more[/dim]"
                    )

            elif key == "issues" and isinstance(value, list):
                issues_branch = tree.add(f"⚠️  Issues: {len(value)} found")
                for issue in value[:MAX_ITEMS_TO_DISPLAY]:
                    if isinstance(issue, dict):
                        file = issue.get("file", "unknown")
                        msg = issue.get("message", "")
                        issues_branch.add(f"[red]{file}[/red]: {msg}")
                if len(value) > MAX_ITEMS_TO_DISPLAY:
                    issues_branch.add(
                        f"[dim]... and {len(value) - MAX_ITEMS_TO_DISPLAY} more[/dim]"
                    )

            elif isinstance(value, (int, float)):
                tree.add(f"[cyan]{key}[/cyan]: [magenta]{value}[/magenta]")
            else:
                tree.add(f"[cyan]{key}[/cyan]: {value}")

        # Display tree
        tree_str = self._cli.formatters.render_tree_to_string(tree)
        if tree_str.is_success:
            self._cli.formatters.print(tree_str.value)

    def route_code_quality(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route code-quality command (SOLID/DRY/KISS validation) with Rich UI."""
        # Configure quiet mode and other settings from args
        self._configure_from_args(args)

        plugin = FlextCodeQualityPlugin()
        workspace_root = Path.home() / "flext"

        if args.workspace:
            result = plugin.check_workspace(
                workspace_root=workspace_root,
                categories=args.categories if hasattr(args, "categories") else None,
            )
            if result.is_failure:
                self.logger.error(f"Code quality check failed: {result.error}")
                return FlextResult[int].ok(2)
            workspace_result = result.value

            # Display workspace analysis with Rich table (respects quiet mode)
            if not self._quiet_mode:
                self._display_workspace_analysis(workspace_result)

            if workspace_result.total_violations == 0:
                self._maybe_print("✅ Code quality check PASSED", "success")
                return FlextResult[int].ok(0)

            critical = workspace_result.violations_by_severity.get("ERROR", 0)
            if critical > 0:
                self._maybe_print(
                    f"❌ Code quality FAILED - {critical} critical violations", "error"
                )
                return FlextResult[int].ok(2)

            self._maybe_print(
                f"⚠️  Completed with {workspace_result.total_violations} warnings",
                "warning",
            )
            return FlextResult[int].ok(1)

        target_path = Path(args.target) if args.target else Path.cwd()
        if not target_path.exists():
            self.logger.error(f"Target does not exist: {target_path}")
            return FlextResult[int].ok(2)
        targets = (
            [target_path]
            if target_path.is_file()
            else list(
                target_path.rglob("*.py"),
            )
        )
        result_check: FlextResult[FlextCodeQualityPlugin.CheckResult] = plugin.check(
            targets=targets,
            categories=args.categories if hasattr(args, "categories") else None,
        )
        if result_check.is_failure:
            self.logger.error(f"Code quality check failed: {result_check.error}")
            return FlextResult[int].ok(2)
        check_result: FlextCodeQualityPlugin.CheckResult = result_check.value

        # Display single-target analysis with Rich table (respects quiet mode)
        if not self._quiet_mode:
            self._display_check_analysis(check_result)

        if check_result.total_violations == 0:
            self._maybe_print("✅ Code quality check PASSED", "success")
            return FlextResult[int].ok(0)

        critical = check_result.violations_by_severity.get("ERROR", 0)
        if critical > 0:
            self._maybe_print(
                f"❌ Code quality FAILED - {critical} critical violations", "error"
            )
            return FlextResult[int].ok(2)

        self._maybe_print(
            f"⚠️  Completed with {check_result.total_violations} warnings", "warning"
        )
        return FlextResult[int].ok(1)

    def _display_workspace_analysis(
        self,
        result: FlextCodeQualityPlugin.WorkspaceCheckResult,
    ) -> None:
        """Display workspace analysis."""
        self.logger.info("📊 Code Quality Analysis (Workspace)")
        self.logger.info(f"  Projects: {result.total_projects}")
        self.logger.info(f"  Files Checked: {result.total_files}")
        self.logger.info(f"  Total Violations: {result.total_violations}")

        if result.violations_by_category:
            self.logger.info("  Violations by Category:")
            for cat, count in result.violations_by_category.items():
                self.logger.info(f"    {cat}: {count}")

        if result.violations_by_severity:
            self.logger.info("  Violations by Severity:")
            for sev, count in result.violations_by_severity.items():
                self.logger.info(f"    {sev}: {count}")

    def _display_check_analysis(
        self,
        result: FlextCodeQualityPlugin.CheckResult,
    ) -> None:
        """Display single-target analysis."""
        self.logger.info("📊 Code Quality Analysis")
        self.logger.info(f"  Files Checked: {result.files_checked}")
        self.logger.info(f"  Total Violations: {result.total_violations}")

        if result.violations_by_category:
            self.logger.info("  Violations by Category:")
            for cat, count in result.violations_by_category.items():
                self.logger.info(f"    {cat}: {count}")

        if result.violations_by_severity:
            self.logger.info("  Violations by Severity:")
            for sev, count in result.violations_by_severity.items():
                self.logger.info(f"    {sev}: {count}")

    def route_report(self, args: argparse.Namespace) -> FlextResult[int]:
        """Route report command - generate quality reports."""
        plugin = FlextCodeQualityPlugin()
        ws = Path(args.workspace) if args.workspace else Path.home() / "flext"
        result = plugin.check_workspace(workspace_root=ws)

        if result.is_failure:
            self.logger.error(f"Report generation failed: {result.error}")
            return FlextResult[int].ok(2)

        check_result = result.value
        output_path = Path(args.output) if args.output else Path(".quality-reports")
        output_path.mkdir(parents=True, exist_ok=True)

        report_file = output_path / "code-quality-report.txt"
        lines = [
            "FLEXT Code Quality Report",
            f"Workspace: {ws}",
            f"Total violations: {check_result.total_violations}",
            f"Files checked: {check_result.total_files}",
            "",
            "By Project:",
        ]
        for proj, count in check_result.violations_by_project.items():
            lines.append(f"  {proj}: {count}")

        report_file.write_text("\n".join(lines))
        self.logger.info(f"Report saved to: {report_file}")
        return FlextResult[int].ok(0)


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
        return result.map_or(1)

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

    # Check command - quick lint + type (matches 'make check')
    check_parser = subparsers.add_parser("check", help="Quick check: lint + type")
    check_parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Path to project",
    )

    # Validate command - full validation (matches 'make validate')
    validate_parser = subparsers.add_parser(
        "validate",
        help="Full validation: lint + type + security + test",
    )
    validate_parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Path to project",
    )
    validate_parser.add_argument(
        "--min-coverage",
        type=float,
        default=None,
        help="Minimum test coverage percentage (default from constants)",
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

    # Test quality command - test quality operations
    test_quality_parser = subparsers.add_parser(
        "test-quality",
        help="Test quality operations (antipatterns, inheritance, structure, fixtures)",
        description="Analyze and fix test quality issues across FLEXT projects",
    )
    test_quality_subparsers = test_quality_parser.add_subparsers(
        dest="test_subcommand",
        help="Test quality subcommands",
    )

    # Common arguments for all test-quality subcommands
    def _add_test_quality_args(subparser: argparse.ArgumentParser) -> None:
        """Add common arguments to test quality subparsers."""
        subparser.add_argument(
            "--dry-run",
            action="store_true",
            default=True,
            help="Preview changes without modification (default)",
        )
        subparser.add_argument(
            "--execute",
            action="store_true",
            help="Apply changes with backup",
        )
        subparser.add_argument(
            "--rollback",
            action="store_true",
            help="Restore from backup",
        )
        subparser.add_argument(
            "--project",
            help="Target project name (e.g., flext-core)",
        )
        subparser.add_argument(
            "--workspace",
            action="store_true",
            help="Apply to all projects in workspace",
        )
        subparser.add_argument(
            "--target",
            type=Path,
            help="Specific file path to analyze",
        )

    # Test antipatterns subcommand
    antipatterns_parser = test_quality_subparsers.add_parser(
        "antipatterns",
        help="Detect and remove test anti-patterns (Mock, type:ignore, Any, cast)",
    )
    _add_test_quality_args(antipatterns_parser)

    # Test inheritance subcommand
    inheritance_parser = test_quality_subparsers.add_parser(
        "inheritance",
        help="Fix test class inheritance patterns",
    )
    _add_test_quality_args(inheritance_parser)

    # Test structure subcommand
    structure_parser = test_quality_subparsers.add_parser(
        "structure",
        help="Ensure test structure matches src/ modules",
    )
    _add_test_quality_args(structure_parser)

    # Test fixtures subcommand
    fixtures_parser = test_quality_subparsers.add_parser(
        "fixtures",
        help="Consolidate duplicate fixtures across projects",
    )
    _add_test_quality_args(fixtures_parser)

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
        return result.map_or(1)
    if args.command == "score":
        result = router.route_score(args)
        return result.map_or(1)
    if args.command == "web":
        result = router.route_web(args)
        return result.map_or(1)
    if args.command == "check":
        result = router.route_check(args)
        return result.map_or(1)
    if args.command == "validate":
        result = router.route_validate(args)
        return result.map_or(1)
    if args.command == "test-quality":
        subcommand = args.test_subcommand
        if subcommand == "antipatterns":
            result = router.route_test_antipatterns(args)
            return result.map_or(1)
        if subcommand == "inheritance":
            result = router.route_test_inheritance(args)
            return result.map_or(1)
        if subcommand == "structure":
            result = router.route_test_structure(args)
            return result.map_or(1)
        if subcommand == "fixtures":
            result = router.route_test_fixtures(args)
            return result.map_or(1)
        test_quality_parser.print_help()
        return 1

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
