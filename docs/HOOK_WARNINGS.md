# Hook Warning Reference Guide

**Status**: ⚠️ **WARNING-ONLY MODE** - All warnings allow execution to proceed

This guide explains the 197 validation rules that hooks monitor, organized into 5 warning categories.

---

## ⚠️ How Warning-Only Mode Works

**The hook system is configured to warn but NOT block**:

```
Tool execution → Hook validates → Violations found? →
  YES: Show warnings + suggestions → Allow execution anyway ✅
  NO:  Silent pass → Allow execution ✅
```

**Key behavior**:

- ✅ **All operations proceed** (no blocking)
- ⚠️ **Warnings are informational** (help you improve code)
- 📖 **Guidance provided** (how to fix violations)
- 🔄 **Iterative validation** (fix and try again)

---

## 📂 Warning Categories

### 1. Security Warnings (16 rules)

**Purpose**: Protect against dangerous shell operations and destructive commands.

#### File Deletion (SEC001-003)

- **SEC001**: `rm -rf` detected
  - Problem: Permanent, irreversible file deletion
  - Fix: Use `mv file file.bak` instead
  - Example: `rm -rf old_dir` → `mv old_dir old_dir.bak`

- **SEC002**: `rm` (simple delete)
  - Problem: Loses files without recovery option
  - Fix: Use `mv file file.bak` for reversibility

- **SEC003**: `sudo rm` (deletion with sudo)
  - Problem: Can delete system files permanently
  - Fix: Ask user first, use `sudo mv file file.bak` if needed

#### In-Place Editing (SEC004-006)

- **SEC004**: `sed -i` (sed in-place)
  - Problem: No backup created automatically
  - Fix: Use Edit tool or create `/tmp/fix_*.sh` with backup modes

- **SEC005**: `awk -i inplace` (awk in-place)
  - Problem: Batch file modification without validation
  - Fix: Use validation script with dry-run, backup, rollback

- **SEC006**: `perl -i/-p` (perl in-place)
  - Problem: In-place editing of multiple files unsafely
  - Fix: Create `/tmp` script with 4 modes (dry-run, backup, exec, rollback)

#### System Destructive Operations (SEC007-011)

- **SEC007**: `dd if=` (disk write)
  - ⛔ CRITICAL: Can overwrite entire disks
  - Fix: Double-check paths, ask user for explicit approval

- **SEC008**: `mkfs.` (filesystem formatting)
  - ⛔ CRITICAL: Erases entire partitions permanently
  - Fix: Requires explicit user confirmation

- **SEC009**: `fdisk` (partition editing)
  - ⛔ CRITICAL: Can destroy filesystems
  - Fix: Only with user approval and verification

- **SEC010**: `parted` (partition editor)
  - ⛔ CRITICAL: Partition modification can cause data loss
  - Fix: User must explicitly approve

- **SEC011**: `chmod -R 777`
  - Problem: Creates world-writable files (security vulnerability)
  - Fix: Use specific permissions: `chmod 755`, `chmod 644`, `chmod 700`

#### Piping & Package Management (SEC012-016)

- **SEC012**: Truncation redirection (`>`)
  - Problem: Can overwrite existing files
  - Fix: Use Write tool or verify file doesn't exist

- **SEC013**: Pipe to shell (`| bash`, `| sh`)
  - ⛔ CRITICAL: Executes remote code without review
  - Fix: Download separately, review, then execute

- **SEC014**: `pip install` (direct pip usage)
  - Problem: Bypasses Poetry dependency management
  - Fix: Use `poetry add package-name`

- **SEC015**: `pip install --upgrade`
  - Problem: Can break compatibility
  - Fix: Use `poetry update` for safe upgrades

- **SEC016**: `uv pip` (uv package installer)
  - Problem: Inconsistent with FLEXT Poetry approach
  - Fix: Use Poetry for FLEXT projects

---

### 2. Git Operations Warnings (29 rules)

**Purpose**: Prevent accidental loss of git commits, branches, and stashes.

#### Destructive Operations (GIT001-007)

- **GIT001**: `git restore`
  - Problem: Discards working directory changes
  - Fix: Review with `git diff`, fix manually with Edit tool

- **GIT002**: `git checkout --`
  - Problem: Discards changes to files
  - Fix: Review changes first, fix manually

- **GIT003**: `git reset --hard`
  - ⛔ CRITICAL: Discards all uncommitted changes
  - Fix: Use `git stash`, `git diff HEAD`, or `git reset --soft`

- **GIT004**: `git reset --mixed`
  - Problem: Unstages changes confusingly
  - Fix: Use `git restore --staged <file>` for specific files

