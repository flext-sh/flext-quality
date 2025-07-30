"""Test repository implementations."""

from __future__ import annotations

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

    def test_save_entity(self) -> None:
        """Test saving an entity - using real FlextResult API."""
        repo = AnalysisResultRepository()

        # Create a simple object with id attribute
        class TestEntity:
            def __init__(self, entity_id: str, data: str) -> None:
                self.id = entity_id
                self.data = data

        entity = TestEntity("test-analysis", "test")

        result = repo.save(entity)

        assert result.is_success
        assert result.data is None  # save returns FlextResult[None]

    def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists - using real FlextResult API."""
        repo = AnalysisResultRepository()
        entity_id = "test-id"
        entity = {"id": entity_id, "data": "test"}

        # Use string ID as per flext-core FlextRepository interface
        repo._storage[entity_id] = entity

        result = repo.find_by_id(entity_id)

        assert result.is_success
        assert result.data == entity

    def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist - using real FlextResult API."""
        repo = AnalysisResultRepository()
        entity_id = "nonexistent-id"

        result = repo.find_by_id(entity_id)

        assert result.is_failure
        assert result.error is not None
        assert "Entity not found" in result.error

    def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty - using real FlextResult API."""
        repo = AnalysisResultRepository()

        result = repo.find_all()

        assert result.is_success
        assert result.data == []

    def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities - using real FlextResult API."""
        repo = AnalysisResultRepository()
        entity1 = {"id": "entity1", "data": "test1"}
        entity2 = {"id": "entity2", "data": "test2"}

        # Use string IDs as per flext-core interface
        repo._storage["entity1"] = entity1
        repo._storage["entity2"] = entity2

        result = repo.find_all()

        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data


class TestQualityMetricsRepository:
    """Test QualityMetricsRepository class."""

    def test_repository_initialization(self) -> None:
        """Test repository initialization."""
        repo = QualityMetricsRepository()
        assert repo._storage == {}

    def test_save_entity(self) -> None:
        """Test saving an entity - using real FlextResult API."""
        repo = QualityMetricsRepository()

        # Create a simple object with id attribute
        class TestEntity:
            def __init__(self, entity_id: str, score: float) -> None:
                self.id = entity_id
                self.score = score

        entity = TestEntity("test-metrics", 85.5)

        result = repo.save(entity)

        assert result.is_success
        assert result.data is None  # save returns FlextResult[None]

    def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists - using real FlextResult API."""
        repo = QualityMetricsRepository()
        entity_id = "test-entity-id"
        entity = {"id": entity_id, "score": 90.0}

        repo._storage[entity_id] = entity

        result = repo.find_by_id(entity_id)

        assert result.is_success
        assert result.data == entity

    def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist - using real FlextResult API."""
        repo = QualityMetricsRepository()
        entity_id = "test-entity-id"

        result = repo.find_by_id(entity_id)

        assert result.is_failure
        assert result.error is not None
        assert "Entity not found" in result.error

    def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty - using real FlextResult API."""
        repo = QualityMetricsRepository()

        result = repo.find_all()

        assert result.is_success
        assert result.data == []

    def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities - using real FlextResult API."""
        repo = QualityMetricsRepository()
        entity1 = {"id": "metrics1", "score": 85.0}
        entity2 = {"id": "metrics2", "score": 92.5}

        repo._storage[str(entity1["id"])] = entity1
        repo._storage[str(entity2["id"])] = entity2

        result = repo.find_all()

        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data


class TestQualityRuleRepository:
    """Test QualityRuleRepository class."""

    def test_repository_initialization(self) -> None:
        """Test repository initialization."""
        repo = QualityRuleRepository()
        assert repo._storage == {}

    def test_save_entity(self) -> None:
        """Test saving an entity - using real FlextResult API."""
        repo = QualityRuleRepository()

        # Create a simple object with id attribute
        class TestEntity:
            def __init__(self, entity_id: str, name: str) -> None:
                self.id = entity_id
                self.name = name

        entity = TestEntity("test-rule", "complexity-check")

        result = repo.save(entity)

        assert result.is_success
        assert result.data is None  # save returns FlextResult[None]

    def test_find_by_id_existing(self) -> None:
        """Test finding entity by ID when it exists - using real FlextResult API."""
        repo = QualityRuleRepository()
        entity_id = "test-entity-id"
        entity = {"id": entity_id, "name": "security-check"}

        repo._storage[entity_id] = entity

        result = repo.find_by_id(entity_id)

        assert result.is_success
        assert result.data == entity

    def test_find_by_id_not_found(self) -> None:
        """Test finding entity by ID when it doesn't exist - using real FlextResult API."""
        repo = QualityRuleRepository()
        entity_id = "test-entity-id"

        result = repo.find_by_id(entity_id)

        assert result.is_failure
        assert result.error is not None
        assert "Entity not found" in result.error

    def test_find_all_empty(self) -> None:
        """Test finding all entities when repository is empty - using real FlextResult API."""
        repo = QualityRuleRepository()

        result = repo.find_all()

        assert result.is_success
        assert result.data == []

    def test_find_all_with_entities(self) -> None:
        """Test finding all entities with multiple entities - using real FlextResult API."""
        repo = QualityRuleRepository()
        entity1 = {"id": "rule1", "name": "rule1"}
        entity2 = {"id": "rule2", "name": "rule2"}

        repo._storage[str(entity1["id"])] = entity1
        repo._storage[str(entity2["id"])] = entity2

        result = repo.find_all()

        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 2
        assert entity1 in result.data
        assert entity2 in result.data


