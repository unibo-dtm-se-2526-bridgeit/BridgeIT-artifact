from abc import ABC, abstractmethod

from bridgeit.domain.requirement import Requirement


class RequirementRepository(ABC):
    """Port (interface) for persisting and retrieving Requirement aggregates.

    This is an abstraction, not an implementation: the Application Layer
    depends on this contract, never on a concrete storage technology.
    Concrete implementations (e.g. an in-memory fake for testing, or a
    future SQLite adapter) live outside the application/domain layers and
    implement this same interface.
    """

    @abstractmethod
    def save(self, requirement_id: str, requirement: Requirement) -> None:
        """Persist a Requirement under the given identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, requirement_id: str) -> Requirement | None:
        """Retrieve a Requirement by its identifier, or None if not found."""
        raise NotImplementedError
