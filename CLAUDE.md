# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

**FLEXT Quality - Code Quality Analysis & Metrics Library**
**Version**: 0.9.0 | **Updated**: 2025-10-10
**Status**: Solid domain architecture with accessibility and integration barriers requiring resolution

## 📋 DOCUMENT STRUCTURE & REFERENCES

**Quick Links**:
- **[~/.claude/commands/flext.md](~/.claude/commands/flext.md)**: Optimization command for module refactoring (USE with `/flext` command)
- **[../CLAUDE.md](../CLAUDE.md)**: FLEXT ecosystem standards and domain library rules
- **[README.md](README.md)**: Project overview and usage documentation
- **[TODO.md](TODO.md)**: Current technical issues and development priorities

**Document Purpose**:
- **This file (CLAUDE.md)**: Project-specific flext-quality standards and quality analysis patterns
- **flext.md command**: Practical refactoring workflows and MCP tool usage patterns
- **Workspace CLAUDE.md**: Domain library standards and ecosystem architectural principles

**DO NOT DUPLICATE**: This file focuses on flext-quality specifics. The `/flext` command provides HOW-TO workflows. The workspace CLAUDE.md provides ecosystem-wide standards.

**Hierarchy**: This document provides project-specific standards based on workspace-level patterns defined in [../CLAUDE.md](../CLAUDE.md). For architectural principles, quality gates, and MCP server usage, reference the main workspace standards.

---

## 🔗 MCP SERVER INTEGRATION (MANDATORY)

As defined in [../CLAUDE.md](../CLAUDE.md), all FLEXT development MUST use:

| MCP Server              | Purpose                                                     | Status          |
|-------------------------|-------------------------------------------------------------|-----------------|
| **serena**              | Semantic code analysis, symbol manipulation, refactoring    | **MANDATORY**   |
| **sequential-thinking** | Quality architecture and analysis problem decomposition     | **RECOMMENDED** |
| **context7**            | Third-party library documentation (Pydantic, AST)           | **RECOMMENDED** |
| **github**              | Repository operations and quality ecosystem PRs             | **ACTIVE**      |

**Usage**: Reference [~/.claude/commands/flext.md](~/.claude/commands/flext.md) for MCP workflows. Use `/flext` command for module optimization.

---

## 🎯 FLEXT-QUALITY MISSION

**ROLE**: flext-quality provides comprehensive code quality analysis and metrics collection for the FLEXT ecosystem, enabling automated quality assessment, scoring, and reporting across Python projects.

**CURRENT CAPABILITIES**:

- ✅ **Domain Architecture**: Well-structured entities with FlextResult patterns and domain events
- ⚠️ **Quality Analysis Engine**: AST-based analysis engine exists but has flext-core integration issues
- ✅ **Service Layer**: Quality services with proper error handling and FlextLogger integration
- ✅ **Grade Calculator**: Comprehensive quality scoring and grading system
- ✅ **Report Generation**: Multiple format reporting (JSON, HTML, text)
- ⚠️ **FLEXT Integration**: Uses flext-core patterns but has BaseModel compatibility issues
- ❌ **Accessibility**: Core analyzer not accessible via standard imports due to model integration failures
- ❌ **Quality Gates**: Import errors and type issues blocking automated testing and development
- ❌ **Integration Barriers**: Test execution blocked by import issues and model compatibility problems

**ECOSYSTEM USAGE**:

- **FLEXT Projects**: Quality analysis and validation for entire ecosystem Python codebases
- **CI/CD Integration**: Automated quality gates and reporting in build pipelines
- **Development Workflow**: Real-time quality feedback during development

**QUALITY STANDARDS**:

- **Type Safety**: Pyrefly strict mode compliance (currently blocked by import issues and model compatibility)
- **Test Coverage**: Comprehensive testing (currently blocked by import issues and integration failures)
- **FLEXT Integration**: Partial flext-core pattern adherence (BaseModel compatibility issues)
- **Code Quality**: Ruff linting and formatting compliance

