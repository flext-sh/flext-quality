# Python Module Organization - FLEXT Quality

This document defines the Python module organization standards for FLEXT Quality, following FLEXT ecosystem patterns and Clean Architecture principles. All modules must adhere to these patterns for consistency, maintainability, and seamless integration with the broader FLEXT platform.

## Overview

FLEXT Quality follows **Clean Architecture + Domain-Driven Design (DDD)** patterns with strict layer separation and dependency direction enforcement. The module organization reflects the architectural boundaries and provides a clear, predictable structure for developers.

### Core Principles

1. **Clean Architecture Compliance**: Strict layer separation with inward-pointing dependencies
2. **FLEXT Core Integration**: Built on flext-core foundation patterns
3. **DDD Alignment**: Module structure reflects domain boundaries
4. **Semantic Clarity**: Module names clearly indicate purpose and layer
5. **Import Simplicity**: Public API accessible through root imports

## Directory Structure

### Source Code Organization

```
src/flext_quality/
├── __init__.py                     # Public API exports and simplified imports
├── __version__.py                  # Version information
├── py.typed                        # Type information marker
├── exceptions.py                   # Quality-specific exceptions
│
├── domain/                         # Domain Layer (Core Business Logic)
│   ├── __init__.py                # Domain public exports
│   ├── entities.py                # Domain entities (FlextEntity-based)
│   ├── value_objects.py           # Value objects and domain primitives
│   ├── ports.py                   # Interfaces and contracts
│   ├── services.py                # Domain services
│   ├── events.py                  # Domain events
│   └── quality_grade_calculator.py # Specialized domain service
│
├── application/                    # Application Layer (Use Cases)
│   ├── __init__.py                # Application public exports
│   ├── services.py                # Application services
│   ├── handlers.py                # Command/Query handlers (CQRS)
│   ├── commands.py                # Command definitions
│   ├── queries.py                 # Query definitions
│   └── validators.py              # Input validation
│
├── infrastructure/                 # Infrastructure Layer (External Dependencies)
│   ├── __init__.py                # Infrastructure public exports
│   ├── repositories.py            # Data access implementations
│   ├── external_services.py       # External service integrations
│   ├── adapters.py                # External system adapters
│   ├── container.py               # Dependency injection container
│   ├── config.py                  # Configuration management
│   └── persistence/               # Database-specific implementations
│       ├── __init__.py
│       ├── models.py              # ORM models (if used)
│       └── migrations/            # Database migrations
│
├── presentation/                   # Presentation Layer (External Interfaces)
│   ├── __init__.py                # Presentation public exports
│   ├── api/                       # REST API
│   │   ├── __init__.py
│   │   ├── routers.py            # FastAPI routers
│   │   ├── schemas.py            # Request/Response schemas
│   │   └── middleware.py         # API middleware
│   ├── web/                       # Web interface
│   │   ├── __init__.py
│   │   ├── views.py              # Web views
│   │   └── templates/            # HTML templates
│   └── cli/                       # Command-line interface
│       ├── __init__.py
│       ├── commands.py           # CLI commands
│       └── formatters.py         # Output formatters
│
├── shared/                         # Shared utilities (Cross-cutting)
│   ├── __init__.py                # Shared public exports
│   ├── utils.py                   # General utilities
│   ├── constants.py               # Application constants
│   ├── types.py                   # Type definitions
│   └── logging.py                 # Logging configuration
│
└── legacy/                         # Legacy code (Deprecated)
    ├── __init__.py                # Legacy exports with deprecation warnings
    ├── analyzer.py                # Legacy analyzer (to be removed)
    ├── metrics.py                 # Legacy metrics (to be removed)
    └── reports.py                 # Legacy reports (to be removed)
```

## Layer-Specific Organization

### Domain Layer (`domain/`)

The domain layer contains core business logic and must have **no dependencies** on outer layers.

#### Module Structure

