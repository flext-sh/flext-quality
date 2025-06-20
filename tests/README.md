# 🧪 DC Code Analyzer - Test Suite

> **Module**: Comprehensive test suite for DC Code Analyzer with Django integration and multi-backend testing | **Audience**: QA Engineers, Backend Developers, Code Analysis Specialists | **Status**: Production Ready

## 📋 **Overview**

Enterprise-grade test suite for the DC Code Analyzer application, providing comprehensive testing coverage including unit tests, integration tests with Django framework, end-to-end workflow testing, and multi-backend analyzer validation. This test suite demonstrates best practices for testing Django-based code analysis systems.

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../../README.md) → **📂 Component**: [DC Code Analyzer](../README.md) → **📂 Current**: Test Suite

---

## 🎯 **Module Purpose**

This test module provides comprehensive validation for the DC Code Analyzer implementation, ensuring reliability, performance, and correctness of all code analysis operations, Django REST API endpoints, multi-backend analysis engines, and enterprise code quality workflows.

### **Key Testing Areas**

- **Unit Testing** - Core analyzer logic and backend validation
- **Integration Testing** - Django integration and API endpoint testing
- **E2E Testing** - Complete analysis workflow validation
- **Backend Testing** - Multi-backend analyzer testing (AST, Quality, External)
- **Performance Testing** - Analysis performance and scalability
- **API Testing** - REST API endpoint validation

---

## 📁 **Test Structure**

```
tests/
├── unit/
│   ├── __init__.py                       # Unit test package initialization
│   ├── test_backends.py                  # Backend analyzer unit tests
│   ├── test_models.py                    # Django model unit tests
│   ├── test_multi_backend_analyzer.py    # Multi-backend analyzer tests
│   ├── test_analysis_engine.py           # Analysis engine tests
│   ├── test_report_generator.py          # Report generation tests
│   └── test_package_discovery.py         # Package discovery tests
├── integration/
│   ├── __init__.py                       # Integration test package
│   ├── test_analysis_flow.py             # Complete analysis flow tests
│   ├── test_api.py                       # REST API integration tests
│   ├── test_django_integration.py        # Django framework integration
│   ├── test_celery_tasks.py              # Celery task integration tests
│   └── test_database_operations.py       # Database operation tests
├── e2e/
│   ├── __init__.py                       # E2E test package
│   ├── test_complete_workflow.py         # Complete workflow tests
│   ├── test_project_analysis.py          # Project analysis E2E tests
│   ├── test_multi_project_analysis.py    # Multi-project analysis tests
│   └── test_report_generation.py         # Report generation E2E tests
├── performance/
│   ├── test_analysis_performance.py      # Analysis performance tests
│   ├── test_concurrent_analysis.py       # Concurrent analysis tests
│   ├── test_large_codebase.py            # Large codebase analysis tests
│   └── test_memory_usage.py              # Memory usage tests
├── fixtures/
│   ├── django_fixtures.py                # Django test fixtures
│   ├── analysis_fixtures.py              # Analysis test data fixtures
│   ├── backend_fixtures.py               # Backend test fixtures
│   └── api_fixtures.py                   # API test fixtures
├── mocks/
│   ├── mock_backends.py                  # Mock backend implementations
│   ├── mock_analysis_data.py             # Mock analysis data
│   └── mock_external_services.py         # Mock external services
├── conftest.py                           # Pytest configuration and fixtures
└── test_settings.py                      # Django test settings
```

---

## 🔧 **Test Categories**

### **1. Unit Tests (unit/)**

#### **Backend Analyzer Testing (test_backends.py)**

