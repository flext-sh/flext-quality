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
make dev-install              # Install in development mode
make pre-commit               # Setup pre-commit hooks
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

### Build & Distribution

```bash
# Build operations
make build                    # Build distribution packages
make package                  # Create deployment package
make clean                    # Remove all artifacts
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

1. **Setup**: Run `make setup` for complete development environment
2. **Development**: Make changes following Clean Architecture patterns
3. **Quality Gates**: Run `make validate` before committing
4. **Testing**: Ensure 90% coverage with `make test`
5. **Analysis**: Use quality analysis tools to validate code quality

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

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Integration com Ecosystem Services Missing

**Status**: ALTO - Quality service não integrado com outros services
**Problema**:

- Django web interface não integra com flext-web ou flext-api
- Quality analysis não conecta com flext-observability metrics
- Não tem CLI integration com flext-cli
- Reports não acessíveis via ecosystem dashboard

**TODO**:

- [ ] Integrar Django interface com flext-web patterns
- [ ] Conectar quality metrics com flext-observability
- [ ] Criar quality commands para flext-cli
- [ ] Implementar quality dashboard no ecosystem web interface

### 🚨 GAP 2: Multi-Project Analysis Not Ecosystem-Aware

**Status**: ALTO - Workspace analysis não conhece ecosystem structure
**Problema**:

- `make workspace-analyze` não entende 32-project ecosystem structure
- Quality thresholds não diferenciados por tipo de project (core, service, tap, target)
- Cross-project dependency analysis missing
- Ecosystem-wide quality metrics não consolidados

**TODO**:

- [ ] Implementar ecosystem-aware analysis patterns
- [ ] Criar quality thresholds específicos por project type
- [ ] Implementar cross-project dependency quality analysis
- [ ] Criar consolidated ecosystem quality dashboard

### 🚨 GAP 3: Django vs Clean Architecture Inconsistency

**Status**: ALTO - Django patterns conflitam com Clean Architecture
**Problema**:

- Django usado para web interface vs flext-web Flask patterns
- Django ORM vs flext-core domain patterns
- Django settings vs flext-core configuration patterns

**TODO**:

- [ ] Refatorar para usar flext-web patterns ou justificar Django choice
- [ ] Integrar Django models com flext-core domain entities
- [ ] Migrar Django settings para flext-core configuration patterns
- [ ] Documentar web interface architecture decisions