```python
# domain/__init__.py
"""Domain layer public API exports."""

from flext_quality.domain.entities import (
    QualityProject,
    QualityAnalysis,
    QualityIssue,
    QualityReport,
    QualityRule,
)

from flext_quality.domain.value_objects import (
    QualityScore,
    QualityGrade,
    IssueLocation,
    IssueSeverity,
    IssueType,
)

from flext_quality.domain.services import (
    QualityScoreCalculator,
    ComplianceValidator,
    IssueClassifier,
)

__all__ = [
    # Entities
    "QualityProject",
    "QualityAnalysis",
    "QualityIssue",
    "QualityReport",
    "QualityRule",
    # Value Objects
    "QualityScore",
    "QualityGrade",
    "IssueLocation",
    "IssueSeverity",
    "IssueType",
    # Domain Services
    "QualityScoreCalculator",
    "ComplianceValidator",
    "IssueClassifier",
]
```

#### Domain Entity Pattern

```python
# domain/entities.py
"""Domain entities following flext-core patterns."""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Optional, List

from flext_core import FlextEntity, FlextResult
from flext_quality.domain.value_objects import QualityScore, QualityGrade

class QualityProject(FlextEntity):
    """Quality project aggregate root."""

    # Domain attributes
    name: str
    project_path: str
    repository_url: Optional[str] = None
    language: str = "python"

    # Quality configuration
    min_coverage: float = 90.0
    max_complexity: int = 10
    auto_analyze: bool = True

    def validate_standards(self) -> FlextResult[bool]:
        """Validate project meets quality standards."""
        if not self.project_path:
            return FlextResult.fail("Project path is required")

        if self.min_coverage < 0 or self.min_coverage > 100:
            return FlextResult.fail("Coverage must be between 0 and 100")

        return FlextResult.ok(True)

    def calculate_compliance(self, analysis: QualityAnalysis) -> float:
        """Calculate compliance percentage for this project."""
        # Domain business logic
        compliance_score = 0.0

        if analysis.coverage_score >= self.min_coverage:
            compliance_score += 30.0

        if analysis.complexity_score <= self.max_complexity:
            compliance_score += 25.0

        # Additional compliance checks...

        return min(compliance_score, 100.0)

class QualityAnalysis(FlextEntity):
    """Quality analysis aggregate."""

    project_id: str
    status: AnalysisStatus
    started_at: datetime
    completed_at: Optional[datetime] = None

    # Quality metrics
    overall_score: float = 0.0
    coverage_score: float = 0.0
    complexity_score: float = 0.0
    security_score: float = 0.0

    # Issue counts
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0

    def calculate_overall_score(self) -> QualityAnalysis:
        """Calculate overall quality score from component scores."""
        # Domain business logic for score calculation
        weights = {
            'coverage': 0.30,
            'complexity': 0.25,
            'security': 0.25,
            'maintainability': 0.20,
        }

        weighted_score = (
            self.coverage_score * weights['coverage'] +
            (100 - self.complexity_score) * weights['complexity'] +
            self.security_score * weights['security'] +
            self.maintainability_score * weights.get('maintainability', 0.20)
        )

        return self.model_copy(update={'overall_score': weighted_score})

    def generate_grade(self) -> QualityGrade:
        """Generate quality grade from overall score."""
        return QualityGrade.from_score(self.overall_score)

    def complete_analysis(self) -> QualityAnalysis:
        """Mark analysis as completed."""
        return self.model_copy(update={
            'status': AnalysisStatus.COMPLETED,
            'completed_at': datetime.now(UTC)
        })
```

#### Value Objects Pattern

