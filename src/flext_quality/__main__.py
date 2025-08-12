"""Console script entrypoint for flext-quality.

Thin wrapper to invoke `flext_quality.cli.main`.
"""

import sys

from flext_quality.cli import main

if __name__ == "__main__":
    sys.exit(main())
