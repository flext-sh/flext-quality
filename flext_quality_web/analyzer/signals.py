"""Signals for the analyzer Django app.

This module contains Django signals for handling code analysis events.
"""


# Quality analysis signals
def analysis_started(*args: object, **kwargs: object) -> None:
    def analysis_completed(*args: object, **kwargs: object) -> None:
        pass
