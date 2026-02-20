#!/usr/bin/env python3
"""FLEXT Quality - Complete API Integration Example.

This example demonstrates comprehensive usage of the FLEXT Quality API including:
- Simple API usage with QualityAPI
- Advanced service integration patterns
- FLEXT ecosystem integration (flext-core, flext-observability)
- /patterns for enterprise applications
- Error handling with FlextResult patterns
- Custom quality workflows and automation

This showcases complete API integration patterns for enterprise applications.
"""

import sys
import tempfile
from pathlib import Path

from flext_core import FlextContainer, FlextLogger
from flext_observability import (
    flext_log_entry,
    flext_metric,
    flext_trace,
)
from flext_quality import (
    CodeAnalyzer,
    QualityAPI,
    QualityMetrics,
)
from flext_quality.reports import FlextQualityReportGenerator

logger = FlextLogger(__name__)


def demonstrate_simple_api() -> None:
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

def calculate_score(values: t.FloatList) -> float:
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

    def process_item(self, item: object) -> t.Optional[object]:
      """Process individual item with validation."""
      if item is None:
          return None


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

    def get_stats(self) -> dict[str, t.GeneralValueType]:
      """Get processing statistics."""
      return {
          "processed_count": self.processed_count,
          "threshold": self.threshold,
          "efficiency": min(1.0, self.processed_count / 100)
      }

if __name__ == "__main__":

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
        result = analyzer.analyze_project()

        # Unwrap FlextResult
        if result.is_failure:
            logger.error(f"Analysis failed: {result.error}")
            return

        results = result.value

        analyzer.get_quality_score()
        analyzer.get_quality_grade()

        # 2. QualityMetrics usage

        metrics = QualityMetrics.from_analysis_results(results)

        # Show detailed scores
        for _category, _score_val in metrics.scores_summary.items():
            pass

        # 3. QualityReport generation

        report = FlextQualityReportGenerator(results)

        # Generate JSON report
        json_report = report.generate_json_report()

        # Generate HTML report
        html_report = report.generate_html_report()

        # Save reports
        json_path = project_path / "api_demo_report.json"
        html_path = project_path / "api_demo_report.html"

        json_path.write_text(json_report)
        html_path.write_text(html_report)


def demonstrate_service_integration() -> None:
    """Demonstrate advanced service integration patterns.

    Note: Service integration APIs are under development.
    This demo shows conceptual patterns only.
    """
    logger.info("Service integration patterns - conceptual demonstration")
    logger.info("Services are available via FlextQualityServices class")
    logger.info("For actual usage, see CodeAnalyzer and QualityMetrics examples")


def demonstrate_flext_ecosystem_integration() -> None:
    """Demonstrate FLEXT ecosystem integration patterns."""
    # FLEXT ecosystem integration is always available

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
            result = analyzer.analyze_project()

            # Unwrap FlextResult
            if result.is_failure:
                logger.error(f"Analysis failed: {result.error}")
                return

            results = result.value

            analysis_data = {
                "quality_score": analyzer.get_quality_score(),
                "quality_grade": analyzer.get_quality_grade(),
                "files_analyzed": getattr(results.overall_metrics, "files_analyzed", 0),
                "total_lines": getattr(results.overall_metrics, "total_lines", 0),
                "analysis_results": results,
            }

        except Exception:
            return

        try:
            # Create metrics
            score_value = analysis_data.get("quality_score", 0.0)
            if isinstance(score_value, (int, float)):
                flext_metric(
                    name="quality_analysis_score",
                    value=float(score_value),
                )

            # Create trace
            flext_trace("api.analyze_project")

            # Create log entry
            flext_log_entry(
                message="FLEXT Quality ecosystem integration demonstration completed",
                level="info",
            )
        except Exception as e:
            logger.warning("Observability integration failed: %s", e)

        # Demonstrate container-based dependency injection
        logger.info("Container-based DI demonstration - using FlextContainer")
        container = FlextContainer()

        # Register quality analyzer
        analyzer_instance = CodeAnalyzer(str(project_path))
        container.register("quality_analyzer", analyzer_instance)

        # Resolve and use
        analyzer_result = container.get("quality_analyzer")
        if analyzer_result.is_success:
            resolved_analyzer = analyzer_result.value
            logger.info(f"Resolved analyzer from container: {type(resolved_analyzer)}")


def demonstrate_custom_workflows() -> None:
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


logger = FlextLogger(__name__)

class Application:
    """Main application class."""

    def __init__(self, config: dict[str, t.GeneralValueType]):
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

    def process_data(self, data: list[t.GeneralValueType]) -> list[t.GeneralValueType]:
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

    def _process_item(self, item: object) -> object:
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

def calculate_average(numbers: t.FloatList) -> float:
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
        result = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True,
        )

        # Unwrap FlextResult
        if result.is_failure:
            logger.error(f"Analysis failed: {result.error}")
            return

        results = result.value

        # Step 3: Process quality metrics
        metrics = QualityMetrics.from_analysis_results(results)
        score = analyzer.get_quality_score()
        analyzer.get_quality_grade()

        # Step 4: Generate comprehensive reports
        report = FlextQualityReportGenerator(results)

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


def main() -> int:
    """Main demonstration of complete API integration functionality."""
    try:
        # Demonstrate all API integration patterns
        demonstrate_simple_api()
        demonstrate_service_integration()
        demonstrate_flext_ecosystem_integration()
        demonstrate_custom_workflows()

        return 0

    except Exception:
        logger.exception("API integration demonstration failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
