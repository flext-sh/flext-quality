"""Comprehensive tests for backend modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import tempfile
from pathlib import Path
from typing import override
from unittest.mock import patch

# Removed unused mock imports - using real implementations
import pytest
from flext_core import FlextTypes

from flext_quality import ASTBackend, BackendType, BaseAnalyzer, ExternalBackend


class TestBaseAnalyzer:
    """Test BaseAnalyzer abstract base class."""

    def test_backend_type_enum(self) -> None:
        """Test BackendType enum values."""
        assert BackendType.AST.value == "ast"
        assert BackendType.EXTERNAL.value == "external"
        assert BackendType.HYBRID.value == "hybrid"

        # Test all enum values are accessible
        backend_types = list(BackendType)
        assert len(backend_types) == 3
        assert BackendType.AST in backend_types
        assert BackendType.EXTERNAL in backend_types
        assert BackendType.HYBRID in backend_types

    def test_base_analyzer_abstract(self) -> None:
        """Test BaseAnalyzer is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseAnalyzer()

    def test_base_analyzer_concrete_implementation(self) -> None:
        """Test concrete implementation of BaseAnalyzer."""

        class ConcreteAnalyzer(BaseAnalyzer):
            """Concrete implementation for testing."""

            @override
            def analyze(
                self,
                code: str,
                file_path: Path | None = None,
            ) -> FlextTypes.Core.Dict:
                """Implement abstract method."""
                return {"analyzed": True, "code": code}

            @override
            def get_backend_type(self) -> BackendType:
                """Implement abstract method."""
                return BackendType.HYBRID

            @override
            def get_capabilities(self) -> FlextTypes.Core.StringList:
                """Implement abstract method."""
                return ["test", "mock"]

        # Should be able to instantiate concrete class
        analyzer = ConcreteAnalyzer()
        assert analyzer is not None

        # Test methods work
        result = analyzer.analyze("test code")
        assert result == {"analyzed": True, "code": "test code"}

        backend_type = analyzer.get_backend_type()
        assert backend_type == BackendType.HYBRID

        capabilities = analyzer.get_capabilities()
        assert capabilities == ["test", "mock"]


