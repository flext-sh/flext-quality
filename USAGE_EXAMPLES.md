# FLEXT-QUALITY TOOLS USAGE EXAMPLES

## 📖 Comprehensive Guide to Migrated Quality Tools

**Last Updated**: 2025-10-04
**Status**: Production Ready
**Coverage**: All 11 migrated modules

---

## 🔧 FlextQualityOperations

### Quality Gateway - Complete Quality Pipeline

```python
from flext_quality.tools import FlextQualityOperations

quality = FlextQualityOperations()

# Run all quality checks
result = quality.gateway.run_all_checks(
    project_path="/path/to/project",
    config=None,  # Optional configuration
)

if result.is_success:
    check_result = result.value
    print(f"Lint passed: {check_result.lint_passed}")
    print(f"Type check passed: {check_result.type_check_passed}")
    print(f"Coverage: {check_result.coverage}%")
else:
    print(f"Quality checks failed: {result.error}")
```

### Linting Service - Fix Issues Gradually

```python
# ALWAYS test in dry-run first (MANDATORY default)
result = quality.linting.fix_issues(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
)

if result.is_success:
    print(f"Would fix: {result.value['would_fix']} issues")

    # Only then run for real if dry-run succeeds
    result = quality.linting.fix_issues(
        module_path="src/my_module.py",
        dry_run=False,  # Explicit opt-in to real changes
    )
```

### Type Checker - Run Type Validation

```python
# Run type checking with console output
result = quality.types.check_types(
    module_path="src/my_module.py"
)

if result.is_success:
    print(f"Type checking passed using: {result.value['tool']}")
else:
    print(f"Type checking failed: {result.error}")
```

### Duplicate Detector - Find Code Duplicates

```python
result = quality.duplicates.detect_duplicates(
    project_path=".",
    threshold=10,  # Minimum lines for duplicate detection
)

if result.is_success:
    print(f"Duplicates found: {result.value['duplicates_found']}")
```

### Export Repairer - Fix **init**.py Exports

```python
result = quality.exports.repair_exports(
    package_path="src/my_package",
    dry_run=True,  # MANDATORY default
)
```

### Docstring Normalizer - Google Style

```python
result = quality.docstrings.normalize_docstrings(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
)
```

### Pattern Auditor - Code Quality Patterns

```python
result = quality.patterns.audit_patterns(
    project_path="."
)
```

### False Positive Auditor - Filter Results

```python
results = [
    {"issue": "error1", "false_positive": False},
    {"issue": "error2", "false_positive": True},
]

result = quality.audit.audit_false_positives(results)
# Returns only non-false positives
```

---

## ⚙️ FlextQualityOptimizerOperations

### Module Optimizer - Analyze and Optimize

```python
from flext_quality.tools import FlextQualityOptimizerOperations

optimizer = FlextQualityOptimizerOperations()

# Analyze module for optimization opportunities
result = optimizer.module.analyze_module(
    module_path="src/my_module.py"
)

if result.is_success:
    analysis = result.value
    print(f"Complexity score: {analysis.complexity_score}")
    print(f"Violations: {analysis.violations}")
    print(f"Suggestions: {analysis.suggestions}")
```

### Optimize Module with Dry-Run

```python
# ALWAYS test in dry-run first (MANDATORY default)
result = optimizer.module.optimize(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
    temp_path="/tmp/test-workspace",  # Optional
)

if result.is_success:
    opt_result = result.value
    print(f"Changes made: {opt_result.changes_made}")

    # Only then run for real if dry-run succeeds
    result = optimizer.module.optimize(
        module_path="src/my_module.py",
        dry_run=False,  # Explicit opt-in
    )
```

### Import Refactorer - Domain Library Enforcement

```python
result = optimizer.imports.refactor_imports(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
)
```

### Syntax Modernizer - Modern Python

```python
result = optimizer.syntax.modernize_syntax(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
)
```

### Type Modernizer - Type Annotations

```python
result = optimizer.types.modernize_types(
    module_path="src/my_module.py",
    dry_run=True,  # MANDATORY default
)
```

---

## 🏗️ FlextQualityArchitectureTools

### Violation Analyzer - Architecture Violations

```python
from flext_quality.tools import FlextQualityArchitectureTools

arch = FlextQualityArchitectureTools()

result = arch.violations.analyze_violations(
    project_path="/path/to/project"
)

if result.is_success:
    print("Architecture analysis completed")
```

### Pattern Enforcer - Enforce Patterns

```python
result = arch.patterns.enforce_patterns(
    project_path="/path/to/project",
    dry_run=True,  # MANDATORY default
)
```

### Import Tester - Test Import Structure

```python
result = arch.imports.test_imports(
    module_path="src/my_module.py"
)
```

---

## 📦 FlextQualityDependencyTools

### Dependency Analyzer - Analyze Dependencies

```python
from flext_quality.tools import FlextQualityDependencyTools

deps = FlextQualityDependencyTools()

result = deps.analyzer.analyze_dependencies(
    project_path="/path/to/project"
)

if result.is_success:
    dependencies = result.value
    print(f"Dependencies analyzed: {len(dependencies)}")
```

### Dependency Consolidator - Consolidate Dependencies

```python
result = deps.consolidator.consolidate_dependencies(
    project_path=".",
    dry_run=True,  # MANDATORY default
)
```

### Poetry Operations - Poetry Commands