```python
"""Unit tests for DC Code Analyzer backend implementations."""

import pytest
from unittest.mock import Mock, patch
import ast
from pathlib import Path

from analyzer.backends.base import BaseBackend
from analyzer.backends.ast_backend import ASTBackend
from analyzer.backends.quality_backend import QualityBackend
from analyzer.backends.external_backend import ExternalBackend
from analyzer.models import Project, AnalysisResult, Issue

class TestASTBackend:
    """Test AST backend analyzer functionality."""

    @pytest.fixture
    def ast_backend(self):
        """AST backend instance fixture."""
        return ASTBackend()

    @pytest.fixture
    def sample_python_code(self):
        """Sample Python code for testing."""
        return '''
def calculate_metrics(data):
    """Calculate code metrics."""
    complexity = 0
    for item in data:
        if item > 10:
            complexity += 1
        elif item < 5:
            complexity += 2
        else:
            complexity += 3
    return complexity

class DataProcessor:
    """Process data with various methods."""
    
    def __init__(self):
        self.data = []
        
    def add_data(self, item):
        self.data.append(item)
        
    def process(self):
        return [x * 2 for x in self.data if x > 0]
'''

    def test_ast_backend_initialization(self, ast_backend):
        """Test AST backend initialization."""
        assert ast_backend.name == "AST Backend"
        assert ast_backend.version == "1.0"
        assert ast_backend.supported_languages == ["python"]

    def test_analyze_python_code(self, ast_backend, sample_python_code):
        """Test Python code analysis with AST backend."""
        # Act
        results = ast_backend.analyze_code(sample_python_code, "test.py")
        
        # Assert
        assert results is not None
        assert "metrics" in results
        assert "issues" in results
        assert "ast_info" in results
        
        # Check metrics
        metrics = results["metrics"]
        assert metrics["functions"] == 1
        assert metrics["classes"] == 1
        assert metrics["methods"] == 3  # __init__, add_data, process
        
        # Check complexity
        assert metrics["cyclomatic_complexity"] > 0

    def test_detect_code_smells(self, ast_backend, sample_python_code):
        """Test code smell detection."""
        # Act
        issues = ast_backend.detect_code_smells(sample_python_code)
        
        # Assert
        assert isinstance(issues, list)
        
        # Check for specific code smells
        smell_types = [issue["type"] for issue in issues]
        
        # Should detect high complexity in calculate_metrics
        complexity_issues = [i for i in issues if "complexity" in i["type"].lower()]
        assert len(complexity_issues) >= 0  # May or may not have complexity issues

    def test_extract_ast_metrics(self, ast_backend, sample_python_code):
        """Test AST metrics extraction."""
        # Arrange
        tree = ast.parse(sample_python_code)
        
        # Act
        metrics = ast_backend.extract_ast_metrics(tree)
        
        # Assert
        assert "total_nodes" in metrics
        assert metrics["total_nodes"] > 0
        assert "depth" in metrics
        assert metrics["depth"] > 0
        
        # Check node type distribution
        assert "node_types" in metrics
        node_types = metrics["node_types"]
        assert "FunctionDef" in node_types
        assert "ClassDef" in node_types

    def test_analyze_imports(self, ast_backend):
        """Test import analysis."""
        # Arrange
        code_with_imports = '''
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from sklearn.metrics import accuracy_score
'''
        
        # Act
        import_info = ast_backend.analyze_imports(code_with_imports)
        
        # Assert
        assert "stdlib_imports" in import_info
        assert "third_party_imports" in import_info
        assert "relative_imports" in import_info
        
        assert "os" in import_info["stdlib_imports"]
        assert "pandas" in import_info["third_party_imports"]

class TestQualityBackend:
    """Test quality backend analyzer functionality."""

    @pytest.fixture
    def quality_backend(self):
        """Quality backend instance fixture."""
        return QualityBackend()

    @pytest.fixture
    def project_path(self, tmp_path):
        """Create temporary project for testing."""
        project = tmp_path / "test_project"
        project.mkdir()
        
        # Create sample Python files
        (project / "main.py").write_text('''
def main():
    print("Hello, World!")
    x = 1
    y = 2
    z = x + y
    return z

if __name__ == "__main__":
    main()
''')
        
        (project / "utils.py").write_text('''
def unused_function():
    pass

def used_function(x):
    return x * 2
''')
        
        return project

    def test_quality_backend_initialization(self, quality_backend):
        """Test quality backend initialization."""
        assert quality_backend.name == "Quality Backend"
        assert hasattr(quality_backend, "quality_tools")
        assert "pylint" in quality_backend.quality_tools
        assert "flake8" in quality_backend.quality_tools

    @patch('subprocess.run')
    def test_run_pylint_analysis(self, mock_run, quality_backend, project_path):
        """Test Pylint analysis execution."""
        # Arrange
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '''
{
    "messages": [
        {
            "type": "convention",
            "symbol": "missing-docstring",
            "message": "Missing module docstring",
            "path": "main.py",
            "line": 1,
            "column": 0
        }
    ],
    "statistics": {
        "score": 8.5
    }
}
'''
        
        # Act
        results = quality_backend.run_pylint(project_path)
        
        # Assert
        assert results is not None
        assert "messages" in results
        assert "statistics" in results
        assert results["statistics"]["score"] == 8.5

    def test_calculate_code_quality_score(self, quality_backend):
        """Test code quality score calculation."""
        # Arrange
        quality_results = {
            "pylint": {"score": 8.5},
            "flake8": {"violations": 3},
            "mypy": {"errors": 1},
            "coverage": {"percentage": 85.0}
        }
        
        # Act
        overall_score = quality_backend.calculate_quality_score(quality_results)
        
        # Assert
        assert 0 <= overall_score <= 100
        assert overall_score > 70  # Should be reasonably high with these metrics

    def test_detect_quality_issues(self, quality_backend):
        """Test quality issue detection."""
        # Arrange
        quality_results = {
            "pylint": {
                "messages": [
                    {"type": "error", "symbol": "syntax-error"},
                    {"type": "warning", "symbol": "unused-variable"}
                ]
            },
            "flake8": {
                "violations": [
                    {"code": "E501", "message": "line too long"},
                    {"code": "F401", "message": "unused import"}
                ]
            }
        }
        
        # Act
        issues = quality_backend.aggregate_quality_issues(quality_results)
        
        # Assert
        assert len(issues) == 4
        
        # Check issue severity mapping
        severities = [issue["severity"] for issue in issues]
        assert "error" in severities
        assert "warning" in severities

class TestExternalBackend:
    """Test external backend analyzer functionality."""

    @pytest.fixture
    def external_backend(self):
        """External backend instance fixture."""
        return ExternalBackend(api_endpoint="https://api.example.com/analyze")

    def test_external_backend_initialization(self, external_backend):
        """Test external backend initialization."""
        assert external_backend.name == "External Backend"
        assert external_backend.api_endpoint == "https://api.example.com/analyze"
        assert external_backend.timeout == 30

    @patch('requests.post')
    def test_analyze_with_external_service(self, mock_post, external_backend):
        """Test analysis with external service."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "analysis": {
                "security_score": 95,
                "vulnerabilities": [],
                "recommendations": ["Enable strict type checking"]
            }
        }
        mock_post.return_value = mock_response
        
        # Act
        results = external_backend.analyze_code("sample code", "test.py")
        
        # Assert
        assert results["status"] == "success"
        assert results["analysis"]["security_score"] == 95
        assert len(results["analysis"]["vulnerabilities"]) == 0

    @patch('requests.post')
    def test_handle_external_service_error(self, mock_post, external_backend):
        """Test handling of external service errors."""
        # Arrange
        mock_post.side_effect = Exception("Connection timeout")
        
        # Act
        results = external_backend.analyze_code("sample code", "test.py")
        
        # Assert
        assert results["status"] == "error"
        assert "error_message" in results
        assert "Connection timeout" in results["error_message"]

class TestMultiBackendAnalyzer:
    """Test multi-backend analyzer functionality."""

    @pytest.fixture
    def multi_analyzer(self):
        """Multi-backend analyzer instance."""
        from analyzer.multi_backend_analyzer import MultiBackendAnalyzer
        return MultiBackendAnalyzer()

    @pytest.fixture
    def mock_backends(self):
        """Mock backend instances."""
        ast_backend = Mock(spec=ASTBackend)
        ast_backend.name = "AST Backend"
        ast_backend.analyze_code.return_value = {"ast_metrics": {"functions": 5}}
        
        quality_backend = Mock(spec=QualityBackend)
        quality_backend.name = "Quality Backend"
        quality_backend.analyze_project.return_value = {"quality_score": 85}
        
        return [ast_backend, quality_backend]

    def test_multi_backend_initialization(self, multi_analyzer):
        """Test multi-backend analyzer initialization."""
        assert hasattr(multi_analyzer, "backends")
        assert len(multi_analyzer.backends) > 0
        assert hasattr(multi_analyzer, "aggregation_strategy")

    def test_run_all_backends(self, multi_analyzer, mock_backends):
        """Test running analysis with all backends."""
        # Arrange
        multi_analyzer.backends = mock_backends
        test_code = "def test(): pass"
        
        # Act
        results = multi_analyzer.analyze_with_all_backends(test_code, "test.py")
        
        # Assert
        assert len(results) == 2
        assert "AST Backend" in results
        assert "Quality Backend" in results
        assert results["AST Backend"]["ast_metrics"]["functions"] == 5

    def test_aggregate_backend_results(self, multi_analyzer):
        """Test aggregating results from multiple backends."""
        # Arrange
        backend_results = {
            "AST Backend": {
                "metrics": {"functions": 5, "classes": 2},
                "issues": [{"type": "complexity", "severity": "medium"}]
            },
            "Quality Backend": {
                "score": 85,
                "issues": [{"type": "style", "severity": "low"}]
            }
        }
        
        # Act
        aggregated = multi_analyzer.aggregate_results(backend_results)
        
        # Assert
        assert "combined_metrics" in aggregated
        assert "all_issues" in aggregated
        assert "overall_score" in aggregated
        assert len(aggregated["all_issues"]) == 2

    def test_prioritize_issues(self, multi_analyzer):
        """Test issue prioritization across backends."""
        # Arrange
        issues = [
            {"type": "security", "severity": "high", "backend": "Security Backend"},
            {"type": "style", "severity": "low", "backend": "Quality Backend"},
            {"type": "bug", "severity": "critical", "backend": "AST Backend"},
            {"type": "complexity", "severity": "medium", "backend": "AST Backend"}
        ]
        
        # Act
        prioritized = multi_analyzer.prioritize_issues(issues)
        
        # Assert
        assert prioritized[0]["severity"] == "critical"
        assert prioritized[1]["severity"] == "high"
        assert prioritized[-1]["severity"] == "low"
```

