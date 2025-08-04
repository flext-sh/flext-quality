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
from flext_quality import QualityAPI, CodeAnalyzer, QualityMetrics, QualityReport
from flext_quality.application.services import (
    QualityProjectService,
    QualityAnalysisService,
    QualityIssueService,
    QualityReportService
)

# Import FLEXT core patterns
try:
    from flext_core import FlextResult, get_logger
    FLEXT_CORE_AVAILABLE = True
except ImportError:
    print("⚠️ flext-core not available - using basic patterns")
    FLEXT_CORE_AVAILABLE = False

# Setup logging
if FLEXT_CORE_AVAILABLE:
    logger = get_logger(__name__)
else:
    import logging
    logger = logging.getLogger(__name__)


async def demonstrate_simple_api() -> None:
    """Demonstrate simple API usage patterns."""
    print("\n" + "="*60)
    print("🚀 Simple API Usage Demonstration")
    print("="*60)

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

        print(f"📁 Created sample project: {project_path}")
        print(f"📄 Sample file: {sample_file.name}")

        # 1. Direct CodeAnalyzer usage
        print("\n📋 1. Direct CodeAnalyzer Usage")
        print("-" * 40)

        analyzer = CodeAnalyzer(str(project_path))
        results = analyzer.analyze_project()

        print("✅ Analysis completed!")
        print(f"   Files analyzed: {results.get('files_analyzed', 0)}")
        print(f"   Total lines: {results.get('total_lines', 0)}")

        score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()
        print(f"   Quality Score: {score:.1f}/100")
        print(f"   Quality Grade: {grade}")

        # 2. QualityMetrics usage
        print("\n📋 2. QualityMetrics Processing")
        print("-" * 40)

        metrics = QualityMetrics.from_analysis_results(results)
        print("✅ Metrics calculated!")
        print(f"   Overall Score: {metrics.overall_score:.1f}")
        print(f"   Quality Grade: {metrics.quality_grade}")
        print(f"   Total Issues: {metrics.total_issues}")
        print(f"   Files: {metrics.total_files}, Functions: {metrics.total_functions}")

        # Show detailed scores
        print("   Detailed Scores:")
        for category, score_val in metrics.scores_summary.items():
            print(f"     {category.title()}: {score_val:.1f}/100")

        # 3. QualityReport generation
        print("\n📋 3. Quality Report Generation")
        print("-" * 40)

        report = QualityReport(results)

        # Generate JSON report
        json_report = report.generate_json_report()
        print(f"✅ JSON report generated ({len(json_report)} characters)")

        # Generate HTML report
        html_report = report.generate_html_report()
        print(f"✅ HTML report generated ({len(html_report)} characters)")

        # Save reports
        json_path = project_path / "api_demo_report.json"
        html_path = project_path / "api_demo_report.html"

        json_path.write_text(json_report)
        html_path.write_text(html_report)

        print("✅ Reports saved:")
        print(f"   JSON: {json_path}")
        print(f"   HTML: {html_path}")


