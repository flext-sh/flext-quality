"""External tools backend for security and quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import shutil
import subprocess  # nosec B404 # Required for external tool integration
import tempfile
import warnings
from importlib import import_module, util
from pathlib import Path
from typing import override

from flext_core import FlextTypes

from flext_quality.backend_type import BackendType
from flext_quality.base import BaseAnalyzer


class FlextQualityExternalBackend(BaseAnalyzer):
    """Backend using external tools like ruff, mypy, bandit, vulture."""

    @override
    def get_backend_type(self) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    @override
    def get_capabilities(self) -> FlextTypes.Core.StringList:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture"]

    @override
    def analyze(
        self,
        code: str,
        file_path: Path | None = None,
        tool: str = "ruff",
    ) -> FlextTypes.Core.Dict:
        """Analyze code using external tools.

        Args:
            code: Python source code to analyze
            file_path: Optional file path for context
            tool: Tool to use (ruff, mypy, bandit, vulture)

        Returns:
            Dictionary with analysis results

        """
        result: FlextTypes.Core.Dict = {"tool": tool}
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
                f.write(code)
                temp_path = Path(f.name)

            # Run the specified tool
            if tool == "ruff":
                result.update(self._run_ruff(code, temp_path))
            elif tool == "mypy":
                result.update(self._run_mypy(code, temp_path))
            elif tool == "bandit":
                result.update(self._run_bandit(code, temp_path))
            elif tool == "vulture":
                result.update(self._run_vulture(code, temp_path))
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
        self, result_list: FlextTypes.Core.List
    ) -> list[FlextTypes.Core.Dict]:
        """Convert result list to properly typed dict format."""
        typed_results: list[FlextTypes.Core.Dict] = []
        for item in result_list:
            if isinstance(item, dict):
                # Ensure all dict values are properly typed as object
                typed_dict: FlextTypes.Core.Dict = dict(item.items())
                typed_results.append(typed_dict)
            else:
                # Convert non-dict items to dict format
                typed_results.append({"raw": str(item)})
        return typed_results

    def _run_ruff(self, code: str, file_path: Path) -> FlextTypes.Core.Dict:
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
                    "ruff_available": False,
                }  # Return empty dict if ruff is not available

            result = subprocess.run(  # nosec B603 # Validated ruff execution with timeout
                [ruff_path, "check", str(abs_file_path), "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=30,  # Prevent hanging
                check=False,  # Don't raise exception on non-zero exit
            )

            # Parse output even if ruff found issues (non-zero exit is expected)
            issues = self._parse_ruff_output(result.stdout) if result.stdout else []

            return {"issues": issues, "code_length": len(code)}

        except subprocess.TimeoutExpired:
            return {"error": "Ruff execution timed out"}
        except FileNotFoundError:
            return {
                "error": "Ruff not found; install with: pip install ruff",
                "code_length": len(code),
            }
        except Exception as e:
            return {"error": str(e)}

    def _run_mypy(self, code: str, file_path: Path) -> FlextTypes.Core.Dict:
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
                    "error": "MyPy in-process API indisponível; execute manualmente: 'mypy <file>'",
                    "code_length": len(code),
                }
            stdout, _stderr, _status = mypy_api.run([str(file_path.resolve())])
            issues = self._parse_mypy_output(stdout)
            return {"issues": issues, "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_bandit(self, code: str, file_path: Path) -> FlextTypes.Core.Dict:
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
                "error": "Bandit in-process execution not supported; run 'bandit -f json <file>' manually",
                "code_length": len(code),
            }

        except Exception as e:
            return {"error": str(e)}

    def _run_vulture(self, code: str, file_path: Path) -> FlextTypes.Core.Dict:
        """Run vulture dead code detector."""
        try:
            # Validate file path is safe (no shell injection)
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for vulture to avoid S607

            # Vulture has no stable in-process API here; avoid subprocess for policy compliance.
            return {
                "error": "Vulture in-process execution not supported; run 'vulture <file>' manually",
                "code_length": len(code),
            }

        except Exception as e:
            return {"error": str(e)}

    def _parse_ruff_output(self, output: str) -> list[FlextTypes.Core.Dict]:
        """Parse ruff JSON output."""
        try:
            if output.strip():
                result = json.loads(output)
                # Safe type conversion
                if isinstance(result, list):
                    return self._convert_result_to_typed_dicts(result)
                return []
            return []
        except json.JSONDecodeError:
            return []

    def _parse_mypy_output(self, output: str) -> list[FlextTypes.Core.Dict]:
        """Parse mypy text output."""
        issues: list[FlextTypes.Core.Dict] = []
        for line in output.splitlines():
            if "error:" in line or "warning:" in line:
                issue: FlextTypes.Core.Dict = {"message": line.strip()}
                issues.append(issue)
        return issues


# Legacy compatibility facade (TEMPORARY)
class ExternalBackend(FlextQualityExternalBackend):
    """Legacy external backend class - replaced by FlextQualityExternalBackend.

    DEPRECATED: Use FlextQualityExternalBackend directly.
    This facade provides compatibility during migration.
    """

    def __init__(self) -> None:
        """Initialize the instance."""
        warnings.warn(
            "ExternalBackend is deprecated; use FlextQualityExternalBackend",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()
