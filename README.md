# FLEXT Quality

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FLEXT Ecosystem](https://img.shields.io/badge/FLEXT-Quality%20Service-blue.svg)](https://github.com/flext-sh/flext)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean%20%2B%20DDD%20%2B%20CQRS-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Coverage](https://img.shields.io/badge/coverage-90%25+-brightgreen.svg)](https://pytest.org)
[![Quality Gate](https://img.shields.io/badge/Quality%20Gate-Passing-brightgreen.svg)](https://sonarqube.com)

**Enterprise-grade code quality analysis and governance service for the FLEXT distributed data integration platform.**

FLEXT Quality serves as the centralized quality governance hub for the FLEXT ecosystem, providing comprehensive quality assessment, automated governance enforcement, and ecosystem-wide quality metrics across all FLEXT projects. Built with Clean Architecture principles and integrated with flext-core foundation patterns for consistency and reliability.

## What is FLEXT Quality

FLEXT Quality is the **centralized quality governance service** for the FLEXT ecosystem, providing automated code analysis, quality metrics, and governance enforcement across all FLEXT projects. It ensures consistent quality standards, detects technical debt, and maintains the high-quality standards required for an enterprise-grade distributed data integration platform.

### Purpose in FLEXT Ecosystem

As part of the **Application Services layer** in FLEXT architecture, FLEXT Quality provides:

- **Quality Governance**: Automated quality gates and standards enforcement across all 32+ FLEXT projects
- **Technical Debt Detection**: Proactive identification of maintainability issues and architectural violations
- **Ecosystem-Wide Metrics**: Unified quality dashboards and reports for the entire FLEXT platform
- **Integration Quality**: Cross-project dependency analysis and API compatibility validation
- **Compliance Assurance**: Automated verification of coding standards, security requirements, and architectural patterns

### Core Capabilities

- **Multi-Backend Analysis Engine**: Pluggable analyzers (AST, Ruff, MyPy, Bandit, Semgrep) with extensible architecture
- **FLEXT Pattern Validation**: Automated verification of Clean Architecture, DDD, and CQRS patterns
- **Quality Scoring**: Composite quality scores with weighted metrics aligned to business impact
- **Automated Governance**: Quality gates integrated with CI/CD pipelines and development workflows
- **Executive Reporting**: Quality dashboards and reports for technical leadership and stakeholders

## Architecture

FLEXT Quality follows **Clean Architecture + DDD + CQRS** patterns, built on **flext-core** foundation libraries for consistency across the FLEXT ecosystem.

### FLEXT Integration Architecture

```
FLEXT Quality Service (Application Layer)
├── Built on flext-core Foundation
│   ├── FlextEntity (Domain entities)
│   ├── FlextResult (Error handling)
│   ├── FlextContainer (Dependency injection)
│   └── FlextObservability (Monitoring)
├── Integrates with FLEXT Services
│   ├── flext-observability (Quality metrics)
│   ├── flext-web (Dashboard integration)
│   ├── flext-cli (Quality commands)
│   └── flext-api (REST API endpoints)
└── Analyzes FLEXT Projects
    ├── Core Libraries (flext-core, flext-observability)
    ├── Application Services (flext-api, flext-web, flext-auth)
    ├── Infrastructure Libraries (flext-db-*, flext-ldap, flext-grpc)
    └── Singer Ecosystem (taps, targets, dbt projects)
```

### Domain Layer (Clean Architecture)

Following flext-core patterns with enterprise-grade domain modeling:

```python
# Quality Project Aggregate
QualityProject (FlextEntity)
├── project_path: str
├── repository_url: Optional[str]
├── quality_config: QualityConfig
└── Domain Methods: validate_standards(), calculate_compliance()

# Quality Analysis Aggregate
QualityAnalysis (FlextEntity)
├── analysis_metrics: QualityMetrics
├── quality_issues: List[QualityIssue]
├── analysis_scores: QualityScores
└── Domain Methods: calculate_overall_score(), generate_grade()

# Quality Issue Entity
QualityIssue (FlextEntity)
├── severity: IssueSeverity
├── issue_type: IssueType
├── location: CodeLocation
└── Domain Methods: assess_impact(), suggest_fix()
```

### Application Layer (CQRS Pattern)

**Commands** (Write Operations):

- `AnalyzeProjectCommand` → Quality analysis orchestration
- `CreateQualityReportCommand` → Report generation
- `UpdateQualityStandardsCommand` → Governance rules management

**Queries** (Read Operations):

- `GetProjectQualityQuery` → Quality metrics retrieval
- `GetEcosystemDashboardQuery` → Ecosystem-wide quality view
- `GetComplianceReportQuery` → Compliance status reporting

**Handlers** (Business Logic):

- Built using flext-core service patterns with FlextResult error handling
- Integrated with flext-observability for quality metrics tracking
- Event-driven communication with other FLEXT services

## Quick Start

### Prerequisites

- Python 3.13+
- Poetry (package management)
- Docker & Docker Compose (for full service stack)
- Access to FLEXT ecosystem projects

### Installation

```bash
# Clone the repository
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality

# Install dependencies
make setup

# Run database migrations
make web-migrate
```

### Basic Usage

#### Analyze a FLEXT Project

```bash
# Quick analysis of a project
make analyze PROJECT=flext-core

# Full ecosystem analysis
make workspace-analyze

# Generate quality reports
make generate-reports
```

#### Using the Python API

```python
from flext_quality.application.services import QualityProjectService
from flext_quality.domain.entities import QualityProject
from flext_core import FlextResult

# Initialize service
project_service = QualityProjectService()

# Create project for analysis
result: FlextResult[QualityProject] = await project_service.create_project(
    name="flext-core",
    project_path="/path/to/flext-core",
    repository_url="https://github.com/flext-sh/flext-core"
)

if result.success:
    project = result.data
    print(f"Project created: {project.name}")
else:
    print(f"Error: {result.error}")
```

#### Web Dashboard

```bash
# Start web interface
make web-start

# Access dashboard
open http://localhost:8000
```

## Development

### Development Setup

```bash
# Complete development environment
make setup

# Start all services (PostgreSQL, Redis, Celery, Web)
./start_all.sh

# Or use Docker
docker-compose up -d
```

### Quality Gates

All code must pass these quality gates:

```bash
# Run all quality checks
make validate

# Individual checks
make lint          # Ruff linting (ALL rules enabled)
make type-check    # MyPy strict mode
make test          # Tests with 90% coverage minimum
make security      # Security scanning (Bandit + pip-audit)
```

### Testing

```bash
# Run test suite
make test

# Run specific test categories
pytest -m unit           # Unit tests
pytest -m integration    # Integration tests
pytest -m quality        # Quality analysis tests
```

## Integration with FLEXT Ecosystem

### flext-core Integration

FLEXT Quality is built on flext-core foundation:

```python
from flext_core import FlextEntity, FlextResult, FlextContainer
from flext_observability import flext_monitor_function

# All domain entities extend FlextEntity
class QualityProject(FlextEntity):
    # Inherits ID, timestamps, validation, etc.
    pass

# All operations return FlextResult
@flext_monitor_function("quality_analysis")
async def analyze_project(project: QualityProject) -> FlextResult[QualityAnalysis]:
    # Automatic monitoring and error handling
    pass
```

### flext-observability Integration

Quality metrics are automatically integrated with ecosystem monitoring:

```python
from flext_observability import flext_create_metric, flext_create_trace

# Quality metrics sent to central monitoring
flext_create_metric(
    name="quality_score",
    value=analysis.overall_score,
    tags={"project": project.name, "ecosystem": "flext"}
)
```

### flext-cli Integration

Quality commands available through flext-cli:

```bash
# Via flext-cli (when integrated)
flext quality analyze --project flext-core
flext quality report --format executive
flext quality dashboard --ecosystem
```

## Use Cases

### For FLEXT Platform Teams

- **Ecosystem Quality Dashboard**: Monitor quality across all 32+ FLEXT projects
- **Technical Debt Management**: Identify and track technical debt across the platform
- **Architecture Compliance**: Ensure all projects follow Clean Architecture + DDD patterns
- **Integration Quality**: Validate API compatibility and cross-project dependencies

### For Development Teams

- **Pre-commit Quality Gates**: Automated quality validation before code commits
- **Pull Request Analysis**: Quality reports integrated with GitHub/GitLab workflows
- **Continuous Quality Monitoring**: Real-time quality metrics and alerts
- **Refactoring Guidance**: Automated suggestions for code improvements

### For Engineering Leadership

- **Quality Metrics Reporting**: Executive dashboards and quality trend analysis
- **Compliance Auditing**: Automated verification of coding standards and best practices
- **Risk Assessment**: Technical debt and maintainability risk analysis
- **Resource Planning**: Quality-based prioritization for technical improvements

## Configuration

### Environment Variables

```bash
# Database configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flext_quality

# Redis/Celery configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Quality thresholds
QUALITY_MIN_COVERAGE=90.0
QUALITY_MAX_COMPLEXITY=10
QUALITY_MIN_SECURITY_SCORE=90.0

# FLEXT ecosystem integration
FLEXT_OBSERVABILITY_ENABLED=true
FLEXT_QUALITY_DASHBOARD_URL=http://localhost:8000
```

### Quality Standards Configuration

```python
# pyproject.toml quality configuration
[tool.flext-quality]
min_coverage = 90.0
max_complexity = 10
max_duplication = 5.0
enabled_analyzers = ["ruff", "mypy", "bandit", "semgrep"]
report_formats = ["html", "json", "executive"]
```

## API Reference

### REST API Endpoints

```bash
# Projects
GET    /api/v1/projects/                    # List all projects
POST   /api/v1/projects/                    # Create project
GET    /api/v1/projects/{id}/               # Get project details
DELETE /api/v1/projects/{id}/               # Delete project

# Analysis
POST   /api/v1/projects/{id}/analyze/       # Start analysis
GET    /api/v1/analyses/{id}/               # Get analysis results
GET    /api/v1/analyses/{id}/report/        # Download report

# Quality metrics
GET    /api/v1/metrics/ecosystem/           # Ecosystem-wide metrics
GET    /api/v1/metrics/projects/{id}/       # Project-specific metrics
GET    /api/v1/metrics/trends/              # Quality trends over time

# Quality issues
GET    /api/v1/issues/                      # List quality issues
GET    /api/v1/issues/{id}/                 # Get issue details
PUT    /api/v1/issues/{id}/suppress/        # Suppress issue
```

### Python SDK

```python
from flext_quality import FlextQualitySDK

# Initialize SDK
sdk = FlextQualitySDK(base_url="http://localhost:8000")

# Analyze project
analysis = await sdk.analyze_project(
    project_path="/path/to/project",
    wait_for_completion=True
)

# Get quality metrics
metrics = await sdk.get_project_metrics(project_id="123")

# Generate reports
report = await sdk.generate_report(
    analysis_id="456",
    format="executive"
)
```

## Deployment

### Docker Deployment

```bash
# Build and deploy
docker-compose up -d

# Scale services
docker-compose up -d --scale web=3 --scale celery=2

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=flext-quality
```

## Monitoring and Observability

FLEXT Quality provides comprehensive monitoring through flext-observability integration:

### Quality Metrics

- **Project Quality Scores**: Overall quality scores and trends
- **Issue Detection Rates**: Quality issues found and resolved
- **Analysis Performance**: Analysis execution times and throughput
- **Coverage Metrics**: Test coverage across projects
- **Security Metrics**: Security issues and vulnerability counts

### Dashboards

- **Executive Dashboard**: High-level quality metrics and trends
- **Technical Dashboard**: Detailed quality analysis and issue tracking
- **Ecosystem Dashboard**: Quality status across all FLEXT projects

### Alerts

- **Quality Gate Failures**: When projects fail quality thresholds
- **Security Issues**: When critical security vulnerabilities are detected
- **Technical Debt**: When technical debt exceeds acceptable levels

## Contributing

1. Follow FLEXT development standards in [CLAUDE.md](CLAUDE.md)
2. Maintain 90%+ test coverage for all new features
3. Use flext-core patterns for all domain logic
4. Update quality thresholds and metrics for new analysis types
5. Ensure integration with flext-observability for all new metrics

## Documentation

- **[Architecture Guide](docs/architecture/README.md)** - Clean Architecture + DDD implementation
- **[API Documentation](docs/api/README.md)** - Complete API reference
- **[Development Guide](docs/development/README.md)** - Development setup and patterns
- **[Integration Guide](docs/integration/README.md)** - FLEXT ecosystem integration
- **[Deployment Guide](docs/deployment/README.md)** - Production deployment instructions

## Status and Roadmap

**Current Status**: Development (v0.9.0)

### Known Issues

- [ ] Architecture refactoring needed (see [docs/TODO.md](docs/TODO.md))
- [ ] Django vs Clean Architecture integration
- [ ] Complete flext-observability integration

### Roadmap

- **v1.0**: Production-ready quality service with full FLEXT integration
- **v1.1**: Advanced quality metrics and ML-based issue detection
- **v1.2**: Real-time quality monitoring and automated remediation

## License

This project is part of the FLEXT ecosystem. See [LICENSE](LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext-quality/issues)
- **Documentation**: [FLEXT Quality Docs](docs/)
- **FLEXT Ecosystem**: [Main Repository](https://github.com/flext-sh/flext)
