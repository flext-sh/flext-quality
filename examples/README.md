# FLEXT Quality Examples

Comprehensive examples demonstrating FLEXT Quality usage patterns, integration scenarios, and best practices for code quality analysis within the FLEXT ecosystem.

## Overview

This directory contains practical examples that showcase the capabilities of FLEXT Quality, from basic analysis operations to advanced ecosystem integration scenarios. Each example includes detailed explanations, configuration files, and expected outputs.

## Example Categories

### **Basic Usage** (`basic/`)

Fundamental quality analysis operations and simple API usage:

- **Simple Analysis**: Basic project analysis with default settings
- **Custom Configuration**: Analysis with custom thresholds and settings
- **Result Processing**: Working with analysis results and quality metrics
- **Error Handling**: Proper error handling with FlextResult patterns

### **Advanced Analysis** (`advanced/`)

Sophisticated analysis scenarios and enterprise features:

- **Multi-Backend Integration**: Using multiple analysis backends simultaneously
- **Custom Rules**: Creating and implementing custom quality rules
- **Performance Optimization**: Large project analysis with resource management
- **Historical Analysis**: Trend analysis and quality evolution tracking

### **FLEXT Ecosystem Integration** (`integration/`)

Integration patterns with other FLEXT services and components:

- **flext-core Integration**: Using foundation patterns and dependency injection
- **flext-observability Integration**: Monitoring and metrics integration
- **flext-web Integration**: Dashboard and web interface integration
- **Cross-Project Analysis**: Ecosystem-wide quality assessment

### **CI/CD Integration** (`ci-cd/`)

Continuous integration and deployment examples:

- **GitHub Actions**: Quality gates in GitHub workflows
- **GitLab CI**: Quality analysis in GitLab pipelines
- **Jenkins**: Integration with Jenkins build systems
- **Quality Gates**: Automated quality enforcement strategies

### **API Examples** (`api/`)

REST API usage patterns and integration examples:

- **REST API Usage**: Direct API calls and responses
- **Python SDK**: Using the Python client library
- **CLI Usage**: Command-line interface examples
- **Webhook Integration**: Event-driven quality notifications

### **Reports and Dashboards** (`reports/`)

Report generation and dashboard integration examples:

- **Executive Reports**: High-level quality summaries for leadership
- **Technical Reports**: Detailed analysis for development teams
- **Custom Templates**: Creating custom report formats
- **Dashboard Integration**: Embedding quality metrics in dashboards

## Quick Start Examples

### Basic Project Analysis

```python

# examples/basic/simple_analysis.py
from flext_quality import CodeAnalyzer

# Initialize analyzer for your project
analyzer = CodeAnalyzer("/path/to/your/project")

# Execute comprehensive analysis
results = analyzer.analyze_project()

# Check quality score and grade
score = analyzer.get_quality_score()
grade = analyzer.get_quality_grade()

print(f"Quality Assessment: {grade} ({score:.1f}/100)")
print(f"Files Analyzed: {results['files_analyzed']}")
print(f"Issues Found: {len(results['issues']['security']) + len(results['issues']['complexity'])}")
```

### FLEXT Ecosystem Integration

```python

# examples/integration/flext_ecosystem.py
from flext_quality import QualityAPI
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
from flext_observability import create_metric

# Initialize with dependency injection
container = FlextContainer()
quality_api = QualityAPI(container)

# Execute analysis with observability
def analyze_with_monitoring(project_path: str):
    result = quality_api.analyze_project(project_path)

    # Use current API pattern
    data = result.unwrap_or(None)
    if data is not None:
        # Publish metrics to observability stack
        create_metric(
            name="project_quality_score",
            value=data.overall_score,
            tags={"project": project_path}
        )
        return data
    else:
        print(f"Analysis failed: {result.error}")
        return None
```

### CI/CD Quality Gate

```yaml
# examples/ci-cd/github-actions.yml
name: Quality Gate
on: [push, pull_request]

jobs:
  quality-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install FLEXT Quality
        run: pip install flext-quality

      - name: Run Quality Analysis
        run: |
          flext-quality analyze . \
            --min-score 85.0 \
            --max-complexity 10 \
            --format json \
            --output quality-report.json

      - name: Upload Quality Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json
```

## Example Structure

Each example directory contains:

### Standard Files

- **`README.md`**: Detailed explanation and usage instructions
- **`example.py`**: Main example code with comprehensive comments
- **`config.yaml`**: Configuration file demonstrating customization options
- **`expected_output.json`**: Sample output showing expected results
- **`requirements.txt`**: Python dependencies for the example

### Optional Files

- **`docker-compose.yml`**: Containerized execution environment
- **`Makefile`**: Automation scripts for easy execution
- **`.env.example`**: Environment variable configuration template
- **`test_example.py`**: Unit tests validating the example functionality