---

## 🏗️ ARCHITECTURE

### Clean Architecture with Domain-Driven Design

**Design Philosophy**: Domain-first design with clean separation of concerns, following FLEXT ecosystem patterns with FlextResult[T] railway-oriented programming.

**Core Architecture**:

- **Domain Layer**: Quality business logic with entities, value objects, and domain services
- **Application Layer**: Use cases and application services orchestrating domain operations
- **Infrastructure Layer**: Analysis backends, external tools, and persistence
- **Presentation Layer**: CLI interface, web API, and report generation

### Module Organization

```
src/flext_quality/
├── api.py                      # FlextQuality facade (main entry point)
├── analyzer.py                 # FlextQualityAnalyzer (core analysis engine)
├── services.py                 # FlextQualityServices (service orchestration)
├── models.py                   # FlextQualityModels (ALL Pydantic models)
├── entities.py                 # Quality domain entities
├── value_objects.py            # Quality value objects
├── constants.py                # FlextQualityConstants (system constants)
├── config.py                   # FlextQualityConfig (configuration)
├── container.py                # Dependency injection container
├── exceptions.py               # FlextQualityExceptions (error hierarchy)
├── handlers.py                 # FlextQualityHandlers (event handlers)
├── integrations.py             # FlextQualityIntegrations (external systems)
├── metrics.py                  # Quality metrics calculation
├── grade_calculator.py         # QualityGradeCalculator (scoring system)
├── reports.py                  # FlextQualityReportGenerator (reporting)
├── cli.py                      # Command-line interface
├── web.py                      # Web interface (Django)
├── ports.py                    # Interface definitions
├── protocols.py                # Protocol definitions
├── typings.py                  # Type definitions
├── utilities.py                # Helper utilities
├── ast_backend.py              # AST analysis backend
├── external_backend.py         # External tool integration
├── base.py                     # Base classes and interfaces
└── tools/                      # Internal quality tools
    ├── architecture.py         # Architecture analysis tools
    ├── dependencies.py         # Dependency analysis tools
    ├── git.py                  # Git integration tools
    ├── optimizer_operations.py # Optimization operations
    ├── quality_operations.py   # Quality operations
    └── validation.py           # Validation tools
```

### Key Architectural Components

#### 1. Domain Layer (Business Logic)

```python
# Domain entities with business rules
from flext_quality.entities import (
    QualityProject,      # Project entity with validation
    QualityAnalysis,     # Analysis run entity
    QualityIssue,        # Quality issue entity
    QualityRule,         # Quality rule entity
    QualityReport,       # Quality report entity
)

# Value objects for immutable data
from flext_quality.value_objects import (
    QualityScore,        # Quality score value object
    ComplexityMetrics,   # Complexity measurement
    SecurityMetrics,     # Security assessment
)
```

#### 2. Application Layer (Use Cases)

```python
# Application services orchestrating domain operations
from flext_quality.services import FlextQualityServices

# Quality analysis service
service = FlextQualityServices()
result = service.analyze_project(project_path)
```

#### 3. Infrastructure Layer (Analysis Engine)

```python
# Analysis backends and external tool integration
from flext_quality.analyzer import FlextQualityAnalyzer
from flext_quality.ast_backend import FlextQualityASTBackend
from flext_quality.external_backend import FlextQualityExternalBackend

# Core analyzer with multiple backends
analyzer = FlextQualityAnalyzer(project_path)
result = analyzer.analyze_project()
```

#### 4. Quality Scoring and Grading

```python
# Quality grade calculation system
from flext_quality.grade_calculator import QualityGradeCalculator

calculator = QualityGradeCalculator()
grade_result = calculator.calculate_quality_grade(
    coverage_score=95.0,
    complexity_score=8.5,
    security_score=98.0,
    maintainability_score=87.0
)
```

### Railway-Oriented Programming (FLEXT Pattern)

All operations return `FlextResult[T]` for composable error handling:

