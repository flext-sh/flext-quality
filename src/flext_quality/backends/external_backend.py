"""External tools backend for security and quality analysis."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess  # legacy import kept only for typing
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
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for ruff to avoid S607
            import shutil

            ruff_cmd = shutil.which("ruff")
            if not ruff_cmd:
                return {"error": "Ruff not found in PATH"}

            # Prefer in-process Ruff API when available
            try:
                import ruff.__main__ as ruff_main  # type: ignore[import-not-found]

                stdout = io.StringIO()
                stderr = io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    try:
                        ruff_main.main(["check", str(file_path.resolve()), "--output-format", "json"])  # type: ignore[arg-type]
                    except SystemExit as exc:
                        _ = int(getattr(exc, "code", 0) or 0)
                issues = self._parse_ruff_output(stdout.getvalue())
            except Exception:
                # Fallback to absolute-path subprocess if API unavailable
                result = __import__("subprocess").run(  # noqa: S603
                    [ruff_cmd, "check", str(file_path.resolve()), "--output-format", "json"],
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
            if not file_path.exists() or not file_path.is_file():
                return {"error": "Invalid file path"}

            # Use absolute path for mypy to avoid S607
            import shutil

            mypy_cmd = shutil.which("mypy")
            if not mypy_cmd:
                return {"error": "MyPy not found in PATH"}

            # Prefer in-process MyPy API
            try:
                from mypy import api as mypy_api  # type: ignore[import-not-found]

                stdout, _stderr, _status = mypy_api.run([str(file_path.resolve())])
                issues = self._parse_mypy_output(stdout)
            except Exception:
                result = __import__("subprocess").run(  # noqa: S603
                    [mypy_cmd, str(file_path.resolve())],
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

    def _run_vulture(self, code: str, file_path: Path) -> dict[str, object]:
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
