"""Signals for the analyzer Django app.

This module contains Django signals for handling code analysis events.
"""

from typing import Any


# Quality analysis signals
def analysis_started(*args: Any, **kwargs: object) -> None:
    def analysis_completed(*args: Any, **kwargs: object) -> None:
        pass
