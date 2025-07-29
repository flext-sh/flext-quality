"""External tools backend for security and quality analysis."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, ClassVar

from analyzer.backends.base import AnalysisBackend, AnalysisResult


class ExternalToolsBackend(AnalysisBackend):
    """Backend using external tools like bandit, vulture, etc."""

    # Trusted tool paths - only these are allowed to be executed
    TRUSTED_TOOLS: ClassVar[dict[str, str]] = {
        "bandit": "bandit",
        "vulture": "vulture",
    }

    @property
    def name(self) -> str:
        """Return the name of this backend."""
        return "external"

    @property
    def description(self) -> str:
        """Return the description of this backend."""
        return "External tools for security and dead code analysis"

    @property
    def capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        return [
            "security_analysis",
            "dead_code_analysis",
            "dependency_analysis",
        ]

    def _get_tool_path(self, tool_name: str) -> str | None:
        """Get the absolute path of a trusted tool.

        Returns:
            Absolute path to the tool if found and trusted, None otherwise.

        """
        if tool_name not in self.TRUSTED_TOOLS:
            return None

        return shutil.which(self.TRUSTED_TOOLS[tool_name])

    def _validate_file_path(self, file_path: Path) -> bool:
        """Validate that the file path is safe to process.

        Args:
            file_path: Path to validate

        Returns:
            True if path is safe, False otherwise.

        """
        try:
            # Resolve path and ensure it's a Python file within project
            resolved_path = file_path.resolve()

            # Check if it's a Python file
            if resolved_path.suffix != ".py":
                return False

            # Check if it's within the project directory
            project_resolved = self.project_path.resolve()
            try:
                resolved_path.relative_to(project_resolved)
            except ValueError:
                # Path is outside project directory
                return False
            else:
                return True

        except (OSError, ValueError):
            return False

    def is_available(self) -> bool:
        """Check if external tools are available."""
        for tool_name in self.TRUSTED_TOOLS:
            tool_path = self._get_tool_path(tool_name)
            if not tool_path:
                self.logger.warning("Tool %s not available", tool_name)
                return False

            try:
                # Use absolute path to prevent execution of untrusted binaries
                subprocess.run(
                    [tool_path, "--version"],
                    capture_output=True,
                    check=True,
                    timeout=10,
                )
            except (
                subprocess.CalledProcessError,
                FileNotFoundError,
                subprocess.TimeoutExpired,
            ):
                self.logger.warning("Tool %s not available", tool_name)
                return False
        return True

    def analyze(self, python_files: list[Path]) -> AnalysisResult:
        """Run analysis using external tools."""
        result = AnalysisResult()

        if not python_files:
            return result

        # Run bandit for security analysis
        try:
            security_issues = self._run_bandit(python_files)
            result.security_issues.extend(security_issues)
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Bandit analysis failed")
            result.errors.append(
                {"tool": "bandit", "error": str(e), "backend": self.name},
            )

        # Run vulture for dead code analysis
        try:
            dead_code_issues = self._run_vulture(python_files)
            # Add to results (you might want to create a separate field)
            result.quality_metrics["dead_code_issues"] = dead_code_issues
        except (RuntimeError, ValueError, TypeError) as e:
            self.logger.exception("Vulture analysis failed")
            result.errors.append(
                {"tool": "vulture", "error": str(e), "backend": self.name},
            )

        return result

    def _run_bandit(self, python_files: list[Path]) -> list[dict[str, Any]]:
        """Run bandit security analysis on Python files.

        Args:
            python_files: List of Python files to analyze

        Returns:
            List of security issues found by bandit.

        """
        security_issues: list[dict[str, Any]] = []

        # Get secure tool path
        bandit_path = self._get_tool_path("bandit")
        if not bandit_path:
            self.logger.error("Bandit tool not available")
            return security_issues

        # Validate all file paths
        safe_files = []
        for file_path in python_files:
            if self._validate_file_path(file_path):
                safe_files.append(str(file_path.resolve()))
            else:
                self.logger.warning("Skipping unsafe file path: %s", file_path)

        if not safe_files:
            self.logger.warning("No safe files to analyze with bandit")
            return security_issues

        try:
            # Run bandit with validated inputs
            cmd = [bandit_path, "-f", "json", "-ll", *safe_files]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.project_path.resolve()),
                check=False,
            )

            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    for issue in data.get("results", []):
                        security_issue = {
                            "file_path": self._get_relative_path(
                                Path(issue["filename"]),
                            ),
                            "line_number": issue["line_number"],
                            "issue_type": issue["test_name"],
                            "severity": issue["issue_severity"],
                            "confidence": issue["issue_confidence"],
                            "description": issue["issue_text"],
                            "code_snippet": issue.get("code", ""),
                            "cwe_id": issue.get("cwe", {}).get("id", ""),
                            "more_info": issue.get("more_info", ""),
                        }
                        security_issues.append(security_issue)
                except json.JSONDecodeError:
                    self.logger.exception("Failed to parse bandit JSON output")

        except (RuntimeError, ValueError, TypeError):
            self.logger.exception("Bandit execution failed")

        return security_issues

    def _run_vulture(self, python_files: list[Path]) -> list[dict[str, Any]]:
        """Run vulture dead code analysis on Python files.

        Args:
            python_files: List of Python files to analyze

        Returns:
            List of dead code issues found by vulture.

        """
        dead_code_issues: list[dict[str, Any]] = []

        # Get secure tool path
        vulture_path = self._get_tool_path("vulture")
        if not vulture_path:
            self.logger.error("Vulture tool not available")
            return dead_code_issues

        # Validate all file paths
        safe_files = []
        for file_path in python_files:
            if self._validate_file_path(file_path):
                safe_files.append(str(file_path.resolve()))
            else:
                self.logger.warning("Skipping unsafe file path: %s", file_path)

        if not safe_files:
            self.logger.warning("No safe files to analyze with vulture")
            return dead_code_issues

        try:
            cmd = [vulture_path, "--json", *safe_files]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.project_path.resolve()),
                check=False,
            )

            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    for issue in data:
                        dead_code_issue = {
                            "file_path": self._get_relative_path(
                                Path(issue["filename"]),
                            ),
                            "line_number": issue["lineno"],
                            "issue_type": issue["typ"],
                            "name": issue["name"],
                            "message": issue["message"],
                            "confidence": issue.get("confidence", 100),
                        }
                        dead_code_issues.append(dead_code_issue)
                except json.JSONDecodeError:
                    self.logger.exception("Failed to parse vulture JSON output")

        except (RuntimeError, ValueError, TypeError):
            self.logger.exception("Vulture execution failed")

        return dead_code_issues