```python
# domain/value_objects.py
"""Domain value objects."""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Union

from pydantic import BaseModel, Field, model_validator

class QualityGrade(str, Enum):
    """Quality grade enumeration."""

    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    F = "F"

    @classmethod
    def from_score(cls, score: float) -> QualityGrade:
        """Convert numeric score to quality grade."""
        if score >= 97: return cls.A_PLUS
        if score >= 93: return cls.A
        if score >= 90: return cls.A_MINUS
        if score >= 87: return cls.B_PLUS
        if score >= 83: return cls.B
        if score >= 80: return cls.B_MINUS
        if score >= 77: return cls.C_PLUS
        if score >= 73: return cls.C
        if score >= 70: return cls.C_MINUS
        if score >= 67: return cls.D_PLUS
        if score >= 60: return cls.D
        return cls.F

class QualityScore(BaseModel):
    """Composite quality score value object."""

    overall: float = Field(ge=0.0, le=100.0)
    coverage: float = Field(ge=0.0, le=100.0)
    complexity: float = Field(ge=0.0, le=100.0)
    security: float = Field(ge=0.0, le=100.0)
    maintainability: float = Field(ge=0.0, le=100.0)

    @model_validator(mode='after')
    def validate_scores(self) -> QualityScore:
        """Validate score consistency."""
        component_avg = (
            self.coverage + self.complexity +
            self.security + self.maintainability
        ) / 4

        # Allow reasonable variance
        if abs(self.overall - component_avg) > 10.0:
            raise ValueError("Overall score inconsistent with components")

        return self

    @property
    def grade(self) -> QualityGrade:
        """Get quality grade from overall score."""
        return QualityGrade.from_score(self.overall)

class IssueLocation(BaseModel):
    """Code location value object."""

    file_path: str
    line_number: int = Field(ge=1)
    column_number: int = Field(ge=1, default=1)
    end_line_number: Optional[int] = Field(ge=1, default=None)
    end_column_number: Optional[int] = Field(ge=1, default=None)

    @model_validator(mode='after')
    def validate_location(self) -> IssueLocation:
        """Validate location coordinates."""
        if self.end_line_number and self.end_line_number < self.line_number:
            raise ValueError("End line must be >= start line")
        return self

    def __str__(self) -> str:
        """String representation of location."""
        if self.end_line_number and self.end_line_number != self.line_number:
            return f"{self.file_path}:{self.line_number}-{self.end_line_number}"
        return f"{self.file_path}:{self.line_number}:{self.column_number}"
```

### Application Layer (`application/`)

The application layer orchestrates domain operations and implements use cases.

#### Application Service Pattern

```python
# application/services.py
"""Application services implementing use cases."""

from __future__ import annotations

from typing import List, Optional
from uuid import uuid4

from flext_core import FlextResult
from flext_observability import flext_monitor_function

from flext_quality.domain.entities import QualityProject, QualityAnalysis
from flext_quality.domain.ports import (
    QualityProjectRepository,
    QualityAnalysisRepository,
    AnalysisEngine
)

class QualityProjectService:
    """Application service for quality project management."""

    def __init__(
        self,
        project_repository: QualityProjectRepository,
        analysis_repository: QualityAnalysisRepository,
        analysis_engine: AnalysisEngine,
    ):
        self._project_repository = project_repository
        self._analysis_repository = analysis_repository
        self._analysis_engine = analysis_engine

    @flext_monitor_function("create_quality_project")
    async def create_project(
        self,
        name: str,
        project_path: str,
        repository_url: Optional[str] = None,
        min_coverage: float = 90.0,
        max_complexity: int = 10,
    ) -> FlextResult[QualityProject]:
        """Create a new quality project."""
        try:
            # Create domain entity
            project = QualityProject(
                id=str(uuid4()),
                name=name,
                project_path=project_path,
                repository_url=repository_url,
                min_coverage=min_coverage,
                max_complexity=max_complexity,
            )

            # Domain validation
            validation_result = project.validate_standards()
            if not validation_result.is_success:
                return validation_result

            # Persist project
            saved_project = await self._project_repository.save(project)
            return FlextResult.ok(saved_project)

        except Exception as e:
            return FlextResult.fail(f"Failed to create project: {e}")

    @flext_monitor_function("analyze_quality_project")
    async def analyze_project(
        self,
        project_id: str,
        commit_hash: Optional[str] = None,
    ) -> FlextResult[QualityAnalysis]:
        """Analyze project quality."""
        try:
            # Get project
            project_result = await self._project_repository.get_by_id(project_id)
            if not project_result.is_success:
                return project_result

            project = project_result.data

            # Create analysis
            analysis = QualityAnalysis(
                id=str(uuid4()),
                project_id=project_id,
                status=AnalysisStatus.STARTED,
                commit_hash=commit_hash,
            )

            # Run analysis engine
            analysis_result = await self._analysis_engine.analyze(project, analysis)
            if not analysis_result.is_success:
                return analysis_result

            # Calculate scores and complete
            completed_analysis = analysis_result.data.calculate_overall_score().complete_analysis()

            # Persist analysis
            saved_analysis = await self._analysis_repository.save(completed_analysis)
            return FlextResult.ok(saved_analysis)

        except Exception as e:
            return FlextResult.fail(f"Failed to analyze project: {e}")
```

