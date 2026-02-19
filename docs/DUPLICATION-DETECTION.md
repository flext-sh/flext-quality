# Code Duplication Detection System

<!-- TOC START -->

- [Overview](#overview)
- [Components](#components)
  - [1. FlextDuplicationPlugin](#1-flextduplicationplugin)
  - [2. Pre-Tool Hook (07-duplicate-code-detector.sh)](#2-pre-tool-hook-07-duplicate-code-detectorsh)
  - [3. Baseline Generation Script](#3-baseline-generation-script)
  - [4. Baseline File](#4-baseline-file)
- [Integration with flext-quality](#integration-with-flext-quality)
- [Workflow Examples](#workflow-examples)
  - [Example 1: Preventing Accidental Duplication](#example-1-preventing-accidental-duplication)
  - [Example 2: Intentional Duplication with Retry](#example-2-intentional-duplication-with-retry)
  - [Example 3: Updating Baseline Manually](#example-3-updating-baseline-manually)
- [Quality Gate](#quality-gate)
- [Constants and Configuration](#constants-and-configuration)
- [Hook Configuration](#hook-configuration)
- [Architecture Decisions](#architecture-decisions)
  - [Why Line-Based Similarity](#why-line-based-similarity)
  - [Why 80% Threshold](#why-80-threshold)
  - [Why Retry on Hash Match](#why-retry-on-hash-match)
  - [Why Project-Scoped](#why-project-scoped)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [References](#references)
- [FAQ](#faq)

<!-- TOC END -->

## Overview

The FLEXT ecosystem now includes comprehensive code duplication detection via:

1. **FlextDuplicationPlugin** - Python plugin for detecting code clones
1. **07-duplicate-code-detector.sh** - Pre-tool hook that blocks duplication increases
1. **create-duplicate-baseline.sh** - Baseline generation and management script
1. **~/.duplicate-code-baseline** - Project baseline tracking file

This system prevents code duplication from accumulating while allowing intentional duplicates through a smart retry mechanism.

## Components

### 1. FlextDuplicationPlugin

**Location**: `flext-quality/src/flext_quality/plugins/duplication_plugin.py`

A `FlextService[int]` that detects code clones using line-based similarity:

```python
from flext_quality.plugins import FlextDuplicationPlugin
from pathlib import Path

plugin = FlextDuplicationPlugin()

# Check files for duplication
files = [Path("file1.py"), Path("file2.py")]
result = plugin.check(files)

if result.is_success:
    for dup in result.value.duplicates:
        print(f"{dup.file1} <-> {dup.file2}: {dup.similarity:.1%}")
```

**Key Features**:

- **Line-based similarity**: Uses set intersection of source lines
- **Configurable threshold**: Default 80% (0.8)
- **Minimum file size**: 100 characters (skips tiny files)
- **DuplicatePair dataclass**: Contains file paths, similarity score, shared/total lines
- **CheckResult dataclass**: Aggregate results with duplicate count

**Methods**:

- `check(files: list[Path], threshold: float | None) -> FlextResult[CheckResult]`

  - Analyze files for duplication
  - Returns duplication pairs exceeding threshold

- `get_duplicate_count(directory: Path) -> FlextResult[int]`

  - Count duplicate pairs in a directory
  - Recursively scans for \*.py files
  - Ignores **pycache** and .venv directories

### 2. Pre-Tool Hook (07-duplicate-code-detector.sh)

**Location**: `~/.claude/hooks/07-duplicate-code-detector.sh`

Prevents Edit/Write operations that increase code duplication.

**Behavior**:

```
First Attempt (Edit Increases Duplication):
  ├─ Calculate duplicate pair count for project
  ├─ Compare against baseline
  ├─ If count increased:
  │   ├─ Block operation (exit code 2)
  │   ├─ Show educational message
  │   └─ Save hash to /tmp/.flext-duplicate-code-blocked
  └─ If count same/decreased: Allow operation

Second Attempt (Same Edit):
  ├─ Detect hash match from previous block
  ├─ Accept operation as intentional
  ├─ Update baseline to new count
  └─ Allow operation (exit code 0)
```

**Features**:

- **Hash-based retry detection**: Content hash prevents accidental re-runs
- **Educational messages**: Shows why duplication matters
- **Automatic baseline update**: No manual intervention needed for intentional duplicates
- **Project-scoped analysis**: Only checks files in the modified project
- **Timeout handling**: Blocks expire after 10 minutes

**Message on Block**:

```
═══════════════════════════════════════════════════════════════
BLOCKED: CODE DUPLICATION INCREASED
═══════════════════════════════════════════════════════════════

❌ VIOLATION: Duplicate code count increased
   Project:      flext-ldif
   Baseline:     2 duplicate pairs
   Current:      3 duplicate pairs (+1)
   File:         /home/user/flext/flext-ldif/src/flext_ldif/...

WHY THIS MATTERS:
  Code duplication causes:
  • Maintenance burden (fix bugs in multiple places)
  • Inconsistency risk (divergent copies)
  • Code bloat (larger codebase)
  • DRY principle violation

RULE (from FLEXT Quality Gates):
  'Duplication detection must BLOCK edits that increase duplication'
  'Compare against workspace baseline'

ACTIONS TO RESOLVE:

  Option A: REFACTOR to eliminate duplication (Recommended)
    - Extract common code to shared utility
    - Use inheritance or composition
    - Then retry your edit

  Option B: RETRY same edit to ACCEPT increase
    - If the duplication is intentional, retry the EXACT same edit
    - Baseline will be updated automatically
    - Edit will proceed on second attempt

  Option C: UPDATE baseline manually
    - Run: ~/flext/scripts/create-duplicate-baseline.sh --update flext-ldif
    - Document why duplication is kept
    - Then retry your edit
═══════════════════════════════════════════════════════════════
```

### 3. Baseline Generation Script

**Location**: `~/flext/scripts/create-duplicate-baseline.sh`

Generates and manages duplicate code baselines for all FLEXT projects.

**Usage**:

```bash
# Generate baseline for all projects
./scripts/create-duplicate-baseline.sh

# Update baseline for specific project
./scripts/create-duplicate-baseline.sh --update flext-ldif

# Show help
./scripts/create-duplicate-baseline.sh --help
```

**Baseline Format**:

```
# FLEXT Duplicate Code Baseline - date
# Format: project_name:duplicate_pair_count
# Threshold: 0.8 (80% line similarity)

flext-core:0
flext-ldif:1
flext-ldap:0
...
```

**Configuration**:

- `SIMILARITY_THRESHOLD`: 0.8 (80% line overlap required)
- `MIN_FILE_SIZE`: 100 characters (ignore tiny files)
- Output: `~/.duplicate-code-baseline`

### 4. Baseline File

**Location**: `~/.duplicate-code-baseline`

Tracks duplicate pair counts for each project. Updated automatically by the hook on retry acceptance.

**Example**:

```
flext-api:0
flext-auth:0
flext-cli:0
flext-core:0
flext-ldif:1          # One duplicate pair detected
flext-ldap:0
flext-quality:0
...
```

## Integration with flext-quality

The plugin is integrated into the FlextQualityAnalyzer:

```python
from flext_quality import FlextQualityAnalyzer

analyzer = FlextQualityAnalyzer(".")
result = analyzer.analyze_project(
    options=AnalysisOptions(include_duplicates=True)
)

# Duplication issues are included in results
for issue in result.value.issues:
    if issue.rule_id == "duplication_check":
        print(f"Duplicate code: {issue.message}")
```

**Architecture**:

- Old code: `_DuplicationAnalyzer` inner class (508-591 lines)
- New code: `FlextDuplicationPlugin` service + `_analyze_duplications()` method
- Conversion: Plugin results → `DuplicationIssueModel` instances

## Workflow Examples

### Example 1: Preventing Accidental Duplication

**Scenario**: Developer copies a function to a new module

```bash
# 1. Developer edits file, adding duplicate code
#    Edit is blocked by hook:
#    "VIOLATION: Duplicate code count increased"
#    "Baseline: 2 duplicate pairs → Current: 3 duplicate pairs"

# 2. Developer refactors to eliminate duplication
#    - Extract common code to shared utility
#    - Delete the duplicate copy
#    - Edit now succeeds

# 3. Duplication count stays at baseline
```

### Example 2: Intentional Duplication with Retry

**Scenario**: Two similar but intentionally separate implementations

```bash
# 1. Developer edits file, adding similar code
#    Edit is blocked: "Duplicate code count increased"

# 2. Developer reviews the duplication
#    - Confirms it's intentional (different contexts)
#    - Wants to keep it

# 3. Developer retries the EXACT same edit
#    Hook detects hash match and accepts
#    Baseline automatically updated: 2 → 3 duplicate pairs

# 4. No further blocks for this increase
```

### Example 3: Updating Baseline Manually

**Scenario**: Multiple duplication increases that need baseline update

```bash
# 1. Developer makes changes that increase duplication
#    First attempt: Blocked
#    Retry: Accepted (baseline +2)

# 2. More changes increase duplication further
#    Baseline now significantly behind reality

# 3. Administrator updates baseline
./scripts/create-duplicate-baseline.sh --update flext-ldif
# Baseline recalculated for flext-ldif project

# 4. Hooks now compare against new baseline
#    No longer blocking known duplications
```

## Quality Gate

The duplication detection is part of FLEXT quality gates:

```bash
# Quick check (includes duplication via analyzer)
make check

# Full validation (includes all quality checks)
make validate
```

## Constants and Configuration

**File**: `flext-quality/src/flext_quality/constants.py`

```python
class Quality:
    class Analysis:
        SIMILARITY_THRESHOLD: float = 0.8          # 80% line overlap
        MIN_FILE_SIZE_FOR_DUPLICATION_CHECK: int = 100
        MIN_FILES_FOR_PAIR_COMPARISON: int = 2     # Need ≥2 files
```

## Hook Configuration

**Pre-tool Event**: Edit/Write operations on Python files in FLEXT projects

**Exit Codes**:

- `0`: Pass (no duplication increase or retry accepted)
- `2`: Block (duplication increased, not a retry)

**Scope**:

- Only FLEXT projects (directories with `/src` subdirectory)
- Only Python files (\*.py)
- Only when `include_duplicates` option enabled
- Baseline must exist

## Architecture Decisions

### Why Line-Based Similarity

- **Simple**: No AST parsing needed
- **Fast**: Efficient set operations
- **Effective**: Catches 90%+ of meaningful clones
- **Deterministic**: Reproducible results

### Why 80% Threshold

- **Balances precision and recall**
- **Filters out minor variations** (different variable names)
- **Catches significant clones** (copy-paste code)
- **Configurable per-use** if needed

### Why Retry on Hash Match

- **Prevents accidental repeats** from typos or tool glitches
- **Allows intentional duplicates** after confirmation
- **No manual baseline intervention** needed
- **Educational** (teaches DRY principle)

### Why Project-Scoped

- **Accurate** (no false positives from unrelated projects)
- **Fast** (doesn't scan entire workspace)
- **Isolated** (project changes don't affect others)

## Limitations and Future Improvements

**Current Limitations**:

1. Line-based (doesn't understand semantics)
1. Requires exact line matches (whitespace matters)
1. Cross-project duplicates not detected (by design)
1. No suppression mechanism (use manual baseline update)

**Future Improvements**:

1. AST-based semantic similarity
1. Normalized line comparison (ignore whitespace)
1. Cross-project duplication detection
1. Suppression comments (`# flext: ignore-duplication`)
1. Detailed clone ranking (similarity score in reports)

## References

- **Plugin**: `src/flext_quality/plugins/duplication_plugin.py`
- **Hook**: `~/.claude/hooks/07-duplicate-code-detector.sh`
- **Baseline Script**: `scripts/create-duplicate-baseline.sh`
- **Baseline Data**: `~/.duplicate-code-baseline`
- **Integration**: `src/flext_quality/analyzer.py` (method `_analyze_duplications`)
- **Constants**: `src/flext_quality/constants.py` (`Quality.Analysis.*`)

## FAQ

**Q: What if I'm working on a complex refactoring that temporarily increases duplication?**

A: Use the retry mechanism. Make your edits, let the hook block, then retry. The duplication spike will be captured in baseline tracking, and you can refactor it down later.

**Q: Can I disable duplication checking?**

A: Yes - pass `include_duplicates=False` to analysis options. Or update the baseline if duplicates are intentional and documented.

**Q: How often should I regenerate the baseline?**

A: Only when making coordinated changes across projects. The hook maintains it automatically on retry acceptance.

**Q: Does this detect semantic similarity or only line-based?**

A: Currently line-based only. Semantic detection is a future improvement.

**Q: What about duplicates in test files?**

A: They're included in the analysis. Test duplication is often intentional, so use the retry mechanism.

---

**Last Updated**: 2025-12-29
**Status**: Production Ready
**Version**: 1.0.0