- **GIT005**: `git reset HEAD~`
  - ⛔ CRITICAL: Undoes commits irreversibly
  - Fix: Use `git revert <commit>` (creates new commit, safer)

- **GIT006**: `git reset <commit-hash>`
  - ⛔ CRITICAL: Resets to specific commit
  - Fix: Use `git revert <commit>` for reversible undo

- **GIT007**: `git clean -f/-d`
  - ⛔ CRITICAL: Deletes untracked files permanently
  - Fix: Use `git clean -n` (dry-run) first to preview

#### Staging & Push Operations (GIT008-010)

- **GIT008**: `git stage`
  - Problem: Can cause code loss in hook sequences
  - Fix: Use `git add <file>` or `git add -p` (interactive)

- **GIT009**: `git push --force`
  - ⛔ CRITICAL: Overwrites remote history
  - Fix: Use `git push --force-with-lease` (safer alternative)

- **GIT010**: `git push -f` (short form)
  - ⛔ CRITICAL: Force push with short flag
  - Fix: Never force push to main/master branch

#### Rebase & Merge (GIT011-013)

- **GIT011**: `git rebase -i` (interactive rebase)
  - Problem: Requires terminal interaction
  - Fix: User must run manually or use non-interactive rebase

- **GIT012**: `git rebase --abort`
  - ⛔ CRITICAL: Loses rebase work in progress
  - Fix: Resolve conflicts manually, use `git rebase --continue`

- **GIT013**: `git merge --abort`
  - ⛔ CRITICAL: Loses merge work in progress
  - Fix: Resolve conflicts manually, use `git commit`

#### Conflict Resolution (GIT014-018)

- **GIT014**: `git checkout --ours`
  - Problem: Discards changes from other branch
  - Fix: Resolve conflicts manually with Edit tool

- **GIT015**: `git checkout --theirs`
  - Problem: Discards your changes
  - Fix: Review both sides, resolve manually

- **GIT016**: `git merge -X ours`
  - Problem: Ignores other branch changes
  - Fix: Manually resolve conflicts

- **GIT017**: `git merge -X theirs`
  - Problem: Ignores your changes
  - Fix: Manually review and resolve

- **GIT018**: `git mergetool`
  - Problem: Requires interactive terminal
  - Fix: Resolve conflicts with Edit tool manually

#### Branch & Stash (GIT019-024)

- **GIT019**: `git branch -d/-D`
  - ⛔ CRITICAL: Deletes branch permanently
  - Fix: Verify merged first, ask user for confirmation

- **GIT020**: `git branch -m`
  - Problem: Can break references and CI/CD
  - Fix: Ask user for approval before renaming

- **GIT021**: `git push origin :branch`
  - ⛔ CRITICAL: Deletes remote branch permanently
  - Fix: Ask user, verify merged, use confirmation

- **GIT022**: `git stash drop`
  - ⛔ CRITICAL: Deletes stash permanently
  - Fix: List first (`git stash list`), preview (`git stash show -p`)

- **GIT023**: `git stash clear`
  - ⛔ CRITICAL: Deletes ALL stashes permanently
  - Fix: Ask user, list all stashes first

- **GIT024**: `git cherry-pick --abort`
  - ⛔ CRITICAL: Loses cherry-pick work
  - Fix: Resolve conflicts, use `git cherry-pick --continue`

#### Automation Scripts (GIT025-029)

- **GIT025-029**: Git commands in scripts
  - Problem: Automated git operations need explicit review
  - Fix: Execute git directly or ask user to run command

---

### 3. Code Quality Warnings (14 rules)

**Purpose**: Ensure proper type safety, organization, and testing practices.

#### Type Annotations (CQ001-005)

- **CQ001**: Missing return type on function
  - Problem: Type checking is incomplete
  - Fix: Add `-> ReturnType` annotation to all public functions

- **CQ002**: `TypeAlias` outside typings.py
  - Problem: Type aliases scattered across codebase
  - Fix: Move to `src/*/typings.py`, import as `from flext_core import FlextTypes as t`

- **CQ003**: `Protocol` outside protocols.py
  - Problem: Protocol definitions scattered
  - Fix: Move to `src/*/protocols.py`, import as `p.*`

- **CQ004**: `TypeVar` outside typings.py
  - Problem: Generic type variables scattered
  - Fix: Centralize in typings.py

- **CQ005**: Complex `Callable` (3+ parameters)
  - Problem: Unclear function signatures
  - Fix: Use `Protocol` with `__call__` method for clarity

