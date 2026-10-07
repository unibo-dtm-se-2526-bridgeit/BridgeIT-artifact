"""Application layer use case: request an AI analysis for a Requirement (FR-02).

Orchestrates the domain (Requirement), the persistence port
(RequirementRepository), and the AIGateway port -- consistent with
architecture.md: the application layer is the only layer allowed to
depend on both ports at once.
"""

from __future__ import annotations

from bridgeit.application.errors import RequirementNotFoundError
from bridgeit.application.ports.ai_gateway import AIGateway
from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.ai_analysis import AIAnalysis


class AnalyseRequirementUseCase:
    """Use case backing POST /requirements/{id}/analyse."""

    def __init__(
        self, repository: RequirementRepository, ai_gateway: AIGateway
    ) -> None:
        self._repository = repository
        self._ai_gateway = ai_gateway

    def execute(self, requirement_id: str) -> AIAnalysis:
        requirement = self._repository.get_by_id(requirement_id)
        if requirement is None:
            raise RequirementNotFoundError(requirement_id)

        # Check the lifecycle rule BEFORE calling the AI provider, so that an
        # invalid request (e.g. analysing a Validated requirement) is
        # rejected with InvalidStateTransitionError -> 409 without
        # consuming any Gemini free-tier quota.
        requirement.ensure_can_be_analyzed()

        analysis = self._ai_gateway.analyse(requirement.text.content)

        requirement.mark_analyzed()
        self._repository.save(requirement_id, requirement)
        return analysis
