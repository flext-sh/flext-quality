# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Quality is a comprehensive code quality analysis and metrics service for the FLEXT ecosystem. It provides automated quality assessment, issue detection, and reporting capabilities using Python 3.13 with Clean Architecture patterns and Domain-Driven Design (DDD) principles.

## Architecture

### High-Level Architecture

The project follows Clean Architecture with clear separation of concerns:

- **Domain Layer** (`src/flext_quality/domain/`): Core business entities, value objects, and domain logic
- **Application Layer** (`src/flext_quality/application/`): Service classes and application-specific business rules  
- **Infrastructure Layer** (`src/flext_quality/infrastructure/`): External dependencies, repositories, and adapters
- **CLI Interface** (`src/flext_quality/cli.py`): Command-line interface for quality operations

### Key Components

- **Quality Analyzer Engine** (`analyzer.py`): Multi-backend analysis system (AST, Ruff, MyPy, Bandit)
- **Backend System** (`backends/`): Pluggable analyzer backends for extensibility
- **Domain Entities** (`domain/entities.py`): Quality projects, analyses, issues, and reports
- **Service Layer** (`application/services.py`): Application services for quality operations
- **Reporting System** (`reports.py`): Quality reports in multiple formats (HTML, JSON, PDF)

### Domain Model

The domain is centered around these core entities:

- `QualityProject`: Represents a code project under analysis
- `QualityAnalysis`: Represents a single analysis run with metrics and scores
- `QualityIssue`: Individual quality issues detected during analysis
- `QualityRule`: Configuration rules for quality analysis
- `QualityReport`: Generated reports from analysis results

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation - ALL must pass
make validate                 # Full validation (lint + type + security + test + quality-check)

# Essential checks
make check                    # Quick health check (lint + type)
make lint                     # Ruff linting 
make type-check               # MyPy strict mode type checking
make security                 # Security scans (bandit + pip-audit)
make format                   # Format code with ruff
make fix                      # Auto-fix issues with ruff
```

### Testing (90% Coverage Minimum)

```bash
# Test execution
make test                     # Run tests with 90% coverage requirement
make test-unit                # Unit tests only
make test-integration         # Integration tests only  
make test-quality             # Quality analysis tests
make test-django              # Django-specific tests
make test-analysis            # Analysis engine tests
make test-e2e                 # End-to-end tests
make test-fast                # Run tests without coverage
make coverage-html            # Generate HTML coverage report
```

### Development Setup

```bash
# Complete setup
make setup                    # Complete development setup (install-dev + pre-commit)
make install                  # Install dependencies with Poetry
make install-dev              # Install dev dependencies
make pre-commit               # Run pre-commit hooks
```

### Quality Analysis Operations

The core functionality of the service:

```bash
# Analysis operations
make analyze                  # Run comprehensive quality analysis
make quality-check            # Check quality thresholds
make metrics                  # Collect quality metrics  
make report                   # Generate quality reports
make workspace-analyze        # Analyze entire FLEXT workspace
make detect-issues            # Detect quality issues
make calculate-scores         # Calculate quality scores
make quality-grade            # Calculate overall quality grade
make coverage-score           # Calculate coverage score
```

### CLI Interface

```bash
# Use the flext-quality CLI directly
poetry run python -m flext_quality.cli analyze
poetry run python -m flext_quality.cli check-thresholds
poetry run python -m flext_quality.cli collect-metrics
poetry run python -m flext_quality.cli generate-report
poetry run python -m flext_quality.cli analyze-workspace
```

### Web Interface

```bash
# Django development server
make web-start                # Start Django web interface (port 8000)
make web-migrate              # Run Django migrations
make web-shell                # Open Django shell
make web-collectstatic        # Collect static files
make web-createsuperuser      # Create Django superuser
```

### Documentation & Dependencies

```bash
# Documentation
make docs                     # Build documentation
make docs-serve               # Serve documentation

# Dependencies
make deps-update              # Update dependencies
make deps-show                # Show dependency tree
make deps-audit               # Audit dependencies

