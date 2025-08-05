#!/usr/bin/env python3
"""FLEXT Quality - Complete API Integration Example.

This example demonstrates comprehensive usage of the FLEXT Quality API including:
- Simple API usage with QualityAPI
- Advanced service integration patterns
- FLEXT ecosystem integration (flext-core, flext-observability)
- Async/await patterns for enterprise applications
- Error handling with FlextResult patterns
- Custom quality workflows and automation

This showcases complete API integration patterns for enterprise applications.
"""

import asyncio
import sys
import tempfile
from pathlib import Path

# Import FLEXT Quality components
from flext_quality import CodeAnalyzer, QualityAPI, QualityMetrics, QualityReport
from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)

# Import FLEXT core patterns
try:
    from flext_core import FlextResult, get_logger

    FLEXT_CORE_AVAILABLE = True
except ImportError:
    FLEXT_CORE_AVAILABLE = False

# Setup logging
if FLEXT_CORE_AVAILABLE:
    logger = get_logger(__name__)
else:
    import logging

    logger = logging.getLogger(__name__)


async def demonstrate_simple_api() -> None:
    """Demonstrate simple API usage patterns."""
    # Create sample project for analysis
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "sample_project"
        project_path.mkdir()

        # Create sample Python file
        sample_file = project_path / "sample.py"
        sample_file.write_text('''
"""Sample module for API demonstration."""

import os
import sys
from typing import Optional, List

def calculate_score(values: List[float]) -> float:
    """Calculate average score from values.

    Args:
        values: List of numeric values

    Returns:
        Average score as float
    """
    if not values:
        return 0.0

    total = sum(values)
    return total / len(values)

class DataProcessor:
    """Process data with quality analysis."""

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.processed_count = 0

    def process_item(self, item: Any) -> Optional[Any]:
        """Process individual item with validation."""
        if item is None:
            return None

        # Simple processing logic
        if isinstance(item, (int, float)):
            result = item * 2
            self.processed_count += 1
            return result
        elif isinstance(item, str):
            result = item.upper()
            self.processed_count += 1
            return result
        else:
            logger.warning(f"Unsupported item type: {type(item)}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "processed_count": self.processed_count,
            "threshold": self.threshold,
            "efficiency": min(1.0, self.processed_count / 100)
        }

if __name__ == "__main__":
    # Simple usage example
    processor = DataProcessor()

    test_values = [1, 2, 3, 4, 5]
    average = calculate_score(test_values)
    print(f"Average score: {average}")

    for value in test_values:
        result = processor.process_item(value)
        print(f"Processed {value} -> {result}")

    stats = processor.get_stats()
    print(f"Processing stats: {stats}")
''')

        # 1. Direct CodeAnalyzer usage

        analyzer = CodeAnalyzer(str(project_path))
        results = analyzer.analyze_project()

        analyzer.get_quality_score()
        analyzer.get_quality_grade()

        # 2. QualityMetrics usage

        metrics = QualityMetrics.from_analysis_results(results)

        # Show detailed scores
        for _category, _score_val in metrics.scores_summary.items():
            pass

        # 3. QualityReport generation

        report = QualityReport(results)

        # Generate JSON report
        json_report = report.generate_json_report()

        # Generate HTML report
        html_report = report.generate_html_report()

        # Save reports
        json_path = project_path / "api_demo_report.json"
        html_path = project_path / "api_demo_report.html"

        json_path.write_text(json_report)
        html_path.write_text(html_report)


