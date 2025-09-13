"""Backend type enumeration for FLEXT Quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum

"""

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


class BackendType(Enum):
    """Enumeration of backend types."""

    AST = "ast"
    EXTERNAL = "external"
    HYBRID = "hybrid"
