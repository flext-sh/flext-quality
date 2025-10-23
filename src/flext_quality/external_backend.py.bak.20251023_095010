"""External tools backend for security and quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import shutil
import tempfile
from importlib import import_module, util
from pathlib import Path
from typing import override

from flext_core import FlextResult, FlextUtilities

from .backend_type import BackendType
from .base import FlextQualityAnalyzer


class FlextQualityExternalBackend(FlextQualityAnalyzer):
    """Backend using external tools like ruff, mypy, bandit, vulture."""

    @override
    def get_backend_type(self: object) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self: object) -> list[str]:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture"]

    @override
    def analyze(
        self,
        _code: str,
        file_path: Path | None = None,
        tool: str = "ruff",
    ) -> FlextResult[dict[str, object]]:
        """Analyze code using external tools.

        Args:
        _code: Python source code to analyze
        file_path: Optional file path for context
        tool: Tool to use (ruff, mypy, bandit, vulture)

        Returns:
        Dictionary with analysis results

        """
        result: dict[str, object] = {"tool": "tool"}
        temp_path: Path | None = None

        if file_path:
            result["file_path"] = str(file_path)

        # Create temporary file for analysis
        try:
            with tempfile.NamedTemporaryFile(
                encoding="utf-8",
                mode="w",
                suffix=".py",
                delete=False,
            ) as f:
                f.write(_code)
                temp_path = Path(f.name)

            # Run the specified tool
            if tool == "ruff":
                ruff_result = self._run_ruff(_code, temp_path)
                if ruff_result.is_failure:
                    return FlextResult.fail(
                        f"Ruff analysis failed: {ruff_result.error}"
                    )
                result.update(ruff_result.value)
            elif tool == "mypy":
                mypy_result = self._run_mypy(_code, temp_path)
                if mypy_result.is_failure:
                    return FlextResult.fail(
                        f"MyPy analysis failed: {mypy_result.error}"
                    )
                result.update(mypy_result.value)
            elif tool == "bandit":
                bandit_result = self._run_bandit(_code, temp_path)
                if bandit_result.is_failure:
                    return FlextResult.fail(
                        f"Bandit analysis failed: {bandit_result.error}"
                    )
                result.update(bandit_result.value)
            elif tool == "vulture":
                vulture_result = self._run_vulture(_code, temp_path)
                if vulture_result.is_failure:
                    return FlextResult.fail(
                        f"Vulture analysis failed: {vulture_result.error}"
                    )
                result.update(vulture_result.value)
            else:
                return FlextResult.fail(f"Unknown tool: {tool}")

        except FileNotFoundError as e:
            return FlextResult.fail(f"Tool {tool} not found: {e}")
        except TimeoutError as e:
            return FlextResult.fail(f"Tool {tool} timed out: {e}")
        except Exception as e:
            return FlextResult.fail(f"Analysis failed: {e}")
        finally:
            # Clean up temp file
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

        return FlextResult.ok(result)

    def _convert_result_to_typed_dicts(
        self,
        result_list: list[object],
    ) -> list[dict[str, object]]:
        """Convert result list to properly typed dict[str, object] format."""
        typed_results: list[dict[str, object]] = []
        for item in result_list:
            if isinstance(item, dict):
                # Ensure all dict[str, object] values are properly typed as object
                typed_dict: dict[str, object] = dict[str, object](item.items())
                typed_results.append(typed_dict)
            else:
                # Convert non-dict items to dict[str, object] format
                typed_results.append({"raw": str(item)})
        return typed_results

    def _run_ruff(self, code: str, file_path: Path) -> FlextResult[dict[str, object]]:
        """Run ruff linter using subprocess."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return FlextResult.fail("Invalid file path")

            # Use absolute path for security
            abs_file_path = file_path.resolve()

            # Run ruff with JSON output format using validated executable path
            ruff_path = shutil.which("ruff")
            if not ruff_path:
                return FlextResult.ok({
                    "issues": [],
                    "ruff_available": False,
                })

            # Execute ruff with validated path and arguments only
            cmd_result = FlextUtilities.run_external_command(
                cmd=[ruff_path, "check", str(abs_file_path), "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=30.0,
                check=False,
            )

            if cmd_result.is_failure:
                return FlextResult.fail(f"Ruff execution failed: {cmd_result.error}")

            result = cmd_result.value
            issues = self._parse_ruff_output(result.stdout) if result.stdout else []

            return FlextResult.ok({
                "issues": issues,
                "code_length": len(code),
                "ruff_available": True,
            })

        except Exception as e:
            return FlextResult.fail(f"Ruff analysis failed: {e}")

    def _run_mypy(self, code: str, file_path: Path) -> FlextResult[dict[str, object]]:
        """Run mypy type checker."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return FlextResult.fail("Invalid file path")

            # Prefer in-process API; avoid subprocess PATH lookups per policy
            mypy_api = import_module("mypy.api") if util.find_spec("mypy.api") else None
            if mypy_api is None:
                return FlextResult.ok({
                    "issues": [],
                    "code_length": len(code),
                    "mypy_available": False,
                })

            stdout, _stderr, _status = mypy_api.run([str(file_path.resolve())])
            issues = self._parse_mypy_output(stdout)
            return FlextResult.ok({
                "issues": issues,
                "code_length": len(code),
                "mypy_available": True,
            })

        except Exception as e:
            return FlextResult.fail(f"MyPy analysis failed: {e}")

    def _run_bandit(self, code: str, file_path: Path) -> FlextResult[dict[str, object]]:
        """Run bandit security scanner."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for bandit to avoid S607

            # Bandit lacks a stable public Python API in our environment.
            # For security policy compliance, avoid spawning external processes here.
            # Advise manual execution through CLI integration.
            return {
                "error": "Bandit in-process execution not supported; run bandit -f json <file> manually",
                "code_length": len(code),
            }

        except Exception as e:
            return {"error": str(e)}

    def _run_vulture(
        self, code: str, file_path: Path
    ) -> FlextResult[dict[str, object]]:
        """Run vulture dead code detector."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for vulture to avoid S607

            # Vulture has no stable in-process API here; avoid subprocess for policy compliance.
            return {
                "error": "Vulture in-process execution not supported; run vulture <file> manually",
                "code_length": len(code),
            }

        except Exception as e:
            return {"error": str(e)}

    def _parse_ruff_output(self, output: str) -> list[dict[str, object]]:
        """Parse ruff JSON output."""
        try:
            if output.strip():
                result: FlextResult[object] = json.loads(output)
                # Safe type conversion
                if isinstance(result, list):
                    return self._convert_result_to_typed_dicts(result)
                return []
            return []
        except json.JSONDecodeError:
            return []

    def _parse_mypy_output(self, output: str) -> list[dict[str, object]]:
        """Parse mypy text output."""
        issues: list[dict[str, object]] = []
        for line in output.splitlines():
            if "error:" in line or "warning:" in line:
                issue: dict[str, object] = {"message": line.strip()}
                issues.append(issue)
        return issues
