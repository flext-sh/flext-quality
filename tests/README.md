# FLEXT Quality Test Suite

Comprehensive test suite for FLEXT Quality ensuring robust validation of code quality analysis functionality, domain business rules, and ecosystem integration.

## Test Architecture

### Test Structure

```
tests/
├── __init__.py              # Test suite initialization and configuration
├── conftest.py              # Shared test fixtures and configuration
├── unit/                    # Unit tests with isolation and mocking
├── integration/             # Integration tests with real dependencies
├── e2e/                     # End-to-end user journey testing
├── helpers/                 # Test utilities and helper functions
└── test_*.py               # Component-specific test modules
```

### Test Categories

#### **Unit Tests** (`unit/`)

Isolated component testing with comprehensive mocking:

- **Domain Entity Testing**: Business logic and state validation
- **Value Object Testing**: Immutability and business rule enforcement
- **Service Interface Testing**: Contract validation and behavior testing
- **Algorithm Testing**: Quality scoring and metric calculation validation

#### **Integration Tests** (`integration/`)

Component interaction testing with real dependencies:

- **Database Integration**: Repository and persistence layer testing
- **External Tool Integration**: Ruff, MyPy, Bandit integration validation
- **Service Layer Integration**: Application service workflow testing
- **API Integration**: REST API endpoint and response validation

#### **End-to-End Tests** (`e2e/`)

Complete user journey testing with full system integration:

- **Analysis Workflow**: Complete project analysis from start to finish
- **Report Generation**: Multi-format report creation and validation
- **CLI Interface**: Command-line interface functionality testing
- **Web Interface**: Web dashboard and API integration testing

## Test Categories by Component

### Core Analysis Engine

- **`test_analyzer.py`**: Multi-backend analysis engine testing
- **`test_analyzer_comprehensive.py`**: Complete analysis workflow validation
- **`test_analyzer_edge_cases.py`**: Error handling and edge case testing

### Domain Layer Testing

- **`test_domain_entities.py`**: Business entity behavior and validation
- **`test_value_objects.py`**: Immutable value object testing
- **`test_handlers.py`**: Command and query handler testing

### Application Layer Testing

- **`test_application_services.py`**: Service orchestration and workflow testing
- **`test_services_comprehensive.py`**: Complete service integration testing
- **`test_services_error_scenarios.py`**: Error handling and resilience testing

### Infrastructure Layer Testing

- **`test_repositories.py`**: Data persistence and retrieval testing
- **`test_container.py`**: Dependency injection container testing
- **`test_di_container.py`**: Service resolution and lifecycle testing

### API and Interface Testing

- **`test_cli.py`**: Command-line interface functionality
- **`test_cli_comprehensive.py`**: Complete CLI workflow testing
- **`test_simple_api.py`**: Simplified API interface testing

### Quality and Metrics Testing

- **`test_metrics.py`**: Quality metrics calculation and validation
- **`test_reports.py`**: Report generation and formatting testing
- **`test_check_detected_issues.py`**: Issue detection accuracy testing

### Configuration and Setup Testing

- **`test_config.py`**: Configuration management and validation
- **`test_settings.py`**: Settings and environment configuration
- **`test_version.py`**: Version management and compatibility

## Quality Standards

### Coverage Requirements

- **Minimum 90% test coverage** across all source modules
- **Branch coverage** for conditional logic and error paths
- **Function coverage** for all public APIs and interfaces
- **Integration coverage** for external dependency interactions

### Test Quality Metrics

- **Test Reliability**: Tests must be deterministic and repeatable
- **Test Performance**: Unit tests complete in < 100ms, integration tests < 5s
- **Test Maintainability**: Clear test structure and comprehensive documentation
- **Test Isolation**: No test dependencies or shared state between tests

### Validation Standards

- **Business Rule Testing**: All domain rules validated with positive and negative cases
- **Error Scenario Testing**: Comprehensive error handling and edge case coverage
- **Performance Testing**: Analysis speed and resource usage benchmarking
- **Security Testing**: Vulnerability detection accuracy and false positive rates

## Test Execution

### Running Tests

#### Complete Test Suite

```bash

# Run all tests with coverage
make test                           # Complete test suite with 90% coverage requirement
pytest --cov=src --cov-fail-under=90

# Run with detailed output
pytest -v --cov=src --cov-report=html --cov-report=term-missing
```

#### Test Categories

```bash

# Unit tests only
make test-unit
pytest tests/unit/ -v

# Integration tests only
make test-integration
pytest tests/integration/ -v

# End-to-end tests only
pytest tests/e2e/ -v

# Specific component tests
pytest tests/test_analyzer.py -v
pytest tests/test_domain_entities.py -v
```

#### Test Filtering

```bash

# Run tests matching pattern
pytest -k "analyzer" -v                    # All analyzer-related tests
pytest -k "domain and not integration" -v  # Domain tests excluding integration

# Run by markers
pytest -m "unit" -v                        # Unit tests only
pytest -m "integration" -v                 # Integration tests only
pytest -m "slow" -v                        # Long-running tests only
pytest -m "not slow" -v                    # Fast tests only
```

