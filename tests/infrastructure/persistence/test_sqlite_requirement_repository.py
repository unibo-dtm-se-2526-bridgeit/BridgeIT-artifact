import pytest

from bridgeit.domain.requirement import Requirement
from bridgeit.infrastructure.persistence.sqlite_requirement_repository import (
    SQLiteRequirementRepository,
)


@pytest.fixture
def repository(tmp_path) -> SQLiteRequirementRepository:
    # tmp_path is a pytest built-in fixture: a fresh temporary directory,
    # unique per test, automatically cleaned up afterwards. Using a real
    # file (instead of ":memory:") is closer to how the repository will
    # actually be used, while still keeping tests isolated from each other.
    db_path = tmp_path / "test_bridgeit.db"
    return SQLiteRequirementRepository(db_path)


def test_save_then_get_by_id_returns_an_equivalent_requirement(
    repository: SQLiteRequirementRepository,
) -> None:
    requirement = Requirement.submit("The system shall do X")

    repository.save(requirement.id, requirement)
    retrieved = repository.get_by_id(requirement.id)

    assert retrieved is not None
    assert retrieved.id == requirement.id
    assert retrieved.text.content == requirement.text.content
    assert retrieved.status == requirement.status


def test_get_by_id_returns_none_when_not_found(
    repository: SQLiteRequirementRepository,
) -> None:
    assert repository.get_by_id("does-not-exist") is None


def test_save_does_not_alter_the_requirement_content(
    repository: SQLiteRequirementRepository,
) -> None:
    requirement = Requirement.submit("Original text")

    repository.save(requirement.id, requirement)
    retrieved = repository.get_by_id(requirement.id)

    assert retrieved is not None
    assert retrieved.text.content == "Original text"
    assert retrieved.status.value == "Submitted"


def test_save_persists_updated_status(repository: SQLiteRequirementRepository) -> None:
    requirement = Requirement.submit("The system shall do X")
    requirement.mark_analyzed()

    repository.save(requirement.id, requirement)
    retrieved = repository.get_by_id(requirement.id)

    assert retrieved is not None
    assert retrieved.status.value == "Analyzed"


def test_data_survives_across_repository_instances(tmp_path) -> None:
    # Confirms persistence is real (on disk), not just an in-memory cache:
    # a second repository instance pointed at the same file must see data
    # saved by the first one.
    db_path = tmp_path / "test_bridgeit.db"
    requirement = Requirement.submit("Persisted across instances")

    first_repository = SQLiteRequirementRepository(db_path)
    first_repository.save(requirement.id, requirement)

    second_repository = SQLiteRequirementRepository(db_path)
    retrieved = second_repository.get_by_id(requirement.id)

    assert retrieved is not None
    assert retrieved.text.content == "Persisted across instances"
