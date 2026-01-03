# flext-quality - FLEXT Quality Analysis Framework

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2026-01-03

---

## Project Overview

**FLEXT-Quality** provides comprehensive code quality analysis, validation, and metrics collection for the FLEXT ecosystem. It integrates with flext-cli for consistent CLI output and provides both programmatic and command-line interfaces for quality assessment across Python projects.

**Version**: 1.0.0
**Status**: Production-ready
**Python**: 3.13+
**Architecture**: FLEXT-compliant with FlextResult[T] railway-oriented error handling

**CURRENT CAPABILITIES**:

- ✅ CLI service with flext-cli integration (status, check, validate commands)
- ✅ Code quality analysis (ruff linting, basedpyright type checking)
- ✅ Security validation (bandit scanning)
- ✅ Test coverage analysis (pytest with coverage reporting)
- ✅ MCP tools for claude-mem and claude-context integration
- ✅ YAML rules engine for custom validation
- ✅ Hook-based extensibility system
- ✅ Command-based execution strategy with quality thresholds
- ✅ Dead code detection (Vulture)
- ✅ Modernization suggestions (Refurb)
- ✅ Cognitive complexity analysis (Complexipy)
- ✅ AST-based refactoring suggestions (Rope)

---

## Essential Commands

### Development Workflow

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Basedpyright type checking
make security                 # Bandit security scan
make test                     # Run tests (96% coverage)
```

### CLI Usage

```bash
# Display service status
flext-quality                 # Show status (no args defaults to status)
flext-quality status          # Explicitly show service status

# Quick quality check (lint + type)
flext-quality check [path]    # Run ruff + basedpyright (default: current dir)
flext-quality check /path/to/project

# Full validation (lint + type + security + tests)
flext-quality validate [path] [--min-coverage N]
flext-quality validate /path/to/project --min-coverage 85
```

### Extended Quality Tools

```bash
# Quality analysis
make quality-analysis         # Run quality analysis
make quality-report           # Generate quality report

# Extended quality tools
make dead-code                # Vulture dead code detection
make modernize                # Refurb modernization suggestions
make cognitive-complexity     # Complexipy cognitive complexity
```

---

## Architecture

### CLI Service Architecture

The flext-quality CLI is built on FLEXT patterns with three layers:

1. **Public Interface** (`FlextQualityCliService`):
   - `display_status()` - Returns service status
   - `build_check_commands(path)` - Builds ruff + basedpyright commands
   - `build_validate_commands(path, min_coverage)` - Builds full validation command set

2. **Command Handlers** (`_CommandHandlers` - private):
   - `handle_status()` - Process status command
   - `handle_check()` - Process check command
   - `handle_validate()` - Process validate command

3. **Routing** (`_dispatch` - private):
   - Routes commands to appropriate handlers
   - Handles unknown commands

4. **Entry Point** (`main()`):
   - Parses sys.argv
   - Initializes service
   - Routes to appropriate command

**Integration with flext-cli**:
- Uses `FlextCliOutput` for consistent formatting
- Provides `print_success()`, `print_error()`, `print_message()`, `print_warning()`
- Output service handles styling, colors, and formatting

**Delegation Model**:
- CLI builds command lists (doesn't execute)
- Delegates execution to `FlextQualityCodeExecutionBridge`
- Maintains security boundaries between CLI and execution

### Project Structure

```
flext-quality/
├── src/flext_quality/
│   ├── api.py                    # Public facade
│   ├── constants.py              # Constants (Tier 0)
│   ├── models.py                 # Pydantic models (Tier 1)
│   ├── protocols.py              # Interfaces (Tier 0)
│   ├── typings.py                # Type definitions (Tier 0)
│   ├── utilities.py              # Helpers (Tier 1)
│   ├── integrations/             # External integrations
│   │   ├── code_execution.py     # Command builder
│   │   ├── claude_context.py     # Claude context integration
│   │   ├── claude_mem.py         # Claude memory integration
│   │   └── mcp_client.py         # MCP client base
│   ├── mcp/                      # MCP server and tools
│   │   ├── server.py             # MCP server setup
│   │   └── tools.py              # MCP tools
│   ├── rules/                    # YAML rules engine
│   │   └── engine.py             # Rules validation
│   ├── hooks/                    # Hook system
│   │   └── manager.py            # Hook manager
│   └── services/                 # Services (Tier 3)
│       ├── cli.py                # CLI service
│       ├── core.py               # Core service
│       └── health.py             # Health checks
├── tests/
│   ├── unit/                     # Unit tests
│   └── integration/              # Integration tests
├── CLAUDE.md                     # This file
└── README.md                     # User documentation
```

## Key Patterns

### CLI Service Usage

```python
from flext_quality.services.cli import FlextQualityCliService

