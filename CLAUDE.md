# CLAUDE.md - FLEXT-QUALITY MODULE

**Hierarchy**: PROJECT-SPECIFIC
**Project**: Code Quality Analysis Tools
**Status**: NEEDS VERIFICATION
**Last Updated**: 2025-07-12

**Reference**: `/home/marlonsc/CLAUDE.md` → Universal principles
**Reference**: `/home/marlonsc/CLAUDE.local.md` → Cross-workspace issues
**Reference**: `../CLAUDE.md` → FLEXT workspace standards

---

## ⛔ ANTI-CHAOS PROTOCOL

### FORBIDDEN ACTIONS WITHOUT EXPLICIT USER PERMISSION:

1. **NEVER modify pyproject.toml** - Dependencies are carefully managed
2. **NEVER modify .gitignore** - Version control rules are set
3. **NEVER modify Makefile** - Build automation is configured
4. **NEVER create fix\_\*.py scripts** - They cause more problems than solutions
5. **NEVER duplicate code** - Use existing patterns and imports
6. **NEVER make fake implementations** - Only real, working code

### MANDATORY ACTIONS:

1. **ALWAYS use debug/trace** for diagnostics (no print statements)
2. **ALWAYS check project docs** before making changes
3. **ALWAYS follow existing patterns** in the codebase
4. **ALWAYS run quality gates** before completing work
5. **ALWAYS use workspace venv** at `/home/marlonsc/flext/.venv`

---

## 🎯 PROJECT PURPOSE

Code quality analysis and enforcement tools for FLEXT ecosystem:

- Static code analysis
- Linting rule enforcement
- Code metrics collection
- Quality reports generation
- Pre-commit hook integration

---

## 📊 PROJECT STATUS

**Current State**: NEEDS VERIFICATION

- Implementation details unknown
- Tools integration needs documentation
- Quality metrics undefined

---

## 🔧 DEVELOPMENT STANDARDS

### Environment

```bash
# MANDATORY: Use workspace venv
source /home/marlonsc/flext/.venv/bin/activate
# NOT project-specific venv
```

### Quality Gates (MANDATORY)

```bash
# Before completing ANY work:
make lint      # Must pass
make typecheck # Must pass
make test      # Must pass
make check     # Must pass ALL checks
```

---

## 📁 PROJECT STRUCTURE

```
flext-quality/
├── src/
│   └── flext_quality/
│       ├── __init__.py
│       ├── analyzers/       # Code analyzers
│       ├── reporters/       # Report generators
│       ├── rules/          # Quality rules
│       └── cli.py          # CLI interface
├── tests/
├── pyproject.toml
├── Makefile
├── README.md
└── CLAUDE.md               # This file
```

---

## 🚨 KNOWN ISSUES

- Quality tools configuration needs investigation
- Integration with ruff/black/mypy unclear
- Reporting format not documented

---

**MANTRA**: INVESTIGATE FIRST, IMPLEMENT REAL SOLUTIONS, NO SHORTCUTS
