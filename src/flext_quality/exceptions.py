"""FLEXT Quality Exceptions - Simple exception classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


class FlextQualityException(Exception):
    """Base exception for FLEXT Quality."""


class AnalysisError(FlextQualityException):
    """Raised when analysis fails."""


class ConfigError(FlextQualityException):
    """Raised when configuration is invalid."""


class ModelError(FlextQualityException):
    """Raised when model creation/validation fails."""


class FlextQualityExceptions:
    """Exception classes namespace."""

    Base = FlextQualityException
    Analysis = AnalysisError
    Config = ConfigError
    Model = ModelError
