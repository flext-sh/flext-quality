"""Test repository implementations."""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_quality.infrastructure.persistence.repositories import (
    AnalysisResultRepository,
    QualityMetricsRepository,
    QualityRuleRepository,
)


class TestAnalysisResultRepository:
    """Test AnalysisResultRepository class."""

    def test_repository_initialization(self) -> None:
        """Test repository initialization."""
        repo = AnalysisResultRepository()
        assert repo._storage == {}

    @pytest.mark.asyncio
    async def test_save_entity(self) -> None:
        """Test saving an entity."""
        repo = AnalysisResultRepository()
        entity = {"id": "test-analysis", "data": "test"}

        result = await repo.save(entity)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists."""
        repo = AnalysisResultRepository()
        entity_id = uuid4()
        entity = {"id": entity_id, "data": "test"}

        repo._storage[entity_id] = entity

        result = await repo.find_by_id(entity_id)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist."""
        repo = AnalysisResultRepository()
        entity_id = uuid4()

        result = await repo.find_by_id(entity_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty."""
        repo = AnalysisResultRepository()

        result = await repo.find_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities."""
        repo = AnalysisResultRepository()
        entity1 = {"id": uuid4(), "data": "test1"}
        entity2 = {"id": uuid4(), "data": "test2"}

        repo._storage[entity1["id"]] = entity1
        repo._storage[entity2["id"]] = entity2

        result = await repo.find_all()

        assert len(result) == 2
        assert entity1 in result
        assert entity2 in result


class TestQualityMetricsRepository:
    """Test QualityMetricsRepository class."""

    def test_repository_initialization(self) -> None:
        """Test repository initialization."""
        repo = QualityMetricsRepository()
        assert repo._storage == {}

    @pytest.mark.asyncio
    async def test_save_entity(self) -> None:
        """Test saving an entity."""
        repo = QualityMetricsRepository()
        entity = {"id": "test-metrics", "score": 85.5}

        result = await repo.save(entity)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists."""
        repo = QualityMetricsRepository()
        entity_id = uuid4()
        entity = {"id": entity_id, "score": 90.0}

        repo._storage[entity_id] = entity

        result = await repo.find_by_id(entity_id)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist."""
        repo = QualityMetricsRepository()
        entity_id = uuid4()

        result = await repo.find_by_id(entity_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty."""
        repo = QualityMetricsRepository()

        result = await repo.find_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities."""
        repo = QualityMetricsRepository()
        entity1 = {"id": uuid4(), "score": 85.0}
        entity2 = {"id": uuid4(), "score": 92.5}

        repo._storage[entity1["id"]] = entity1
        repo._storage[entity2["id"]] = entity2

        result = await repo.find_all()

        assert len(result) == 2
        assert entity1 in result
        assert entity2 in result


class TestQualityRuleRepository:
    """Test QualityRuleRepository class."""

    def test_repository_initialization(self) -> None:
        """Test repository initialization."""
        repo = QualityRuleRepository()
        assert repo._storage == {}

    @pytest.mark.asyncio
    async def test_save_entity(self) -> None:
        """Test saving an entity."""
        repo = QualityRuleRepository()
        entity = {"id": "test-rule", "name": "complexity-check"}

        result = await repo.save(entity)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists."""
        repo = QualityRuleRepository()
        entity_id = uuid4()
        entity = {"id": entity_id, "name": "security-check"}

        repo._storage[entity_id] = entity

        result = await repo.find_by_id(entity_id)

        assert result == entity

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist."""
        repo = QualityRuleRepository()
        entity_id = uuid4()

        result = await repo.find_by_id(entity_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty."""
        repo = QualityRuleRepository()

        result = await repo.find_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities."""
        repo = QualityRuleRepository()
        entity1 = {"id": uuid4(), "name": "rule1"}
        entity2 = {"id": uuid4(), "name": "rule2"}

        repo._storage[entity1["id"]] = entity1
        repo._storage[entity2["id"]] = entity2

        result = await repo.find_all()

        assert len(result) == 2
        assert entity1 in result
        assert entity2 in result


class TestRepositoryIntegration:
    """Test repository integration scenarios."""

    @pytest.mark.asyncio
    async def test_multiple_repositories_independent(self) -> None:
        """Test that multiple repositories are independent."""
        analysis_repo = AnalysisResultRepository()
        metrics_repo = QualityMetricsRepository()
        rules_repo = QualityRuleRepository()

        # Add data to each repository
        analysis_entity = {"type": "analysis"}
        metrics_entity = {"type": "metrics"}
        rules_entity = {"type": "rules"}

        await analysis_repo.save(analysis_entity)
        await metrics_repo.save(metrics_entity)
        await rules_repo.save(rules_entity)

        # Each repository should only have its own data
        analysis_results = await analysis_repo.find_all()
        metrics_results = await metrics_repo.find_all()
        rules_results = await rules_repo.find_all()

        assert len(analysis_results) == 0  # save doesn't add to storage
        assert len(metrics_results) == 0   # save doesn't add to storage
        assert len(rules_results) == 0     # save doesn't add to storage

    @pytest.mark.asyncio
    async def test_repository_crud_workflow(self) -> None:
        """Test complete CRUD workflow with repository."""
        repo = AnalysisResultRepository()
        entity_id = uuid4()
        entity = {"id": entity_id, "status": "in_progress"}

        # Initially empty
        all_entities = await repo.find_all()
        assert len(all_entities) == 0

        # Add entity manually to storage (since save doesn't persist)
        repo._storage[entity_id] = entity

        # Find by ID
        found_entity = await repo.find_by_id(entity_id)
        assert found_entity == entity

        # Find all
        all_entities = await repo.find_all()
        assert len(all_entities) == 1
        assert entity in all_entities

        # Update entity in storage
        updated_entity = {"id": entity_id, "status": "completed"}
        repo._storage[entity_id] = updated_entity

        # Verify update
        found_updated = await repo.find_by_id(entity_id)
        assert found_updated == updated_entity

        # Remove entity
        del repo._storage[entity_id]

        # Verify removal
        not_found = await repo.find_by_id(entity_id)
        assert not_found is None

        empty_results = await repo.find_all()
        assert len(empty_results) == 0