## Running Examples

### Prerequisites

```bash

# Install FLEXT Quality
pip install flext-quality

# Or install from source
git clone https://github.com/flext-sh/flext-quality
cd flext-quality
make install
```

### Execute Examples

```bash

# Navigate to example directory
cd examples/basic/simple_analysis

# Install example dependencies
pip install -r requirements.txt

# Run the example
python example.py

# View generated reports
ls -la reports/
```

### Docker Execution

```bash

# Use Docker for isolated execution
cd examples/advanced/multi_backend

# Build and run example
docker-compose up --build

# View results
docker-compose exec quality-analysis cat /app/reports/analysis_results.json
```

## Example Index

### Basic Examples

| Example               | Description                   | Complexity   | Integration |
| --------------------- | ----------------------------- | ------------ | ----------- |
| **simple_analysis**   | Basic project analysis        | Beginner     | None        |
| **custom_config**     | Custom analysis configuration | Beginner     | flext-core  |
| **result_processing** | Working with analysis results | Intermediate | flext-core  |
| **error_handling**    | FlextResult error patterns    | Intermediate | flext-core  |

### Advanced Examples

| Example            | Description                 | Complexity | Integration         |
| ------------------ | --------------------------- | ---------- | ------------------- |
| **multi_backend**  | Multiple analysis backends  | Advanced   | External tools      |
| **custom_rules**   | Custom quality rules        | Advanced   | Domain layer        |
| **large_projects** | Performance optimization    | Advanced   | Resource management |
| **trend_analysis** | Historical quality tracking | Advanced   | Database            |

### Integration Examples

| Example             | Description            | Complexity   | Integration             |
| ------------------- | ---------------------- | ------------ | ----------------------- |
| **observability**   | Monitoring integration | Intermediate | flext-observability     |
| **web_dashboard**   | Dashboard integration  | Intermediate | flext-web               |
| **cross_project**   | Ecosystem analysis     | Advanced     | Multiple FLEXT projects |
| **api_integration** | REST API usage         | Intermediate | Web services            |

## Best Practices Demonstrated

### Code Quality

- **Type Safety**: Comprehensive type hints and MyPy validation
- **Error Handling**: Consistent FlextResult patterns throughout
- **Documentation**: Enterprise-grade docstrings and code comments
- **Testing**: Unit tests and integration test examples

### Architecture Patterns

- **Clean Architecture**: Clear layer separation and dependency inversion
- **Domain-Driven Design**: Rich domain models and business logic
- **CQRS**: Command and query separation patterns
- **Event-Driven Design**: Domain events and observability integration

### Integration Standards

- **FLEXT Patterns**: Consistent usage of flext-core foundation patterns
- **Configuration Management**: Environment-specific configuration examples
- **Monitoring**: Comprehensive observability and metrics integration
- **Security**: Security best practices and vulnerability prevention

## Contributing Examples

### Example Development Guidelines

1. **Follow Structure**: Use the standard example directory structure
2. **Comprehensive Documentation**: Include detailed README and code comments
3. **Realistic Scenarios**: Use realistic data and use cases
4. **Test Coverage**: Include unit tests validating example functionality
5. **Integration Focus**: Demonstrate FLEXT ecosystem integration patterns

### Submission Process

1. **Create Branch**: `feature/example-<example-name>`
2. **Follow Standards**: Adhere to FLEXT coding and documentation standards
3. **Test Thoroughly**: Ensure examples work in clean environments
4. **Update Index**: Add example to the main README index
5. **Submit PR**: Include comprehensive description and testing notes

## Troubleshooting

### Common Issues

#### **Import Errors**

```bash

# Ensure FLEXT Quality is properly installed
pip install --upgrade flext-quality

# Check Python path
python -c "import flext_quality; print(flext_quality.__version__)"
```

#### **Configuration Issues**

```bash

# Validate configuration file
flext-quality validate-config config.yaml

# Check environment variables
flext-quality check-env
```

#### **Permission Issues**

```bash

# Ensure proper file permissions
chmod +x example.py

# Check directory access
ls -la /path/to/project
```

### Getting Help

- **Documentation**: [docs/README.md](../docs/README.md)
- **API Reference** - (_Documentation coming soon_)
- **Integration Guide** - (_Documentation coming soon_)
- **Troubleshooting** - (_Documentation coming soon_)

## Related Resources

- **[FLEXT Quality Documentation](../docs/README.md)** - Complete system documentation
- **API Reference** - REST API and Python SDK documentation (_Documentation coming soon_)
- **Integration Guide** - FLEXT ecosystem integration patterns (_Documentation coming soon_)
- **Development Guide** - Development setup and contribution guidelines (_Documentation coming soon_)