#### Data Structures (CQ006-007)

- **CQ006**: `@dataclass` instead of Pydantic
  - Problem: Missing validation and serialization
  - Fix: Use `pydantic.BaseModel` for data validation

- **CQ007**: Excessive `isinstance()` checks
  - Problem: Indicates loose coupling
  - Fix: Use `Protocol` for structural typing instead

#### FLEXT Patterns (CQ008-010)

- **CQ008**: `FlextResult` returning None
  - ⛔ CRITICAL: FlextResult never returns None
  - Fix: Use `.ok(value)` for success, `.fail(error)` for failure

- **CQ009**: `FlextResult` without type parameter
  - ⛔ CRITICAL: Must specify type parameter
  - Fix: `FlextResult[T]` always, never bare `FlextResult`

- **CQ010**: Uncentralized dict types
  - Problem: Repeated `dict[str, str]` patterns
  - Fix: Use centralized types like `t.StringDict` from typings.py

#### Testing (CQ011)

- **CQ011**: Mock usage in tests
  - ⛔ CRITICAL: FLEXT uses real implementations
  - Problem: Mocks hide implementation details, create brittle tests
  - Fix: Use real objects, fixtures, factories instead

---

### 4. File Operations Warnings (19 rules)

**Purpose**: Prevent project pollution and maintain organization standards.

#### Script Creation (FO001-004)

- **FO001**: Script in project root
  - Problem: Clogs project with temporary scripts
  - Fix: Create in `/tmp/fix_*.sh` with validation modes

- **FO002**: Reports/logs in project
  - Problem: Clutters project directory
  - Fix: Create in `/tmp/` for temporary, `docs/` for permanent

- **FO003**: File creation via `tee`
  - Problem: Creates files without validation
  - Fix: Use `tee /tmp/file` or Write tool

- **FO004**: File creation via `touch`
  - Problem: Creates files without structure
  - Fix: Use `/tmp/file` for temporary

#### Batch Operations (FO005-009)

- **FO005**: `sed -i` on multiple Python files
  - ⛔ CRITICAL: No validation or rollback
  - Fix: Create `/tmp/fix_*.sh` with 4 modes:
    1. `dry-run` - preview changes
    2. `backup` - create .bak files
    3. `exec` - execute + validate
    4. `rollback` - restore if fails

- **FO006**: `find -exec sed` (batch editing)
  - ⛔ CRITICAL: Dangerous batch operation
  - Fix: Use validation script with dry-run and rollback

- **FO007**: `xargs sed -i`
  - ⛔ CRITICAL: Batch modification without control
  - Fix: Use `/tmp/fix_*.sh` with 4 modes

- **FO008**: Loop with sed
  - Problem: Uncontrolled batch modification
  - Fix: Convert to script with validation

- **FO009**: Python inline `-c` modifying files
  - Problem: Unvalidated file modification
  - Fix: Use Edit tool or `/tmp` script

#### Backup Conventions (FO010-011)

- **FO010**: `.backup` extension (wrong)
  - Problem: Inconsistent backup naming
  - Fix: Use `.bak` convention only

- **FO011**: `.orig` extension (wrong)
  - Problem: Legacy naming convention
  - Fix: Use `.bak` for consistency

#### Temporary Files (FO012-019)

- **FO012**: fix/verify/check scripts in project
  - Problem: Ad-hoc scripts clutter project
  - Fix: Use `/tmp/fix_*.sh` for temporary scripts

- **FO013**: Generic `script_*.sh` in project
  - Problem: Scripts outside proper location
  - Fix: `/tmp/script_*.py` for temporary, `/scripts/` for permanent

- **FO014**: Files with `temp/tmp/temporary` in name
  - Problem: Temporary files in project
  - Fix: Store in `/tmp/` only

- **FO015**: Experimental scripts in project
  - Problem: Try/test/experiment scripts clutter project
  - Fix: `/tmp/` for ad-hoc, `/scripts/experiments/` for organized

- **FO016**: Reports in project root
  - Problem: Analysis output clutters project
  - Fix: `/tmp/report_*.md` for temporary, `docs/` for permanent

- **FO017**: Log/output files in project
  - Problem: Debug files pollute project
  - Fix: Use `/tmp/debug.log`, `/tmp/output.txt`

- **FO018**: Results files in project
  - Problem: Analysis results scatter in project
  - Fix: `/tmp/results_*.json` for temporary

- **FO019**: Output files in project
  - Problem: Generated output clogs project
  - Fix: `/tmp/output_*.txt` for temporary

---

### 5. Project Files Warnings (14 rules)