#### CQRS Handler Pattern

```python
# application/handlers.py
"""CQRS command and query handlers."""

from __future__ import annotations

from flext_core import FlextResult
from flext_observability import flext_monitor_function

from flext_quality.application.commands import (
    AnalyzeProjectCommand,
    CreateProjectCommand,
    UpdateProjectCommand,
)
from flext_quality.application.queries import (
    GetProjectQuery,
    GetAnalysisQuery,
    GetEcosystemMetricsQuery,
)

class QualityProjectCommandHandler:
    """Command handler for quality project operations."""

    def __init__(self, project_service: QualityProjectService):
        self._project_service = project_service

    @flext_monitor_function("handle_create_project_command")
    async def handle_create_project(
        self,
        command: CreateProjectCommand
    ) -> FlextResult[QualityProject]:
        """Handle create project command."""
        return await self._project_service.create_project(
            name=command.name,
            project_path=command.project_path,
            repository_url=command.repository_url,
            min_coverage=command.min_coverage,
            max_complexity=command.max_complexity,
        )

    @flext_monitor_function("handle_analyze_project_command")
    async def handle_analyze_project(
        self,
        command: AnalyzeProjectCommand
    ) -> FlextResult[QualityAnalysis]:
        """Handle analyze project command."""
        return await self._project_service.analyze_project(
            project_id=command.project_id,
            commit_hash=command.commit_hash,
        )

class QualityProjectQueryHandler:
    """Query handler for quality project queries."""

    def __init__(self, project_repository: QualityProjectRepository):
        self._project_repository = project_repository

    @flext_monitor_function("handle_get_project_query")
    async def handle_get_project(
        self,
        query: GetProjectQuery
    ) -> FlextResult[QualityProject]:
        """Handle get project query."""
        return await self._project_repository.get_by_id(query.project_id)

    @flext_monitor_function("handle_get_ecosystem_metrics_query")
    async def handle_get_ecosystem_metrics(
        self,
        query: GetEcosystemMetricsQuery
    ) -> FlextResult[EcosystemMetrics]:
        """Handle ecosystem metrics query."""
        # Implementation for ecosystem-wide metrics
        pass
```

### Infrastructure Layer (`infrastructure/`)

The infrastructure layer implements technical concerns and external dependencies.

#### Repository Pattern

```python
# infrastructure/repositories.py
"""Repository implementations."""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from flext_core import FlextResult

from flext_quality.domain.entities import QualityProject, QualityAnalysis
from flext_quality.domain.ports import QualityProjectRepository, QualityAnalysisRepository

class PostgreSQLQualityProjectRepository(QualityProjectRepository):
    """PostgreSQL implementation of quality project repository."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get_by_id(self, project_id: str) -> FlextResult[QualityProject]:
        """Get project by ID."""
        try:
            async with self._session_factory() as session:
                # ORM query implementation
                result = await session.get(QualityProjectModel, project_id)
                if not result:
                    return FlextResult.fail(f"Project not found: {project_id}")

                # Convert ORM model to domain entity
                project = self._to_domain_entity(result)
                return FlextResult.ok(project)

        except Exception as e:
            return FlextResult.fail(f"Failed to get project: {e}")

    async def save(self, project: QualityProject) -> FlextResult[QualityProject]:
        """Save project."""
        try:
            async with self._session_factory() as session:
                # Convert domain entity to ORM model
                model = self._to_orm_model(project)
                session.add(model)
                await session.commit()

                # Return domain entity
                return FlextResult.ok(project)

        except Exception as e:
            return FlextResult.fail(f"Failed to save project: {e}")

    def _to_domain_entity(self, model: QualityProjectModel) -> QualityProject:
        """Convert ORM model to domain entity."""
        return QualityProject(
            id=model.id,
            name=model.name,
            project_path=model.project_path,
            repository_url=model.repository_url,
            min_coverage=model.min_coverage,
            max_complexity=model.max_complexity,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_orm_model(self, project: QualityProject) -> QualityProjectModel:
        """Convert domain entity to ORM model."""
        return QualityProjectModel(
            id=project.id,
            name=project.name,
            project_path=project.project_path,
            repository_url=project.repository_url,
            min_coverage=project.min_coverage,
            max_complexity=project.max_complexity,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
```