```python
from flext_core import FlextResult
from flext_quality import FlextQualityAnalyzer

def analyze_project(project_path: str) -> FlextResult[QualityAnalysis]:
    """Analyze project with railway-oriented error handling."""
    analyzer = FlextQualityAnalyzer(project_path)

    return (
        analyzer.analyze_project()
        .flat_map(lambda result: validate_analysis(result))
        .map(lambda result: generate_report(result))
        .map_error(lambda error: log_analysis_error(error))
    )

# Safe usage
result = analyze_project("/path/to/project")
if result.is_success:
    analysis = result.unwrap()
    print(f"Quality score: {analysis.overall_score}")
else:
    print(f"Analysis failed: {result.error}")
```

---

## 🔧 DEVELOPMENT WORKFLOW

### Essential Commands

```bash
# Setup and installation
make setup                    # Complete development environment setup
make install                  # Install dependencies only
make install-dev              # Install with dev dependencies

# Quality gates (MANDATORY before commit)
make validate                 # Complete validation pipeline
make check                    # Quick validation (lint + type-check)
make lint                     # Ruff linting
make type-check               # Pyrefly type checking (currently blocked)
make security                 # Security scanning

# Testing (currently blocked by import issues)
make test                     # Full test suite with coverage
make test-unit                # Unit tests only
make test-integration         # Integration tests

# Quality analysis commands (when fixed)
make analyze                  # Run quality analysis
make quality-check            # Validate quality thresholds
make report                   # Generate quality reports

# Development utilities
make format                   # Auto-format code
make clean                    # Clean build artifacts
make diagnose                 # System diagnostics
```

### Running Specific Tests

```bash
# Basic tests (when import issues resolved)
PYTHONPATH=src poetry run pytest tests/unit/test_basic.py -v

# Test specific modules
PYTHONPATH=src poetry run pytest tests/unit/test_entities.py -v
PYTHONPATH=src poetry run pytest tests/unit/test_services.py -v

# Test with coverage
PYTHONPATH=src poetry run pytest --cov=flext_quality --cov-report=html

# Run integration tests
PYTHONPATH=src poetry run pytest -m integration -v
```

### Quality Gates Status

**Current Blockers**:
- ❌ **Import Issues**: FlextModels.BaseModel compatibility preventing module loading
- ❌ **Type Checking**: MyPy errors in external_backend.py and metrics.py (cannot run due to import failures)
- ❌ **Testing**: ImportError due to model integration issues preventing test execution
- ✅ **Linting**: Ruff passes with no violations
- ⚠️ **Security**: Bandit scanning functional but incomplete

**Resolution Priority**:
1. Fix flext-core integration issues (FlextModels.BaseModel compatibility)
2. Resolve import failures to enable module loading
3. Fix type errors once imports work
4. Enable test execution and validate coverage
5. Enhance integration with modern Python quality ecosystem

---

## 🚨 CRITICAL PATTERNS

### MANDATORY: FlextResult[T] Railway Pattern

**ALL operations that can fail MUST return FlextResult[T]**:

```python
from flext_core import FlextResult

# ✅ CORRECT - Railway pattern for all operations
def analyze_project(project_path: str) -> FlextResult[QualityAnalysis]:
    if not Path(project_path).exists():
        return FlextResult.fail("Project path does not exist")

    analyzer = FlextQualityAnalyzer(project_path)
    return analyzer.analyze_project()

# ❌ FORBIDDEN - Exception-based error handling
def analyze_project(project_path: str) -> QualityAnalysis:
    if not Path(project_path).exists():
        raise ValueError("Project path does not exist")  # DON'T DO THIS
    return analyzer.analyze_project()
```

### MANDATORY: FLEXT Import Patterns

```python
# ✅ CORRECT - Root-level flext-quality imports
from flext_quality import (
    CodeAnalyzer,              # Main analyzer (when fixed)
    QualityGradeCalculator,    # Scoring system
    FlextQualityServices,      # Service layer
)

# ❌ FORBIDDEN - Internal module imports
from flext_quality.analyzer import FlextQualityCodeAnalyzer  # DON'T DO THIS
```

