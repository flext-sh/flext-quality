"""FLEXT Quality Command Strategies - Re-export from constants module.

Command execution strategy thresholds are defined in FlextQualityConstants.Quality.CommandStrategies.

Import from constants directly:
```python
from flext_quality.constants import FlextQualityConstants as c

threshold = c.Quality.CommandStrategies.Analysis.SUCCESS_THRESHOLD
```

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.constants import FlextQualityConstants

# Re-export CommandStrategies for backward compatibility
CommandStrategies = FlextQualityConstants.Quality.CommandStrategies

__all__ = ["CommandStrategies"]