# Diagnostics
make diagnose                 # Project diagnostics
make doctor                   # Full health check
```

### Build & Distribution

```bash
# Build operations
make build                    # Build distribution packages
make build-clean              # Clean and build
make clean                    # Remove all artifacts
make clean-all                # Deep clean including venv
make reset                    # Reset project (clean-all + setup)
```

## Key Architecture Patterns

### Clean Architecture Implementation

The codebase strictly follows Clean Architecture principles:

1. **Dependency Rule**: Dependencies flow inward toward the domain
2. **Interface Segregation**: Clear boundaries between layers
3. **Dependency Injection**: Uses FlextContainer from flext-core for DI

### Domain-Driven Design

- **Entities**: Rich domain objects with business behavior
- **Value Objects**: Immutable objects representing domain concepts
- **Services**: Domain and application services for complex operations
- **Repository Pattern**: Abstraction for data persistence

### FlextResult Pattern

All operations use the FlextResult pattern for error handling:

```python
from flext_core import FlextResult

# Service methods return FlextResult[T]
result = await service.create_project(...)
if result.success:
    project = result.data
else:
    error = result.error
```

### Immutable Entity Pattern

Entities use immutable update patterns:

```python
# Domain entities use model_copy for updates
updated_analysis = analysis.model_copy(update={
    "status": AnalysisStatus.COMPLETED,
    "completed_at": datetime.now(UTC)
})
```

## Quality Standards

### Zero Tolerance Quality Gates

- **Coverage**: Minimum 90% test coverage (`--cov-fail-under=90`)
- **Type Safety**: Strict MyPy configuration with no untyped code
- **Linting**: Ruff with ALL rule categories enabled (select = ["ALL"])
- **Security**: Bandit security scanning and pip-audit
- **Pre-commit**: Automated quality checks on every commit

### Testing Strategy

- **Unit Tests**: Comprehensive domain and service layer testing
- **Integration Tests**: End-to-end analysis workflows
- **Quality Tests**: Analysis engine validation
- **Performance Tests**: Benchmark analysis operations

### Code Quality Thresholds

```bash
# Environment variables for quality thresholds
export QUALITY_MIN_COVERAGE=90.0
export QUALITY_MAX_COMPLEXITY=10
export QUALITY_MAX_DUPLICATION=5.0
export QUALITY_MIN_SECURITY_SCORE=90.0
export QUALITY_MIN_MAINTAINABILITY=80.0
```

## Integration with FLEXT Ecosystem

FLEXT Quality integrates with the broader FLEXT ecosystem:

- **flext-core**: Base patterns, FlextResult, FlextEntity, DI container
- **flext-observability**: Monitoring, metrics, tracing, health checks
- Dependencies declared in pyproject.toml using local file paths

## Development Workflow

### Local Development Setup

1. **Initial Setup**: Run `make setup` for complete development environment
2. **Django Setup**: Run `make web-migrate` to setup database
3. **Development**: Make changes following Clean Architecture patterns
4. **Testing**: Run `make test` to ensure 90% coverage
5. **Quality Gates**: Run `make validate` before committing

### Containerized Development Setup

1. **Docker Setup**: Run `docker-compose up -d` for full containerized environment
2. **Database Setup**: Migrations run automatically in container
3. **Development**: Make changes with hot reload enabled
4. **Testing**: Run `docker-compose exec web pytest`
5. **Monitoring**: Access Flower at <http://localhost:5555> for Celery monitoring

### Quick Start Development

```bash
# Option 1: All-in-one script (recommended for new developers)
./start_all.sh --create-superuser

# Option 2: Manual setup with make commands
make setup
make web-migrate
make web-start

# Option 3: Docker development
docker-compose up -d
```

## Common Patterns

### Service Implementation

Services follow consistent patterns:

```python
class QualityProjectService:
    async def create_project(self, ...) -> FlextResult[QualityProject]:
        try:
            # Business logic
            project = QualityProject(...)
            # Validation
            validation_result = project.validate_domain_rules()
            if not validation_result.success:
                return validation_result
            # Storage
            self._projects[project.id] = project
            return FlextResult.ok(project)
        except Exception as e:
            return FlextResult.fail(f"Failed to create project: {e}")
```

### Domain Entity Updates

Entities use immutable update patterns:

```python
def update_analysis_scores(self, scores: dict) -> QualityAnalysis:
    """Update analysis scores and return new instance."""
    return self.model_copy(update=scores).calculate_overall_score()
