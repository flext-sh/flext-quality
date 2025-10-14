"""Extra coverage tests for AST backend internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_quality import ASTBackend


def test_ast_backend_syntax_error() -> None:
    """Ensure syntax errors are reported in analyze()."""
    backend = ASTBackend()
    # Missing colon
    result = backend.analyze("def foo()\n    return 1")
    assert "error" in result
    error_msg = result["error"]
    assert isinstance(error_msg, str)
    assert "Syntax error" in error_msg