### Test Configuration

#### pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-fail-under=90
    --cov-report=term-missing
    --cov-report=html:htmlcov

markers =
    unit: Unit tests with mocking and isolation
    integration: Integration tests with real dependencies
    e2e: End-to-end tests with full system
    slow: Long-running tests (>5 seconds)
    security: Security-related testing
    performance: Performance and benchmarking tests
```

#### Test Fixtures (`conftest.py`)

Shared test fixtures and configuration:

- **Database Fixtures**: Test database setup and teardown
- **Mock Fixtures**: Consistent mocking for external dependencies
- **Data Fixtures**: Test data generation and management
- **Environment Fixtures**: Test environment configuration

## Test Development Guidelines

### Test Structure Standards

```python
def test_should_do_something_when_condition():
    """Test description following should/when pattern.

    Tests that the system performs expected behavior under specific
    conditions, validating both success and failure scenarios.
    """
    # Given (Arrange)
    test_data = create_test_data()
    service = create_test_service()

    # When (Act)
    result = service.perform_operation(test_data)

    # Then (Assert) - Using current API
    data = result.unwrap_or(None)
    assert data is not None
    assert data.expected_property == expected_value
```

### Naming Conventions

- **Test Files**: `test_<component>.py` (e.g., `test_analyzer.py`)
- **Test Functions**: `test_should_<expected_behavior>_when_<condition>()`
- **Test Classes**: `Test<ComponentName>` (e.g., `TestQualityAnalyzer`)
- **Fixtures**: `<resource_type>_fixture` (e.g., `quality_project_fixture`)

### Test Data Management

```python

# Test data builders for consistent test object creation
class QualityProjectBuilder:
    def __init__(self):
        self._project = QualityProject(
            name="test-project",
            path="/test/path",
            quality_thresholds={"min_score": 80.0}
        )

    def with_name(self, name: str) -> "QualityProjectBuilder":
        self._project = self._project.model_copy(update={"name": name})
        return self

    def build(self) -> QualityProject:
        return self._project
```

### Mock Standards

```python

# Consistent mocking patterns for external dependencies
@pytest.fixture
def mock_external_analyzer():
    """Mock external analysis tool for unit testing."""
    mock = Mock(spec=ExternalAnalyzerService)
    mock.analyze_project.return_value = FlextCore.Result[None].ok(
        create_test_analysis_result()
    )
    return mock
```

## Performance Testing

### Benchmarking Tests

```python
@pytest.mark.performance
def test_analyzer_performance_benchmarks():
    """Validate analysis performance meets requirements."""
    analyzer = CodeAnalyzer("/path/to/medium/project")

    start_time = time.time()
    result = analyzer.analyze_project()
    execution_time = time.time() - start_time

    # Performance assertions
    assert execution_time < 30.0  # Analysis completes within 30 seconds
    data = result.unwrap_or({})
    assert data.get("files_analyzed", 0) > 0
    assert len(data.get("issues", [])) >= 0
```

### Resource Usage Testing

```python
@pytest.mark.performance
def test_memory_usage_within_limits():
    """Ensure analysis stays within memory limits."""
    import psutil

    process = psutil.Process()
    initial_memory = process.memory_info().rss

    analyzer = CodeAnalyzer("/path/to/large/project")
    result = analyzer.analyze_project()

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Memory usage should not exceed 500MB for typical projects
    assert memory_increase < 500 * 1024 * 1024
```

## Continuous Integration

### CI/CD Pipeline Integration

```yaml

# GitHub Actions example
- name: Run Test Suite
  run: |
    make test
    make test-integration
    make test-e2e

- name: Upload Coverage Reports
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

### Quality Gates

- **Test Coverage**: Minimum 90% coverage required for merge
- **Test Performance**: All tests must complete within time limits
- **Test Reliability**: No flaky tests allowed in main branch
- **Security Testing**: All security tests must pass

## Troubleshooting

### Common Test Issues

#### **Test Failures**

```bash

# Run specific failing test with detailed output
pytest tests/test_analyzer.py::test_specific_function -vvv --tb=long

# Run with debugging
pytest tests/test_analyzer.py --pdb

# Run with coverage debug info
pytest --cov=src --cov-report=term-missing --cov-debug=trace
```

#### **Performance Issues**

```bash

# Profile test execution
pytest --profile

# Run only fast tests during development
pytest -m "not slow"

# Parallel test execution
pytest -n auto  # Requires pytest-xdist
```

#### **Environment Issues**

```bash

# Clean test environment
make clean-test-env

# Reset test database
make reset-test-db

# Update test dependencies
poetry install --group test
```

## Related Documentation

- **[Source Code Documentation](../src/flext_quality/README.md)** - Implementation details
- **[Development Guide](../docs/development/README.md)** - Development setup and workflows
- **[Architecture Documentation](../docs/architecture/README.md)** - System design and patterns
- **[Quality Standards](../docs/development/quality-standards.md)** - Quality requirements and validation
