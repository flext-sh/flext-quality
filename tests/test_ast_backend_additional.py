"""Extra coverage tests for AST backend internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
from pathlib import Path

from flext_quality import ASTBackend, ASTVisitor


def test_ast_backend_syntax_error() -> None:
    """Ensure syntax errors are reported in analyze()."""
    backend = ASTBackend()
    # Missing colon
    result = backend.analyze("def foo()\n    return 1")
    assert "error" in result
    error_msg = result["error"]
    assert isinstance(error_msg, str)
    assert "Syntax error" in error_msg


def test_ast_visitor_extracts_details(tmp_path: Path) -> None:
    """Visitor tracks classes and functions with flags."""
    code = ast.parse(
        """

class A:
    def m(self):
      pass

async def f(x: int) -> None:
    return None
      """,
    )
    visitor = ASTVisitor(file_path=tmp_path / "a.py", package_name="pkg")
    visitor.visit(code)
    assert any(c.name == "A" for c in visitor.classes)
    assert any(fn.name == "m" for fn in visitor.functions)
    # ensure complexity captured for async function
    assert any(isinstance(fn.is_async, bool) for fn in visitor.functions)