### Domain Model Usage

```python
# Use unified Models namespace
from flext_quality import FlextQualityModels

# Access nested models
project = FlextQualityModels.ProjectModel(
    name="my_project",
    path="/path/to/project",
    config=FlextQualityModels.QualityConfig()
)

# Use entities
from flext_quality import FlextQualityEntities
analysis = FlextQualityEntities.QualityAnalysis.create(
    project_id=project.id,
    status=AnalysisStatus.QUEUED
)
```

### Configuration and Constants

```python
# Configuration singleton
from flext_quality import FlextQualityConfig
config = FlextQualityConfig()

# Constants access
from flext_quality import FlextQualityConstants
thresholds = FlextQualityConstants.QUALITY_THRESHOLDS
```

---

## 📊 CURRENT STATUS (v0.9.0)

### What Works

- **Domain Architecture**: Complete - Well-designed entities with FlextResult patterns
- **Service Layer**: Functional - Services with proper error handling and FlextLogger integration
- **Analysis Engine**: Implemented - AST analysis, complexity calculation, security checks (but blocked by imports)
- **Grade Calculator**: Complete - Comprehensive quality scoring and grading system
- **Report Generation**: Functional - Multiple format reporting capabilities
- **FLEXT Integration**: Partial - Uses flext-core patterns but has BaseModel compatibility issues
- **Code Quality**: Good - Ruff linting compliance, proper structure
- **Documentation**: Outdated - Implementation status indicators need synchronization

### Known Limitations

- **Import Issues**: FlextModels.BaseModel compatibility preventing module loading and accessibility
- **Type Safety**: MyPy errors cannot be assessed due to import failures preventing type checking
- **Testing**: Import errors blocking automated test execution and coverage measurement
- **Modern Integration**: Limited integration with 2025 Python quality ecosystem tools
- **CLI Integration**: Command-line interface blocked by import issues
- **Core Analyzer**: Functional but inaccessible due to model integration problems

### Documentation Status

**Assessment**: Documentation reflects outdated implementation status and needs synchronization with current codebase state.

**Current Issues**:
- Implementation status indicators across multiple files are inconsistent
- Status tables in README.md, docs/README.md, and docs/quick-start.md show different assessments
- Documentation claims certain functionalities are "working" but actual testing reveals import barriers
- No centralized documentation maintenance process

**Required Updates**:
- Synchronize status indicators across all documentation files
- Update implementation percentages based on actual functional testing
- Document current accessibility barriers and user experience limitations
- Add troubleshooting section for import issues in documentation
- Create clear distinction between "architecturally complete" vs "user-accessible"

#### Development Priorities

#### Phase 1: Critical Integration Fixes (Immediate)

1. **Fix Flext-Core Compatibility**
   - Resolve FlextModels.BaseModel compatibility issues in models.py
   - Fix model inheritance to use proper pydantic BaseModel
   - Ensure all modules can be imported without AttributeError

2. **Restore Module Accessibility**
   - Enable standard imports for core analyzer and services
   - Fix __init__.py exports to work with corrected models
   - Validate all main components are accessible via standard import patterns

3. **Resolve Quality Gates**
   - Fix MyPy type errors in external_backend.py and metrics.py once imports work
   - Enable test execution by resolving import failures
   - Validate quality standards compliance and coverage measurement

#### Phase 2: Modern Quality Ecosystem

1. **2025 Python Standards**
   - Integrate advanced Ruff capabilities
   - Add Semgrep security analysis
   - Implement modern static analysis patterns

2. **Performance and Scalability**
   - Optimize analysis performance for large codebases
   - Add concurrent analysis capabilities
   - Implement intelligent caching

#### Phase 3: Enterprise Features

1. **Advanced Reporting**
   - Executive summary generation
   - Trend analysis capabilities
   - Integration with enterprise dashboards

2. **CI/CD Integration**
   - Automated quality gates
   - Comprehensive reporting pipelines
   - Enterprise security validation

