"""Example validation helper - Run and validate examples.

Pragmatic utilities for:
- Running example Python files
- Validating example structure
- Ensuring examples work correctly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult

from flext_quality.subprocess_utils import SubprocessUtils


def validate_examples_directory(
    examples_dir: Path,
) -> FlextResult[dict[str, object]]:
    """Run all example.py files in directory and validate they work.

    Args:
        examples_dir: Directory containing examples

    Returns:
        FlextResult with validation results

    """
    try:
        if not examples_dir.exists():
            return FlextResult.fail(f"Directory not found: {examples_dir}")

        results = {}
        passed = 0
        failed = 0

        # Find all example.py files
        for example_file in examples_dir.rglob("example.py"):
            try:
                result = SubprocessUtils.run_external_command(
                    ["python3", str(example_file)],
                    capture_output=True,
                    timeout=30.0,
                )

                if result.is_failure:
                    error_msg = result.error or ""
                    if "timed out" in error_msg.lower():
                        results[str(example_file)] = "⏱️ TIMEOUT"
                    else:
                        error_snippet = (
                            error_msg[:100] if error_msg else "Unknown error"
                        )
                        results[str(example_file)] = f"❌ FAILED: {error_snippet}"
                    failed += 1
                else:
                    wrapper = result.unwrap()
                    if wrapper.returncode == 0:
                        results[str(example_file)] = "✅ PASSED"
                        passed += 1
                    else:
                        results[str(example_file)] = (
                            f"❌ FAILED: {wrapper.stderr[:100]}"
                        )
                        failed += 1

            except Exception as e:
                results[str(example_file)] = f"⚠️ ERROR: {str(e)[:100]}"
                failed += 1

        return FlextResult.ok(
            {
                "directory": str(examples_dir),
                "total_examples": passed + failed,
                "passed": passed,
                "failed": failed,
                "results": results,
                "status": "all_passed" if failed == 0 else "some_failures",
            }
        )

    except Exception as e:
        return FlextResult.fail(f"Example validation failed: {e}")


def check_example_structure(
    example_dir: Path,
) -> FlextResult[dict[str, object]]:
    """Check if example directory has proper structure.

    Expected structure:
    - example.py (required)
    - README.md (optional but recommended)
    - requirements.txt (optional)
    - config.yaml (optional)

    Args:
        example_dir: Example directory to check

    Returns:
        FlextResult with structure validation

    """
    try:
        required_files = {
            "example.py": example_dir / "example.py",
        }

        recommended_files = {
            "README.md": example_dir / "README.md",
            "requirements.txt": example_dir / "requirements.txt",
            "config.yaml": example_dir / "config.yaml",
        }

        issues = []

        # Check required files
        for name, path in required_files.items():
            if not path.exists():
                issues.append(f"Missing required: {name}")

        # Check recommended files
        missing_recommended = []
        for name, path in recommended_files.items():
            if not path.exists():
                missing_recommended.append(name)

        if missing_recommended:
            issues.append(f"Missing recommended: {', '.join(missing_recommended)}")

        return FlextResult.ok(
            {
                "directory": str(example_dir),
                "valid": len(issues) == 0,
                "issues": issues,
                "structure": "complete" if not issues else "incomplete",
            }
        )

    except Exception as e:
        return FlextResult.fail(f"Structure check failed: {e}")


def validate_example_imports(
    example_file: Path,
) -> FlextResult[dict[str, object]]:
    """Check that all imports in example file are available.

    Args:
        example_file: Example Python file to check

    Returns:
        FlextResult with import validation

    """
    try:
        with Path(example_file).open(encoding="utf-8") as f:
            content = f.read()

        # Extract import statements
        imports = [
            line.strip()
            for line in content.splitlines()
            if line.startswith(("import ", "from "))
        ]

        # Try to verify imports work by running a test script
        test_code = "\n".join(imports) + "\nprint('✅ All imports successful')"

        result = SubprocessUtils.run_external_command(
            ["python3", "-c", test_code],
            capture_output=True,
            timeout=10.0,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "timed out" in error_msg.lower():
                return FlextResult.fail("Import validation timed out")
            return FlextResult.fail(f"Import validation failed: {error_msg}")

        wrapper = result.unwrap()

        return FlextResult.ok(
            {
                "file": str(example_file),
                "imports_count": len(imports),
                "imports": imports,
                "status": "valid" if wrapper.returncode == 0 else "invalid",
                "error": wrapper.stderr if wrapper.returncode != 0 else None,
            }
        )

    except Exception as e:
        return FlextResult.fail(f"Import validation failed: {e}")


def run_example_safely(
    example_file: Path,
    timeout: int = 30,
) -> FlextResult[dict[str, object]]:
    """Safely run an example file with timeout and output capture.

    Args:
        example_file: Example file to run
        timeout: Timeout in seconds

    Returns:
        FlextResult with execution results

    """
    try:
        if not example_file.exists():
            return FlextResult.fail(f"File not found: {example_file}")

        result = SubprocessUtils.run_external_command(
            ["python3", str(example_file)],
            capture_output=True,
            timeout=timeout,
        )

        if result.is_failure:
            error_msg = result.error or ""
            if "timed out" in error_msg.lower():
                return FlextResult.fail(f"Example execution timed out after {timeout}s")
            return FlextResult.fail(f"Example execution failed: {error_msg}")

        wrapper = result.unwrap()

        return FlextResult.ok(
            {
                "file": str(example_file),
                "exit_code": wrapper.returncode,
                "status": "passed" if wrapper.returncode == 0 else "failed",
                "stdout": wrapper.stdout[:500],  # First 500 chars
                "stderr": wrapper.stderr[:500],  # First 500 chars
            }
        )

    except Exception as e:
        return FlextResult.fail(f"Example execution failed: {e}")
