"""Infrastructure Layer - External Dependencies and Adapters.

This module contains all external dependencies, third-party integrations,
and adapter implementations that connect the application to the outside world.
Follows Clean Architecture by implementing interfaces defined in the domain layer.

Key Components:
    - Repository Adapters: Data persistence implementations
    - External Tool Integrations: Ruff, MyPy, Bandit, Security scanners
    - File System Adapters: Code analysis and file processing
    - Database Adapters: Quality metrics and analysis result storage
    - Messaging Adapters: Event publishing and notification systems

Tool Integrations:
    - RuffAnalyzer: Python linting and code quality analysis
    - MyPyAnalyzer: Static type checking and validation
    - BanditAnalyzer: Security vulnerability scanning
    - CoverageAnalyzer: Test coverage measurement and reporting
    - ComplexityAnalyzer: Code complexity metrics and thresholds

Data Persistence:
    - QualityProjectRepository: Project data management
    - QualityAnalysisRepository: Analysis result storage
    - QualityMetricsRepository: Metrics data persistence
    - ConfigurationRepository: Analysis configuration management

Architecture:
    All infrastructure components implement domain-defined interfaces,
    ensuring dependency inversion and testability. Uses adapter pattern
    for external tool integration with consistent error handling.

Integration:
    - Implements domain layer repository and service interfaces
    - Integrates with flext-observability for monitoring and tracing
    - Connects to external quality analysis tools and databases
    - Provides file system access for code analysis operations

Author: FLEXT Development Team
Version: 0.9.0
"""