#### Dependency Injection Container

```python
# infrastructure/container.py
"""Dependency injection container."""

from __future__ import annotations

from flext_core import FlextContainer, get_flext_container

from flext_quality.application.services import (
    QualityProjectService,
    QualityAnalysisService,
)
from flext_quality.infrastructure.repositories import (
    PostgreSQLQualityProjectRepository,
    PostgreSQLQualityAnalysisRepository,
)
from flext_quality.infrastructure.external_services import (
    RuffAnalysisEngine,
    MyPyAnalysisEngine,
)

def configure_quality_container() -> FlextContainer:
    """Configure dependency injection container for FLEXT Quality."""

    # Get base FLEXT container
    container = get_flext_container()

    # Register repositories
    container.register_singleton(
        "quality_project_repository",
        PostgreSQLQualityProjectRepository,
        session_factory=container.get("database_session_factory")
    )

    container.register_singleton(
        "quality_analysis_repository",
        PostgreSQLQualityAnalysisRepository,
        session_factory=container.get("database_session_factory")
    )

    # Register analysis engines
    container.register_singleton("ruff_analysis_engine", RuffAnalysisEngine)
    container.register_singleton("mypy_analysis_engine", MyPyAnalysisEngine)

    # Register application services
    container.register_singleton(
        "quality_project_service",
        QualityProjectService,
        project_repository=container.get("quality_project_repository"),
        analysis_repository=container.get("quality_analysis_repository"),
        analysis_engine=container.get("ruff_analysis_engine"),
    )

    container.register_singleton(
        "quality_analysis_service",
        QualityAnalysisService,
        analysis_repository=container.get("quality_analysis_repository"),
        project_repository=container.get("quality_project_repository"),
    )

    return container

# Global container instance
quality_container = configure_quality_container()
```

### Presentation Layer (`presentation/`)

The presentation layer handles external communication and user interfaces.

#### API Router Pattern

```python
# presentation/api/routers.py
"""FastAPI routers for quality API."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from flext_quality.application.services import QualityProjectService
from flext_quality.presentation.api.schemas import (
    CreateProjectRequest,
    ProjectResponse,
    AnalyzeProjectRequest,
    AnalysisResponse,
)
from flext_quality.infrastructure.container import quality_container

router = APIRouter(prefix="/api/v1/quality", tags=["quality"])

def get_project_service() -> QualityProjectService:
    """Dependency injection for project service."""
    return quality_container.get("quality_project_service")

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    request: CreateProjectRequest,
    service: QualityProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Create a new quality project."""

    result = await service.create_project(
        name=request.name,
        project_path=request.project_path,
        repository_url=request.repository_url,
        min_coverage=request.min_coverage,
        max_complexity=request.max_complexity,
    )

    if result.is_success:
        return ProjectResponse.from_domain_entity(result.data)
    else:
        raise HTTPException(status_code=400, detail=result.error)

@router.post("/projects/{project_id}/analyze", response_model=AnalysisResponse)
async def analyze_project(
    project_id: str,
    request: AnalyzeProjectRequest,
    service: QualityProjectService = Depends(get_project_service)
) -> AnalysisResponse:
    """Start quality analysis for project."""

    result = await service.analyze_project(
        project_id=project_id,
        commit_hash=request.commit_hash,
    )

    if result.is_success:
        return AnalysisResponse.from_domain_entity(result.data)
    else:
        raise HTTPException(status_code=400, detail=result.error)
```

