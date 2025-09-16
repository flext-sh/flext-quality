# FLEXT-Quality Task Completion Workflow

## Mandatory Quality Gates (EXECUTE ALWAYS)

### 1. Pre-Completion Validation
Before marking any task complete, ALWAYS run:
```bash
make validate    # Complete pipeline: lint + type + security + test + quality
```

### 2. Step-by-Step Quality Gates

#### A. Lint Check (ZERO TOLERANCE)
```bash
make lint        # Ruff linting - must pass with zero errors
```

#### B. Type Check (ZERO TOLERANCE) 
```bash
make type-check  # MyPy strict mode - must pass with zero errors
```

#### C. Security Check (ZERO TOLERANCE)
```bash
make security    # Bandit + pip-audit - zero vulnerabilities
```

#### D. Test Execution (90% COVERAGE MINIMUM)
```bash
make test        # Run tests with coverage reporting
```

### 3. FLEXT Compliance Verification

#### CLI Compliance Check
```bash
# Verify no direct click/rich imports
grep -r "import click\|import rich\|from rich" src/ || echo "✅ CLI compliant"
```

#### Unified Class Pattern Check  
```bash
# Check for multiple classes per module (current violations exist)
for file in $(find src/ -name "*.py"); do
    class_count=$(grep -c "^class " "$file" 2>/dev/null || echo 0)
    [ "$class_count" -gt 1 ] && echo "❌ Multiple classes: $file"
done
```

#### Helper Functions Check
```bash
# Check for loose helper functions outside classes
grep -r "^def [^_].*:" src/ --exclude-dir=tests | grep -v "class" || echo "✅ No loose functions"
```

### 4. Build Verification
```bash
make build       # Ensure package builds successfully
```

### 5. Integration Testing
For quality analysis changes:
```bash
make test-quality      # Quality analysis specific tests
make test-integration  # Integration tests with backends
make analyze          # Run actual quality analysis
```

## Failure Response Protocol

### If Any Quality Gate Fails:
1. **STOP** immediately - do not continue
2. **FIX** the specific issue causing failure
3. **RE-RUN** the failed quality gate
4. **PROCEED** only after ALL gates pass

### Common Failure Scenarios:
- **Type Errors**: Fix type annotations, imports, generic usage
- **Lint Errors**: Run `make fix` for auto-fixable issues
- **Test Failures**: Fix broken tests or underlying code
- **Security Issues**: Address security vulnerabilities immediately
- **Coverage**: Add tests for uncovered code paths

## Documentation Updates
After significant changes:
```bash
make docs        # Update documentation if applicable
```

## Final Validation
```bash
make doctor      # Complete health check (diagnose + check)
```

## Pre-Commit Integration
Ensure pre-commit hooks are installed and passing:
```bash
make pre-commit  # Run all pre-commit hooks
```

## NEVER Skip Quality Gates
- ❌ NEVER commit code that fails quality gates
- ❌ NEVER disable quality checks to "make it work"
- ❌ NEVER suppress errors without understanding root cause
- ✅ ALWAYS fix issues at source
- ✅ ALWAYS maintain 90%+ test coverage
- ✅ ALWAYS ensure zero security vulnerabilities