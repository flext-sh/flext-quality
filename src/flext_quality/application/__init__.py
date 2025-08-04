"""Application Layer - Business Workflows and Service Orchestration.

This module contains the application services that orchestrate business workflows
for quality analysis operations. It coordinates between domain entities and
infrastructure services while maintaining clean separation of concerns.

Key Responsibilities:
    - Orchestrate complex quality analysis workflows
    - Coordinate between domain services and infrastructure adapters
    - Implement transaction boundaries and business process flows
    - Handle cross-cutting concerns like logging and error handling
    - Manage application-specific business rules and validations

Service Classes:
    - QualityProjectService: Project lifecycle and management workflows
    - QualityAnalysisService: Analysis execution and result processing
    - QualityReportService: Report generation and distribution workflows
    - QualityMetricsService: Metrics collection and aggregation processes

Workflow Patterns:
    - Command/Query separation following CQRS principles
    - Event-driven workflows with domain event publishing
    - Transaction management with rollback capabilities
    - Async processing for long-running analysis operations

Architecture:
    Built on flext-core application patterns with no code duplication.
    Uses FlextResult for consistent error handling and operation outcomes.
    Implements dependency injection for testability and maintainability.

Integration:
    - Coordinates with domain layer for business logic execution
    - Manages infrastructure layer dependencies through interfaces
    - Publishes events to flext-observability for monitoring
    - Provides APIs for presentation layer consumption

Author: FLEXT Development Team
Version: 0.9.0
"""

from __future__ import annotations

__all__: list[str] = []