## Public API Design

### Root Module Exports (`__init__.py`)

The root module provides a simplified public API for common operations:

```python
# __init__.py
"""FLEXT Quality - Public API exports."""

from __future__ import annotations

# Version information
from flext_quality.__version__ import __version__, __version_info__

# Core patterns from flext-core
from flext_core import FlextResult, FlextEntity, FlextContainer

# Domain exports (most commonly used)
from flext_quality.domain import (
    QualityProject,
    QualityAnalysis,
    QualityScore,
    QualityGrade,
    IssueSeverity,
    IssueType,
)

# Application services (public API)
from flext_quality.application.services import (
    QualityProjectService,
    QualityAnalysisService,
)

# Simple API for basic usage
from flext_quality.simple_api import QualityAPI

# CLI entry point
from flext_quality.cli import main as cli_main

# Public API exports
__all__ = [
    # Version
    "__version__",
    "__version_info__",

    # Core patterns
    "FlextResult",
    "FlextEntity",
    "FlextContainer",

    # Domain models
    "QualityProject",
    "QualityAnalysis",
    "QualityScore",
    "QualityGrade",
    "IssueSeverity",
    "IssueType",

    # Services
    "QualityProjectService",
    "QualityAnalysisService",

    # Simple API
    "QualityAPI",

    # CLI
    "cli_main",
]
```

### Simple API for Common Use Cases

```python
# simple_api.py
"""Simplified API for common FLEXT Quality operations."""

from __future__ import annotations

from typing import Optional, Dict, Any

from flext_core import FlextResult
from flext_quality.infrastructure.container import quality_container

class QualityAPI:
    """Simplified API for FLEXT Quality operations."""

    def __init__(self):
        self._project_service = quality_container.get("quality_project_service")
        self._analysis_service = quality_container.get("quality_analysis_service")

    async def create_project(
        self,
        name: str,
        path: str,
        repository_url: Optional[str] = None,
        **config
    ) -> FlextResult[Dict[str, Any]]:
        """Create a quality project with simplified interface."""

        result = await self._project_service.create_project(
            name=name,
            project_path=path,
            repository_url=repository_url,
            min_coverage=config.get('min_coverage', 90.0),
            max_complexity=config.get('max_complexity', 10),
        )

        if result.is_success:
            return FlextResult.ok({
                'id': result.data.id,
                'name': result.data.name,
                'path': result.data.project_path,
                'status': 'created'
            })
        else:
            return result

    async def analyze_project(
        self,
        project_id: str,
        wait_for_completion: bool = False
    ) -> FlextResult[Dict[str, Any]]:
        """Analyze project with simplified interface."""

        result = await self._project_service.analyze_project(project_id)

        if result.is_success:
            analysis = result.data
            return FlextResult.ok({
                'analysis_id': analysis.id,
                'project_id': analysis.project_id,
                'status': analysis.status.value,
                'quality_score': analysis.overall_score,
                'quality_grade': analysis.generate_grade().value,
                'issues': {
                    'critical': analysis.critical_issues,
                    'high': analysis.high_issues,
                    'medium': analysis.medium_issues,
                    'low': analysis.low_issues,
                }
            })
        else:
            return result
```

## Import Patterns and Standards

### Layer Import Rules

1. **Domain Layer**: Can only import from flext-core and standard library
2. **Application Layer**: Can import from domain and flext-core
3. **Infrastructure Layer**: Can import from domain, application, and external libraries
4. **Presentation Layer**: Can import from all layers

### Import Style Guidelines

```python
# Standard library imports
from __future__ import annotations
import asyncio
from datetime import datetime, UTC
from typing import Optional, List, Dict, Any
from uuid import uuid4

# Third-party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

# FLEXT core imports
from flext_core import FlextResult, FlextEntity, FlextContainer
from flext_observability import flext_monitor_function

# Project imports (relative)
from flext_quality.domain.entities import QualityProject
from flext_quality.domain.value_objects import QualityScore
from flext_quality.application.services import QualityProjectService
```