async def demonstrate_service_integration() -> None:
    """Demonstrate advanced service integration patterns."""
    print("\n" + "="*60)
    print("🚀 Service Integration Demonstration")
    print("="*60)

    # Initialize services
    project_service = QualityProjectService()
    analysis_service = QualityAnalysisService()
    issue_service = QualityIssueService()
    report_service = QualityReportService()

    print("✅ Services initialized successfully!")

    # Create a sample project using service
    print("\n📋 1. Project Management")
    print("-" * 40)

    # Create project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_result = await project_service.create_project(
            name="API Demo Project",
            project_path=temp_dir,
            language="python"
        )

        if project_result.is_success:
            project = project_result.data
            print(f"✅ Project created: {project.id}")
            print(f"   Path: {project.project_path}")
            print(f"   Language: {project.language}")
            print(f"   Auto-analyze: {project.auto_analyze}")
        else:
            print(f"❌ Project creation failed: {project_result.error}")
            return

        # Create analysis
        print("\n📋 2. Analysis Management")
        print("-" * 40)

        analysis_result = await analysis_service.create_analysis(project_id=project.id)

        if analysis_result.is_success:
            analysis = analysis_result.data
            print(f"✅ Analysis created: {analysis.id}")
            print(f"   Project ID: {analysis.project_id}")
            print(f"   Status: {analysis.status.value}")
            print(f"   Created: {analysis.started_at}")
        else:
            print(f"❌ Analysis creation failed: {analysis_result.error}")
            return

        # Update analysis metrics
        metrics_result = await analysis_service.update_metrics(
            analysis_id=analysis.id,
            total_files=5,
            total_lines=250,
            code_lines=200,
            comment_lines=30,
            blank_lines=20
        )

        if metrics_result.is_success:
            updated_analysis = metrics_result.data
            print("✅ Metrics updated:")
            print(f"   Files: {updated_analysis.total_files}")
            print(f"   Lines: {updated_analysis.total_lines}")
        else:
            print(f"❌ Metrics update failed: {metrics_result.error}")
            return

        # Update quality scores
        scores_result = await analysis_service.update_scores(
            analysis_id=analysis.id,
            coverage_score=85.0,
            complexity_score=78.0,
            duplication_score=92.0,
            security_score=95.0,
            maintainability_score=80.0
        )

        if scores_result.is_success:
            scored_analysis = scores_result.data
            print("✅ Scores updated:")
            print(f"   Coverage: {scored_analysis.coverage_score}")
            print(f"   Complexity: {scored_analysis.complexity_score}")
            print(f"   Security: {scored_analysis.security_score}")
        else:
            print(f"❌ Scores update failed: {scores_result.error}")
            return

        # Create issues
        print("\n📋 3. Issue Management")
        print("-" * 40)

        # Create different types of issues
        issues_data = [
            {
                "issue_type": "security",
                "severity": "high",
                "rule_id": "S001",
                "file_path": "src/auth.py",
                "line_number": 42,
                "message": "Potential SQL injection vulnerability"
            },
            {
                "issue_type": "complexity",
                "severity": "medium",
                "rule_id": "C001",
                "file_path": "src/processor.py",
                "line_number": 15,
                "message": "Cyclomatic complexity too high (12)"
            },
            {
                "issue_type": "style",
                "severity": "low",
                "rule_id": "E301",
                "file_path": "src/utils.py",
                "line_number": 8,
                "message": "Expected 1 blank line, found 0"
            }
        ]

        created_issues = []
        for issue_data in issues_data:
            issue_result = await issue_service.create_issue(
                analysis_id=analysis.id,
                **issue_data
            )

            if issue_result.is_success:
                issue = issue_result.data
                created_issues.append(issue)
                print(f"✅ {issue_data['issue_type'].title()} issue created: {issue.id}")
                print(f"   File: {issue.file_path}:{issue.line_number}")
                print(f"   Severity: {issue.severity}")
            else:
                print(f"❌ Issue creation failed: {issue_result.error}")

        # Update issue counts in analysis
        issue_counts_result = await analysis_service.update_issue_counts(
            analysis_id=analysis.id,
            critical=0,
            high=1,
            medium=1,
            low=1
        )

        if issue_counts_result.is_success:
            print("✅ Issue counts updated in analysis")

        # Complete the analysis
        complete_result = await analysis_service.complete_analysis(analysis.id)

        if complete_result.is_success:
            completed_analysis = complete_result.data
            print(f"✅ Analysis completed: {completed_analysis.status.value}")
            print(f"   Completed at: {completed_analysis.completed_at}")
        else:
            print(f"❌ Analysis completion failed: {complete_result.error}")

        # Create reports
        print("\n📋 4. Report Management")
        print("-" * 40)

        # Create different report types
        report_types = ["html", "json", "pdf"]

        for report_type in report_types:
            report_result = await report_service.create_report(
                analysis_id=analysis.id,
                report_type=report_type
            )

            if report_result.is_success:
                report = report_result.data
                print(f"✅ {report_type.upper()} report created: {report.id}")
                print(f"   Type: {report.report_type}")
                print(f"   Created: {report.generated_at}")
            else:
                print(f"❌ {report_type.upper()} report creation failed: {report_result.error}")

        # List all reports for the analysis
        reports_result = await report_service.list_reports(analysis.id)

        if reports_result.is_success:
            reports = reports_result.data
            print(f"✅ Total reports for analysis: {len(reports)}")
            for report in reports:
                print(f"   - {report.report_type.upper()}: {report.id}")
        else:
            print(f"❌ Reports listing failed: {reports_result.error}")

        print("\n🎉 Service integration demonstration completed successfully!")


