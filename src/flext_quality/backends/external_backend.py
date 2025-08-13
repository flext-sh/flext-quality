"""External tools backend for security and quality analysis."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from flext_quality.backends.base import (
    BackendType,
    BaseAnalyzer,
)


class ExternalBackend(BaseAnalyzer):
    """Backend using external tools like ruff, mypy, bandit, vulture."""

    def get_backend_type(self) -> BackendType:
        """Return the backend type."""
        return BackendType.EXTERNAL

    def get_capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        return ["ruff", "mypy", "bandit", "vulture"]

    def analyze(
        self,
        code: str,
        file_path: Path | None = None,
        tool: str = "ruff",
    ) -> dict[str, object]:
        """Analyze code using external tools.

        Args:
            code: Python source code to analyze
            file_path: Optional file path for context
            tool: Tool to use (ruff, mypy, bandit, vulture)

        Returns:
            Dictionary with analysis results

        """
        result: dict[str, object] = {"tool": tool}

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
        except subprocess.TimeoutExpired:
            result["error"] = f"Tool {tool} timed out"
        except Exception as e:
            result["error"] = str(e)
        finally:
            # Clean up temp file
            if "temp_path" in locals():
                temp_path.unlink(missing_ok=True)

        return result

    def _run_ruff(self, code: str, file_path: Path) -> dict[str, object]:
        """Run ruff linter."""
        try:
            # Validate file path is safe (no shell injection)
            safe_path = str(file_path.resolve())
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for ruff to avoid S607
            import shutil

            ruff_cmd = shutil.which("ruff")
            if not ruff_cmd:
                return {"error": "Ruff not found in PATH"}

            # Safe invocation of external tool without shell, fixed timeout
            result = subprocess.run(  # noqa: S603
                [ruff_cmd, "check", safe_path, "--output-format", "json"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            issues = self._parse_ruff_output(result.stdout)
            return {"issues": issues, "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_mypy(self, code: str, file_path: Path) -> dict[str, object]:
        """Run mypy type checker."""
        try:
            # Validate file path is safe (no shell injection)
            safe_path = str(file_path.resolve())
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for mypy to avoid S607
            import shutil

            mypy_cmd = shutil.which("mypy")
            if not mypy_cmd:
                return {"error": "MyPy not found in PATH"}

            # Safe invocation of external tool without shell, fixed timeout
            result = subprocess.run(  # noqa: S603
                [mypy_cmd, safe_path],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            issues = self._parse_mypy_output(result.stdout)
            return {"issues": issues, "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_bandit(self, code: str, file_path: Path) -> dict[str, object]:
        """Run bandit security scanner."""
        try:
            # Validate file path is safe (no shell injection)
            safe_path = str(file_path.resolve())
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for bandit to avoid S607
            import shutil

            bandit_cmd = shutil.which("bandit")
            if not bandit_cmd:
                return {"error": "Bandit not found in PATH"}

            # Safe invocation of external tool without shell, fixed timeout
            result = subprocess.run(  # noqa: S603
                [bandit_cmd, "-f", "json", safe_path],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.stdout:
                data = json.loads(result.stdout)
                return {"issues": data.get("results", []), "code_length": len(code)}
            return {"issues": [], "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _run_vulture(self, code: str, file_path: Path) -> dict[str, object]:
        """Run vulture dead code detector."""
        try:
            # Validate file path is safe (no shell injection)
            safe_path = str(file_path.resolve())
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for vulture to avoid S607
            import shutil

            vulture_cmd = shutil.which("vulture")
            if not vulture_cmd:
                return {"error": "Vulture not found in PATH"}

            # Safe invocation of external tool without shell, fixed timeout
            result = subprocess.run(  # noqa: S603
                [vulture_cmd, safe_path],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            dead_code = [
                line.strip() for line in result.stdout.splitlines() if line.strip()
            ]

            return {"dead_code": dead_code, "code_length": len(code)}

        except Exception as e:
            return {"error": str(e)}

    def _parse_ruff_output(self, output: str) -> list[dict[str, object]]:
        """Parse ruff JSON output."""
        try:
            if output.strip():
                result = json.loads(output)
                # Ensure we return the proper type by casting the result
                return result if isinstance(result, list) else []
            return []
        except json.JSONDecodeError:
            return []

    def _parse_mypy_output(self, output: str) -> list[dict[str, object]]:
        """Parse mypy text output."""
        return [
            {"message": line.strip()}
            for line in output.splitlines()
            if "error:" in line or "warning:" in line
        ]
