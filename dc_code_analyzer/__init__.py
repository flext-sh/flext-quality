"""DC Code Analyzer - Advanced Python code analysis tool."""

__version__ = "0.1.0"
__author__ = "Code Analysis Team"
__email__ = "team@codeanalyzer.dev"


# Import main components
try:
    from dc_code_analyzer import analyzer, code_analyzer_web, dashboard
except ImportError:
    # Fallback for development mode
    pass

__all__ = ["analyzer", "code_analyzer_web", "dashboard"]
