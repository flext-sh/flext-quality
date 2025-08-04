# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Quality is a comprehensive code quality analysis and metrics service that provides enterprise-grade quality assessment, issue detection, and reporting capabilities. It's built using Python 3.13, Django, and follows Clean Architecture patterns with Domain-Driven Design (DDD) principles.

## Architecture

### High-Level Architecture

The project follows Clean Architecture with clear separation of concerns:

- **Domain Layer** (`src/flext_quality/domain/`): Core business entities, value objects, and domain logic
- **Application Layer** (`src/flext_quality/application/`): Service classes and application-specific business rules
- **Infrastructure Layer** (`src/flext_quality/infrastructure/`): External dependencies, repositories, and adapters
- **Presentation Layer**: Django web interface and REST API endpoints

### Key Components

- **Quality Analyzer Engine**: Core analysis functionality with multiple backend analyzers (AST, external tools)
- **Multi-Backend System**: Pluggable analyzer backends for extensibility
- **Domain Entities**: Quality projects, analyses, issues, rules, and reports
- **Service Layer**: Application services for managing quality operations
- **Reporting System**: Comprehensive quality reports in multiple formats (HTML, JSON, PDF)

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
make validate                 # Strict compliance validation (lint + type + security + test + quality-check)

# Essential checks
make check                    # Essential quality checks (lint + type + test)
make lint                     # Ruff linting with ALL rules enabled
make type-check               # MyPy strict mode type checking
make security                 # Security scans (bandit + pip-audit + secrets)
make format                   # Format code with ruff
```

### Testing (90% Coverage Minimum)

```bash
# Test execution
make test                     # Run tests with 90% coverage requirement
make test-unit                # Unit tests only
make test-integration         # Integration tests only
make test-quality             # Quality analysis tests
make coverage                 # Generate detailed coverage report
make coverage-html            # Generate and open HTML coverage report
```

### Development Setup

```bash
# Complete setup
make setup                    # Complete development setup
make install                  # Install dependencies with Poetry
make install-dev              # Install dev dependencies
make pre-commit               # Setup pre-commit hooks

# Django-specific setup
make web-migrate              # Run Django migrations
make web-shell               # Open Django shell
```

### Quality Analysis Operations

The core functionality of the service:

```bash
# Analysis operations
make analyze                  # Run comprehensive quality analysis on workspace
make quality-check            # Check quality thresholds against standards
make metrics                  # Collect and calculate quality metrics
make report                   # Generate comprehensive quality reports
make workspace-analyze        # Analyze entire FLEXT workspace
make project-analyze PROJECT=name  # Analyze specific project

# Quality tools integration
make quality-tools            # Test all quality tool integrations
make ruff-analysis            # Run Ruff analysis with custom configuration
make mypy-analysis            # Run MyPy analysis with strict configuration
make coverage-analysis        # Run coverage analysis with thresholds
make security-analysis        # Run security analysis with vulnerability scanning
make complexity-analysis      # Run complexity analysis
make duplication-analysis     # Run code duplication analysis
```

### Quality Metrics & Scoring

```bash
# Score calculations
make calculate-scores         # Calculate quality scores for all projects
make coverage-score           # Calculate coverage score
make complexity-score         # Calculate complexity score
make security-score           # Calculate security score
make maintainability-score    # Calculate maintainability score
make quality-grade            # Calculate overall quality grade
```

### Quality Reporting

```bash
# Report generation
make generate-reports         # Generate all quality reports
make executive-report         # Generate executive summary report
make technical-report         # Generate technical detailed report
make dashboard-report         # Generate dashboard overview report
make html-report              # Generate HTML quality report
make json-report              # Generate JSON quality report
make pdf-report               # Generate PDF quality report
```

### Issue Management

```bash
# Issue detection and management
make detect-issues            # Detect quality issues across projects
make classify-issues          # Classify detected issues by severity
make prioritize-issues        # Prioritize issues by impact
make track-issues             # Track issue resolution progress
```

### Django Web Interface

```bash
# Django development server
make web-start                # Start Django web interface (port 8000)
make web-migrate              # Run Django migrations
make web-shell                # Open Django shell

# Quick start with all services
./start_all.sh                # Start complete system (Redis, Celery, Django)
./start_all.sh --create-superuser  # Include superuser creation
```

### Docker Operations

```bash
# Full containerized development
docker-compose up -d          # Start all services (web, db, redis, celery, flower)
docker-compose up web         # Start web service only
docker-compose logs -f web    # Follow web service logs
docker-compose exec web python manage.py shell  # Django shell in container

# Individual services
docker-compose up db redis    # Start database and Redis only
docker-compose exec db psql -U postgres -d dc_analyzer  # Access PostgreSQL

# Monitoring
docker-compose up flower      # Start Celery monitoring (port 5555)
```

### Build & Distribution

```bash
# Build operations
make build                    # Build distribution packages
make build-clean              # Clean and build
make clean                    # Remove all artifacts
make clean-all                # Deep clean including venv
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
if result.is_success:
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
            if not validation_result.is_success:
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

