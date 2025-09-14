#!/usr/bin/env python3
"""Script para testar progresso sem interferência cross-project."""

import asyncio
import os
import sys
from pathlib import Path
from subprocess import CompletedProcess

from flext_core import FlextTypes


def run_tests() -> "CompletedProcess[str]":
    """Executa testes sem interferência."""
    # Change to project directory
    project_dir = Path(__file__).parent
    original_dir = Path.cwd()

    try:
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

        async def _run(cmd_list: FlextTypes.Core.StringList) -> tuple[int, str, str]:
            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            # Ensure returncode is not None
            returncode = process.returncode if process.returncode is not None else -1
            return returncode, stdout.decode(), stderr.decode()

        rc, out, err = asyncio.run(_run(cmd))

        return CompletedProcess(args=cmd, returncode=rc, stdout=out, stderr=err)

    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    result = run_tests()
    sys.exit(result.returncode)
