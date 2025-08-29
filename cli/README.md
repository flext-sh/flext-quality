# CLI Module - Command-Line Interface

The CLI module provides comprehensive command-line interface functionality for FLEXT Quality, enabling developers and operations teams to perform quality analysis, generate reports, and manage quality governance from the command line.

## Overview

The CLI module implements a structured command architecture that provides:

- **Quality Analysis Commands**: Execute comprehensive code quality analysis
- **Report Generation**: Create quality reports in multiple formats
- **Configuration Management**: Manage analysis configuration and thresholds
- **Integration Commands**: Integrate with FLEXT ecosystem services
- **Development Tools**: Utilities for development and debugging

## Architecture

### Command Structure

```
cli/
├── __init__.py              # CLI module initialization and main entry
├── commands/                # Individual command implementations
│   ├── __init__.py         # Command registration and discovery
│   ├── analyze.py          # Analysis execution commands
│   ├── config.py           # Configuration management commands
│   ├── report.py           # Report generation commands
│   └── ecosystem.py        # FLEXT ecosystem integration commands
└── README.md               # This documentation
```

### Command Categories

#### **Analysis Commands** (`commands/analyze.py`)

Execute quality analysis operations:

- `analyze`: Comprehensive project analysis
- `analyze-file`: Single file analysis
- `analyze-workspace`: Multi-project workspace analysis
- `check-quality`: Quality threshold validation

#### **Report Commands** (`commands/report.py`)

Generate and manage quality reports:

- `generate-report`: Create comprehensive quality reports
- `dashboard`: Generate dashboard overview
- `export`: Export analysis results in various formats
- `compare`: Compare analysis results between versions

#### **Configuration Commands** (`commands/config.py`)

Manage analysis configuration:

- `config-init`: Initialize default configuration
- `config-validate`: Validate configuration files
- `config-show`: Display current configuration
- `threshold-set`: Configure quality thresholds

#### **Ecosystem Commands** (`commands/ecosystem.py`)

FLEXT ecosystem integration:

- `ecosystem-status`: Check ecosystem service status
- `publish-metrics`: Publish quality metrics to observability
- `register-service`: Register with ecosystem service registry
- `health-check`: Comprehensive health validation

## Usage Examples

### Basic Analysis

```bash
# Analyze current directory
flext-quality analyze

# Analyze specific project
flext-quality analyze /path/to/project

# Analyze with custom configuration
flext-quality analyze --config quality.yaml --min-score 85.0
```

### Report Generation

```bash
# Generate HTML report
flext-quality generate-report --format html --output report.html

# Generate executive summary
flext-quality dashboard --executive --output dashboard.json

# Compare analysis results
flext-quality compare baseline.json current.json --output comparison.html
```

### Configuration Management

```bash
# Initialize configuration
flext-quality config-init --template enterprise

# Validate configuration
flext-quality config-validate quality.yaml

# Set quality thresholds
flext-quality threshold-set --min-score 90 --max-complexity 8
```

### Ecosystem Integration

```bash
# Check ecosystem status
flext-quality ecosystem-status

# Publish metrics to observability
flext-quality publish-metrics --project-id flext-core

# Register with service registry
flext-quality register-service --endpoint http://localhost:8080
```

## Command Implementation

### Command Base Class

All commands inherit from a base command class that provides common functionality:

```python
from abc import ABC, abstractmethod
from flext_core import FlextResult
import click

class BaseCommand(ABC):
    """Base class for all CLI commands."""

    def __init__(self, container: FlextContainer):
        self.container = container
        self.logger = FlextLogger(self.__class__.__name__)

    @abstractmethod
    async def execute(self, **kwargs) -> FlextResult[dict]:
        """Execute the command with provided arguments."""
        pass

    def handle_result(self, result: FlextResult[dict]) -> int:
        """Handle command result and return exit code."""
        if result.success:
            self.display_success(result.data)
            return 0
        else:
            self.display_error(result.error)
            return 1
```

### Analysis Command Example

