"""Unit tests for the Requirement entity and its value objects.

These tests exercise the domain layer in complete isolation: no
FastAPI, no database, no AI client -- consistent with NFR-02
(Testability) and the Dependency Rules in architecture.md.
"""

import pytest

from bridgeit.domain.requirement import (
    InvalidStateTransitionError,
    Requirement,
    RequirementStatus,
    RequirementText,
)


class TestRequirementText:
    def test_holds_the_given_content(self) -> None:
        text = RequirementText("The system shall do X.")
        assert text.content == "The system shall do X."

    def test_rejects_empty_content(self) -> None:
        with pytest.raises(ValueError):
            RequirementText("")

    def test_rejects_whitespace_only_content(self) -> None:
        with pytest.raises(ValueError):
            RequirementText("   ")

    def test_two_texts_with_same_content_are_equal(self) -> None:
        assert RequirementText("same text") == RequirementText("same text")


class TestRequirementCreation:
    def test_submit_creates_a_requirement_in_submitted_status(self) -> None:
        requirement = Requirement.submit("The system shall do X.")

        assert requirement.status == RequirementStatus.SUBMITTED
        assert requirement.text.content == "The system shall do X."

    def test_each_submitted_requirement_has_a_unique_id(self) -> None:
        first = Requirement.submit("Requirement A")
        second = Requirement.submit("Requirement B")

        assert first.id != second.id


class TestRequirementValidLifecycle:
    def test_can_move_from_submitted_to_analyzed(self) -> None:
        requirement = Requirement.submit("The system shall do X.")

        requirement.mark_analyzed()

        assert requirement.status == RequirementStatus.ANALYZED

    def test_can_be_clarified_after_analysis_and_then_re_analyzed(self) -> None:
        requirement = Requirement.submit("Original text.")
        requirement.mark_analyzed()

        requirement.clarify("Clarified, less ambiguous text.")

        assert requirement.status == RequirementStatus.CLARIFIED
        assert requirement.text.content == "Clarified, less ambiguous text."

        requirement.mark_analyzed()
        assert requirement.status == RequirementStatus.ANALYZED

    def test_can_be_validated_after_analysis(self) -> None:
        requirement = Requirement.submit("The system shall do X.")
        requirement.mark_analyzed()

        requirement.validate()

        assert requirement.status == RequirementStatus.VALIDATED

    def test_can_be_rejected_after_analysis(self) -> None:
        requirement = Requirement.submit("The system shall do X.")
        requirement.mark_analyzed()

        requirement.reject()

        assert requirement.status == RequirementStatus.REJECTED


class TestRequirementInvalidTransitions:
    def test_cannot_be_validated_directly_from_submitted(self) -> None:
        requirement = Requirement.submit("The system shall do X.")

        with pytest.raises(InvalidStateTransitionError):
            requirement.validate()

    def test_cannot_be_analyzed_again_once_validated(self) -> None:
        requirement = Requirement.submit("The system shall do X.")
        requirement.mark_analyzed()
        requirement.validate()

        with pytest.raises(InvalidStateTransitionError):
            requirement.mark_analyzed()

    def test_cannot_be_clarified_directly_from_submitted(self) -> None:
        requirement = Requirement.submit("The system shall do X.")

        with pytest.raises(InvalidStateTransitionError):
            requirement.clarify("New text")