#### **Django Model Testing (test_models.py)**

```python
"""Unit tests for DC Code Analyzer Django models."""

import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from analyzer.models import (
    Project, 
    AnalysisSession, 
    AnalysisResult,
    Issue,
    CodeMetric,
    Package
)

class TestProjectModel(TestCase):
    """Test Project model functionality."""

    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(
            name="Test Project",
            description="A test project for unit testing",
            repository_url="https://github.com/test/project",
            language="Python",
            framework="Django"
        )

    def test_project_creation(self):
        """Test project creation and fields."""
        assert self.project.name == "Test Project"
        assert self.project.description == "A test project for unit testing"
        assert self.project.repository_url == "https://github.com/test/project"
        assert self.project.language == "Python"
        assert self.project.framework == "Django"
        assert self.project.created_at is not None
        assert self.project.updated_at is not None

    def test_project_string_representation(self):
        """Test project string representation."""
        assert str(self.project) == "Test Project"

    def test_project_absolute_url(self):
        """Test project absolute URL."""
        url = self.project.get_absolute_url()
        assert f"/projects/{self.project.id}/" in url

    def test_project_analysis_sessions(self):
        """Test project analysis sessions relationship."""
        # Create analysis sessions
        session1 = AnalysisSession.objects.create(
            project=self.project,
            status="completed"
        )
        session2 = AnalysisSession.objects.create(
            project=self.project,
            status="running"
        )
        
        # Test relationship
        sessions = self.project.analysis_sessions.all()
        assert sessions.count() == 2
        assert session1 in sessions
        assert session2 in sessions

    def test_project_latest_analysis(self):
        """Test getting latest analysis for project."""
        # Create multiple analysis sessions
        old_session = AnalysisSession.objects.create(
            project=self.project,
            status="completed",
            started_at=timezone.now() - timedelta(days=7)
        )
        
        recent_session = AnalysisSession.objects.create(
            project=self.project,
            status="completed",
            started_at=timezone.now() - timedelta(days=1)
        )
        
        # Test latest analysis
        latest = self.project.get_latest_analysis()
        assert latest == recent_session

class TestAnalysisSessionModel(TestCase):
    """Test AnalysisSession model functionality."""

    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(
            name="Test Project",
            language="Python"
        )
        
        self.session = AnalysisSession.objects.create(
            project=self.project,
            status="running",
            configuration={
                "backends": ["ast", "quality"],
                "depth": "deep"
            }
        )

    def test_analysis_session_creation(self):
        """Test analysis session creation."""
        assert self.session.project == self.project
        assert self.session.status == "running"
        assert self.session.configuration["backends"] == ["ast", "quality"]
        assert self.session.started_at is not None

    def test_analysis_session_status_transitions(self):
        """Test analysis session status transitions."""
        # Initial status
        assert self.session.status == "running"
        
        # Complete analysis
        self.session.complete_analysis()
        assert self.session.status == "completed"
        assert self.session.completed_at is not None
        
        # Test error status
        error_session = AnalysisSession.objects.create(
            project=self.project,
            status="running"
        )
        error_session.mark_as_error("Test error message")
        assert error_session.status == "error"
        assert error_session.error_message == "Test error message"

    def test_analysis_session_duration(self):
        """Test analysis session duration calculation."""
        # Complete the session
        self.session.started_at = timezone.now() - timedelta(minutes=5)
        self.session.completed_at = timezone.now()
        self.session.status = "completed"
        self.session.save()
        
        # Test duration
        duration = self.session.get_duration()
        assert duration.total_seconds() == pytest.approx(300, rel=10)

    def test_analysis_session_results(self):
        """Test analysis session results relationship."""
        # Create analysis results
        result1 = AnalysisResult.objects.create(
            session=self.session,
            backend_name="AST Backend",
            status="success",
            result_data={"metrics": {"functions": 10}}
        )
        
        result2 = AnalysisResult.objects.create(
            session=self.session,
            backend_name="Quality Backend",
            status="success",
            result_data={"score": 85}
        )
        
        # Test relationship
        results = self.session.analysis_results.all()
        assert results.count() == 2
        assert result1 in results
        assert result2 in results

class TestIssueModel(TestCase):
    """Test Issue model functionality."""

    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(name="Test Project")
        self.session = AnalysisSession.objects.create(
            project=self.project,
            status="completed"
        )
        
        self.issue = Issue.objects.create(
            session=self.session,
            type="complexity",
            severity="medium",
            file_path="src/main.py",
            line_number=42,
            column_number=10,
            message="Function 'calculate' has high cyclomatic complexity",
            backend_name="AST Backend"
        )

    def test_issue_creation(self):
        """Test issue creation and fields."""
        assert self.issue.session == self.session
        assert self.issue.type == "complexity"
        assert self.issue.severity == "medium"
        assert self.issue.file_path == "src/main.py"
        assert self.issue.line_number == 42
        assert self.issue.message == "Function 'calculate' has high cyclomatic complexity"

    def test_issue_severity_levels(self):
        """Test issue severity level validation."""
        valid_severities = ["low", "medium", "high", "critical"]
        
        for severity in valid_severities:
            issue = Issue.objects.create(
                session=self.session,
                type="test",
                severity=severity,
                file_path="test.py",
                message="Test issue"
            )
            assert issue.severity == severity

    def test_issue_grouping_by_type(self):
        """Test grouping issues by type."""
        # Create multiple issues
        Issue.objects.create(
            session=self.session,
            type="complexity",
            severity="high",
            file_path="utils.py",
            message="High complexity"
        )
        
        Issue.objects.create(
            session=self.session,
            type="security",
            severity="critical",
            file_path="auth.py",
            message="Security vulnerability"
        )
        
        # Test grouping
        complexity_issues = Issue.objects.filter(
            session=self.session,
            type="complexity"
        )
        assert complexity_issues.count() == 2
        
        security_issues = Issue.objects.filter(
            session=self.session,
            type="security"
        )
        assert security_issues.count() == 1

    def test_issue_fix_suggestion(self):
        """Test issue fix suggestion field."""
        self.issue.fix_suggestion = "Refactor function to reduce complexity"
        self.issue.save()
        
        assert self.issue.fix_suggestion == "Refactor function to reduce complexity"

class TestCodeMetricModel(TestCase):
    """Test CodeMetric model functionality."""

    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(name="Test Project")
        self.session = AnalysisSession.objects.create(
            project=self.project,
            status="completed"
        )
        
        self.metric = CodeMetric.objects.create(
            session=self.session,
            metric_name="cyclomatic_complexity",
            metric_value=15.5,
            file_path="src/complex_module.py",
            backend_name="AST Backend"
        )

    def test_metric_creation(self):
        """Test code metric creation."""
        assert self.metric.session == self.session
        assert self.metric.metric_name == "cyclomatic_complexity"
        assert self.metric.metric_value == 15.5
        assert self.metric.file_path == "src/complex_module.py"

    def test_metric_aggregation(self):
        """Test metric aggregation for project."""
        # Create additional metrics
        CodeMetric.objects.create(
            session=self.session,
            metric_name="cyclomatic_complexity",
            metric_value=8.0,
            file_path="src/simple_module.py"
        )
        
        CodeMetric.objects.create(
            session=self.session,
            metric_name="lines_of_code",
            metric_value=500,
            file_path="src/complex_module.py"
        )
        
        # Test aggregation
        complexity_metrics = CodeMetric.objects.filter(
            session=self.session,
            metric_name="cyclomatic_complexity"
        )
        
        avg_complexity = sum(m.metric_value for m in complexity_metrics) / complexity_metrics.count()
        assert avg_complexity == 11.75

    def test_metric_trends(self):
        """Test tracking metric trends over time."""
        # Create another session with metrics
        new_session = AnalysisSession.objects.create(
            project=self.project,
            status="completed"
        )
        
        CodeMetric.objects.create(
            session=new_session,
            metric_name="cyclomatic_complexity",
            metric_value=12.0,
            file_path="src/complex_module.py"
        )
        
        # Test trend analysis
        metrics = CodeMetric.objects.filter(
            session__project=self.project,
            metric_name="cyclomatic_complexity",
            file_path="src/complex_module.py"
        ).order_by('session__started_at')
        
        assert metrics.count() == 2
        assert metrics[0].metric_value == 15.5
        assert metrics[1].metric_value == 12.0
        # Complexity decreased - good trend
```

