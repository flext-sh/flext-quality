"""Test configuration for flext-quality.

Provides pytest fixtures and configuration for testing quality analysis functionality
using Django test framework and flext-core patterns.
"""

from __future__ import annotations

import os
import tempfile
from typing import TYPE_CHECKING, TypeVar

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from flext_core import FlextResult, TAnyDict

# Type variable for FlextResult data
T = TypeVar("T")


def assert_result_success_with_data[T](result: FlextResult[T]) -> T:
    """DRY helper: Assert FlextResult success and return data with null safety.

    Eliminates duplicated pattern: assert result.is_success + assert result.data is not None
    Following flext-core patterns with proper type safety.

    Args:
        result: FlextResult to validate

    Returns:
        The validated data from result

    Raises:
        AssertionError: If result is failure or data is None

    """
    assert result.is_success, f"Expected success but got failure: {result.error}"
    assert result.data is not None, "Expected data but got None"
    return result.data


def assert_result_failure_with_error[T](result: FlextResult[T]) -> str:
    """DRY helper: Assert FlextResult failure and return error message.

    Eliminates duplicated pattern: assert result.is_failure + assert result.error is not None

    Args:
        result: FlextResult to validate

    Returns:
        The error message from result

    Raises:
        AssertionError: If result is success or error is None

    """
    assert result.is_failure, "Expected failure but got success"
    assert result.error is not None, "Expected error message but got None"
    return result.error


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
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
    from django.test.utils import setup_test_environment, teardown_test_environment
    setup_test_environment()
    yield
    teardown_test_environment()


# Quality analysis fixtures
@pytest.fixture
def secure_temp_dir() -> Generator[str]:
    """DRY fixture: Secure temporary directory for tests.

    SOLID principle: Single Responsibility - manages temp dir lifecycle
    Eliminates S108 security warnings by using proper temp dir creation.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_code_repository(tmp_path: Path) -> TAnyDict:
    """Sample code repository for testing."""
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
def quality_metrics_data() -> TAnyDict:
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
def code_analysis_config() -> TAnyDict:
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
def analysis_results() -> list[TAnyDict]:
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
def report_config(tmp_path: Path) -> TAnyDict:
    """Report configuration for testing."""
    return {
        "format": "json",
        "include_metrics": True,
        "include_details": True,
        "output_path": str(tmp_path / "report.json"),
        "template": "default",
    }


@pytest.fixture
def dashboard_data() -> TAnyDict:
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
def sonarqube_config() -> TAnyDict:
    """SonarQube configuration for testing."""
    return {
        "host": "http://localhost:9000",
        "token": "test-token",
        "project_key": "test-project",
        "organization": "test-org",
        "quality_gate": "Sonar way",
    }


@pytest.fixture
def codeclimate_config() -> TAnyDict:
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
    """Create temporary project structure for testing."""
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
def package_metadata() -> TAnyDict:
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
def celery_config() -> TAnyDict:
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
def analysis_task_data() -> TAnyDict:
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
    """Configure pytest markers."""
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
    """Mock quality analyzer for testing."""

    class MockQualityAnalyzer:
        def __init__(self) -> None:
            self.analyzed_files: list[str] = []

        async def analyze_project(self, project_path: str) -> TAnyDict:
            self.analyzed_files.append(project_path)
            return {
                "quality_score": 85.0,
                "issues": 5,
                "files_analyzed": 10,
                "analysis_time": 2.5,
            }

        async def analyze_file(self, file_path: str) -> TAnyDict:
            return {
                "file": file_path,
                "complexity": 3.2,
                "issues": 2,
                "coverage": 90.0,
            }

        async def get_metrics(self, project_path: str) -> TAnyDict:
            return {
                "maintainability": 78.5,
                "complexity": 5.2,
                "duplication": 2.1,
                "security": 95.0,
            }

    return MockQualityAnalyzer()


@pytest.fixture
def mock_report_generator() -> object:
    """Mock report generator for testing."""

    class MockReportGenerator:
        def __init__(self) -> None:
            self.generated_reports: list[TAnyDict] = []

        async def generate_report(
            self,
            data: TAnyDict,
            output_format: str = "json",
        ) -> str:
            report: TAnyDict = {
                "format": output_format,
                "data": data,
                "timestamp": "2023-01-01T12:00:00Z",
            }
            self.generated_reports.append(report)
            return f"report_{len(self.generated_reports)}.{output_format}"

        async def generate_dashboard_data(self) -> TAnyDict:
            return {
                "projects": 5,
                "recent_analyses": 3,
                "avg_quality_score": 82.5,
                "trend": "improving",
            }

    return MockReportGenerator()
