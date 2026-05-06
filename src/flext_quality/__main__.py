"""CLI entrypoint for python -m flext_quality."""

from __future__ import annotations

from flext_cli import cli
from flext_quality import main

if __name__ == "__main__":
    cli.exit(main())
