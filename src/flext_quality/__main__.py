"""Console script entrypoint for flext-quality.

Thin wrapper to invoke `flext_quality.cli.main`.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import sys

from flext_quality.cli import main

if __name__ == "__main__":
    sys.exit(main())
