# FLEXT Quality Plugin Architecture Plan

<!-- TOC START -->
- [Current State](#current-state)
- [MCP Python Refactoring Integration](#mcp-python-refactoring-integration)
- [Integration Points](#integration-points)
  - [1. Hook-Based Integration (Implemented)](#1-hook-based-integration-implemented)
  - [2. Makefile Targets (Implemented)](#2-makefile-targets-implemented)
  - [3. MCP Server Access (Available)](#3-mcp-server-access-available)
  - [4. Future: Plugin Interface](#4-future-plugin-interface)
  - [5. Baseline Management](#5-baseline-management)
- [Architecture Diagram](#architecture-diagram)
- [Summary](#summary)
<!-- TOC END -->

## Current State

flext-quality already integrates:

- **Ruff** - Fast Python linter (via subprocess)
- **Mypy** - Static type checker (via library API)
- **Vulture** - Dead code detection (via library import)
- **Bandit** - Security scanner (via library API)
- **Radon** - Complexity metrics (via library import)
- **Black** - Code formatter (via library import)
- **Coverage** - Test coverage (via library import)
- **Pytest** - Test runner (via library import)

## MCP Python Refactoring Integration

The MCP project at `~/mcp-python-refactoring` provides additional analyzers:

- **Rope** - AST-based refactoring
- **Refurb** - Modern pattern suggestions
- **Complexipy** - Cognitive complexity
- **LibCST** - Syntax tree manipulation
- **Jedi** - Semantic analysis

## Integration Points

### 1. Hook-Based Integration (Implemented)

Hooks in `~/.claude/hooks/` use CLI tools directly:

- `05-dead-code-detector.sh` - Vulture with baseline tracking
- `06-modernization-advisor.sh` - Refurb for suggestions

### 2. Makefile Targets (Implemented)

Added to `~/flext/base.mk`:

```makefile
dead-code: ## Dead code detection (Vulture)
modernize: ## Modern patterns suggestions (Refurb)
cognitive-complexity: ## Cognitive complexity (Complexipy)
validate-full: ## Full validation including dead code
```

### 3. MCP Server Access (Available)

The MCP server provides tools via Claude Code:

- `analyze_python_code` - Comprehensive analysis
- `extract_function` - Guided refactoring
- `quick_analyze` - Fast function/complexity check

### 4. Future: Plugin Interface

Planned plugin interface for flext-quality:

```python
from typing import Protocol
from flext_core import FlextResult

class QualityPlugin(Protocol):
    """Plugin interface for quality analyzers."""

    @property
    def name(self) -> str:
        """Plugin name."""
        ...

    @property
    def description(self) -> str:
        """Plugin description."""
        ...

    def analyze(
        self,
        path: Path,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[AnalysisResult]:
        """Run analysis on path."""
        ...

    def supports_fix(self) -> bool:
        """Whether plugin can auto-fix issues."""
        ...

    def fix(
        self,
        path: Path,
        issues: list[Issue],
    ) -> FlextResult[FixResult]:
        """Apply fixes for issues."""
        ...
```

### 5. Baseline Management

Baseline tracking for dead code:

- File: `~/flext/.dead-code-baseline`
- Generator: `~/flext/scripts/create-dead-code-baseline.sh`
- Hook auto-updates on retry

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Hooks                        │
├─────────────────────────────────────────────────────────────┤
│  05-dead-code-detector.sh    06-modernization-advisor.sh   │
│         (blocking)                  (advisory)              │
└────────────────┬──────────────────────────┬─────────────────┘
                 │                          │
                 ▼                          ▼
┌────────────────────────┐    ┌───────────────────────────────┐
│   Vulture (dead code)  │    │    Refurb (modern patterns)   │
└────────────────────────┘    └───────────────────────────────┘
                 │                          │
                 ▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    ~/flext/base.mk                           │
├─────────────────────────────────────────────────────────────┤
│  make dead-code    make modernize    make cognitive-complexity│
│  make validate-full                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    flext-quality                             │
├─────────────────────────────────────────────────────────────┤
│  FlextQualityPythonTools    FlextQualityAnalyzer            │
│  - Vulture                  - Orchestrates all tools        │
│  - Mypy                     - Generates reports             │
│  - Bandit                   - Calculates scores             │
│  - Radon                                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                MCP Python Refactoring Server                 │
├─────────────────────────────────────────────────────────────┤
│  ~/mcp-python-refactoring                                    │
│  - Rope (AST refactoring)                                    │
│  - Refurb (modern patterns)                                  │
│  - Complexipy (cognitive complexity)                         │
│  - LibCST, Jedi                                              │
└─────────────────────────────────────────────────────────────┘
```

## Summary

The integration follows a layered approach:

1. **Hooks** - Real-time quality gates during development
1. **Makefile** - CLI-accessible quality commands
1. **MCP Server** - On-demand analysis via Claude Code
1. **flext-quality** - Unified API for programmatic access
