"""Application layer use case: request an AI analysis for a Requirement (FR-02).

Orchestrates the domain (Requirement), the persistence port
(RequirementRepository), and the AIGateway port -- consistent with
architecture.md: the application layer is the only layer allowed to
depend on both ports at once.
"""

from __future__ import annotations

from bridgeit.application.ports.ai_gateway import AIGateway
from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.ai_analysis import AIAnalysis


class RequirementNotFoundError(Exception):
    """Raised when no Requirement exists with the given id."""


class AnalyseRequirementUseCase:
    """Use case backing POST /requirements/{id}/analyse."""

    def __init__(self, repository: RequirementRepository, ai_gateway: AIGateway) -> None:
        self._repository = repository
        self._ai_gateway = ai_gateway

    def execute(self, requirement_id: str) -> AIAnalysis:
        requirement = self._repository.get_by_id(requirement_id)
        if requirement is None:
            raise RequirementNotFoundError(requirement_id)

        analysis = self._ai_gateway.analyse(requirement.text.content)

        # mark_analyzed() raises InvalidStateTransitionError (already
        # defined on Requirement) if the requirement isn't in a state
        # that allows analysis -- maps directly to the agreed
        # "invalid_status_transition" -> 409 API error.
        requirement.mark_analyzed()
        self._repository.save(requirement_id, requirement)
        return analysis
