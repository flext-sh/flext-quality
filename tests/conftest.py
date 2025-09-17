"""FLEXT Quality Test Configuration - Comprehensive Testing Infrastructure.

Provides pytest fixtures, configuration, and testing utilities for comprehensive
validation of FLEXT Quality functionality including domain entities, application
services, and infrastructure integrations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from django.test.utils import setup_test_environment, teardown_test_environment

from flext_core import FlextResult, FlextTypes, T


def assert_result_success_with_data[T](result: FlextResult[T]) -> T:
    """Assert FlextResult success and return validated data with type safety.

    Provides a DRY helper for the common test pattern of validating FlextResult
    success and extracting data with proper null safety checks. Eliminates
    boilerplate code while maintaining type safety and clear error messages.

    Args:
      result: FlextResult instance to validate for success state

    Returns:
      The validated data from the successful result

    Raises:
      AssertionError: If result indicates failure or data is None

    Example:
      >>> result = service.perform_operation()
      >>> data = assert_result_success_with_data(result)
      >>> assert data.expected_property == expected_value

    Note:
      This helper follows flext-core patterns and provides clear error
      messages for test debugging and failure analysis.

    """
    assert result.success, f"Expected success but got failure: {result.error}"
    assert result.value is not None, "Expected data but got None"
    return result.value


def assert_result_failure_with_error[T](result: FlextResult[T]) -> str:
    """Assert FlextResult failure and return validated error message.

    Provides a DRY helper for validating FlextResult failure states and
    extracting error messages with proper null safety. Essential for
    testing error handling and negative test scenarios.

    Args:
      result: FlextResult instance to validate for failure state

    Returns:
      The validated error message from the failed result

    Raises:
      AssertionError: If result indicates success or error message is None

    Example:
      >>> result = service.perform_invalid_operation()
      >>> error = assert_result_failure_with_error(result)
      >>> assert "validation failed" in error.lower()

    Note:
      This helper ensures consistent error handling validation across
      the test suite and provides clear debugging information.

    """
    assert result.is_failure, "Expected failure but got success"
    assert result.error is not None, "Expected error message but got None"
    return result.error


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Configure test environment variables for isolated testing.

    Automatically sets up the test environment for all tests, ensuring
    proper isolation from development and production environments.
    Configures logging, Django settings, and FLEXT-specific variables.

    Environment Variables:
      FLEXT_ENV: Set to 'test' for test-specific behavior
      FLEXT_LOG_LEVEL: Set to 'debug' for comprehensive test logging
      DJANGO_SETTINGS_MODULE: Django configuration for web interface testing

    Note:
      This fixture runs automatically for all tests and handles
      proper cleanup to prevent environment variable leakage.

    """
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    os.environ["DJANGO_SETTINGS_MODULE"] = "code_analyzer_web.settings"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)


# Django fixtures
@pytest.fixture
def django_db_setup() -> Generator[None]:
    """Django database setup for testing."""
    setup_test_environment()
    yield
    teardown_test_environment()


