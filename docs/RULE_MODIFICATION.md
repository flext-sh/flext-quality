# Rule Modification Quick Reference

**How to customize validation rules during testing and development**

---

## 🚀 Quick Start

### Find Rule Files

All 197 rules are in YAML files:

```bash
ls /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/*.yaml
```

**16 YAML files with rule categories**:

```
architecture.yaml          (12 rules)  - Architecture layering
bash_commands.yaml         (21 rules)  - Shell command safety
behavioral.yaml            (3 rules)   - Behavioral patterns
code_quality.yaml          (14 rules)  - Type safety & quality
dependencies.yaml          (16 rules)  - FLEXT ecosystem dependencies
dry_principle.yaml         (3 rules)   - DRY principle
file_operations.yaml       (19 rules)  - File operation safety
file_protection.yaml       (13 rules)  - File access control
flextresult.yaml           (3 rules)   - FlextResult patterns
git_operations.yaml        (29 rules)  - Git command safety
namespace.yaml             (14 rules)  - Module organization
project_files.yaml         (14 rules)  - Project file protection
python_code.yaml           (13 rules)  - Python code quality
quality_gates.yaml         (3 rules)   - Quality validation gates
security.yaml              (16 rules)  - Security operations
solid_principles.yaml      (4 rules)   - SOLID principle enforcement
type_system.yaml           (16 rules)  - Type system rules
```

### Reload Rules Automatically

After editing YAML files, rules reload on next hook execution:

```bash
# No restart needed - rules load automatically on next validation
# Just save your YAML changes and the system will use them immediately
```

---

## 📝 Common Modifications

### 1. Reduce Severity of a Rule

**Before** (Critical):

```yaml
- code: SEC001
  name: file_deletion_recursive
  pattern: 'rm\s+-rf?\s+[^|;&]+'
  severity: critical
  blocking: true
  guidance: |
    Use 'mv file file.bak' instead of rm...
```

**After** (Medium warning):

```yaml
- code: SEC001
  name: file_deletion_recursive
  pattern: 'rm\s+-rf?\s+[^|;&]+'
  severity: medium # Reduced from critical
  blocking: false # Optional: warning only
  guidance: |
    Use 'mv file file.bak' instead of rm...
```

---

### 2. Disable Rule Temporarily

**Add exceptions** to skip specific files:

```yaml
- code: FO001
  name: script_creation_in_project
  pattern: '>\s*(?!/tmp)[^|&\s]*\.(sh|bash|py)\s*$'
  severity: critical
  blocking: true
  exceptions:
    - "**/tests/**" # Skip in tests directory
    - "**/scripts/**" # Skip in scripts directory
    - "**/build/**" # Skip in build output
  guidance: |
    Use /tmp/ for temporary scripts...
```

**Or disable entirely**:

```yaml
- code: FO001
  ...
  blocking: false           # Won't block execution
  severity: low             # Low priority warning
```

---

### 3. Modify Guidance Message

Update guidance for clarity:

```yaml
- code: CQ008
  name: flextresult_returning_none
  pattern: 'return\s+None\s*$'
  severity: critical
  blocking: true
  guidance: |
    ❌ WRONG: FlextResult should never return None directly.

    ✅ CORRECT: Use FlextResult patterns:
      - Return .ok(value) for success
      - Return .fail(error) for failure
      - Never return bare None

    Example:
      def get_user(id: int) -> FlextResult[User]:
          user = db.find(id)
          if not user:
              return FlextResult.fail(UserNotFound(id))
          return FlextResult.ok(user)
```

---

### 4. Add Custom Rule

Create new rule in appropriate YAML file:

**In `code_quality.yaml`**:

```yaml
- code: CQ999 # Unique code
  name: my_custom_pattern # Short name
  pattern: "some_pattern" # Regex pattern
  severity: medium # critical, high, medium, low
  blocking: false # Block or warn only
  guidance: |
    Explanation of the issue.

    How to fix:
      - Option 1: Do this
      - Option 2: Or this

    Example:
      WRONG: code that triggers rule
      RIGHT: corrected version
  tags: [custom, testing] # Optional tags
  applies_to: # Optional: file patterns
    - "**/*.py" # Python files only
    - "!**/tests/**" # Except tests
```

---

### 5. Change Pattern (Regex)

Update what triggers the rule:

```yaml
# OLD: Triggers on any "cast("
- code: CQ014
  pattern: 'cast\s*\('

# NEW: Only triggers on cast with specific types
- code: CQ014
  pattern: 'cast\s*\(\s*(int|str|dict|list)'
```

---

## 🔍 Rule Structure Reference

**Complete rule anatomy**:

