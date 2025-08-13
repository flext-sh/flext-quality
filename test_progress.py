#!/usr/bin/env python3
"""Script para testar progresso sem interferência cross-project."""

import subprocess
import sys
from pathlib import Path


def run_tests() -> subprocess.CompletedProcess[str]:
    """Executa testes sem interferência."""
    # Change to project directory
    project_dir = Path(__file__).parent
    original_dir = Path.cwd()

    try:
        import os

        os.chdir(project_dir)

        # Isolar pytest apenas para este projeto
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--tb=no",
            "-q",
            "--confcutdir=.",  # Apenas conftest local
            "--disable-warnings",
        ]

        return subprocess.run(cmd, check=False, capture_output=True, text=True)  # noqa: S603 - Test runner command, cmd is constructed from known pytest args

    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    result = run_tests()
    sys.exit(result.returncode)