# Quality analysis fixtures
@pytest.fixture
def secure_temp_dir() -> Generator[str]:
    """Provide secure temporary directory for file system testing.

    Creates a secure temporary directory using Python's tempfile module
    with proper cleanup and security practices. Eliminates security
    warnings while providing isolated file system testing environment.

    Yields:
      Absolute path to the secure temporary directory

    Security:
      - Uses tempfile.TemporaryDirectory for secure creation
      - Automatically handles cleanup on test completion
      - Prevents S108 security warnings in static analysis

    Example:
      >>> def test_file_operations(secure_temp_dir):
      ...     test_file = Path(secure_temp_dir) / "test.py"
      ...     test_file.write_text("print('test')")
      ...     # Directory automatically cleaned up after test

    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_code_repository(tmp_path: Path) -> FlextTypes.Core.Dict:
    """Provide sample code repository metadata for quality analysis testing.

    Creates realistic repository metadata that simulates typical project
    structures and properties for comprehensive quality analysis testing.

    Args:
      tmp_path: pytest-provided temporary path for test isolation

    Returns:
      Dictionary containing repository metadata:
      - name: Repository name for identification
      - path: File system path for analysis
      - language: Primary programming language
      - files: List of representative file paths
      - size: Repository size in bytes
      - last_modified: ISO timestamp of last modification

    Example:
      >>> def test_repo_analysis(sample_code_repository):
      ...     analyzer = CodeAnalyzer(sample_code_repository["path"])
      ...     result = analyzer.analyze_project()
      ...     assert result.success

    """
    return {
        "name": "test-repository",
        "path": str(tmp_path / "test-repo"),
        "language": "python",
        "files": [
            "src/main.py",
            "src/utils.py",
            "tests/test_main.py",
        ],
        "size": 1024,
        "last_modified": "2023-01-01T12:00:00Z",
    }


@pytest.fixture
def quality_metrics_data() -> FlextTypes.Core.Dict:
    """Quality metrics data for testing."""
    return {
        "complexity": {
            "cyclomatic": 5.2,
            "cognitive": 3.8,
            "average": 4.5,
        },
        "maintainability": {
            "index": 78.5,
            "rating": "A",
            "debt_ratio": 0.15,
        },
        "coverage": {
            "line": 85.0,
            "branch": 78.5,
            "function": 92.0,
        },
        "security": {
            "vulnerabilities": 2,
            "hotspots": 1,
            "rating": "B",
        },
    }


@pytest.fixture
def code_analysis_config() -> FlextTypes.Core.Dict:
    """Code analysis configuration for testing."""
    return {
        "analyzers": {
            "ruff": {
                "enabled": True,
                "config_file": "pyproject.toml",
                "rules": ["E", "W", "F"],
            },
            "mypy": {
                "enabled": True,
                "strict": True,
                "ignore_missing_imports": False,
            },
            "bandit": {
                "enabled": True,
                "confidence": "medium",
                "severity": "low",
            },
        },
        "thresholds": {
            "complexity": 10,
            "coverage": 80.0,
            "maintainability": 70.0,
        },
    }


@pytest.fixture
def analysis_results() -> list[FlextTypes.Core.Dict]:
    """Analysis results for testing."""
    return [
        {
            "file": "src/main.py",
            "line": 42,
            "column": 10,
            "rule": "E501",
            "message": "Line too long (88 > 79 characters)",
            "severity": "warning",
            "tool": "ruff",
        },
        {
            "file": "src/utils.py",
            "line": 15,
            "column": 5,
            "rule": "F401",
            "message": "'unused_import' imported but unused",
            "severity": "error",
            "tool": "ruff",
        },
        {
            "file": "src/main.py",
            "line": 25,
            "column": 1,
            "rule": "B101",
            "message": "Use of assert detected",
            "severity": "low",
            "tool": "bandit",
        },
    ]


# Report generation fixtures
@pytest.fixture
def report_config(tmp_path: Path) -> FlextTypes.Core.Dict:
    """Report configuration for testing."""
    return {
        "format": "json",
        "include_metrics": True,
        "include_details": True,
        "output_path": str(tmp_path / "report.json"),
        "template": "default",
    }


@pytest.fixture
def dashboard_data() -> FlextTypes.Core.Dict:
    """Dashboard data for testing."""
    return {
        "summary": {
            "total_projects": 5,
            "analyzed_today": 3,
            "critical_issues": 12,
            "warnings": 45,
        },
        "trends": {
            "quality_score": [78, 79, 81, 80, 82],
            "issue_count": [25, 23, 20, 22, 18],
            "coverage": [75, 78, 80, 82, 85],
        },
        "top_issues": [
            {"type": "complexity", "count": 8},
            {"type": "security", "count": 5},
            {"type": "maintainability", "count": 3},
        ],
    }


# Multi-backend fixtures
@pytest.fixture
def sonarqube_config() -> FlextTypes.Core.Dict:
    """SonarQube configuration for testing."""
    return {
        "host": "http://localhost:9000",
        "token": "test-token",
        "project_key": "test-project",
        "organization": "test-org",
        "quality_gate": "Sonar way",
    }


@pytest.fixture
def codeclimate_config() -> FlextTypes.Core.Dict:
    """CodeClimate configuration for testing."""
    return {
        "api_token": "test-api-token",
        "repo_id": "test-repo-123",
        "maintainability_threshold": 3.0,
        "coverage_threshold": 80.0,
    }


# File system fixtures
@pytest.fixture
def temporary_project_structure(tmp_path: Path) -> str:
    """Create realistic temporary project structure for integration testing.

    Builds a complete Python project structure with source files, tests,
    and configuration files that can be used for comprehensive quality
    analysis integration testing.

    Args:
      tmp_path: pytest-provided temporary path for project creation

    Returns:
      Absolute path to the created project directory

    Project Structure:
      - src/ directory with Python modules
      - tests/ directory with test files
      - pyproject.toml with tool configurations
      - Realistic code samples with various quality scenarios

    Example:
      >>> def test_project_analysis(temporary_project_structure):
      ...     analyzer = CodeAnalyzer(temporary_project_structure)
      ...     result = analyzer.analyze_project()
      ...     assert len(result["python_files"]) > 0

    Note:
      The created project includes intentional quality issues for
      testing issue detection accuracy and analysis capabilities.

    """
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    # Create source files
    src_dir = project_dir / "src"
    src_dir.mkdir()
    main_py = src_dir / "main.py"
    main_py.write_text("""

