import pytest

from bridgeit.application.ports.requirement_repository import RequirementRepository
from tests.application.fakes import InMemoryRequirementRepository


class TestInMemoryRequirementRepository:
    """Verifies that InMemoryRequirementRepository honours the
    RequirementRepository port's contract."""

    def test_is_a_requirement_repository(self) -> None:
        # The fake must be a genuine implementation of the port: this is
        # what guarantees it can be used anywhere the port is expected.
        repository = InMemoryRequirementRepository()
        assert isinstance(repository, RequirementRepository)

    def test_save_then_get_by_id_returns_the_same_requirement(self) -> None:
        repository = InMemoryRequirementRepository()
        fake_requirement = {"text": "The system shall do X"}

        repository.save("req-1", fake_requirement)
        retrieved = repository.get_by_id("req-1")

        assert retrieved == fake_requirement

    def test_get_by_id_returns_none_when_not_found(self) -> None:
        repository = InMemoryRequirementRepository()

        retrieved = repository.get_by_id("does-not-exist")

        assert retrieved is None

    def test_save_does_not_alter_the_stored_requirement(self) -> None:
        # Sanity check: the repository must not mutate or lose data between
        # a write and a read (relevant now, and even more so once a real
        # persistence adapter replaces this fake in Week 2).
        repository = InMemoryRequirementRepository()
        original = {"text": "Original text", "status": "Submitted"}

        repository.save("req-2", original)
        retrieved = repository.get_by_id("req-2")

        assert retrieved is not None
        assert retrieved["text"] == "Original text"
        assert retrieved["status"] == "Submitted"


@pytest.fixture
def repository() -> InMemoryRequirementRepository:
    return InMemoryRequirementRepository()


def test_repository_starts_empty(repository: InMemoryRequirementRepository) -> None:
    assert repository.get_by_id("anything") is None