async def demonstrate_flext_ecosystem_integration() -> None:
    """Demonstrate FLEXT ecosystem integration patterns."""
    print("\n" + "="*60)
    print("🚀 FLEXT Ecosystem Integration Demonstration")
    print("="*60)

    if not FLEXT_CORE_AVAILABLE:
        print("⚠️ flext-core not available - using basic patterns")
        print("   In production, install flext-core for full ecosystem integration")
    else:
        print("✅ flext-core available - demonstrating full integration")

    # Demonstrate FlextResult pattern usage
    print("\n📋 1. FlextResult Pattern Usage")
    print("-" * 40)

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
        api = QualityAPI()

        print("📊 Running ecosystem-integrated analysis...")

        try:
            # Use direct analyzer (QualityAPI is a simple wrapper)
            analyzer = CodeAnalyzer(str(project_path))
            results = analyzer.analyze_project()

            analysis_data = {
                'quality_score': analyzer.get_quality_score(),
                'quality_grade': analyzer.get_quality_grade(),
                'files_analyzed': results.get('files_analyzed', 0),
                'total_lines': results.get('total_lines', 0),
                'analysis_results': results
            }

            print("✅ Ecosystem analysis successful")
            print(f"   Quality Score: {analysis_data['quality_score']:.1f}")
            print(f"   Quality Grade: {analysis_data['quality_grade']}")
            print(f"   Files Analyzed: {analysis_data['files_analyzed']}")

        except Exception as e:
            print(f"❌ Ecosystem analysis failed: {e}")
            return

        # Demonstrate observability integration (if available)
        print("\n📋 2. Observability Integration")
        print("-" * 40)

        try:
            from flext_observability import flext_create_metric, flext_create_trace, flext_create_log_entry

            # Create metrics
            flext_create_metric(
                name="quality_analysis_score",
                value=analysis_data.get('quality_score', 0),
                tags={"project": "ecosystem_demo", "integration": "api"}
            )

            # Create trace
            flext_create_trace(
                trace_id="ecosystem_demo_analysis",
                operation="api.analyze_project",
                config={"project_path": str(project_path)}
            )

            # Create log entry
            flext_create_log_entry(
                message="FLEXT Quality ecosystem integration demonstration completed",
                level="info",
                context={
                    "component": "quality_api",
                    "project": "ecosystem_demo",
                    "files_analyzed": analysis_data.get('files_analyzed', 0)
                }
            )

            print("✅ Observability integration successful!")
            print("   Metrics: Quality score published")
            print("   Tracing: Analysis operation traced")
            print("   Logging: Structured log entry created")

        except ImportError:
            print("⚠️ flext-observability not available")
            print("   In production, install flext-observability for monitoring")

            # Simulate observability integration
            print("📊 Simulated observability integration:")
            print(f"   Metric: quality_score = {analysis_data.get('quality_score', 0)}")
            print("   Trace: ecosystem_demo_analysis completed")
            print(f"   Log: Analysis completed with {analysis_data.get('files_analyzed', 0)} files")

        # Demonstrate container-based dependency injection (if available)
        print("\n📋 3. Dependency Injection Integration")
        print("-" * 40)

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

                if project_service_result.is_success and analysis_service_result.is_success:
                    project_service = project_service_result.data
                    analysis_service = analysis_service_result.data

                    print("✅ Dependency injection successful!")
                    print("   Container: FlextContainer initialized")
                    print("   Services: QualityProjectService, QualityAnalysisService registered")

                    # Demonstrate service usage
                    with tempfile.TemporaryDirectory() as temp_service_dir:
                        project_result = await project_service.create_project(
                            name="DI Demo Project",
                            project_path=temp_service_dir
                        )

                        if project_result.is_success:
                            print("   Usage: Project created via DI container")
                        else:
                            print("   Usage: Project creation failed")
                else:
                    print("⚠️ Service resolution failed")
                    print("   Using direct instantiation fallback")

            except ImportError as e:
                print(f"⚠️ FlextContainer not available: {e}")
                print("   Using direct service instantiation")

                # Direct instantiation
                project_service = QualityProjectService()
                analysis_service = QualityAnalysisService()
                print("✅ Direct service instantiation successful")
        else:
            print("⚠️ flext-core not available - using direct instantiation")
            project_service = QualityProjectService()
            analysis_service = QualityAnalysisService()
            print("✅ Direct service instantiation successful")