class TestRepositoryIntegration:
    """Test repository integration scenarios."""

    def test_multiple_repositories_independent(self) -> None:
        """Test that multiple repositories are independent - using real FlextResult API."""
        analysis_repo = AnalysisResultRepository()
        metrics_repo = QualityMetricsRepository()
        rules_repo = QualityRuleRepository()

        # Add data to each repository - entities need 'id' attribute for save to work
        class TestEntity:
            def __init__(self, entity_id: str, entity_type: str) -> None:
                self.id = entity_id
                self.type = entity_type

        analysis_entity = TestEntity("analysis1", "analysis")
        metrics_entity = TestEntity("metrics1", "metrics")
        rules_entity = TestEntity("rules1", "rules")

        # Save entities using sync FlextResult API
        analysis_result = analysis_repo.save(analysis_entity)
        metrics_result = metrics_repo.save(metrics_entity)
        rules_result = rules_repo.save(rules_entity)

        # Verify saves succeeded
        assert analysis_result.is_success
        assert metrics_result.is_success
        assert rules_result.is_success

        # Each repository should have its own data (save DOES add to storage)
        analysis_results = analysis_repo.find_all()
        metrics_results = metrics_repo.find_all()
        rules_results = rules_repo.find_all()

        assert analysis_results.is_success
        assert metrics_results.is_success
        assert rules_results.is_success
        assert analysis_results.data is not None
        assert metrics_results.data is not None
        assert rules_results.data is not None
        assert len(analysis_results.data) == 1
        assert len(metrics_results.data) == 1
        assert len(rules_results.data) == 1

    def test_repository_crud_workflow(self) -> None:
        """Test complete CRUD workflow with repository - using real FlextResult API."""
        repo = AnalysisResultRepository()
        entity_id = "test-entity-id"

        # Create a simple object with id attribute
        class TestEntity:
            def __init__(self, entity_id: str, status: str) -> None:
                self.id = entity_id
                self.status = status

            def __eq__(self, other: object) -> bool:
                return (
                    isinstance(other, TestEntity)
                    and self.id == other.id
                    and self.status == other.status
                )

            def __hash__(self) -> int:
                return hash((self.id, self.status))

        entity = TestEntity(entity_id, "in_progress")

        # Initially empty
        all_entities = repo.find_all()
        assert all_entities.is_success
        assert all_entities.data is not None
        assert len(all_entities.data) == 0

        # Save entity using real save method
        save_result = repo.save(entity)
        assert save_result.is_success

        # Find by ID
        found_result = repo.find_by_id(entity_id)
        assert found_result.is_success
        assert found_result.data == entity

        # Find all
        all_entities = repo.find_all()
        assert all_entities.is_success
        assert all_entities.data is not None
        assert len(all_entities.data) == 1
        assert entity in all_entities.data

        # Update entity in storage
        updated_entity = {"id": entity_id, "status": "completed"}
        repo._storage[entity_id] = updated_entity

        # Verify update
        found_updated = repo.find_by_id(entity_id)
        assert found_updated.is_success
        assert found_updated.data == updated_entity

        # Remove entity using delete method
        delete_result = repo.delete(entity_id)
        assert delete_result.is_success

        # Verify removal
        not_found = repo.find_by_id(entity_id)
        assert not_found.is_failure
        assert not_found.error is not None
        assert "Entity not found" in not_found.error

        empty_results = repo.find_all()
        assert empty_results.is_success
        assert empty_results.data is not None
        assert len(empty_results.data) == 0