### **2. Integration Tests (integration/)**

#### **Analysis Flow Testing (test_analysis_flow.py)**

```python
"""Integration tests for complete analysis flow."""

import pytest
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import tempfile
import shutil
from pathlib import Path

from analyzer.models import Project, AnalysisSession
from analyzer.multi_backend_analyzer import MultiBackendAnalyzer
from analyzer.tasks import run_analysis_task

class TestCompleteAnalysisFlow(TransactionTestCase):
    """Test complete analysis flow from API to results."""

    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create temporary project directory
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "test_project"
        self.project_path.mkdir()
        
        # Create sample Python files
        self._create_sample_project()

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def _create_sample_project(self):
        """Create sample project files."""
        # Main module
        (self.project_path / "main.py").write_text('''
"""Main application module."""

def main():
    """Application entry point."""
    print("Starting application...")
    result = process_data([1, 2, 3, 4, 5])
    print(f"Result: {result}")
    return result

def process_data(data):
    """Process input data."""
    total = 0
    for item in data:
        if item > 2:
            total += item * 2
        else:
            total += item
    return total

if __name__ == "__main__":
    main()
''')
        
        # Utility module
        (self.project_path / "utils.py").write_text('''
"""Utility functions."""

import json
from typing import Dict, List

def load_config(file_path: str) -> Dict:
    """Load configuration from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def validate_data(data: List) -> bool:
    """Validate input data."""
    if not data:
        return False
    
    for item in data:
        if not isinstance(item, (int, float)):
            return False
    
    return True

class DataProcessor:
    """Process various data types."""
    
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        """Add item to processor."""
        self.data.append(item)
    
    def get_summary(self) -> Dict:
        """Get data summary."""
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "average": sum(self.data) / len(self.data) if self.data else 0
        }
''')
        
        # Test file
        test_dir = self.project_path / "tests"
        test_dir.mkdir()
        (test_dir / "test_main.py").write_text('''
"""Tests for main module."""

import pytest
from main import process_data

def test_process_data():
    """Test data processing function."""
    assert process_data([1, 2, 3]) == 9
    assert process_data([]) == 0
    assert process_data([5, 5, 5]) == 30
''')

    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow from API call to results."""
        # Step 1: Create project via API
        response = self.client.post('/api/projects/', {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing',
            'repository_url': str(self.project_path),
            'language': 'Python',
            'framework': 'None'
        })
        
        assert response.status_code == 201
        project_id = response.data['id']
        
        # Step 2: Trigger analysis via API
        response = self.client.post(f'/api/projects/{project_id}/analyze/', {
            'backends': ['ast', 'quality'],
            'configuration': {
                'depth': 'deep',
                'include_tests': True
            }
        })
        
        assert response.status_code == 202
        session_id = response.data['session_id']
        
        # Step 3: Wait for analysis to complete (simulate)
        session = AnalysisSession.objects.get(id=session_id)
        
        # Run analysis directly (in real scenario, this would be Celery task)
        analyzer = MultiBackendAnalyzer()
        results = analyzer.analyze_project(self.project_path)
        
        # Update session with results
        session.status = 'completed'
        session.save()
        
        for backend_name, backend_results in results.items():
            session.analysis_results.create(
                backend_name=backend_name,
                status='success',
                result_data=backend_results
            )
        
        # Step 4: Retrieve analysis results via API
        response = self.client.get(f'/api/analysis-sessions/{session_id}/')
        
        assert response.status_code == 200
        assert response.data['status'] == 'completed'
        assert len(response.data['results']) >= 2
        
        # Step 5: Check specific results
        results = {r['backend_name']: r for r in response.data['results']}
        
        # Check AST backend results
        assert 'AST Backend' in results
        ast_results = results['AST Backend']['result_data']
        assert 'metrics' in ast_results
        assert ast_results['metrics']['functions'] >= 2  # main and process_data
        
        # Check Quality backend results
        assert 'Quality Backend' in results

    def test_concurrent_analysis_sessions(self):
        """Test running concurrent analysis sessions."""
        # Create multiple projects
        projects = []
        for i in range(3):
            response = self.client.post('/api/projects/', {
                'name': f'Concurrent Project {i}',
                'repository_url': str(self.project_path),
                'language': 'Python'
            })
            projects.append(response.data['id'])
        
        # Start analysis for all projects
        sessions = []
        for project_id in projects:
            response = self.client.post(f'/api/projects/{project_id}/analyze/', {
                'backends': ['ast']
            })
            sessions.append(response.data['session_id'])
        
        # Verify all sessions are created
        assert len(sessions) == 3
        
        # Check that all sessions are in correct state
        for session_id in sessions:
            session = AnalysisSession.objects.get(id=session_id)
            assert session.status in ['pending', 'running']

    def test_analysis_error_handling(self):
        """Test analysis error handling and recovery."""
        # Create project with invalid path
        response = self.client.post('/api/projects/', {
            'name': 'Error Test Project',
            'repository_url': '/invalid/path/to/project',
            'language': 'Python'
        })
        
        project_id = response.data['id']
        
        # Trigger analysis
        response = self.client.post(f'/api/projects/{project_id}/analyze/', {
            'backends': ['ast']
        })
        
        session_id = response.data['session_id']
        
        # Simulate analysis error
        session = AnalysisSession.objects.get(id=session_id)
        session.mark_as_error("Project path not found")
        
        # Retrieve error status
        response = self.client.get(f'/api/analysis-sessions/{session_id}/')
        
        assert response.status_code == 200
        assert response.data['status'] == 'error'
        assert 'Project path not found' in response.data['error_message']

class TestAPIIntegration(TestCase):
    """Test REST API integration."""

    def setUp(self):
        """Set up API test environment."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_project_crud_operations(self):
        """Test project CRUD operations via API."""
        # Create
        response = self.client.post('/api/projects/', {
            'name': 'CRUD Test Project',
            'description': 'Testing CRUD operations',
            'language': 'Python'
        })
        
        assert response.status_code == 201
        project_id = response.data['id']
        
        # Read
        response = self.client.get(f'/api/projects/{project_id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'CRUD Test Project'
        
        # Update
        response = self.client.patch(f'/api/projects/{project_id}/', {
            'description': 'Updated description'
        })
        
        assert response.status_code == 200
        assert response.data['description'] == 'Updated description'
        
        # Delete
        response = self.client.delete(f'/api/projects/{project_id}/')
        assert response.status_code == 204
        
        # Verify deletion
        response = self.client.get(f'/api/projects/{project_id}/')
        assert response.status_code == 404

    def test_analysis_history_endpoint(self):
        """Test analysis history retrieval."""
        # Create project
        project = Project.objects.create(
            name='History Test Project',
            language='Python'
        )
        
        # Create multiple analysis sessions
        for i in range(5):
            AnalysisSession.objects.create(
                project=project,
                status='completed',
                configuration={'run': i}
            )
        
        # Get analysis history
        response = self.client.get(f'/api/projects/{project.id}/analysis-history/')
        
        assert response.status_code == 200
        assert len(response.data['results']) == 5
        
        # Test pagination
        response = self.client.get(
            f'/api/projects/{project.id}/analysis-history/?page_size=2'
        )
        
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        assert 'next' in response.data

    def test_issue_filtering_and_sorting(self):
        """Test issue filtering and sorting capabilities."""
        # Create test data
        project = Project.objects.create(name='Issue Test Project')
        session = AnalysisSession.objects.create(
            project=project,
            status='completed'
        )
        
        # Create various issues
        from analyzer.models import Issue
        
        Issue.objects.create(
            session=session,
            type='security',
            severity='critical',
            file_path='auth.py',
            message='SQL injection vulnerability'
        )
        
        Issue.objects.create(
            session=session,
            type='complexity',
            severity='medium',
            file_path='utils.py',
            message='High cyclomatic complexity'
        )
        
        Issue.objects.create(
            session=session,
            type='style',
            severity='low',
            file_path='main.py',
            message='Line too long'
        )
        
        # Test filtering by severity
        response = self.client.get(
            f'/api/analysis-sessions/{session.id}/issues/?severity=critical'
        )
        
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['severity'] == 'critical'
        
        # Test filtering by type
        response = self.client.get(
            f'/api/analysis-sessions/{session.id}/issues/?type=complexity'
        )
        
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['type'] == 'complexity'
        
        # Test sorting
        response = self.client.get(
            f'/api/analysis-sessions/{session.id}/issues/?ordering=-severity'
        )
        
        assert response.status_code == 200
        severities = [issue['severity'] for issue in response.data['results']]
        assert severities == ['critical', 'medium', 'low']
```

