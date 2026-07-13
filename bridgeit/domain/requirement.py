"""Domain layer: the Requirement entity and its value objects.

Pure Python only -- no external imports (no FastAPI, no SQLAlchemy, no AI
client), consistent with the Dependency Rules in architecture.md: the
domain layer must remain independent of any infrastructure or delivery
mechanism.

See docs/domain-model.md for the full conceptual description of
Requirement, RequirementText, and RequirementStatus.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import uuid4


class RequirementStatus(Enum):
    """The lifecycle states a Requirement can be in.

    Mirrors the RequirementStatus enumeration in domain-model.md.
    """

    SUBMITTED = "Submitted"
    ANALYZED = "Analyzed"
    CLARIFIED = "Clarified"
    VALIDATED = "Validated"
    REJECTED = "Rejected"


@dataclass(frozen=True)
class RequirementText:
    """Immutable value object holding a Requirement's natural-language text.

    See domain-model.md -- RequirementText: two texts with identical
    content are equal by value, and a new RequirementText is created
    every time a requirement's wording changes (it is never mutated
    in place).
    """

    content: str

    def __post_init__(self) -> None:
        if not self.content or not self.content.strip():
            raise ValueError("RequirementText cannot be empty.")


class InvalidStateTransitionError(Exception):
    """Raised when a Requirement is asked to move to a status that is
    not reachable from its current status."""


# The state machine described in domain-model.md -- Requirement (lifecycle
# / state transitions): Submitted -> Analyzed -> Clarified -> Validated,
# with Rejected reachable at the validation step.
#
# NOTE (design choice, since domain-model.md leaves this detail open):
# clarifying a requirement always loops back to ANALYZED, since a
# clarified requirement is expected to be re-analyzed before it can be
# validated. If this project later decides otherwise, this is the one
# place to change.
_ALLOWED_TRANSITIONS: dict[RequirementStatus, set[RequirementStatus]] = {
    RequirementStatus.SUBMITTED: {RequirementStatus.ANALYZED},
    RequirementStatus.ANALYZED: {
        RequirementStatus.CLARIFIED,
        RequirementStatus.VALIDATED,
        RequirementStatus.REJECTED,
    },
    RequirementStatus.CLARIFIED: {RequirementStatus.ANALYZED},
    RequirementStatus.VALIDATED: set(),
    RequirementStatus.REJECTED: set(),
}


class Requirement:
    """The Requirement aggregate root.

    See domain-model.md -- Requirement and Aggregate Boundary: Requirement
    is the aggregate root and the central domain concept; it is
    responsible for holding its own current text and status, and for
    governing its own lifecycle transitions.
    """

    def __init__(self, requirement_id: str, text: RequirementText) -> None:
        self._id = requirement_id
        self._text = text
        self._status = RequirementStatus.SUBMITTED

    @classmethod
    def submit(cls, text: str) -> "Requirement":
        """Create a new Requirement from raw text (FR-01).

        A freshly submitted Requirement always starts in the SUBMITTED
        status -- this is not a choice left to the caller.
        """
        return cls(requirement_id=str(uuid4()), text=RequirementText(text))

    @property
    def id(self) -> str:
        return self._id

    @property
    def text(self) -> RequirementText:
        return self._text

    @property
    def status(self) -> RequirementStatus:
        return self._status

    def _transition_to(self, new_status: RequirementStatus) -> None:
        allowed = _ALLOWED_TRANSITIONS[self._status]
        if new_status not in allowed:
            raise InvalidStateTransitionError(
                f"Cannot move from {self._status.value} to {new_status.value}."
            )
        self._status = new_status

    def mark_analyzed(self) -> None:
        """Record that an AI Analysis has been produced for this requirement (FR-02)."""
        self._transition_to(RequirementStatus.ANALYZED)

    def clarify(self, new_text: str) -> None:
        """Revise the requirement's wording in response to an analysis (FR-03).

        Replaces the current RequirementText with a new one -- the value
        object itself is never mutated -- and moves the status to CLARIFIED.
        """
        self._transition_to(RequirementStatus.CLARIFIED)
        self._text = RequirementText(new_text)

    def validate(self) -> None:
        """Mark the requirement as Validated (FR-05), making it eligible
        to become the source of a Derived Artifact (FR-07)."""
        self._transition_to(RequirementStatus.VALIDATED)

    def reject(self) -> None:
        """Mark the requirement as Rejected (FR-05); it will not proceed
        to artifact generation."""
        self._transition_to(RequirementStatus.REJECTED)
