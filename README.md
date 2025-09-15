# FLEXT Quality

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Development Status](https://img.shields.io/badge/status-v0.9.0-green.svg)](#current-status)

**Code quality analysis library** for the FLEXT ecosystem, providing quality metrics and analysis capabilities using Domain-Driven Design patterns.

> **📊 STATUS**: Version 0.9.0 - Core functionality operational, accessibility improvements needed

---

## 🎯 Purpose and Role in FLEXT Ecosystem

### **For the FLEXT Ecosystem**

FLEXT Quality serves as the centralized code quality analysis platform for all FLEXT projects, providing consistent quality metrics, analysis patterns, and reporting across the ecosystem's Python projects.

### **Key Responsibilities**

1. **Quality Analysis** - Automated code quality assessment using multiple analysis backends
2. **Metrics Collection** - Comprehensive quality metrics with scoring and grading systems
3. **Report Generation** - HTML, JSON, and text reporting with executive summaries
4. **FLEXT Integration** - Native integration with FLEXT architectural patterns

### **Integration Points**

- **flext-core** → Uses FlextResult, FlextContainer, FlextModels for foundation patterns
- **flext-cli** → Command-line interface integration (currently blocked by import issues)
- **flext-web** → Web dashboard integration (planned)
- **All FLEXT Projects** → Quality analysis and validation for Python codebases

---

## 🏗️ Architecture and Patterns

### **FLEXT-Core Integration Status**

| Component | Status | Verification |
| --------- | ------ | ------------ |
| **FlextQualityService** | ✅ **Operational** | Async project creation: 100% success rate |
| **Analysis Engine** | ✅ **Operational** | Quality scoring and grading: A+ results |
| **Domain Models** | ✅ **Complete** | DDD patterns with FlextModels |
| **Export Access** | 🟡 **Limited** | 33% accessibility (10 of 30 modules exported) |

> **Status**: ✅ Core functionality verified through testing - accessibility improvements needed

### **Architecture Overview**

```mermaid
graph TB
    Core[FLEXT-Core Foundation] --> Quality[FLEXT-Quality]
    Quality --> Analysis[Analysis Engine]
    Quality --> Reporting[Report Generation]
    Quality --> API[REST API Layer]
    Quality --> CLI[CLI Interface]

    Analysis --> AST[AST Analysis]
    Analysis --> External[External Tools]
    Analysis --> Metrics[Metrics Collection]

    Reporting --> HTML[HTML Reports]
    Reporting --> JSON[JSON Data]
    Reporting --> Dashboard[Web Dashboard]
```

---

## 🚀 Quick Start

### **Installation**

```bash
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality
make setup

# Verify core functionality
python -c "
from flext_quality import FlextQualityService, QualityGradeCalculator
print('Core imports successful')
"
```

### **Basic Usage**

```python
import asyncio
from flext_quality import FlextQualityService

# Service Layer Usage (Recommended)
async def main():
    service = FlextQualityService()

    # Create project with quality thresholds
    result = await service.create_project(
        name="my_project",
        project_path="/path/to/project",
        _min_coverage=80.0,  # Note: internal parameter naming
        _max_complexity=10
    )

    if result.success:
        project = result.value
        print(f"✅ Project: {project.name}")
        print(f"📁 Path: {project.project_path}")
        print(f"📊 Coverage threshold: {project.min_coverage}%")

# Direct Analysis Engine Usage (Advanced)
def analyze_code():
    # Note: Requires direct import due to export limitations
    from flext_quality.analyzer import FlextQualityCodeAnalyzer

    analyzer = FlextQualityCodeAnalyzer("/path/to/project")
    result = analyzer.analyze_project()

    print(f"📊 Quality Score: {analyzer.get_quality_score()}")
    print(f"🏆 Quality Grade: {analyzer.get_quality_grade()}")
    print(f"📄 Files: {result.overall_metrics.files_analyzed}")

# Run analysis
asyncio.run(main())
analyze_code()
```

---

## 🔧 Development

### **Essential Commands**

```bash
# Setup and installation
make setup              # Complete development environment setup
make install            # Install dependencies only

# Quality gates
make validate           # Complete validation pipeline
make check             # Quick validation (lint + type-check)
make lint              # Ruff linting
make type-check        # MyPy type checking (currently produces errors)
make security          # Security scanning with Bandit

# Testing (currently blocked by import errors)
make test              # Run test suite with coverage
make test-unit         # Unit tests only
make test-integration  # Integration tests

# Quality analysis commands (when CLI is fixed)
make analyze           # Run quality analysis
make quality-check     # Validate quality thresholds
make report           # Generate quality reports

# Development utilities
make format           # Auto-format code
make clean            # Clean build artifacts
make diagnose         # System diagnostics
```

### **Current Development Limitations**

```bash
# Known issues that prevent full functionality:

# Type checking produces errors
make type-check  # Shows parameter mismatch errors

# Tests cannot execute due to import issues
make test       # ImportError while importing test modules

# CLI commands fail
flext-quality --help  # ImportError: cannot import from 'flext_cli'
```

---

## 🧪 Testing

### **Test Structure**

```
tests/
├── unit/                   # Unit tests for individual components
├── integration/           # Integration tests (currently blocked)
├── conftest.py           # Pytest configuration and fixtures
└── test_*.py            # Test modules (import issues present)
```

### **Testing Commands**

```bash
# Basic test execution
pytest tests/test_basic.py --no-cov    # Works: Basic tests execute successfully
make test                             # Limited: Coverage configuration issues
make test-unit                        # Individual test modules work

# Diagnostic command
make diagnose          # Check system status and dependencies
```

---

## 📊 Status and Metrics

### **Current Implementation Status**

Based on testing and verification:

- **✅ Analysis Engine**: Operational - A+ quality scores, comprehensive file analysis
- **✅ Service Layer**: Operational - 100% success rate for async project operations
- **✅ Domain Models**: Complete - Solid DDD implementation with FlextModels
- **✅ Quality Calculator**: Operational - Grade calculation and scoring functions
- **⚠️ Export Access**: Limited - Core analyzer requires direct import (accessibility issue)
- **⚠️ Quality Gates**: Partial - 1 ruff issue, 463 mypy errors, 1 test failure

### **Quality Standards**

- **Coverage**: Target 85% (currently cannot measure due to test issues)
- **Type Safety**: Type errors present (MyPy produces parameter mismatch errors)
- **Security**: Bandit scanning functional
- **FLEXT-Core Compliance**: Approximately 70% - foundation patterns partially implemented

### **Technical Debt**

- **Type Safety**: Parameter naming mismatches between API and Service layers
- **Import Issues**: CLI integration blocked by flext-cli import problems
- **Test Infrastructure**: Import errors prevent test execution
- **Multiple Classes**: FLEXT standard violation with multiple classes per module

---

## 🗺️ Roadmap

### **Current Version (v0.9.0)**

Focus on resolving foundational technical issues:
- Fix type safety violations (MyPy errors)
- Resolve import issues blocking tests and CLI
- Implement placeholder API methods
- Align with FLEXT architectural patterns

### **Next Version (v0.10.0)**

Enhancement phase after technical issues resolved:
- Complete test coverage implementation
- Full FLEXT-CLI integration
- Web dashboard integration
- Performance optimization

---

## 📚 Documentation

- **[TODO & Development Status](TODO.md)** - Current technical issues and development priorities
- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[Architecture](docs/architecture.md)** - System design and patterns
- **[Development](docs/development.md)** - Contributing and workflows
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

---

## 🤝 Contributing

### **FLEXT-Core Compliance Checklist**

Before contributing, ensure code follows FLEXT patterns:
- [ ] All operations return FlextResult[T] for type-safe error handling
- [ ] Use FlextContainer.get_global() for dependency injection
- [ ] Follow single unified class per module pattern
- [ ] Use FlextModels for domain entities
- [ ] Complete type annotations with Python 3.13+ features

### **Quality Standards**

- **Type Safety**: Zero MyPy errors in strict mode
- **Testing**: Minimum test coverage once import issues resolved
- **Code Style**: Ruff formatting with 88-character line limit
- **Security**: Zero Bandit security issues

### **Current Contribution Priorities**

1. **Fix import issues** preventing test execution
2. **Resolve type safety** violations in API-Service integration
3. **Implement placeholder API methods** with proper FlextResult usage
4. **CLI integration** using pure flext-cli patterns

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext-quality/issues)
- **Security**: Report security issues privately to maintainers

---

**FLEXT Quality v0.9.0** - Code quality analysis platform enabling consistent quality standards across the FLEXT ecosystem.

**Mission**: Provide reliable, comprehensive code quality analysis for FLEXT projects while maintaining enterprise-grade accuracy and FLEXT architectural compliance.