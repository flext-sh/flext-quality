# FLEXT Quality - Source Code Documentation

This directory contains the source code for FLEXT Quality, an enterprise-grade code quality analysis and governance service for the FLEXT ecosystem.

## Architecture Overview

The source code follows Clean Architecture principles with clear layer separation:

```
src/flext_quality/
├── __init__.py              # Public API exports and deprecation handling
├── analyzer.py              # Multi-backend analysis engine
├── metrics.py               # Quality metrics and scoring
├── reports.py               # Report generation and formatting
├── domain/                  # Domain layer - business logic
├── application/             # Application layer - service orchestration
└── infrastructure/          # Infrastructure layer - external dependencies
```

## Core Components

### Public API (`__init__.py`)

- **QualityAPI**: Simplified API for external integration
- **CodeAnalyzer**: Main analysis interface
- **QualityMetrics**: Comprehensive quality measurements
- **Deprecation Management**: Guides migration to stable APIs

### Analysis Engine (`analyzer.py`)

- **Multi-Backend Architecture**: AST, security, complexity, duplicate detection
- **Configurable Analysis**: Enable/disable analysis types as needed
- **Quality Scoring**: Comprehensive scoring with penalty weights
- **Observability Integration**: Metrics and tracing through flext-observability

### Quality Metrics (`metrics.py`)

- **Comprehensive Scoring**: Multi-dimensional quality assessment
- **Standardized Grading**: Letter grades (A+ to F) with consistent thresholds
- **Domain Validation**: Business rule enforcement for data integrity
- **Export Capabilities**: Dictionary and summary format support

### Report Generation (`reports.py`)

- **Multi-Format Support**: HTML, JSON, PDF report generation
- **Template-Based**: Customizable report layouts and styling
- **Executive Summaries**: High-level quality overviews for stakeholders
- **Technical Details**: Comprehensive issue breakdowns for developers

## Layer Architecture

### Domain Layer (`domain/`)

Contains core business entities, value objects, and service interfaces:

- **QualityProject**: Project representation and lifecycle
- **QualityAnalysis**: Analysis execution and result management
- **QualityIssue**: Issue detection and classification
- **QualityReport**: Report generation and distribution
- **Service Ports**: Interface definitions for external dependencies

### Application Layer (`application/`)

Orchestrates business workflows and coordinates between layers:

- **Service Classes**: Business workflow orchestration
- **Command/Query Handlers**: CQRS pattern implementation
- **Transaction Management**: Consistency and rollback handling
- **Cross-Cutting Concerns**: Logging, error handling, validation

### Infrastructure Layer (`infrastructure/`)

Implements external dependencies and adapters:

- **Repository Adapters**: Data persistence implementations
- **Tool Integrations**: Ruff, MyPy, Bandit, security scanners
- **File System Access**: Code analysis and processing
- **Event Publishing**: Integration with flext-observability

## Integration Patterns

### FLEXT Core Integration

All components built on flext-core foundation patterns:

- **FlextResult**: Consistent error handling and operation outcomes
- **FlextEntity**: Domain entity base classes with validation
- **FlextValue**: Immutable value objects with business rules
- **FlextContainer**: Dependency injection for testability

### Observability Integration

Comprehensive monitoring through flext-observability:

- **Structured Logging**: Correlation IDs and contextual information
- **Metrics Collection**: Quality scores, analysis times, issue counts
- **Distributed Tracing**: End-to-end analysis workflow tracking
- **Health Monitoring**: Service availability and performance tracking

### External Tool Integration

Pluggable architecture for quality analysis tools:

- **Adapter Pattern**: Consistent interface for all external tools
- **Configuration Management**: Tool-specific settings and thresholds
- **Error Handling**: Graceful degradation when tools are unavailable
- **Result Normalization**: Consistent issue format across tools

## Development Guidelines

### Code Organization

- **Single Responsibility**: Each module has a clear, focused purpose
- **Dependency Inversion**: Depend on abstractions, not concretions
- **Interface Segregation**: Small, focused interfaces for better testability
- **Open/Closed Principle**: Extensible without modification

### Quality Standards

- **Type Safety**: Comprehensive type hints with strict MyPy validation
- **Test Coverage**: Minimum 90% coverage with comprehensive test suites
- **Documentation**: Enterprise-grade docstrings with examples
- **Error Handling**: Consistent FlextResult patterns throughout

### Performance Considerations

- **Async Processing**: Long-running analyses use async patterns
- **Memory Management**: Efficient handling of large codebases
- **Caching**: Intelligent result caching for repeated analyses
- **Resource Limits**: Configurable timeouts and resource constraints

## Usage Examples

### Basic Analysis

```python
from flext_quality import CodeAnalyzer

# Analyze a project
analyzer = CodeAnalyzer("/path/to/project")
results = analyzer.analyze_project()

# Get quality assessment
score = analyzer.get_quality_score()
grade = analyzer.get_quality_grade()
print(f"Quality: {grade} ({score:.1f}/100)")
```

### Comprehensive Metrics

```python
from flext_quality import QualityMetrics

# Create metrics from analysis results
metrics = QualityMetrics.from_analysis_results(results)

# Display summary
print(metrics.get_summary())

# Export for integration
data = metrics.to_dict()
```

### Custom Analysis Configuration

```python
# Selective analysis
results = analyzer.analyze_project(
    include_security=True,
    include_complexity=True,
    include_dead_code=False,
    include_duplicates=True
)
```

## Testing

The source code includes comprehensive test coverage:

- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Analysis speed and memory usage
- **Security Tests**: Vulnerability detection accuracy

Run tests with:

```bash
make test                    # Full test suite with coverage
make test-unit               # Unit tests only
make test-integration        # Integration tests only
```

## Contributing

When contributing to the source code:

1. **Follow Architecture**: Respect Clean Architecture boundaries
2. **Maintain Quality**: Pass all quality gates (lint, type, test)
3. **Update Documentation**: Keep docstrings and README current
4. **Add Tests**: Maintain coverage requirements
5. **Use FLEXT Patterns**: Leverage flext-core consistently

## Related Documentation

- **[Architecture Documentation](../docs/architecture/)** - Detailed system design
- **[Development Guide](../docs/development/)** - Setup and workflows
- **[API Reference](../docs/api/)** - Complete API documentation
- **[Integration Guide](../docs/integration/)** - FLEXT ecosystem integration