```python
class AnalyzeCommand(BaseCommand):
    """Command to execute comprehensive quality analysis."""

    async def execute(self, project_path: str, **kwargs) -> FlextResult[dict]:
        """Execute quality analysis on specified project."""
        try:
            # Get analysis service from container
            analysis_service = self.container.get("quality_analysis_service")

            # Configure analysis based on CLI arguments
            config = self._build_analysis_config(kwargs)

            # Execute analysis
            result = await analysis_service.execute_comprehensive_analysis(
                project_path, config
            )

            if result.success:
                return FlextResult[None].ok({
                    "analysis_id": result.data.id,
                    "quality_score": result.data.overall_score,
                    "quality_grade": result.data.quality_grade,
                    "issues_found": len(result.data.issues),
                    "files_analyzed": result.data.files_analyzed
                })
            else:
                return result.cast()

        except Exception as e:
            return FlextResult[None].fail(f"Analysis execution failed: {e}")
```

### Click Integration

Commands are exposed through Click decorators for user-friendly CLI:

```python
@click.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.option('--min-score', type=float, help='Minimum quality score threshold')
@click.option('--format', type=click.Choice(['json', 'text', 'table']), default='table')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.pass_context
async def analyze(ctx, project_path: str, **kwargs):
    """Execute comprehensive quality analysis on a project."""
    command = AnalyzeCommand(ctx.obj['container'])
    result = await command.execute(project_path, **kwargs)
    exit_code = command.handle_result(result)
    ctx.exit(exit_code)
```

## Configuration Integration

### Configuration File Support

The CLI supports multiple configuration formats:

```yaml
# quality.yaml - Analysis configuration
analysis:
  include_security: true
  include_complexity: true
  include_dead_code: true
  include_duplicates: true

thresholds:
  min_overall_score: 85.0
  max_complexity: 10
  min_coverage: 90.0

tools:
  ruff:
    enabled: true
    config_file: pyproject.toml
  mypy:
    enabled: true
    strict: true
  bandit:
    enabled: true
    confidence: medium

output:
  format: html
  include_details: true
  output_path: reports/quality-report.html
```

### Environment Variable Support

```bash
# CLI behavior configuration
export FLEXT_QUALITY_CONFIG=/path/to/quality.yaml
export FLEXT_QUALITY_OUTPUT_FORMAT=json
export FLEXT_QUALITY_VERBOSE=true

# Analysis configuration
export FLEXT_QUALITY_MIN_SCORE=85.0
export FLEXT_QUALITY_MAX_COMPLEXITY=10
export FLEXT_QUALITY_TIMEOUT=600
```

## Output Formatting

### Multiple Output Formats

The CLI supports various output formats for different use cases:

#### **Table Format** (Default)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT Quality Analysis Report                │
├─────────────────────────────────────────────────────────────────┤
│ Project Path    │ /path/to/project                              │
│ Analysis Date   │ 2025-08-04 14:30:25                          │
│ Quality Score   │ 87.3/100 (B+)                                │
│ Files Analyzed  │ 42                                            │
│ Total Issues    │ 8                                             │
├─────────────────────────────────────────────────────────────────┤
│ Issue Breakdown │ Security: 0 │ Complexity: 3 │ Dead Code: 2   │
│                 │ Duplicates: 3 │ Style: 0                     │
└─────────────────────────────────────────────────────────────────┘
```

#### **JSON Format**

```json
{
  "analysis_id": "analysis_20250804_143025",
  "project_path": "/path/to/project",
  "timestamp": "2025-08-04T14:30:25Z",
  "quality_score": 87.3,
  "quality_grade": "B+",
  "files_analyzed": 42,
  "total_issues": 8,
  "issue_breakdown": {
    "security": 0,
    "complexity": 3,
    "dead_code": 2,
    "duplicates": 3,
    "style": 0
  },
  "recommendations": [
    "Address 3 high-complexity functions",
    "Remove 2 unused code blocks",
    "Eliminate 3 code duplications"
  ]
}
```

#### **Text Format**

```
FLEXT Quality Analysis Report
============================
Project: /path/to/project
Date: 2025-08-04 14:30:25
Score: 87.3/100 (B+)

Files Analyzed: 42
Total Issues: 8

