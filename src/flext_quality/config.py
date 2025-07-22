"""Configuration module bridge for backward compatibility.

This module provides backward compatibility by re-exporting
QualityConfig from infrastructure.config.
"""

from __future__ import annotations

# Re-export from infrastructure for backward compatibility
from flext_quality.infrastructure.config import QualityConfig

__all__ = ["QualityConfig"]
