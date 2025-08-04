#!/usr/bin/env python3
"""Script para testar progresso sem interferência cross-project."""

import subprocess
import sys
from pathlib import Path

def run_tests():
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
            "-m", "pytest",
            "tests/",
            "--tb=no",
            "-q",
            "--confcutdir=.",  # Apenas conftest local
            "--disable-warnings"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("RETURN CODE:", result.returncode)

        return result

    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    run_tests()
