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

from flext_core import FlextCore

from .backend_type import BackendType
from .base import BaseAnalyzer


class FlextQualityExternalBackend(BaseAnalyzer):
    """Backend using external tools like ruff, mypy, bandit, vulture."""

    @override
    def get_backend_type(self: object) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self: object) -> FlextCore.Types.StringList:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture"]

    @override
    def analyze(
        self,
        _code: str,
        file_path: Path | None = None,
        tool: str = "ruff",
    ) -> FlextCore.Types.Dict:
        """Analyze code using external tools.

        Args:
            _code: Python source code to analyze
            file_path: Optional file path for context
            tool: Tool to use (ruff, mypy, bandit, vulture)

        Returns:
            Dictionary with analysis results

        """
        result: FlextCore.Types.Dict = {"tool": "tool"}
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
                result.update(self._run_ruff(_code, temp_path))
            elif tool == "mypy":
                result.update(self._run_mypy(_code, temp_path))
            elif tool == "bandit":
                result.update(self._run_bandit(_code, temp_path))
            elif tool == "vulture":
                result.update(self._run_vulture(_code, temp_path))
            else:
                result["error"] = f"Unknown tool: {tool}"

        except FileNotFoundError:
            result["error"] = f"Tool {tool} not found"
        except TimeoutError:
            result["error"] = f"Tool {tool} timed out"
        except Exception as e:
            result["error"] = str(e)
        finally:
            # Clean up temp file
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

        return result

    def _convert_result_to_typed_dicts(
        self,
        result_list: FlextCore.Types.List,
    ) -> list[FlextCore.Types.Dict]:
        """Convert result list to properly typed dict[str, object] format."""
        typed_results: list[FlextCore.Types.Dict] = []
        for item in result_list:
            if isinstance(item, dict):
                # Ensure all dict[str, object] values are properly typed as object
                typed_dict: FlextCore.Types.Dict = dict[str, object](item.items())
                typed_results.append(typed_dict)
            else:
                # Convert non-dict items to dict[str, object] format
                typed_results.append({"raw": str(item)})
        return typed_results

    def _run_ruff(self, code: str, file_path: Path) -> FlextCore.Types.Dict:
        """Run ruff linter using subprocess."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use subprocess to run ruff - secure way with explicit path

            # Use absolute path for security
            abs_file_path = file_path.resolve()

            # Run ruff with JSON output format using validated executable path
            ruff_path = shutil.which("ruff")
            if not ruff_path:
                return {
                    "issues": [],
                    "ruff_available": "False",
                }  # Return empty dict[str, object] if ruff is not available

            # Execute ruff with validated path and arguments only
            cmd_result = FlextCore.Utilities.run_external_command(
                cmd=[ruff_path, "check", str(abs_file_path), "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=30.0,  # Prevent hanging
                check=False,  # Don't raise exception on non-zero exit
            )

            # Handle execution failure
            if cmd_result.is_failure:
                return {"error": f"Ruff execution failed: {cmd_result.error}"}

            result = cmd_result.value

            # Parse output even if ruff found issues (non-zero exit is expected)
            (self._parse_ruff_output(result.stdout) if result.stdout else [])

            return {"issues": "issues", "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_mypy(self, code: str, file_path: Path) -> FlextCore.Types.Dict:
        """Run mypy type checker."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Prefer in-process API; avoid subprocess PATH lookups per policy

            # Prefer in-process MyPy API
            mypy_api = import_module("mypy.api") if util.find_spec("mypy.api") else None
            if mypy_api is None:
                # Evita uso de subprocess; orienta execução manual
                return {
                    "error": "MyPy in-process API indisponível; execute manualmente: mypy <file>",
                    "code_length": len(code),
                }
            stdout, _stderr, _status = mypy_api.run([str(file_path.resolve())])
            self._parse_mypy_output(stdout)
            return {"issues": "issues", "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_bandit(self, code: str, file_path: Path) -> FlextCore.Types.Dict:
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

    def _run_vulture(self, code: str, file_path: Path) -> FlextCore.Types.Dict:
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

    def _parse_ruff_output(self, output: str) -> list[FlextCore.Types.Dict]:
        """Parse ruff JSON output."""
        try:
            if output.strip():
                result: FlextCore.Result[object] = json.loads(output)
                # Safe type conversion
                if isinstance(result, list):
                    return self._convert_result_to_typed_dicts(result)
                return []
            return []
        except json.JSONDecodeError:
            return []

    def _parse_mypy_output(self, output: str) -> list[FlextCore.Types.Dict]:
        """Parse mypy text output."""
        issues: list[FlextCore.Types.Dict] = []
        for line in output.splitlines():
            if "error:" in line or "warning:" in line:
                issue: FlextCore.Types.Dict = {"message": line.strip()}
                issues.append(issue)
        return issues
