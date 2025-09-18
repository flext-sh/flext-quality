# FLEXT-Quality Code Style and Conventions

## Code Style Standards

### Python Version & Features

- **Python 3.13+** required
- Modern Python features enabled (pattern matching, union syntax, etc.)
- Type annotations mandatory for all functions and methods

### FLEXT Architectural Patterns (MANDATORY)

#### 1. Unified Class Pattern

- **SINGLE class per module** (current violations found in multiple files)
- Use nested helper classes instead of multiple top-level classes
- Example violation: `analyzer.py` has both `FlextQualityCodeAnalyzer` and `CodeAnalyzer`

#### 2. FlextResult Pattern (MANDATORY)

- ALL operations return `FlextResult[T]` for type-safe error handling
- Use `.is_failure`, `.is_success`, `.value`, `.error` for access
- NO try/except fallbacks - explicit error checking only
- Current code has extensive try/except usage that may need refactoring

#### 3. Import Strategy (ROOT-LEVEL ONLY)

```python
# ✅ CORRECT
from flext_core import FlextResult, FlextLogger, FlextContainer
from flext_cli import FlextCliApi, FlextCliMain  # CLI projects only

# ❌ FORBIDDEN
from flext_core.result import FlextResult  # Internal imports
import click  # Direct CLI imports (GOOD: not found in codebase)
```

#### 4. CLI Implementation (ZERO TOLERANCE)

- **MANDATORY**: Use flext-cli exclusively for ALL CLI operations
- **FORBIDDEN**: Direct click, rich, or any Rich components
- ✅ Current status: No violations found - code properly uses flext-cli

### Type Safety Requirements

- **MyPy strict mode**: Enabled in pyproject.toml
- **Zero type errors** tolerance in source code
- Complete type annotations required
- Pydantic models for all domain entities

### Error Handling Patterns

- Use FlextResult[T] for all operations that can fail
- Explicit error checking via `.is_failure` checks
- NO silent error suppression
- Comprehensive logging via FlextLogger

### Domain-Driven Design Patterns

- **Entities**: FlextQualityProject, FlextQualityAnalysis, FlextQualityIssue
- **Value Objects**: QualityScore, QualityGrade, ComplexityMetric
- **Services**: Application services for business logic
- **Domain Events**: For cross-boundary communication

### Code Organization

- Clean Architecture layer separation
- Domain layer isolated from infrastructure concerns
- Service layer orchestrates business operations
- Infrastructure layer handles external integrations

## Quality Requirements

- **90% test coverage minimum**
- **Zero security vulnerabilities** (Bandit + pip-audit)
- **Ruff formatting** with 88-character line limit
- **Pre-commit hooks** for automated quality checks