---

## 🧪 TESTING STRATEGY

### Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_analyzer.py     # FlextQualityAnalyzer tests
│   ├── test_entities.py     # Domain entity tests
│   ├── test_services.py     # Service layer tests
│   └── test_*.py           # Component-specific tests
├── integration/            # Integration tests
│   ├── test_api_integration.py  # Full API integration
│   └── test_backend_integration.py  # Backend integration
├── e2e/                    # End-to-end tests
│   └── test_full_workflow.py    # Complete analysis workflow
├── helpers/                # Test helpers and fixtures
│   ├── conftest.py         # Pytest configuration and fixtures
│   └── test_helpers.py     # Shared test utilities
└── validation/             # Quality validation tests
    └── test_quality_gates.py   # Quality gate validation
```

### Test Categories and Markers

```python
# Unit tests (fast, isolated)
@pytest.mark.unit
def test_quality_entity_creation():
    """Test domain entity creation and validation."""

# Integration tests (slower, with dependencies)
@pytest.mark.integration
def test_analyzer_with_ast_backend():
    """Test analyzer integration with AST backend."""

# End-to-end tests (slowest, full workflow)
@pytest.mark.e2e
def test_complete_analysis_workflow():
    """Test complete project analysis workflow."""

# Quality-specific tests
@pytest.mark.quality
def test_quality_scoring_accuracy():
    """Test quality scoring calculation accuracy."""
```

### Test Fixtures

Common fixtures available in all tests:

```python
# Service fixtures
flext_quality_analyzer        # FlextQualityAnalyzer instance
flext_quality_services        # FlextQualityServices instance
flext_quality_config          # FlextQualityConfig instance

# Data fixtures
sample_project_data           # Sample project configuration
sample_analysis_results       # Sample analysis results
sample_quality_metrics        # Sample quality metrics

# Utility fixtures
temp_project_dir              # Temporary project directory
mock_external_tools           # Mock external tool responses
clean_flext_container         # Fresh FlextContainer state
```

### Running Tests (When Import Issues Resolved)

```bash
# All tests with coverage
PYTHONPATH=src poetry run pytest --cov=flext_quality --cov-report=html

# Unit tests only
PYTHONPATH=src poetry run pytest -m unit -v

# Integration tests
PYTHONPATH=src poetry run pytest -m integration -v

# Specific test file
PYTHONPATH=src poetry run pytest tests/unit/test_analyzer.py -v

# Test with debugging
PYTHONPATH=src poetry run pytest tests/unit/test_analyzer.py::TestAnalyzer::test_analysis -xvs
```

---

## 🔍 TROUBLESHOOTING

### Import Errors

**Symptom**: `AttributeError: type object 'FlextModels' has no attribute 'BaseModel'` when importing flext_quality

**Root Cause**: Models.py attempts to inherit from FlextModels.BaseModel which doesn't exist in flext-core

**Current Workaround**:
```bash
# Use direct analyzer import (bypasses models.py)
export PYTHONPATH=src
python -c "from flext_quality.analyzer import FlextQualityAnalyzer; print('Direct import successful')"

# Core analyzer is functional but not accessible via standard imports
python -c "from flext_quality import CodeAnalyzer; print('Standard import fails')"
```

**Resolution Required**: Fix model inheritance in models.py to use pydantic BaseModel directly

### Type Checking Errors

**Symptom**: Cannot run type checking due to import failures

**Current Issues**:
- Type checking blocked by FlextModels.BaseModel compatibility issues
- `external_backend.py` and `metrics.py` have reported type errors but cannot be validated
- Import failures prevent MyPy/Pyrefly execution

**Resolution Steps** (After Import Fix):
```bash
# These commands will work once import issues are resolved
PYTHONPATH=src poetry run pyrefly check src/flext_quality/external_backend.py
PYTHONPATH=src poetry run pyrefly check src/flext_quality/metrics.py