```yaml
- code: CATXXX # Unique identifier (CAT = category)
  name: descriptive_name # Human-readable name
  pattern: "regex_pattern" # Pattern to match
  category: category_name # From RuleCategory enum
  severity: critical # critical | high | medium | low
  blocking: true # Whether it blocks execution
  guidance: | # Multi-line guidance text
    Explanation of issue
    How to fix it
    Examples if helpful
  tags: [tag1, tag2] # Optional categorization
  applies_to: # Optional file patterns
    - "**/*.py"
    - "!**/tests/**"
  exceptions: # Optional exclusions
    - "**/tests/**"
    - "**/scripts/**"
  language: python # Optional language
  file_types: # Optional file extensions
    - ".py"
    - ".pyi"
  context_required: # Optional required context
    - "FLEXT_PROJECT"
```

---

## 🔄 Workflow: Test → Adjust → Verify

### Scenario: Rule is too strict

```bash
# 1. Notice warning appears too often
#    [SEC001] rm -rf: ... (appears 5 times in test scripts)

# 2. Edit the YAML file
nano /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/security.yaml

# 3. Add exception for test scripts
#    exceptions:
#      - "**/tests/**"

# 4. Save and test again
#    Rule will now skip test directories

# 5. Verify it works
#    (no warning when matching pattern in tests/)
```

### Scenario: Rule warning is unclear

```bash
# 1. See confusing warning message
#    [CQ999] my_rule: ...

# 2. Edit guidance to be clearer
nano /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/code_quality.yaml
#    Update guidance: | section with better explanation

# 3. Save and trigger rule again
#    New guidance appears in next warning
```

### Scenario: Need to disable rule for time being

```bash
# Option A: Reduce severity
nano /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/security.yaml
# Change: severity: critical → severity: low

# Option B: Add exceptions
# exceptions:
#   - "**/*"  # Skip everywhere

# Option C: Turn off entirely
# blocking: false
```

---

## 🎯 Finding Your Rule

### By rule code (e.g., SEC001)

```bash
# Find the rule file
grep -l "SEC001" /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/*.yaml
# Output: security.yaml

# Edit that file
nano /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/security.yaml
```

### By pattern name

```bash
# Find rule by name
grep -l "file_deletion" /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/*.yaml
# Output: security.yaml
```

### By category

```bash
# All code quality rules
cat /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/code_quality.yaml

# All git operations rules
cat /home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/git_operations.yaml
```

---

## ✅ Validation After Changes

### Test Rule Loads

```bash
cd /home/marlonsc/flext/flext-quality

# Python test (requires dependencies)
# python3 -c "from flext_quality.rules import registry; print(f'Loaded {len(registry.all())} rules')"

# Or validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('src/flext_quality/rules/data/security.yaml'))"
# No error = valid syntax
```

### Trigger Rule to Test

```bash
# Create file that matches pattern
echo 'rm -rf /tmp/test' > /tmp/test_rule.sh

# Run hook (simulated)
# python3 ~/.claude/hooks/pre_tool_use.py

# Check if:
# 1. Rule is detected ✅
# 2. New guidance appears ✅
# 3. Exception works (if added) ✅
```

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Invalid YAML syntax

```yaml
# WRONG - Missing colon
- code SEC001
  name: test

# RIGHT - Colon after key
- code: SEC001
  name: test
```

**Fix**: Use YAML validator:

```bash
python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"
```

### ❌ Mistake 2: Invalid regex pattern

```yaml
# WRONG - Unescaped regex metacharacters
pattern: 'rm -rf +'  # + is metacharacter, needs \\+

# RIGHT - Properly escaped
pattern: 'rm\s+-rf\s+'
```

**Test regex**:

```bash
python3 -c "import re; re.compile(r'your_pattern_here')"
```

### ❌ Mistake 3: Breaking YAML structure

```yaml
# WRONG - Wrong indentation breaks structure
- code: SEC001
name: test  # Not indented under code

# RIGHT - Proper indentation
- code: SEC001
  name: test
```

---

## 📋 Rule Modification Checklist

When modifying a rule:

- [ ] Found correct YAML file
- [ ] Located the rule by code/name
- [ ] Made your change (severity/pattern/guidance/etc)
- [ ] Saved the YAML file
- [ ] Validated YAML syntax (no errors)
- [ ] Tested the rule (triggered it to verify)
- [ ] Verified change works as expected
- [ ] Updated guidance if needed
- [ ] Checked for side effects (other rules)

---

## 🔗 Related Documentation

- **Hook Warnings**: `HOOK_WARNINGS.md` - Complete warning reference
- **Architecture Rules**: Search for architectural patterns in YAML files
- **Testing Rules**: See `flextresult.yaml` and `code_quality.yaml`

---

**Quick Reference**: All rules in `/home/marlonsc/flext/flext-quality/src/flext_quality/rules/data/`

**Reload**: Automatic on next hook execution (no restart needed)

**Help**: See `HOOK_WARNINGS.md` for detailed rule explanations
