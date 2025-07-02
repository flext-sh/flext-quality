from typing import Any


# Quality analysis signals
def analysis_started(*args: Any, **kwargs: Any) -> None:
    """Signal for when analysis starts."""
    pass


def analysis_completed(*args: Any, **kwargs: Any) -> None:
    """Signal for when analysis completes."""
    pass