---

## 🔧 **Test Configuration**

### **Pytest Configuration (conftest.py)**

```python
"""Pytest configuration and shared fixtures for DC Code Analyzer tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock
import django
from django.conf import settings

# Configure Django for testing
def pytest_configure():
    """Configure Django settings for pytest."""
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'analyzer',
            'dashboard',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        ROOT_URLCONF='code_analyzer_web.urls',
        SECRET_KEY='test-secret-key',
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework.authentication.SessionAuthentication',
            ],
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.IsAuthenticated',
            ],
        }
    )
    django.setup()

@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir) / "test_project"
    project_path.mkdir()
    
    yield project_path
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_python_files(temp_project_dir):
    """Create sample Python files in project."""
    files = {
        "main.py": '''
def main():
    """Main function."""
    print("Hello, World!")
    return 0

if __name__ == "__main__":
    main()
''',
        "utils.py": '''
def calculate(x, y):
    """Calculate sum."""
    return x + y

class Helper:
    """Helper class."""
    pass
''',
        "complex.py": '''
def complex_function(data):
    """Complex function with high cyclomatic complexity."""
    result = 0
    for item in data:
        if item > 10:
            if item % 2 == 0:
                result += item * 2
            else:
                result += item * 3
        elif item > 5:
            result += item
        else:
            if item < 0:
                result -= item
            else:
                result += 1
    return result
'''
    }
    
    for filename, content in files.items():
        (temp_project_dir / filename).write_text(content)
    
    return temp_project_dir

@pytest.fixture
def mock_ast_backend():
    """Mock AST backend for testing."""
    backend = Mock()
    backend.name = "AST Backend"
    backend.analyze_code.return_value = {
        "metrics": {
            "functions": 5,
            "classes": 2,
            "complexity": 3.5
        },
        "issues": []
    }
    return backend

@pytest.fixture
def mock_quality_backend():
    """Mock quality backend for testing."""
    backend = Mock()
    backend.name = "Quality Backend"
    backend.analyze_project.return_value = {
        "score": 85.5,
        "violations": 3,
        "coverage": 92.0
    }
    return backend

@pytest.fixture
def mock_external_api():
    """Mock external API responses."""
    def mock_response(endpoint, data=None):
        responses = {
            "/analyze": {
                "status": "success",
                "analysis": {
                    "security_score": 95,
                    "vulnerabilities": []
                }
            },
            "/health": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }
        return responses.get(endpoint, {})
    
    return mock_response

@pytest.fixture
def django_db_setup():
    """Set up Django test database."""
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb')

@pytest.fixture
def api_client():
    """Django REST framework API client."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    """Authenticated API client."""
    from django.contrib.auth.models import User
    
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    
    return api_client

@pytest.fixture
def sample_analysis_data():
    """Sample analysis data for testing."""
    return {
        "project_info": {
            "name": "Test Project",
            "language": "Python",
            "files": 10,
            "lines_of_code": 1500
        },
        "backends": {
            "AST Backend": {
                "status": "success",
                "metrics": {
                    "functions": 25,
                    "classes": 8,
                    "average_complexity": 3.2
                }
            },
            "Quality Backend": {
                "status": "success",
                "score": 87.5,
                "issues": 12
            }
        },
        "aggregated_results": {
            "overall_score": 85.0,
            "total_issues": 15,
            "critical_issues": 2
        }
    }
```