**Purpose**: Protect critical configuration and security files.

#### Configuration Management (PF001-002)

- **PF001**: `pyproject.toml` direct edit
  - Problem: Manual edits cause inconsistencies
  - Fix: Use Poetry commands:
    - `poetry add <pkg>`
    - `poetry remove <pkg>`
    - `poetry version <version>`

- **PF002**: `poetry.lock` manual edit
  - ⛔ CRITICAL: Lock file is generated
  - Problem: Manual edits corrupt dependency resolution
  - Fix: Use `poetry lock` or `poetry update` only

#### Git Configuration (PF003-014)

- **PF003**: `.git/hooks/` modifications
  - Problem: Git hooks should be in `.claude/hooks/`
  - Fix: Use `~/.claude/hooks/` for user hooks, `./.claude/hooks/` for project

- **PF004**: `Makefile` editing
  - Problem: Changes affect all builds and tests
  - Fix: Only edit with user approval after understanding impact

- **PF005**: `Dockerfile` editing
  - Problem: Changes affect containerized deployments
  - Fix: Only edit with careful testing and user approval

- **PF006**: `.env` file editing
  - ⛔ CRITICAL: Contains secrets
  - Problem: Environment variables are user-specific
  - Fix: User manages their own `.env`, never edit directly

- **PF007**: `credentials.*` files
  - ⛔ CRITICAL: Security credentials
  - Fix: Never touch credential files

- **PF008**: `password.*` files
  - ⛔ CRITICAL: Passwords are sensitive
  - Fix: Never edit password files

- **PF009**: `*token.*` files
  - ⛔ CRITICAL: API tokens are secrets
  - Fix: Never modify token files (except `.token` for FLOCK)

- **PF010**: `.pem` key files
  - ⛔ CRITICAL: SSH/TLS private keys
  - Fix: Never edit key files

- **PF011**: `.key` files
  - ⛔ CRITICAL: Encryption keys
  - Fix: Never modify key files

- **PF012**: `.git/config` modifications
  - Problem: Git configuration is user-controlled
  - Fix: User manages with `git config` commands

- **PF013**: `.git/index` modifications
  - Problem: Index is git's staging area (binary)
  - Fix: Use git commands only (`git add`, `git reset`)

- **PF014**: `.git/HEAD` modifications
  - Problem: HEAD points to current branch
  - Fix: Use `git checkout`, `git switch` commands

---

## 🔄 How to Respond to Warnings

### Option 1: Fix the Violation ✅ (Recommended)

Use the guidance provided to correct the code:

```bash
# If you see:
# ⚠️ WARNING [SEC001] L42: rm -rf detected
#    Use: mv file file.bak instead

# Fix it:
mv old_directory old_directory.bak  # Instead of rm -rf
```

### Option 2: Acknowledge and Proceed (If Intentional)

If the violation is truly intentional and necessary:

```
1. Understand the warning
2. Acknowledge in your response to Claude
3. Execution will proceed
4. Warning will be logged for auditing
```

### Option 3: Disable Rule Temporarily (For Testing)

Edit the YAML file to adjust severity:

```yaml
# File: flext-quality/src/flext_quality/rules/data/security.yaml

- code: SEC001
  name: file_deletion_recursive
  pattern: 'rm\s+-rf?\s+[^|;&]+'
  severity: critical
  blocking: true
  # Change above to:
  # severity: low          # Reduce importance
  # blocking: false        # Warning only (not blocking)
  # Or add exceptions:
  exceptions:
    - "**/tests/**" # Skip in test scripts
    - "**/scripts/**" # Skip in scripts
```

---

## 📖 Documentation References

- **Rule Modification**: See `RULE_MODIFICATION.md` for detailed guide
- **Dependencies**: See `../README.md` section on dependency rules
- **Testing**: See `../CLAUDE.md` section on quality gates

---

## 🎯 Summary

| Category        | Count  | Severity | Purpose                              |
| --------------- | ------ | -------- | ------------------------------------ |
| Security        | 16     | Critical | Protect against dangerous operations |
| Git Operations  | 29     | Critical | Prevent commit/branch loss           |
| Code Quality    | 14     | High     | Ensure type safety & testing         |
| File Operations | 19     | High     | Maintain project organization        |
| Project Files   | 14     | Critical | Protect configuration & secrets      |
| **TOTAL**       | **92** | -        | **5 main categories**                |

**All warnings are informational and allow execution to proceed.**

---

**Last Updated**: 2025-12-30
**Status**: ⚠️ WARNING-ONLY MODE - All operations proceed after warning