# Initialize service
service = FlextQualityCliService()

# Get status
status_result = service.display_status()
if status_result.is_success:
    print(status_result.value)

# Build check commands (ruff + basedpyright)
check_result = service.build_check_commands(Path("/path/to/project"))
if check_result.is_success:
    for cmd in check_result.value:
        print(" ".join(cmd))

# Build validate commands (ruff + type + bandit + pytest)
validate_result = service.build_validate_commands(
    Path("/path/to/project"),
    min_coverage=80
)
if validate_result.is_success:
    for cmd in validate_result.value:
        print(" ".join(cmd))
```

### Quality Analysis (FlextQuality API)

```python
from flext_core import FlextResult as r
from flext_quality import FlextQuality

quality = FlextQuality()

# Analyze project quality
result = quality.analyze_project("path/to/project")
if result.is_success:
    metrics = result.value
    print(f"Quality score: {metrics.score}")
elif result.is_failure:
    print(f"Error: {result.error}")
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

## Testing

### Test Coverage

Current coverage: **96%** (near production-ready, project target: 100%)

```bash
# Run all tests
make test

# Run tests with coverage report
PYTHONPATH=src poetry run pytest -q --cov=flext_quality --cov-report=term-missing --cov-fail-under=90

# Run specific test class
PYTHONPATH=src poetry run pytest tests/unit/test_cli.py::TestFlextQualityCliService -v

# Run tests matching pattern
PYTHONPATH=src poetry run pytest tests/ -k "cli" -v
```

### Test Organization

- **Unit Tests** (`tests/unit/`): Test public API with real objects, no mocks
- **Integration Tests** (`tests/integration/`): Test with real dependencies
- **E2E Tests**: CLI commands tested via `pytest.raises(SystemExit)`

### Testing Patterns

```python
# Test public API only (CLI service)
def test_build_check_commands_returns_commands(self, tmp_path: Path) -> None:
    """Test build_check_commands returns list of commands."""
    service = FlextQualityCliService()
    result = service.build_check_commands(tmp_path)
    assert result.is_success
    assert isinstance(result.value, list)
    assert len(result.value) == 2

# Test CLI entry point with SystemExit
def test_main_with_status_command_exits_zero(self) -> None:
    """Test main with status command exits with code 0."""
    sys.argv = ["flext-quality", "status"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
```

### Test Categories

- **TestFlextQualityCliService**: Public service methods (8 tests)
- **TestMainFunction**: CLI entry point with SystemExit (5 tests)

Total: 13 CLI tests + 237 other tests = 250 passing tests

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:

- ❌ Exception-based error handling → Use `FlextResult[T]`
- ❌ Type ignores (`# type: ignore`)
- ❌ `Any` types → Use `Protocol` or proper types
- ❌ `cast()` function → Use proper type definitions
- ❌ `TYPE_CHECKING` blocks → Circular imports are design issues
- ❌ Mocking implementation details (private functions)
- ❌ Importing private functions (`_function`)

**MANDATORY**:

- ✅ Use `FlextResult[T]` for all error handling
- ✅ Complete type annotations on public APIs
- ✅ Zero Ruff violations
- ✅ Zero Pyrefly type errors
- ✅ Test only public interfaces
- ✅ Use dependency injection for testability
- ✅ Railway-oriented error handling patterns

### FLEXT Architecture Rules

**Tier-based Import Rules**:
```
Tier 0 (Foundation): constants.py, typings.py, protocols.py
                     → No imports from other tiers
Tier 1 (Domain):     models.py, utilities.py
                     → Can only import from Tier 0
Tier 2 (Infra):      services/*.py
                     → Can import from Tier 0-1
Tier 3 (App):        api.py, CLI, MCP tools
                     → Can import from any tier
```

**Namespace Rules**:
```python
# MANDATORY: Use short aliases for imports
from flext_core import FlextResult as r
from flext_core import FlextConstants as c
from flext_core import FlextModels as m
from flext_core import FlextProtocols as p
from flext_core import FlextTypings as t
from flext_core import FlextUtilities as u

# MANDATORY: Use full namespace paths
timeout = c.Quality.Defaults.TIMEOUT
entry = m.Quality.Entry(...)
```

---

## Related Documentation

**FLEXT Ecosystem**:
- [Workspace Standards](../CLAUDE.md) - FLEXT architecture and patterns
- [flext-core Patterns](../flext-core/CLAUDE.md) - FlextResult, Ops, Protocols
- [flext-cli Integration](../flext-cli/CLAUDE.md) - Output service patterns

**Quality Tools**:
- [README.md](./README.md) - User-facing documentation
- [pyproject.toml](./pyproject.toml) - Dependencies and configuration
- [Makefile](./Makefile) - Development commands