async def demonstrate_custom_workflows() -> None:
    """Demonstrate custom quality workflow automation."""
    print("\n" + "="*60)
    print("🚀 Custom Quality Workflow Demonstration")
    print("="*60)

    # Define custom workflow
    workflow_steps = [
        "Initialize project analysis",
        "Execute quality analysis",
        "Process quality metrics",
        "Generate comprehensive reports",
        "Apply quality gates",
        "Send notifications"
    ]

    print("📋 Custom Workflow Steps:")
    for i, step in enumerate(workflow_steps, 1):
        print(f"   {i}. {step}")

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
'''
        }

        # Create files
        for filename, content in files_data.items():
            (project_path / filename).write_text(content)

        print(f"✅ Sample project created with {len(files_data)} files")

        # Execute custom workflow
        print("\n🔄 Executing Custom Quality Workflow:")
        print("-" * 40)

        # Step 1: Initialize project analysis
        print("1️⃣ Initialize project analysis...")
        analyzer = CodeAnalyzer(str(project_path))
        print(f"   ✅ CodeAnalyzer initialized for {project_path.name}")

        # Step 2: Execute quality analysis
        print("2️⃣ Execute quality analysis...")
        results = analyzer.analyze_project(
            include_security=True,
            include_complexity=True,
            include_dead_code=True,
            include_duplicates=True
        )
        print(f"   ✅ Analysis completed: {results.get('files_analyzed', 0)} files analyzed")

        # Step 3: Process quality metrics
        print("3️⃣ Process quality metrics...")
        metrics = QualityMetrics.from_analysis_results(results)
        score = analyzer.get_quality_score()
        grade = analyzer.get_quality_grade()
        print(f"   ✅ Metrics processed: {grade} ({score:.1f}/100)")
        print(f"      Total issues: {metrics.total_issues}")
        print(f"      Quality breakdown: Security({metrics.security_issues_count}), "
              f"Complexity({metrics.complexity_issues_count}), "
              f"DeadCode({metrics.dead_code_items_count})")

        # Step 4: Generate comprehensive reports
        print("4️⃣ Generate comprehensive reports...")
        report = QualityReport(results)

        json_report = report.generate_json_report()
        html_report = report.generate_html_report()

        # Save reports
        json_path = project_path / "workflow_report.json"
        html_path = project_path / "workflow_report.html"
        json_path.write_text(json_report)
        html_path.write_text(html_report)

        print("   ✅ Reports generated:")
        print(f"      JSON: {json_path.name} ({len(json_report)} chars)")
        print(f"      HTML: {html_path.name} ({len(html_report)} chars)")

        # Step 5: Apply quality gates
        print("5️⃣ Apply quality gates...")

        # Define quality gates
        quality_gates = {
            "min_score": 70.0,
            "max_security_issues": 0,
            "max_complexity_issues": 3,
            "max_total_issues": 5
        }

        # Check gates
        gates_passed = 0
        total_gates = len(quality_gates)

        # Score gate
        if score >= quality_gates["min_score"]:
            print(f"   ✅ Score Gate: PASS ({score:.1f} >= {quality_gates['min_score']})")
            gates_passed += 1
        else:
            print(f"   ❌ Score Gate: FAIL ({score:.1f} < {quality_gates['min_score']})")

        # Security gate
        if metrics.security_issues_count <= quality_gates["max_security_issues"]:
            print(f"   ✅ Security Gate: PASS ({metrics.security_issues_count} <= {quality_gates['max_security_issues']})")
            gates_passed += 1
        else:
            print(f"   ❌ Security Gate: FAIL ({metrics.security_issues_count} > {quality_gates['max_security_issues']})")

        # Complexity gate
        if metrics.complexity_issues_count <= quality_gates["max_complexity_issues"]:
            print(f"   ✅ Complexity Gate: PASS ({metrics.complexity_issues_count} <= {quality_gates['max_complexity_issues']})")
            gates_passed += 1
        else:
            print(f"   ❌ Complexity Gate: FAIL ({metrics.complexity_issues_count} > {quality_gates['max_complexity_issues']})")

        # Total issues gate
        if metrics.total_issues <= quality_gates["max_total_issues"]:
            print(f"   ✅ Total Issues Gate: PASS ({metrics.total_issues} <= {quality_gates['max_total_issues']})")
            gates_passed += 1
        else:
            print(f"   ❌ Total Issues Gate: FAIL ({metrics.total_issues} > {quality_gates['max_total_issues']})")

        # Overall gate decision
        gates_status = "APPROVED" if gates_passed == total_gates else "REJECTED"
        print(f"   🏆 Quality Gates: {gates_status} ({gates_passed}/{total_gates} passed)")

        # Step 6: Send notifications
        print("6️⃣ Send notifications...")

        # Simulate notifications
        notification_channels = ["email", "slack", "webhook"]

        for channel in notification_channels:
            print(f"   📧 {channel.title()}: Quality analysis completed")
            print(f"      Project: {project_path.name}")
            print(f"      Status: {gates_status}")
            print(f"      Score: {grade} ({score:.1f}/100)")

        print(f"   ✅ Notifications sent to {len(notification_channels)} channels")

        # Workflow summary
        print("\n🎉 Custom Workflow Completed Successfully!")
        print(f"   Project: {project_path.name}")
        print(f"   Files Analyzed: {results.get('files_analyzed', 0)}")
        print(f"   Quality Score: {score:.1f}/100 ({grade})")
        print(f"   Quality Gates: {gates_status} ({gates_passed}/{total_gates})")
        print("   Reports Generated: JSON, HTML")
        print(f"   Notifications: Sent to {len(notification_channels)} channels")


async def main() -> int:
    """Main demonstration of complete API integration functionality."""
    print("🚀 FLEXT Quality - Complete API Integration Demonstration")
    print("="*80)
    print("This example demonstrates comprehensive API usage patterns:")
    print("• Simple API usage with direct components")
    print("• Advanced service integration patterns")
    print("• FLEXT ecosystem integration (flext-core, flext-observability)")
    print("• Custom quality workflow automation")
    print("• Enterprise-grade async/await patterns")
    print("• Error handling with FlextResult patterns")

    try:
        # Demonstrate all API integration patterns
        await demonstrate_simple_api()
        await demonstrate_service_integration()
        await demonstrate_flext_ecosystem_integration()
        await demonstrate_custom_workflows()

        print("\n" + "="*80)
        print("🎉 Complete API Integration Demonstration Completed Successfully!")
        print("="*80)
        print("✅ All integration patterns demonstrated successfully")
        print("✅ Simple API, Services, Ecosystem, and Custom Workflows")
        print("✅ Enterprise-grade patterns and error handling")
        print("✅ Comprehensive functionality coverage achieved")

        return 0

    except Exception as e:
        print(f"\n❌ API Integration demonstration failed: {e}")
        logger.exception("API integration demonstration failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