### Public vs Private Modules

```python
# Public modules (exported in __all__)
from flext_quality import QualityProject, QualityAPI

# Private modules (internal implementation)
from flext_quality.infrastructure.repositories import PostgreSQLRepository  # ❌ Avoid
```

## Migration Strategy

### Current State Assessment

The current module structure has several issues that need addressing:

1. **Legacy modules** in root directory (`analyzer.py`, `metrics.py`, `reports.py`)
2. **Mixed architectural patterns** (Django models alongside Clean Architecture)
3. **Incomplete layer separation** (missing proper ports/adapters)
4. **Inconsistent import patterns**

### Migration Steps

#### Phase 1: Clean Architecture Implementation

1. ✅ Create proper domain layer with entities and value objects
2. ✅ Implement application services with CQRS patterns
3. ✅ Define ports/interfaces for external dependencies
4. ✅ Create infrastructure implementations

#### Phase 2: Legacy Module Deprecation

1. Add deprecation warnings to legacy modules
2. Update all internal imports to use new structure
3. Provide migration guide for external users
4. Remove legacy modules in v1.0.0

#### Phase 3: Django Integration Refactoring

1. Move Django models to infrastructure/persistence/
2. Create adapters for Django ORM
3. Implement proper repository pattern
4. Maintain backward compatibility

### Deprecation Pattern

```python
# legacy/analyzer.py
"""Legacy analyzer module - DEPRECATED."""

import warnings
from flext_quality.application.services import QualityProjectService

warnings.warn(
    "flext_quality.analyzer is deprecated. Use flext_quality.QualityAPI instead.",
    DeprecationWarning,
    stacklevel=2
)

# Provide compatibility layer
class CodeAnalyzer:
    """Deprecated - use QualityAPI instead."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "CodeAnalyzer is deprecated. Use QualityAPI instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._api = QualityAPI()

    def analyze_project(self, *args, **kwargs):
        """Deprecated method - forwards to new API."""
        return self._api.analyze_project(*args, **kwargs)
```

## Testing Organization

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Global fixtures
├── unit/                          # Unit tests by layer
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── test_entities.py       # Domain entity tests
│   │   ├── test_value_objects.py  # Value object tests
│   │   └── test_services.py       # Domain service tests
│   ├── application/
│   │   ├── __init__.py
│   │   ├── test_services.py       # Application service tests
│   │   └── test_handlers.py       # CQRS handler tests
│   └── infrastructure/
│       ├── __init__.py
│       ├── test_repositories.py   # Repository tests
│       └── test_external_services.py
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── test_api_endpoints.py      # API integration tests
│   ├── test_database.py           # Database integration
│   └── test_analysis_engine.py    # Analysis workflow tests
└── e2e/                          # End-to-end tests
    ├── __init__.py
    ├── test_quality_analysis.py   # Full analysis workflow
    └── test_api_integration.py    # Complete API workflows
```

### Test Naming Conventions

```python
# Unit tests
class TestQualityProject:
    """Test QualityProject domain entity."""

    def test_create_project_with_valid_data_succeeds(self):
        """Test creating project with valid data succeeds."""
        pass

    def test_validate_standards_with_invalid_coverage_fails(self):
        """Test validation fails with invalid coverage."""
        pass

# Integration tests
class TestQualityProjectService:
    """Test QualityProjectService integration."""

    async def test_create_project_persists_to_database(self):
        """Test project creation persists to database."""
        pass

# End-to-end tests
class TestQualityAnalysisWorkflow:
    """Test complete quality analysis workflow."""

    async def test_full_analysis_workflow_produces_report(self):
        """Test full workflow from project creation to report generation."""
        pass