async def demonstrate_service_integration() -> None:
    """Demonstrate advanced service integration patterns."""
    # Initialize services
    project_service = QualityProjectService()
    analysis_service = QualityAnalysisService()
    issue_service = QualityIssueService()
    report_service = QualityReportService()

    # Create a sample project using service

    # Create project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_result = await project_service.create_project(
            name="API Demo Project",
            project_path=temp_dir,
            language="python",
        )

        if project_result.success:
            project = project_result.data
        else:
            return

        # Create analysis

        analysis_result = await analysis_service.create_analysis(project_id=project.id)

        if analysis_result.success:
            analysis = analysis_result.data
        else:
            return

        # Update analysis metrics
        metrics_result = await analysis_service.update_metrics(
            analysis_id=analysis.id,
            total_files=5,
            total_lines=250,
            code_lines=200,
            comment_lines=30,
            blank_lines=20,
        )

        if metrics_result.success:
            pass
        else:
            return

        # Update quality scores
        scores_result = await analysis_service.update_scores(
            analysis_id=analysis.id,
            coverage_score=85.0,
            complexity_score=78.0,
            duplication_score=92.0,
            security_score=95.0,
            maintainability_score=80.0,
        )

        if scores_result.success:
            pass
        else:
            return

        # Create issues

        # Create different types of issues
        issues_data = [
            {
                "issue_type": "security",
                "severity": "high",
                "rule_id": "S001",
                "file_path": "src/auth.py",
                "line_number": 42,
                "message": "Potential SQL injection vulnerability",
            },
            {
                "issue_type": "complexity",
                "severity": "medium",
                "rule_id": "C001",
                "file_path": "src/processor.py",
                "line_number": 15,
                "message": "Cyclomatic complexity too high (12)",
            },
            {
                "issue_type": "style",
                "severity": "low",
                "rule_id": "E301",
                "file_path": "src/utils.py",
                "line_number": 8,
                "message": "Expected 1 blank line, found 0",
            },
        ]

        created_issues = []
        for issue_data in issues_data:
            issue_result = await issue_service.create_issue(
                analysis_id=analysis.id,
                **issue_data,
            )

            if issue_result.success:
                issue = issue_result.data
                created_issues.append(issue)

        # Update issue counts in analysis
        issue_counts_result = await analysis_service.update_issue_counts(
            analysis_id=analysis.id,
            critical=0,
            high=1,
            medium=1,
            low=1,
        )

        if issue_counts_result.success:
            pass

        # Complete the analysis
        complete_result = await analysis_service.complete_analysis(analysis.id)

        if complete_result.success:
            pass

        # Create reports

        # Create different report types
        report_types = ["html", "json", "pdf"]

        for report_type in report_types:
            report_result = await report_service.create_report(
                analysis_id=analysis.id,
                report_type=report_type,
            )

            if report_result.success:
                pass

        # List all reports for the analysis
        reports_result = await report_service.list_reports(analysis.id)

        if reports_result.success:
            reports = reports_result.data
            for _report in reports:
                pass


async def demonstrate_flext_ecosystem_integration() -> None:
    """Demonstrate FLEXT ecosystem integration patterns."""
    if not FLEXT_CORE_AVAILABLE:
        pass

    # Demonstrate FlextResult pattern usage

    # Create sample project for analysis
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "ecosystem_demo"
        project_path.mkdir()

        # Create sample file
        (project_path / "demo.py").write_text('''
def process_data(data):
    """Process data with basic validation."""
    if not data:
        return []

    results = []
    for item in data:
        if item and isinstance(item, (str, int, float)):
            results.append(str(item).upper())

    return results
''')

        # Demonstrate API usage with result handling
        QualityAPI()

        try:
            # Use direct analyzer (QualityAPI is a simple wrapper)
            analyzer = CodeAnalyzer(str(project_path))
            results = analyzer.analyze_project()

            analysis_data = {
                "quality_score": analyzer.get_quality_score(),
                "quality_grade": analyzer.get_quality_grade(),
                "files_analyzed": results.get("files_analyzed", 0),
                "total_lines": results.get("total_lines", 0),
                "analysis_results": results,
            }

        except Exception:
            return

        # Demonstrate observability integration (if available)

        try:
            from flext_observability import (
                flext_create_log_entry,
                flext_create_metric,
                flext_create_trace,
            )

            # Create metrics
            flext_create_metric(
                name="quality_analysis_score",
                value=analysis_data.get("quality_score", 0),
                tags={"project": "ecosystem_demo", "integration": "api"},
            )

            # Create trace
            flext_create_trace(
                trace_id="ecosystem_demo_analysis",
                operation="api.analyze_project",
                config={"project_path": str(project_path)},
            )

            # Create log entry
            flext_create_log_entry(
                message="FLEXT Quality ecosystem integration demonstration completed",
                level="info",
                context={
                    "component": "quality_api",
                    "project": "ecosystem_demo",
                    "files_analyzed": analysis_data.get("files_analyzed", 0),
                },
            )

        except ImportError:
            # Simulate observability integration
            pass

        # Demonstrate container-based dependency injection (if available)

        if FLEXT_CORE_AVAILABLE:
            try:
                from flext_core import FlextContainer

                # Create container
                container = FlextContainer()

                # Register services
                project_service_instance = QualityProjectService()
                analysis_service_instance = QualityAnalysisService()

                container.register("QualityProjectService", project_service_instance)
                container.register("QualityAnalysisService", analysis_service_instance)

                # Resolve services (FlextContainer.get returns FlextResult)
                project_service_result = container.get("QualityProjectService")
                analysis_service_result = container.get("QualityAnalysisService")

                if project_service_result.success and analysis_service_result.success:
                    project_service = project_service_result.data

                    # Demonstrate service usage
                    with tempfile.TemporaryDirectory() as temp_service_dir:
                        project_result = await project_service.create_project(
                            name="DI Demo Project",
                            project_path=temp_service_dir,
                        )

                        if project_result.success:
                            pass

            except ImportError:
                # Direct instantiation
                project_service = QualityProjectService()
                QualityAnalysisService()
        else:
            project_service = QualityProjectService()
            QualityAnalysisService()


