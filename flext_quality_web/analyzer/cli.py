#!/usr/bin/env python3
"""Command-line interface for the code analyzer."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from django.core.management import execute_from_command_line


def main() -> None:
    """Run the dc-code-analyzer command-line interface."""
    # Add the current directory to Python path
    current_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(current_dir))

    # Import and run Django management
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "code_analyzer_web.settings")

    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(msg) from exc


if __name__ == "__main__":
    main()
