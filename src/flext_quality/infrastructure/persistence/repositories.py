"""Repository implementations for FLEXT-QUALITY using flext-core patterns.

DRY REFACTOR: Eliminated 3 duplicate repository classes.
Using flext-core FlextRepository interface with proper inheritance.
"""

from __future__ import annotations

from flext_core import FlextRepository, FlextResult


class InMemoryRepository(FlextRepository):
    """Base in-memory repository implementing FlextRepository interface.

    DRY: Single implementation for all repository types.
    SOLID: Follows interface segregation and dependency inversion.
    """

    def __init__(self) -> None:
        self._storage: dict[str, object] = {}

    def find_by_id(self, entity_id: str) -> FlextResult[object]:
        """Find entity by ID."""
        entity = self._storage.get(entity_id)
        if entity is None:
            return FlextResult.fail(f"Entity not found: {entity_id}")
        return FlextResult.ok(entity)

    def save(self, entity: object) -> FlextResult[None]:
        """Save entity."""
        if hasattr(entity, "id"):
            entity_id = str(entity.id)
            self._storage[entity_id] = entity
            return FlextResult.ok(None)
        return FlextResult.fail("Entity must have an 'id' attribute")

    def delete(self, entity_id: str) -> FlextResult[None]:
        """Delete entity by ID."""
        if entity_id in self._storage:
            del self._storage[entity_id]
            return FlextResult.ok(None)
        return FlextResult.fail(f"Entity not found: {entity_id}")

    def find_all(self) -> FlextResult[list[object]]:
        """Find all entities."""
        return FlextResult.ok(list(self._storage.values()))


# Type-specific repository aliases - DRY principle maintained
class AnalysisResultRepository(InMemoryRepository):
    """Repository for analysis results - uses base implementation."""


class QualityMetricsRepository(InMemoryRepository):
    """Repository for quality metrics - uses base implementation."""


class QualityRuleRepository(InMemoryRepository):
    """Repository for quality rules - uses base implementation."""
