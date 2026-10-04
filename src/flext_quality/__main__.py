"""CLI entrypoint for python -m flext_quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import cli

from flext_quality import main

if __name__ == "__main__":
    cli.exit(main())