```

## Documentation Standards

### Module Docstrings

```python
"""Module description following FLEXT standards.

This module provides [specific functionality] for the FLEXT Quality service,
implementing [architectural pattern] patterns and integrating with [FLEXT services].

Key Components:
    - Component1: Description of purpose and usage
    - Component2: Description with architectural notes
    - Component3: Description with integration details

Architecture:
    This module follows Clean Architecture principles, positioned in the
    [Domain/Application/Infrastructure/Presentation] layer with dependencies
    pointing [inward/outward as appropriate].

Examples:
    Basic usage example:

    >>> from flext_quality.module import Component
    >>> component = Component()
    >>> result = component.operation()
    >>> assert result.is_success

Integration:
    - Built on flext-core foundation patterns
    - Integrates with flext-observability for monitoring
    - Coordinates with [other FLEXT services]

See Also:
    - flext_core.FlextEntity: Base entity pattern
    - flext_core.FlextResult: Error handling pattern
    - Related module documentation
"""
```

### Class and Function Docstrings

Follow Google-style docstrings with FLEXT-specific sections:

```python
class QualityProject(FlextEntity):
    """Quality project domain entity following FLEXT patterns.

    Represents a code project under quality analysis within the FLEXT ecosystem.
    Implements domain validation rules and business logic for quality standards.

    Attributes:
        name: Human-readable project name
        project_path: Filesystem path to project root
        repository_url: Optional source control repository URL
        min_coverage: Minimum required test coverage percentage
        max_complexity: Maximum allowed cyclomatic complexity

    Examples:
        Creating a quality project:

        >>> project = QualityProject(
        ...     name="flext-core",
        ...     project_path="/path/to/flext-core",
        ...     min_coverage=95.0
        ... )
        >>> result = project.validate_standards()
        >>> assert result.is_success

    Integration:
        - Extends flext_core.FlextEntity for base functionality
        - Monitored via flext-observability integration
        - Persisted through repository pattern
    """

    def validate_standards(self) -> FlextResult[bool]:
        """Validate project meets FLEXT quality standards.

        Performs domain validation of project configuration against
        FLEXT ecosystem quality requirements.

        Returns:
            FlextResult[bool]: Success if standards met, failure with details

        Raises:
            ValueError: If project data is malformed

        Examples:
            >>> project = QualityProject(name="test", project_path="")
            >>> result = project.validate_standards()
            >>> assert not result.is_success
            >>> assert "path is required" in result.error
        """
        pass
```

## Quality Standards

### Code Quality Metrics

All modules must meet these quality standards:

- **Test Coverage**: 90% minimum
- **Type Coverage**: 95% minimum with mypy strict mode
- **Complexity**: Maximum cyclomatic complexity of 10
- **Documentation**: 100% public API documented
- **Import Quality**: No circular imports, clear dependency direction

### Linting Configuration

```toml
# pyproject.toml - module organization specific rules
[tool.ruff.lint.per-file-ignores]
"**/domain/**" = [
    "D103",  # Allow missing docstrings in domain internal modules
]
"**/infrastructure/**" = [
    "D101",  # Allow missing docstrings in infrastructure adapters
]
"**/legacy/**" = [
    "ALL",   # Legacy modules exempt from new standards
]

[tool.mypy.per-module-overrides]
"flext_quality.domain.*" = {
    strict = true,
    disallow_any_expr = true,
}
"flext_quality.legacy.*" = {
    strict = false,  # Legacy modules exempt
}
```

## Conclusion

This Python module organization standard ensures FLEXT Quality maintains consistency with the broader FLEXT ecosystem while implementing Clean Architecture principles effectively. The structure provides clear separation of concerns, enables testability, and supports the long-term maintainability required for enterprise-grade software.

All developers working on FLEXT Quality must follow these patterns to ensure code quality, architectural consistency, and seamless integration with other FLEXT services.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"id": "analyze-current-structure", "content": "Analisar estrutura atual de m\u00f3dulos Python", "status": "completed", "priority": "high"}, {"id": "create-module-organization-doc", "content": "Criar docs/standards/Python-module-organization.md", "status": "completed", "priority": "high"}, {"id": "define-semantic-patterns", "content": "Definir padr\u00f5es sem\u00e2nticos ideais para o projeto", "status": "completed", "priority": "high"}, {"id": "align-with-flext-core", "content": "Alinhar com padr\u00f5es do flext-core", "status": "completed", "priority": "high"}]