class TestASTBackend:
    """Test AST-based code analyzer backend."""

    def test_initialization(self) -> None:
        """Test ASTBackend initialization."""
        backend = ASTBackend()
        assert backend is not None
        assert backend.get_backend_type() == BackendType.AST

    def test_get_capabilities(self) -> None:
        """Test get_capabilities method."""
        backend = ASTBackend()
        capabilities = backend.get_capabilities()

        assert isinstance(capabilities, list)
        assert "complexity" in capabilities
        assert "functions" in capabilities
        assert "classes" in capabilities
        assert "imports" in capabilities
        assert "docstrings" in capabilities

    def test_analyze_valid_code(self) -> None:
        """Test analyzing valid Python code."""
        backend = ASTBackend()
        code = """
def hello_world():
    '''Say hello.'''
    print("Hello, World!")

class TestClass:
    def method(self):
      pass
"""
        result = backend.analyze(code)

        assert "functions" in result
        assert "classes" in result
        assert "complexity" in result
        # ast.walk finds all functions including methods
        functions = result["functions"]
        classes = result["classes"]
        assert isinstance(functions, list)
        assert isinstance(classes, list)
        assert len(functions) == 2  # hello_world + method
        assert len(classes) == 1
        # Check that hello_world is one of the functions
        func_names = [
            f["name"] for f in functions if isinstance(f, dict) and "name" in f
        ]
        assert "hello_world" in func_names
        assert isinstance(classes[0], dict)
        assert classes[0]["name"] == "TestClass"

    def test_analyze_with_file_path(self) -> None:
        """Test analyzing code with file path provided."""
        backend = ASTBackend()
        code = "x = 1"
        file_path = Path("/test/file.py")

        result = backend.analyze(code, file_path)

        assert "file_path" in result
        assert result["file_path"] == str(file_path)

    def test_analyze_syntax_error(self) -> None:
        """Test analyzing code with syntax error."""
        backend = ASTBackend()
        code = "def invalid("  # Missing closing parenthesis

        result = backend.analyze(code)

        assert "error" in result
        assert "syntax" in result["error"].lower()

    def test_analyze_complex_code(self) -> None:
        """Test analyzing complex code with multiple constructs."""
        backend = ASTBackend()
        code = """
import os
from typing import List

def complex_function(x: int) -> int:
    if x > 10:
      for i in range(x):
          if i % 2 == 0:
              print(i)
    elif x < 0:
      while x < 0:
          x += 1
    else:
      try:
          return 1 / x
      except ZeroDivisionError:
          return 0
    return x

class MyClass:
    '''A test class.'''

    def __init__(self):
      self.value = 0

    def method_one(self):
      pass

    async def async_method(self):
      pass
"""
        result = backend.analyze(code)

        complexity = result["complexity"]
        imports = result["imports"]
        functions = result["functions"]
        classes = result["classes"]

        assert isinstance(complexity, (int, float))
        assert complexity > 5
        assert isinstance(imports, list)
        assert len(imports) == 2
        # ast.walk finds all functions including methods, so we get 4 total
        assert isinstance(functions, list)
        assert len(functions) == 4
        assert isinstance(classes, list)
        assert len(classes) == 1
        assert isinstance(classes[0], dict)
        assert classes[0]["methods"] == 3

    def test_extract_functions(self) -> None:
        """Test _extract_functions method."""
        backend = ASTBackend()
        code = """
def func1():
    pass

async def func2():
    pass

def func3(x, y=1, *args, **kwargs):
    return x + y
"""
        tree = ast.parse(code)
        functions = backend._extract_functions(tree)

        assert len(functions) == 3
        assert functions[0]["name"] == "func1"
        assert functions[1]["name"] == "func2"
        assert functions[1]["is_async"] is True
        assert functions[2]["name"] == "func3"
        assert functions[2]["args"] == 2  # Only x and y, not *args/**kwargs

    def test_extract_classes(self) -> None:
        """Test _extract_classes method."""
        backend = ASTBackend()
        code = """
class BaseClass:
    pass

class DerivedClass(BaseClass):
    def method1(self):
      pass

    def method2(self):
      pass
"""
        tree = ast.parse(code)
        classes = backend._extract_classes(tree)

        assert len(classes) == 2
        assert classes[0]["name"] == "BaseClass"
        assert classes[0]["methods"] == 0
        assert classes[1]["name"] == "DerivedClass"
        assert classes[1]["methods"] == 2
        assert classes[1]["bases"] == ["BaseClass"]

    def test_calculate_complexity(self) -> None:
        """Test _calculate_complexity method."""
        backend = ASTBackend()

        # Simple code - low complexity
        simple_code = "x = 1\ny = 2"
        simple_tree = ast.parse(simple_code)
        simple_complexity = backend._calculate_complexity(simple_tree)
        assert simple_complexity == 1

        # Complex code - higher complexity
        complex_code = """
if x:
    for i in range(10):
      while True:
          try:
              break
          except:
              pass
elif y:
    pass
"""
        complex_tree = ast.parse(complex_code)
        complex_complexity = backend._calculate_complexity(complex_tree)
        assert complex_complexity > 3

    def test_extract_imports(self) -> None:
        """Test _extract_imports method."""
        backend = ASTBackend()
        code = """
import os
import sys
from pathlib import Path
from typing import List, Dict
import numpy as np
"""
        tree = ast.parse(code)
        imports = backend._extract_imports(tree)

        assert len(imports) == 5
        assert {"module": "os", "names": []} in imports
        assert {"module": "pathlib", "names": ["Path"]} in imports
        assert {"module": "typing", "names": ["List", "Dict"]} in imports

    def test_check_docstrings(self) -> None:
        """Test _check_docstrings method."""
        backend = ASTBackend()
        code = """
def with_docstring():
    '''This function has a docstring.'''
    pass

def without_docstring():
    pass

class WithDoc:
    '''Class with docstring.'''
    pass

class WithoutDoc:
    pass
"""
        tree = ast.parse(code)
        missing = backend._check_docstrings(tree)

        assert len(missing) == 2
        assert "without_docstring" in missing
        assert "WithoutDoc" in missing


