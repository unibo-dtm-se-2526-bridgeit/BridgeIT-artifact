"""Unit tests for ValidateRequirementUseCase."""

import pytest

from bridgeit.application.use_cases.validate_requirement import (
    InvalidValidationDecisionError,
    RequirementNotFoundError,
    ValidateRequirementUseCase,
)
from bridgeit.domain.requirement import (
    InvalidStateTransitionError,
    Requirement,
    RequirementStatus,
)
from tests.application.fakes import InMemoryRequirementRepository


def _analyzed_requirement(text: str = "The system shall do X.") -> Requirement:
    requirement = Requirement.submit(text)
    requirement.mark_analyzed()
    return requirement


class TestValidateRequirementUseCase:
    def test_approve_moves_the_requirement_to_validated(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = _analyzed_requirement()
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        result = use_case.execute(requirement.id, decision="approve")

        assert result.status == RequirementStatus.VALIDATED

    def test_reject_moves_the_requirement_to_rejected(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = _analyzed_requirement()
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        result = use_case.execute(requirement.id, decision="reject")

        assert result.status == RequirementStatus.REJECTED

    def test_edit_moves_the_requirement_to_clarified_with_new_text(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = _analyzed_requirement("Original text.")
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        result = use_case.execute(
            requirement.id, decision="edit", modified_text="Better text."
        )

        assert result.status == RequirementStatus.CLARIFIED
        assert result.text.content == "Better text."

    def test_edit_without_modified_text_raises(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = _analyzed_requirement()
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        with pytest.raises(InvalidValidationDecisionError):
            use_case.execute(requirement.id, decision="edit", modified_text=None)

    def test_unknown_decision_value_raises(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = _analyzed_requirement()
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        with pytest.raises(InvalidValidationDecisionError):
            use_case.execute(requirement.id, decision="not-a-real-decision")

    def test_raises_when_requirement_does_not_exist(self) -> None:
        repository = InMemoryRequirementRepository()
        use_case = ValidateRequirementUseCase(repository)

        with pytest.raises(RequirementNotFoundError):
            use_case.execute("does-not-exist", decision="approve")

    def test_approve_on_a_submitted_requirement_raises_invalid_transition(self) -> None:
        # Guarantee required by FR-05: no AIAnalysis / validation can skip
        # the domain's own state machine. A Requirement that has never
        # been analyzed cannot be validated directly.
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall do X.")
        repository.save(requirement.id, requirement)
        use_case = ValidateRequirementUseCase(repository)

        with pytest.raises(InvalidStateTransitionError):
            use_case.execute(requirement.id, decision="approve")