async def demonstrate_custom_workflows() -> None:
    """Demonstrate custom quality workflow automation."""
    # Define custom workflow
    workflow_steps = [
        "Initialize project analysis",
        "Execute quality analysis",
        "Process quality metrics",
        "Generate comprehensive reports",
        "Apply quality gates",
        "Send notifications",
    ]

    for _i, _step in enumerate(workflow_steps, 1):
        pass

    # Create sample project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "workflow_demo"
        project_path.mkdir()

        # Create sample files
        files_data = {
            "main.py": '''
"""Main application module."""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Application:
    """Main application class."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the application."""
        try:
            logger.info("Initializing application...")
            # Initialization logic here
            self.initialized = True
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False

    def process_data(self, data: List[Any]) -> List[Any]:
        """Process input data."""
        if not self.initialized:
            raise RuntimeError("Application not initialized")

        results = []
        for item in data:
            try:
                processed = self._process_item(item)
                if processed is not None:
                    results.append(processed)
            except Exception as e:
                logger.warning(f"Failed to process item {item}: {e}")

        return results

    def _process_item(self, item: Any) -> Any:
        """Process individual item."""
        if isinstance(item, str):
            return item.strip().upper()
        elif isinstance(item, (int, float)):
            return item * 2
        else:
            return None

if __name__ == "__main__":
    app = Application({"debug": True})
    if app.initialize():
        test_data = ["hello", "world", 42, 3.14]
        results = app.process_data(test_data)
        print(f"Processed results: {results}")
''',
            "utils.py": '''
"""Utility functions."""

def calculate_average(numbers: List[float]) -> float:
    """Calculate average of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value * 100:.1f}%"
''',
            "tests.py": '''
"""Test module."""

import unittest
from main import Application
from utils import calculate_average, format_percentage

class TestApplication(unittest.TestCase):
    """Test cases for Application."""

    def setUp(self):
        self.app = Application({"debug": False})

    def test_initialization(self):
        """Test application initialization."""
        self.assertTrue(self.app.initialize())
        self.assertTrue(self.app.initialized)

    def test_data_processing(self):
        """Test data processing."""
        self.app.initialize()
        data = ["test", 42]
        results = self.app.process_data(data)
        self.assertEqual(len(results), 2)

class TestUtils(unittest.TestCase):
    """Test cases for utilities."""

    def test_calculate_average(self):
        """Test average calculation."""
        self.assertEqual(calculate_average([1, 2, 3]), 2.0)
        self.assertEqual(calculate_average([]), 0.0)

    def test_format_percentage(self):
        """Test percentage formatting."""
        self.assertEqual(format_percentage(0.5), "50.0%")

if __name__ == "__main__":
    unittest.main()
''',
        }

        # Create files
        for filename, content in files_data.items():
            (project_path / filename).write_text(content)

        # Execute custom workflow

        # Step 1: Initialize project analysis
        analyzer = CodeAnalyzer(str(project_path))

        # Step 2: Execute quality analysis
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

        # Step 3: Process quality metrics
        metrics = QualityMetrics.from_analysis_results(results)
        score = analyzer.get_quality_score()
        analyzer.get_quality_grade()

        # Step 4: Generate comprehensive reports
        report = QualityReport(results)

        json_report = report.generate_json_report()
        html_report = report.generate_html_report()

        # Save reports
        json_path = project_path / "workflow_report.json"
        html_path = project_path / "workflow_report.html"
        json_path.write_text(json_report)
        html_path.write_text(html_report)

        # Step 5: Apply quality gates

        # Define quality gates
        quality_gates = {
            "min_score": 70.0,
            "max_security_issues": 0,
            "max_complexity_issues": 3,
            "max_total_issues": 5,
        }

        # Check gates
        gates_passed = 0
        len(quality_gates)

        # Score gate
        if score >= quality_gates["min_score"]:
            gates_passed += 1

        # Security gate
        if metrics.security_issues_count <= quality_gates["max_security_issues"]:
            gates_passed += 1

        # Complexity gate
        if metrics.complexity_issues_count <= quality_gates["max_complexity_issues"]:
            gates_passed += 1

        # Total issues gate
        if metrics.total_issues <= quality_gates["max_total_issues"]:
            gates_passed += 1

        # Overall gate decision

        # Step 6: Send notifications

        # Simulate notifications
        notification_channels = ["email", "slack", "webhook"]

        for _channel in notification_channels:
            pass

        # Workflow summary


async def main() -> int:
    """Main demonstration of complete API integration functionality."""
    try:
        # Demonstrate all API integration patterns
        await demonstrate_simple_api()
        await demonstrate_service_integration()
        await demonstrate_flext_ecosystem_integration()
        await demonstrate_custom_workflows()

        return 0

    except Exception:
        logger.exception("API integration demonstration failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
