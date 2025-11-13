"""FLEXT Quality Exceptions - Simple exception classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


class FlextQualityError(Exception):
    """Base exception for FLEXT Quality."""


class AnalysisError(FlextQualityError):
    """Raised when analysis fails."""


class ConfigError(FlextQualityError):
    """Raised when configuration is invalid."""


class ModelError(FlextQualityError):
    """Raised when model creation/validation fails."""


class FlextQualityExceptions:
    """Exception classes namespace."""

    Base = FlextQualityError
    Analysis = AnalysisError
    Config = ConfigError
    Model = ModelError
