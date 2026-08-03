"""Application layer use case: record a human validation decision (FR-05).

This is the mechanism that makes BridgeIT's central principle true:
"AI suggests, the human validates". No AIAnalysis can change a
Requirement's authoritative status -- only this use case, triggered by
an explicit human decision, can.
"""

from __future__ import annotations

from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.requirement import Requirement

_ALLOWED_DECISIONS = {"approve", "edit", "reject"}


class RequirementNotFoundError(Exception):
    """Raised when no Requirement exists with the given id."""


class InvalidValidationDecisionError(Exception):
    """Raised when `decision` is not one of approve/edit/reject, or when
    data required for a decision is missing (e.g. modified_text for
    "edit"). Maps to the agreed "invalid_decision_value" / "missing_field"
    API error codes (400)."""


class ValidateRequirementUseCase:
    """Use case backing POST /requirements/{id}/validate.

    Maps a human's validation decision to the corresponding Requirement
    lifecycle method, per the JSON contract agreed with @marthinaf03:
    - "approve" -> requirement.validate()   -> status "Validated"
    - "edit"    -> requirement.clarify(...) -> status "Clarified"
    - "reject"  -> requirement.reject()     -> status "Rejected"
    """

    def __init__(self, repository: RequirementRepository) -> None:
        self._repository = repository

    def execute(
        self, requirement_id: str, decision: str, modified_text: str | None = None
    ) -> Requirement:
        if decision not in _ALLOWED_DECISIONS:
            raise InvalidValidationDecisionError(f"Unknown decision: {decision!r}")

        requirement = self._repository.get_by_id(requirement_id)
        if requirement is None:
            raise RequirementNotFoundError(requirement_id)

        if decision == "approve":
            requirement.validate()
        elif decision == "reject":
            requirement.reject()
        else:  # decision == "edit"
            if not modified_text:
                raise InvalidValidationDecisionError(
                    "modified_text is required when decision is 'edit'."
                )
            requirement.clarify(modified_text)

        self._repository.save(requirement_id, requirement)
        return requirement