# Focus on error codes
PYTHONPATH=src poetry run pyrefly check . --show-error-codes | grep "error-code"
```

### Test Execution Failures

**Symptom**: Tests fail with AttributeError due to FlextModels.BaseModel

**Root Cause**: Model compatibility issues preventing module imports, blocking all test execution

**Current Status**:
```bash
# All test execution blocked by import failures
PYTHONPATH=src poetry run pytest tests/ -v  # AttributeError on import

# Cannot run any tests until model compatibility is fixed
# Core analyzer exists and is functional but inaccessible via imports
```

### Flext-Core Integration Issues

**Symptom**: AttributeError: type object 'FlextModels' has no attribute 'BaseModel'

**Root Cause**: flext_quality models.py incorrectly assumes FlextModels.BaseModel exists, but flext-core doesn't provide this

**Technical Details**:
```python
# What flext_quality/models.py incorrectly tries to do:
class ProjectModel(FlextModels.BaseModel):  # ❌ FlextModels.BaseModel doesn't exist
    pass

# What should be done:
from pydantic import BaseModel
class ProjectModel(BaseModel):  # ✅ Use pydantic BaseModel directly
    pass
```

**Resolution Required**: Update all model classes in models.py to inherit from pydantic BaseModel instead of FlextModels.BaseModel

### CLI Command Issues

**Symptom**: CLI commands fail with import errors

**Root Cause**: Model compatibility issues prevent CLI module loading, blocking flext-cli integration

**Current Status**:
```bash
# CLI completely blocked by import failures
flext-quality analyze  # AttributeError on module import

# Workaround: Direct analyzer usage (when imports are fixed)
PYTHONPATH=src python -c "
from flext_quality.analyzer import FlextQualityAnalyzer
analyzer = FlextQualityAnalyzer('.')
result = analyzer.analyze_project()
print(f'Quality Score: {analyzer.get_quality_score()}')
"
```

### Quality Analysis Performance

**Symptom**: Analysis runs slowly on large codebases

**Optimizations**:
```python
# Use selective analysis for large projects
analyzer = FlextQualityAnalyzer(large_project_path)
result = analyzer.analyze_project(
    include_complexity=True,    # Enable complexity analysis
    include_security=False,     # Skip security for faster runs
    max_files=1000             # Limit file count
)
```

---

## 📚 PATTERNS AND BEST PRACTICES

### Complete Quality Analysis Workflow

```python
from pathlib import Path
from flext_core import FlextResult
from flext_quality.analyzer import FlextQualityAnalyzer
from flext_quality.grade_calculator import QualityGradeCalculator
from flext_quality.reports import FlextQualityReportGenerator

def complete_quality_analysis(project_path: str) -> FlextResult[dict]:
    """Complete quality analysis workflow following FLEXT patterns."""

    # Initialize analyzer
    analyzer = FlextQualityAnalyzer(project_path)

    # Execute analysis with all backends
    analysis_result = analyzer.analyze_project(
        include_security=True,
        include_complexity=True,
        include_dead_code=True,
        include_duplicates=True
    )

    if analysis_result.is_failure:
        return FlextResult.fail(f"Analysis failed: {analysis_result.error}")

    analysis = analysis_result.value

    # Calculate quality grade
    grade_calculator = QualityGradeCalculator()
    grade_result = grade_calculator.calculate_quality_grade(
        coverage_score=analysis.coverage_score,
        complexity_score=analysis.complexity_score,
        security_score=analysis.security_score,
        maintainability_score=analysis.maintainability_score
    )

    if grade_result.is_failure:
        return FlextResult.fail(f"Grade calculation failed: {grade_result.error}")

    # Generate comprehensive report
    report_generator = FlextQualityReportGenerator()
    report_result = report_generator.generate_report(
        quality_analysis=analysis,
        config={"format": "html", "include_trend_analysis": True}
    )

    if report_result.is_failure:
        return FlextResult.fail(f"Report generation failed: {report_result.error}")

    return FlextResult.ok({
        "analysis": analysis,
        "grade": grade_result.value,
        "report": report_result.value
    })

