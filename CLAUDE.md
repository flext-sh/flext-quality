# flext-quality - FLEXT Data Integration

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-28

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
- ✅ Dead code detection (Vulture)
- ✅ Modernization suggestions (Refurb)
- ✅ Cognitive complexity analysis (Complexipy)
- ✅ AST-based refactoring suggestions (Rope)

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

# Extended quality tools
make dead-code                # Vulture dead code detection
make modernize                # Refurb modernization suggestions
make cognitive-complexity     # Complexipy cognitive complexity
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

### Extended Quality Analysis

```python
from flext_quality import FlextQuality

quality = FlextQuality()

# Dead code detection
result = quality.detect_dead_code("path/to/file.py")

# Modernization suggestions (Refurb)
result = quality.check_modernization("path/to/file.py")

# Cognitive complexity analysis
result = quality.check_cognitive_complexity("path/to/file.py", max_complexity=15)

# Refactoring suggestions (Rope)
result = quality.get_refactoring_suggestions("path/to/file.py")
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

**See Also**:

- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-observability Patterns](../flext-observability/CLAUDE.md)