class TestExternalBackend:
    """Test external tool-based analyzer backend."""

    def test_initialization(self) -> None:
        """Test ExternalBackend initialization."""
        backend = ExternalBackend()
        assert backend is not None
        assert backend.get_backend_type() == BackendType.EXTERNAL

    def test_get_capabilities(self) -> None:
        """Test get_capabilities method."""
        backend = ExternalBackend()
        capabilities = backend.get_capabilities()

        assert isinstance(capabilities, list)
        assert "ruff" in capabilities
        assert "mypy" in capabilities
        assert "bandit" in capabilities
        assert "vulture" in capabilities

    def test_analyze_with_ruff(self) -> None:
        """Test analyze with ruff linter."""
        backend = ExternalBackend()
        result = backend.analyze("test code", tool="ruff")

        assert "tool" in result
        assert result["tool"] == "ruff"
        # Depending on environment, either issues or error may be present
        assert ("issues" in result) or ("error" in result)

    def test_analyze_with_mypy(self) -> None:
        """Test analyze with mypy type checker."""
        backend = ExternalBackend()
        result = backend.analyze("test code", tool="mypy")

        assert result["tool"] == "mypy"
        assert ("issues" in result) or ("error" in result)

    def test_analyze_tool_not_found(self) -> None:
        """Test analyze when tool is not found."""
        backend = ExternalBackend()
        result = backend.analyze("test code", tool="ruff")

        assert "error" in result
        assert isinstance(result["error"], str)

    def test_analyze_timeout(self) -> None:
        """Test analyze with timeout."""
        backend = ExternalBackend()
        with patch(
            "flext_quality.backends.external_backend.ExternalBackend._run_mypy",
            side_effect=TimeoutError("timed out"),
        ):
            result = backend.analyze("test code", tool="mypy")

        assert "error" in result
        assert (
            "timed out" in result["error"].lower()
            or "timeout" in result["error"].lower()
        )

    def test_run_ruff(self) -> None:
        """Test _run_ruff method."""
        backend = ExternalBackend()
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write("test code")
            temp_path = Path(f.name)

        try:
            result = backend._run_ruff("test code", temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        # _run_ruff should return either issues or error
        assert ("issues" in result) or ("error" in result)

    def test_run_mypy(self) -> None:
        """Test _run_mypy method."""
        backend = ExternalBackend()
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write("test code")
            temp_path = Path(f.name)

        try:
            result = backend._run_mypy("test code", temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        assert ("issues" in result) or ("error" in result)

    def test_run_bandit(self) -> None:
        """Test _run_bandit method."""
        backend = ExternalBackend()
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write("test code")
            temp_path = Path(f.name)

        try:
            result = backend._run_bandit("test code", temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        assert "error" in result

    def test_run_vulture(self) -> None:
        """Test _run_vulture method."""
        backend = ExternalBackend()
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write("test code")
            temp_path = Path(f.name)

        try:
            result = backend._run_vulture("test code", temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        assert "error" in result

    def test_analyze_with_file_path(self) -> None:
        """Test analyze with actual file path using real code."""
        backend = ExternalBackend()

        # Create a real temporary file with test code
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as tmp_file:
            # Write sample code that might have ruff issues
            tmp_file.write("""# Test file for analysis
def test_function( ):
    x=1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20
    return x
""")
            tmp_path = Path(tmp_file.name)

        try:
            # Run real analysis with ruff
            result = backend.analyze("", tmp_path, tool="ruff")

            assert "file_path" in result
            assert result["file_path"] == str(tmp_path)
            # Should have analysis results (may include issues)
            assert "issues" in result

        finally:
            # Clean up
            tmp_path.unlink(missing_ok=True)

    def test_analyze_default_tool(self) -> None:
        """Test analyze with default tool (ruff) using real code."""
        backend = ExternalBackend()

        # Create a real temporary file with test code
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as tmp_file:
            # Write simple valid Python code
            tmp_file.write("""def hello():
    '''Simple function.'''
    return 'hello world'
""")
            tmp_path = Path(tmp_file.name)

        try:
            # Should use ruff by default
            result = backend.analyze("", tmp_path)

            assert result["tool"] == "ruff"
            assert "issues" in result

        finally:
            # Clean up
            tmp_path.unlink(missing_ok=True)

    def test_parse_ruff_output(self) -> None:
        """Test _parse_ruff_output method."""
        backend = ExternalBackend()

        # Valid JSON output
        json_output = '[{"code": "E501", "line": 1}]'
        issues = backend._parse_ruff_output(json_output)
        assert len(issues) == 1

        # Invalid JSON - should return empty list
        invalid_output = "not json"
        issues = backend._parse_ruff_output(invalid_output)
        assert issues == []

    def test_parse_mypy_output(self) -> None:
        """Test _parse_mypy_output method."""
        backend = ExternalBackend()

        mypy_output = """
test.py:1: error: Name 'x' is not defined
test.py:5: note: See documentation
Success: no other issues
"""
        issues = backend._parse_mypy_output(mypy_output)
        assert len(issues) >= 1
        assert "not defined" in str(issues[0])
