from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.requirement import Requirement


class InMemoryRequirementRepository(RequirementRepository):
    """Fake, in-memory implementation of the RequirementRepository port.

    Used to verify, in tests, that a concrete implementation can satisfy the
    port's contract, and to test Application Layer logic without depending
    on any real persistence technology. Lives under tests/ because it is a
    test double, not production code: a future SQLiteRequirementRepository
    (Week 2) will implement the same port for real, durable storage, under
    infrastructure/persistence/.
    """

    def __init__(self) -> None:
        self._storage: dict[str, Requirement] = {}

    def save(self, requirement_id: str, requirement: Requirement) -> None:
        self._storage[requirement_id] = requirement

    def get_by_id(self, requirement_id: str) -> Requirement | None:
        return self._storage.get(requirement_id)