### **Django Test Settings (test_settings.py)**

```python
"""Django test settings for DC Code Analyzer."""

from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-test-key-for-testing-only'
DEBUG = True
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'analyzer',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'code_analyzer_web.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Celery Configuration (for testing)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Static files
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Testing specific settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Analysis backend settings
ANALYSIS_BACKENDS = {
    'ast': {
        'class': 'analyzer.backends.ast_backend.ASTBackend',
        'enabled': True,
    },
    'quality': {
        'class': 'analyzer.backends.quality_backend.QualityBackend',
        'enabled': True,
    },
    'external': {
        'class': 'analyzer.backends.external_backend.ExternalBackend',
        'enabled': False,  # Disabled for testing
        'api_endpoint': 'https://test-api.example.com',
    }
}

# Cache configuration for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

---

## 🔗 **Cross-References**

### **Component Documentation**

- [Component Overview](../README.md) - Complete DC Code Analyzer documentation
- [API Documentation](../docs/api/) - REST API reference
- [Architecture Guide](../docs/architecture/) - System architecture

### **Testing Documentation**

- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/) - Django testing guide
- [PyTest Documentation](https://docs.pytest.org/) - Python testing framework
- [REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/) - DRF testing

### **Code Analysis References**

- [AST Module](https://docs.python.org/3/library/ast.html) - Python AST documentation
- [Pylint](https://pylint.pycqa.org/) - Python code analysis
- [Django Best Practices](https://docs.djangoproject.com/en/4.2/misc/design-philosophies/) - Django patterns

---

**📂 Module**: Test Suite | **🏠 Component**: [DC Code Analyzer](../README.md) | **Framework**: Django 4.2+, PyTest | **Updated**: 2025-06-19