- **Environment Variables**: Runtime configuration and thresholds
- **pyproject.toml**: Tool configuration (ruff, mypy, pytest)
- **Django Settings**: Web interface configuration
- **Analysis Config**: Per-analysis configuration in QualityAnalysis entity

Key configuration files:

- `pyproject.toml`: Primary configuration for tools and dependencies
- `code_analyzer_web/settings.py`: Django configuration
- `Makefile`: Development workflow and quality gates
- `docker-compose.yml`: Container orchestration with PostgreSQL, Redis, Celery
- `start_all.sh`: Complete system startup script

### Essential Environment Variables

```bash
# Database configuration
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dc_analyzer

# Redis/Celery configuration
export REDIS_URL=redis://localhost:6379/0
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Django configuration
export DEBUG=True
export SECRET_KEY=your-secret-key-here

# Quality thresholds
export QUALITY_MIN_COVERAGE=90.0
export QUALITY_MAX_COMPLEXITY=10
```

## Critical Architecture Gaps - High Priority Resolution Required

### 🚨 GAP 1: Ecosystem Services Integration Missing

**Status**: HIGH PRIORITY - Quality service not integrated with FLEXT ecosystem services

**Current Issues**:

- Django web interface not integrated with flext-web or flext-api patterns
- Quality analysis not connected to flext-observability metrics collection
- No CLI integration with flext-cli command structure
- Reports not accessible via ecosystem dashboard interfaces

**Required Actions**:

- [ ] Integrate Django interface with flext-web architectural patterns
- [ ] Connect quality metrics pipeline with flext-observability
- [ ] Create quality analysis commands for flext-cli integration
- [ ] Implement quality dashboard integration with ecosystem web interface

### 🚨 GAP 2: Multi-Project Analysis Not Ecosystem-Aware

**Status**: HIGH PRIORITY - Workspace analysis lacks ecosystem structure understanding

**Current Issues**:

- `make workspace-analyze` doesn't understand 32-project ecosystem structure
- Quality thresholds not differentiated by project type (core, service, tap, target)
- Cross-project dependency analysis capabilities missing
- Ecosystem-wide quality metrics not consolidated or available

**Required Actions**:

- [ ] Implement ecosystem-aware analysis patterns for 32+ project structure
- [ ] Create project-type-specific quality thresholds (core, service, tap, target)
- [ ] Implement cross-project dependency quality analysis capabilities
- [ ] Create consolidated ecosystem quality dashboard and metrics

### 🚨 GAP 3: Django vs Clean Architecture Inconsistency

**Status**: HIGH PRIORITY - Django patterns conflict with Clean Architecture principles

**Current Issues**:

- Django used for web interface conflicts with flext-web Flask patterns
- Django ORM conflicts with flext-core domain entity patterns
- Django settings conflict with flext-core configuration management

**Required Actions**:

- [ ] Refactor to use flext-web patterns or document Django architecture decision
- [ ] Integrate Django models with flext-core domain entities
- [ ] Migrate Django settings to flext-core configuration patterns
- [ ] Document web interface architecture decisions and trade-offs

## Troubleshooting

### Common Development Issues

**Database Connection Issues:**

```bash
# Reset database
docker-compose down -v
docker-compose up -d db
make web-migrate

# Check database connection
docker-compose exec db psql -U postgres -d dc_analyzer -c "SELECT version();"
```

**Redis/Celery Issues:**

```bash
# Check Redis connection
redis-cli ping

# Restart Celery worker
pkill -f celery
celery -A code_analyzer_web worker --loglevel=info --detach

# Monitor Celery tasks
docker-compose up flower  # Access at localhost:5555
```

**Django Development Issues:**

```bash
# Reset Django state
make clean
make web-migrate
python manage.py collectstatic --noinput

# Debug Django settings
make web-shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

**Poetry/Dependencies Issues:**

```bash
# Reset virtual environment
make clean-all
make setup

# Check dependency conflicts
poetry show --tree
poetry check
```

### Performance Debugging

```bash
# Profile analysis performance
make analyze PROJECT=small-project  # Start with small projects
time make workspace-analyze         # Time full workspace analysis

# Django debug toolbar (when DEBUG=True)
# Add django-debug-toolbar to see SQL queries and performance

# Celery monitoring
docker-compose up flower            # Monitor task execution
```

### Service Architecture

The project uses a **hybrid architecture** combining:

1. **Django Web Framework**: For admin interface, REST API, and web dashboard
2. **Clean Architecture**: Domain entities in `src/flext_quality/domain/`
3. **Multi-Backend Analysis**: Pluggable analyzers (AST, Ruff, MyPy, Bandit)
4. **Celery Task Processing**: Async analysis execution
5. **Docker Multi-Service**: PostgreSQL, Redis, Celery worker, web server
