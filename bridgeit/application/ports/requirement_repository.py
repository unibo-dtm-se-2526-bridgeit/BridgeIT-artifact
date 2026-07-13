from abc import ABC, abstractmethod
from typing import Any


class RequirementRepository(ABC):
    """Port (interface) for persisting and retrieving Requirement aggregates.

    This is an abstraction, not an implementation: the Application Layer
    depends on this contract, never on a concrete storage technology.
    Concrete implementations (e.g. an in-memory fake for testing, or a
    future SQLite adapter) live outside the application/domain layers and
    implement this same interface.

    NOTE: the `requirement` parameter is typed as `Any` for now, since the
    real `Requirement` domain entity (owned by the Domain Layer) does not
    exist yet on this branch. It will be tightened to the concrete
    `Requirement` type once the domain layer is integrated.
    """

    @abstractmethod
    def save(self, requirement_id: str, requirement: Any) -> None:
        """Persist a Requirement under the given identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, requirement_id: str) -> Any | None:
        """Retrieve a Requirement by its identifier, or None if not found."""
        raise NotImplementedError