def main() -> int:
    print("Hello, World!")
    return 0
if __name__ == "__main__":
    main()
""")
    utils_py = src_dir / "utils.py"
    utils_py.write_text("""

import sys
def get_env_var(name: str) -> str | None:
    return os.environ.get(name)
""")
    # Create test files
    tests_dir = project_dir / "tests"
    tests_dir.mkdir()
    test_main_py = tests_dir / "test_main.py"
    test_main_py.write_text("""

from src.main import main
from typing import Dict
from typing import Generator
from typing import List
def test_main() -> None:
    if main() != 0:
      raise AssertionError(f"Expected {0}, got {main()}")
""")
    # Create config files
    pyproject_toml = project_dir / "pyproject.toml"
    pyproject_toml.write_text("""

[tool.ruff]
line-length = 79
[tool.mypy]
strict = true
""")
    return str(project_dir)


# Package discovery fixtures
@pytest.fixture
def package_metadata() -> FlextTypes.Core.Dict:
    """Package metadata for testing."""
    return {
        "name": "test-package",
        "version": "0.9.0",
        "description": "Test package for quality analysis",
        "author": "Test Author",
        "dependencies": [
            "requests>=2.25.0",
            "pandas>=1.3.0",
            "pytest>=6.0.0",
        ],
        "dev_dependencies": [
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "coverage>=6.0.0",
        ],
    }


# Task management fixtures
@pytest.fixture
def celery_config() -> FlextTypes.Core.Dict:
    """Celery configuration for testing."""
    return {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/0",
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "timezone": "UTC",
        "enable_utc": True,
    }


@pytest.fixture
def analysis_task_data() -> FlextTypes.Core.Dict:
    """Analysis task data for testing."""
    return {
        "task_id": "test-task-123",
        "project_id": "test-project-456",
        "status": "pending",
        "progress": 0,
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers for test categorization and execution control.

    Defines test markers that enable selective test execution, proper test
    categorization, and CI/CD pipeline optimization through targeted testing.

    Args:
      config: pytest configuration object for marker registration

    Markers:
      - unit: Fast, isolated tests with mocking
      - integration: Tests with real dependencies
      - e2e: Complete user journey tests
      - quality: Quality analysis specific tests
      - backend: External tool integration tests
      - slow: Long-running tests (>5 seconds)

    Usage:
      >>> pytest -m unit          # Run only unit tests
      >>> pytest -m "not slow"   # Skip long-running tests
      >>> pytest -m integration  # Run integration tests only

    """
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "quality: Quality analysis tests")
    config.addinivalue_line("markers", "backend: Backend integration tests")
    config.addinivalue_line("markers", "celery: Celery task tests")
    config.addinivalue_line("markers", "django: Django framework tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Mock services
@pytest.fixture
def mock_quality_analyzer() -> object:
    """Provide mock quality analyzer for isolated unit testing.

    Creates a comprehensive mock implementation of the quality analyzer
    that simulates realistic analysis behavior without external dependencies.
    Essential for fast, reliable unit testing.

    Returns:
      Mock analyzer instance with realistic behavior:
      - analyze_project(): Returns comprehensive project analysis
      - analyze_file(): Returns file-level quality metrics
      - get_metrics(): Returns quality metrics summary

    Features:
      - Tracks analyzed files for test verification
      - Returns realistic quality scores and metrics
      - Simulates async operations for testing async workflows
      - Provides consistent, deterministic results

    Example:
      >>> def test_analysis_service(mock_quality_analyzer):
      ...     result = await mock_quality_analyzer.analyze_project("/test")
      ...     assert result["quality_score"] == 85.0
      ...     assert result["issues"] == 5

    """

    class MockQualityAnalyzer:
        """Mock implementation of quality analyzer for testing.

        Provides realistic analyzer behavior without external dependencies,
        enabling fast and reliable unit testing of analysis workflows.
        """

        def __init__(self) -> None:
            """Initialize the instance."""
            self.analyzed_files: FlextTypes.Core.StringList = []

        async def analyze_project(self, project_path: str) -> FlextTypes.Core.Dict:
            """Simulate comprehensive project analysis.

            Args:
                project_path: Path to project for analysis

            Returns:
                Realistic analysis results with quality metrics

            """
            self.analyzed_files.append(project_path)
            return {
                "quality_score": 85.0,
                "issues": 5,
                "files_analyzed": 10,
                "analysis_time": 2.5,
            }

        async def analyze_file(self, file_path: str) -> FlextTypes.Core.Dict:
            """Simulate individual file analysis.

            Args:
                file_path: Path to file for analysis

            Returns:
                File-level quality metrics and statistics

            """
            return {
                "file": file_path,
                "complexity": 3.2,
                "issues": 2,
                "coverage": 90.0,
            }

        async def get_metrics(self, _project_path: str) -> FlextTypes.Core.Dict:
            """Simulate project-wide quality metrics collection.

            Args:
                project_path: Path to project for metrics

            Returns:
                Comprehensive quality metrics across all categories

            """
            return {
                "maintainability": 78.5,
                "complexity": 5.2,
                "duplication": 2.1,
                "security": 95.0,
            }

    return MockQualityAnalyzer()


@pytest.fixture
def mock_report_generator() -> object:
    """Provide mock report generator for isolated reporting tests.

    Creates a mock implementation of the report generation system that
    simulates report creation and management without external dependencies
    or file system operations.

    Returns:
      Mock report generator instance with capabilities:
      - generate_report(): Creates reports in various formats
      - generate_dashboard_data(): Provides dashboard metrics
      - Tracks generated reports for test verification

    Features:
      - Supports multiple output formats (JSON, HTML, PDF)
      - Maintains history of generated reports
      - Returns realistic report metadata and content
      - Simulates async report generation workflows

    Example:
      >>> def test_report_service(mock_report_generator):
      ...     filename = await mock_report_generator.generate_report(data, "json")
      ...     assert filename.endswith(".json")
      ...     assert len(mock_report_generator.generated_reports) == 1

    """

    class MockReportGenerator:
        """Mock implementation of report generator for testing.

        Simulates report generation capabilities without file system
        operations, enabling isolated testing of reporting workflows.
        """

        def __init__(self) -> None:
            """Initialize the instance."""
            self.generated_reports: list[FlextTypes.Core.Dict] = []

        async def generate_report(
            self,
            data: FlextTypes.Core.Dict,
            output_format: str = "json",
        ) -> str:
            """Simulate report generation in specified format.

            Args:
                data: Analysis data for report generation
                output_format: Desired report format (json, html, pdf)

            Returns:
                Generated report filename

            """
            report: FlextTypes.Core.Dict = {
                "format": output_format,
                "data": data,
                "timestamp": "2023-01-01T12:00:00Z",
            }
            self.generated_reports.append(report)
            return f"report_{len(self.generated_reports)}.{output_format}"

        async def generate_dashboard_data(self) -> FlextTypes.Core.Dict:
            """Simulate dashboard data generation.

            Returns:
                Dashboard metrics and summary information

            """
            return {
                "projects": 5,
                "recent_analyses": 3,
                "avg_quality_score": 82.5,
                "trend": "improving",
            }

    return MockReportGenerator()