```

### Analysis Workflow

Quality analysis follows a structured workflow:

1. Create QualityProject
2. Initialize QualityAnalysis
3. Run analyzer backends (AST, external tools)
4. Collect metrics and issues
5. Calculate quality scores
6. Generate reports

## Configuration

The service uses multiple configuration approaches:

- **Environment Variables**: Runtime configuration and quality thresholds
- **pyproject.toml**: Primary tool configuration (ruff, mypy, pytest, dependencies)
- **Makefile**: Development workflow and quality gates
- **Analysis Config**: Per-analysis configuration in QualityAnalysis entity

Key configuration files:

- `pyproject.toml`: Primary configuration for tools, dependencies, and quality standards
- `Makefile`: Development workflow commands and quality gates
- `src/flext_quality/config.py`: Application configuration
- `setup.cfg`: Additional tool configuration

### Quality Thresholds (Environment Variables)

```bash
# Quality standards
export QUALITY_MIN_COVERAGE=90.0
export QUALITY_MAX_COMPLEXITY=10
export QUALITY_MAX_DUPLICATION=5.0
export QUALITY_MIN_SECURITY_SCORE=90.0
export QUALITY_MIN_MAINTAINABILITY=80.0
```

## Integration with FLEXT Ecosystem

FLEXT Quality integrates with the broader FLEXT ecosystem:

- **flext-core**: Base patterns, FlextResult, FlextEntity, DI container
- **flext-observability**: Monitoring, metrics, tracing, health checks  
- **flext-web**: Web interface integration (planned)
- **flext-cli**: CLI command integration (planned)

Dependencies are declared in pyproject.toml using local file paths for ecosystem integration.

## Current Development Status

### What Works Today

- ✅ **Quality Analysis Engine**: Multi-backend system (AST, Ruff, MyPy, Bandit)
- ✅ **Domain Entities**: QualityProject, QualityAnalysis, QualityIssue with business logic
- ✅ **Service Layer**: Application services with FlextResult pattern
- ✅ **CLI Interface**: Command-line analysis and reporting
- ✅ **Quality Scoring**: Composite quality scores and metrics
- ✅ **Report Generation**: HTML, JSON, PDF reports

### In Progress

- 🔄 **Ecosystem Integration**: Multi-project analysis for 32+ FLEXT projects
- 🔄 **Web Interface**: Django-based dashboard and interface
- 🔄 **Type Safety**: Ongoing MyPy strict mode improvements

## Troubleshooting

### Common Development Issues

**Poetry/Dependencies Issues:**

```bash
# Reset virtual environment
make clean-all
make setup

# Check dependency conflicts
poetry show --tree
poetry check

# Update dependencies
make deps-update
```

**Type Checking Issues:**

```bash
# Run MyPy with detailed output
poetry run mypy src --show-error-codes

# Check specific files
poetry run mypy src/flext_quality/analyzer.py --strict
```

**Test Failures:**

```bash
# Run tests with verbose output
make test-fast -v

# Run specific test categories
make test-unit
make test-integration
make test-quality

# Check coverage
make coverage-html
```

**Analysis Issues:**

```bash
# Test analysis engine directly
poetry run python -c "from flext_quality.analyzer import CodeAnalyzer; analyzer = CodeAnalyzer(); print('✅ Working')"

# Run workspace analysis with debugging
poetry run python -m flext_quality.cli analyze-workspace --verbose

# Check quality thresholds
poetry run python -m flext_quality.cli check-thresholds
```

### Performance Debugging

```bash
# Profile analysis performance
time make analyze                   # Time analysis operation
time make workspace-analyze         # Time full workspace analysis

# Check system diagnostics
make diagnose
make doctor

# Monitor test performance
poetry run pytest tests/ --benchmark-only
```

### Development Workflow Issues

**Quality Gates Failing:**

```bash
# Run individual quality checks
make lint                          # Check for linting issues
make type-check                    # Check for type issues
make security                      # Check for security issues
make test                          # Run tests with coverage

# Auto-fix what can be fixed
make fix                          # Auto-fix with ruff
make format                       # Format code
```

**Project Structure Questions:**

Key files and their purposes:
- `src/flext_quality/analyzer.py`: Main analysis engine
- `src/flext_quality/domain/entities.py`: Core domain models
- `src/flext_quality/application/services.py`: Business logic services
- `src/flext_quality/backends/`: Pluggable analyzer backends
- `src/flext_quality/cli.py`: Command-line interface
- `tests/`: Comprehensive test suite with 90% coverage target
