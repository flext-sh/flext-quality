# FLEXT-Quality Project Guidelines

**Reference**: See [../CLAUDE.md](../CLAUDE.md) for FLEXT ecosystem standards and general rules.

---

## Project Overview

**FLEXT-Quality** provides comprehensive code quality analysis and metrics collection for the FLEXT ecosystem, enabling automated quality assessment, scoring, and reporting across Python projects.

**Version**: 0.9.0  
**Status**: Production-ready  
**Python**: 3.13+

**CURRENT CAPABILITIES**:
- ✅ Code quality analysis and metrics
- ✅ Automated quality assessment
- ✅ Quality scoring and reporting
- ✅ Integration with FLEXT ecosystem tools

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests

# Quality analysis
make quality-analysis         # Run quality analysis
make quality-report           # Generate quality report
```

---

## Key Patterns

### Quality Analysis

```python
from flext_core import FlextResult
from flext_quality import FlextQuality

quality = FlextQuality()

# Analyze project quality
result = quality.analyze_project("path/to/project")
if result.is_success:
    metrics = result.unwrap()
    print(f"Quality score: {metrics.score}")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ Real fixtures in tests

---

**Additional Resources**: [../CLAUDE.md](../CLAUDE.md) (workspace), [README.md](README.md) (overview)