```python
result = deps.poetry.update_lock(
    project_path=".",
    dry_run=True,  # MANDATORY default
)
```

---

## ✅ FlextQualityValidationTools

### Equilibrium Validator - Validate Balance

```python
from flext_quality.tools import FlextQualityValidationTools

validator = FlextQualityValidationTools()

result = validator.equilibrium.validate_equilibrium(
    workspace_path="/path/to/workspace"
)

if result.is_success:
    print("Equilibrium validation passed")
```

### Domain Validator - Domain Compliance

```python
result = validator.domain.validate_domain(
    module_path="src/my_module.py"
)
```

### Ecosystem Validator - Ecosystem Health

```python
result = validator.ecosystem.validate_ecosystem(
    workspace_path="/path/to/workspace"
)
```

---

## 🔧 FlextQualityGitTools

### History Rewriter - Remove AI Signatures

```python
from flext_quality.tools import FlextQualityGitTools

git = FlextQualityGitTools()

# ALWAYS test in dry-run first (MANDATORY default)
result = git.HistoryRewriter.rewrite_live(
    repo_path="/path/to/repo",
    dry_run=True,  # MANDATORY default
    temp_path="/tmp/test-workspace",
)

if result.is_success:
    rewrite_result = result.value
    print(f"Commits processed: {rewrite_result.commits_processed}")
    print(f"Commits changed: {rewrite_result.commits_changed}")
    print(f"Errors: {rewrite_result.errors}")

    # Only then run for real if dry-run succeeds
    if rewrite_result.success:
        result = git.HistoryRewriter.rewrite_live(
            repo_path="/path/to/repo",
            dry_run=False,  # Explicit opt-in to real changes
        )
```

### Cleanup Service - Repository Cleanup

```python
result = git.CleanupService.cleanup_cruft(
    repo_path="/path/to/repo",
    dry_run=True,  # MANDATORY default
)

if result.is_success:
    cleanup = result.value
    print(f"Removed count: {cleanup['removed_count']}")
    print(f"Success: {cleanup['success']}")
```

---

## 🛠️ FlextQualityToolsUtilities

### Color Utilities

```python
from flext_quality.tools import (
    Colors,
    colorize,
    print_colored,
    get_project_root,
    normalize_path,
)

# Use color utilities
print_colored("Success!", Colors.GREEN)
print_colored("Warning!", Colors.YELLOW)
print_colored("Error!", Colors.RED)

colored_text = colorize("Info", Colors.CYAN)
```

### Path Utilities

```python
# Get project root
project_root = get_project_root()
print(f"Project root: {project_root}")

# Normalize path
normalized = normalize_path("src/my_module.py")
```

---

## 🎯 Complete Integration Example

### Quality Workflow - From Analysis to Reporting

```python
from flext_quality.tools import (
    FlextQualityOptimizerOperations,
    FlextQualityOperations,
    FlextQualityArchitectureTools,
)

# Step 1: Analyze module with optimizer
optimizer = FlextQualityOptimizerOperations()
analysis_result = optimizer.module.analyze_module("src/my_module.py")

if analysis_result.is_success:
    analysis = analysis_result.value
    print(f"Complexity: {analysis.complexity_score}")
    print(f"Violations: {len(analysis.violations)}")

# Step 2: Run quality checks
quality = FlextQualityOperations()
lint_result = quality.linting.fix_issues("src/my_module.py", dry_run=True)

if lint_result.is_success:
    print(f"Would fix: {lint_result.value['would_fix']} issues")

# Step 3: Validate with architecture tools
arch = FlextQualityArchitectureTools()
arch_result = arch.violations.analyze_violations(".")

if arch_result.is_success:
    print("Architecture validation passed")
```

---

## 🔒 Best Practices

### 1. ALWAYS Use Dry-Run First

```python
# ✅ CORRECT: Test in dry-run first
result = optimizer.module.optimize("module.py", dry_run=True)
if result.is_success:
    # Then run for real
    result = optimizer.module.optimize("module.py", dry_run=False)

# ❌ WRONG: Running directly without dry-run
result = optimizer.module.optimize("module.py", dry_run=False)
```

### 2. ALWAYS Check FlextResult

```python
# ✅ CORRECT: Check result before using value
result = quality.linting.fix_issues("module.py")
if result.is_success:
    value = result.value
else:
    print(f"Error: {result.error}")

# ❌ WRONG: Using value without checking
value = result.value  # May crash if result.is_failure
```

### 3. ALWAYS Use Keyword Arguments

```python
# ✅ CORRECT: Use keyword arguments (enforced by *)
result = optimizer.module.optimize(
    module_path="src/module.py",
    dry_run=True,
    temp_path="/tmp/workspace",
)

# ❌ WRONG: Positional arguments not allowed
result = optimizer.module.optimize("src/module.py", True, "/tmp")
```

---

## 📝 Error Handling

### Handling FlextResult Errors

```python
from flext_quality.tools import FlextQualityOperations

quality = FlextQualityOperations()

# Railway-oriented error handling
result = quality.linting.fix_issues("nonexistent.py")

if result.is_failure:
    # Handle error gracefully
    print(f"Operation failed: {result.error}")
    # Log error
    # Notify user
    # Take corrective action
else:
    # Success path
    print(f"Fixed: {result.value['fixed']}")
```

---

**FLEXT Quality Tools Authority**: All tools follow FLEXT domain library principles with FlextResult railway-oriented programming and mandatory dry-run patterns.