# Usage
result = complete_quality_analysis("/path/to/project")
if result.is_success:
    data = result.unwrap()
    print(f"Quality Grade: {data['grade'].overall_grade}")
    print(f"Report saved: {data['report'].file_path}")
```

### Custom Quality Rules

```python
from flext_quality.entities import QualityRule
from flext_quality.services import FlextQualityServices

# Define custom quality rule
custom_rule = QualityRule(
    name="custom_complexity_rule",
    description="Custom complexity threshold for business logic",
    rule_type="complexity",
    threshold=8.0,
    severity="medium",
    enabled=True
)

# Apply custom rule to analysis
services = FlextQualityServices()
result = services.apply_custom_rules(
    project_path="/path/to/project",
    custom_rules=[custom_rule]
)
```

### Integration with CI/CD Pipeline

```python
# ci_cd_integration.py
from pathlib import Path
from flext_quality.analyzer import FlextQualityAnalyzer
from flext_quality.services import FlextQualityServices

def quality_gate_check(project_path: str, min_score: float = 80.0) -> int:
    """Quality gate check for CI/CD pipelines."""

    analyzer = FlextQualityAnalyzer(project_path)
    services = FlextQualityServices()

    # Run comprehensive analysis
    analysis_result = services.analyze_project_comprehensive(project_path)
    if analysis_result.is_failure:
        print(f"❌ Analysis failed: {analysis_result.error}")
        return 1

    analysis = analysis_result.value

    # Check quality thresholds
    if analysis.overall_score < min_score:
        print(f"❌ Quality score {analysis.overall_score:.1f} below threshold {min_score}")
        return 1

    # Generate CI report
    report_result = services.generate_ci_report(analysis)
    if report_result.is_success:
        print(f"✅ Quality report generated: {report_result.value}")

    print(f"✅ Quality gate passed with score {analysis.overall_score:.1f}")
    return 0

# Usage in CI/CD
if __name__ == "__main__":
    exit(quality_gate_check(".", min_score=85.0))
```

---

## 🤝 CONTRIBUTING

### FLEXT-Core Compliance Checklist

Before contributing, ensure code follows FLEXT patterns:

- [ ] All operations return FlextResult[T] for type-safe error handling
- [ ] Use FlextContainer.get_global() for dependency injection
- [ ] Follow single unified class per module pattern
- [ ] Use FlextModels for domain entities
- [ ] Complete type annotations with Python 3.13+ features

### Quality Standards

- **Type Safety**: Zero MyPy errors in strict mode (currently blocked)
- **Testing**: Unit and integration tests (currently blocked by import issues)
- **Code Style**: Ruff formatting with 88-character line limit
- **Security**: Zero Bandit security issues
- **FLEXT Integration**: Complete flext-core compliance

### Current Contribution Priorities

1. **Fix Import Accessibility**
   - Resolve CodeAnalyzer import issues
   - Ensure all main components are properly exported
   - Fix flext-core integration problems

2. **Resolve Quality Gates**
   - Fix MyPy type errors in external_backend.py and metrics.py
   - Enable test execution and coverage measurement
   - Validate against FLEXT quality standards

3. **Enhance Modern Integration**
   - Complete external backend implementations (mypy, bandit)
   - Add proper error handling for missing tools
   - Integrate with 2025 Python quality ecosystem

4. **Documentation Accuracy**
   - Update all documentation to reflect actual capabilities
   - Remove exaggerated claims and ensure professional accuracy
   - Align with FLEXT documentation standards

---

**FLEXT Quality v0.9.0** - Code quality analysis library with solid domain architecture requiring accessibility improvements for full FLEXT ecosystem integration.

**Purpose**: Provide comprehensive code quality analysis, metrics collection, and automated quality assurance for FLEXT projects with proper domain-driven design patterns.

**Mission**: Enable automated quality assessment, scoring, and reporting across the FLEXT ecosystem with enterprise-grade reliability and integration.

---
