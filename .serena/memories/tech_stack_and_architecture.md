# FLEXT-Quality Tech Stack and Architecture

## Tech Stack

- **Python**: 3.13+ (Latest version support)
- **Build System**: Poetry (poetry-core>=1.9.0)
- **Framework**: Pydantic 2.11.7+ for models and validation
- **Architecture**: Clean Architecture + Domain-Driven Design (DDD)
- **CLI**: flext-cli integration (NO direct click/rich usage)
- **Observability**: flext-observability integration
- **Core Foundation**: flext-core patterns (FlextResult, FlextLogger, FlextContainer)

## Key Dependencies

- **Core**: pydantic, pydantic-settings
- **Local Packages**: flext-core, flext-cli, flext-observability, flext-web (develop=true)
- **Dev Tools**: ruff>=0.12.3, mypy>=1.13.0, pytest>=8.4.0
- **Security**: bandit>=1.8.0, pip-audit>=2.7.3

## Architecture Layers

### Domain Layer (flext_quality/entities.py, value_objects.py)

- Quality entities: FlextQualityProject, FlextQualityAnalysis, FlextQualityIssue
- Value objects: QualityScore, QualityGrade, ComplexityMetric, CoverageMetric
- Domain events: ProjectCreatedEvent, AnalysisCompletedEvent

### Application Layer (flext_quality/services.py)

- BasicQualityProjectService, BasicQualityAnalysisService
- BasicQualityIssueService, BasicQualityReportService
- ExternalAnalysisService

### Infrastructure Layer (flext_quality/analyzer.py, backends)

- FlextQualityCodeAnalyzer (main analysis engine)
- FlextQualityASTBackend, FlextQualityExternalBackend
- Analysis backends: AST analysis, external tools (ruff, mypy, bandit)

### API Layer (flext_quality/api.py, cli.py)

- FlextQualityAPI (REST API interface)
- CLI commands using flext-cli exclusively

## Quality Standards

- **Type Safety**: MyPy strict mode enabled
- **Coverage**: 90% minimum requirement
- **Security**: Bandit security scanning
- **Code Style**: Ruff formatting with 88-character line limit
