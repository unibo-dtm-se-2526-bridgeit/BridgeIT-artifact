"""Application layer use case: submit a new Requirement (FR-01).

Orchestrates the domain (Requirement) and the persistence port
(RequirementRepository) -- consistent with architecture.md: the
application layer coordinates domain objects and ports, the driving
adapter (the FastAPI route) should depend on this use case rather than
on infrastructure directly.
"""

from __future__ import annotations

from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.requirement import Requirement


class SubmitRequirementUseCase:
    """Use case backing POST /requirements."""

    def __init__(self, repository: RequirementRepository) -> None:
        self._repository = repository

    def execute(self, text: str) -> Requirement:
        requirement = Requirement.submit(text)
        self._repository.save(requirement.id, requirement)
        return requirement