Issue Summary:
- Security Issues: 0
- Complexity Issues: 3
- Dead Code Items: 2
- Code Duplications: 3
- Style Violations: 0

Recommendations:
1. Address 3 high-complexity functions
2. Remove 2 unused code blocks
3. Eliminate 3 code duplications
```

## Error Handling

### Consistent Error Reporting

All CLI commands use consistent error handling and reporting:

```python
class CLIErrorHandler:
    """Centralized error handling for CLI commands."""

    @staticmethod
    def handle_analysis_error(error: str) -> None:
        """Handle analysis execution errors."""
        click.echo(
            click.style(f"❌ Analysis failed: {error}", fg='red'),
            err=True
        )

    @staticmethod
    def handle_configuration_error(error: str) -> None:
        """Handle configuration validation errors."""
        click.echo(
            click.style(f"⚙️ Configuration error: {error}", fg='yellow'),
            err=True
        )

    @staticmethod
    def handle_network_error(error: str) -> None:
        """Handle network connectivity errors."""
        click.echo(
            click.style(f"🌐 Network error: {error}", fg='red'),
            err=True
        )
```

### Exit Codes

Standard exit codes for different scenarios:

- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: Analysis failed
- `4`: Network/connectivity error
- `5`: Permission denied
- `6`: Resource not found

## Integration with FLEXT Ecosystem

### Service Discovery

The CLI integrates with FLEXT ecosystem service discovery:

```python
class EcosystemIntegration:
    """Integration with FLEXT ecosystem services."""

    async def discover_services(self) -> FlextResult[dict]:
        """Discover available FLEXT ecosystem services."""
        try:
            # Query service registry
            services = await self._query_service_registry()

            return FlextResult[None].ok({
                "flext-core": services.get("flext-core"),
                "flext-observability": services.get("flext-observability"),
                "flext-web": services.get("flext-web")
            })
        except Exception as e:
            return FlextResult[None].fail(f"Service discovery failed: {e}")
```

### Metrics Publishing

Automatic metrics publishing to ecosystem observability:

```python
async def publish_analysis_metrics(self, analysis_result: dict) -> None:
    """Publish analysis metrics to ecosystem observability."""
    try:
        observability = self.container.get("observability_adapter")

        await observability.publish_metric(
            name="quality_analysis_completed",
            value=1,
            tags={
                "project": analysis_result["project_path"],
                "score": analysis_result["quality_score"],
                "grade": analysis_result["quality_grade"]
            }
        )
    except Exception as e:
        self.logger.warning(f"Failed to publish metrics: {e}")
```

## Development and Debugging

### Debug Mode

Enhanced debugging capabilities for development:

```bash
# Enable debug mode
flext-quality --debug analyze /path/to/project

# Verbose output
flext-quality --verbose analyze /path/to/project

# Trace execution
flext-quality --trace analyze /path/to/project
```

### Development Commands

Special commands for development and testing:

```bash
# Validate CLI installation
flext-quality --version
flext-quality check-install

# Test configuration
flext-quality config-test

# Profile analysis performance
flext-quality analyze --profile /path/to/project
```

## Testing

### CLI Testing Framework

Comprehensive testing for CLI commands:

```python
from click.testing import CliRunner
import pytest

class TestAnalyzeCommand:
    """Test suite for analyze command."""

    def test_analyze_command_success(self, temp_project):
        """Test successful analysis execution."""
        runner = CliRunner()
        result = runner.invoke(analyze, [temp_project])

        assert result.exit_code == 0
        assert "Quality Score" in result.output
        assert "Analysis completed" in result.output

    def test_analyze_command_invalid_path(self):
        """Test analysis with invalid project path."""
        runner = CliRunner()
        result = runner.invoke(analyze, ["/nonexistent/path"])

        assert result.exit_code != 0
        assert "Path does not exist" in result.output
```

## Related Documentation

- **[Main CLI Module](../cli.py)** - CLI entry point and command registration
- **[Application Services](../application/README.md)** - Service layer integration
- **[Configuration Management](../config/README.md)** - Configuration handling
- **[FLEXT CLI Integration](../../../docs/integration/flext-cli.md)** - Ecosystem CLI patterns
