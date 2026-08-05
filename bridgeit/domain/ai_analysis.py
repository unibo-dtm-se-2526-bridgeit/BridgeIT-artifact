"""Domain layer: the AIAnalysis entity and its QualityScore value object.

Pure Python only -- no external imports, consistent with the Dependency
Rules in architecture.md: the domain layer must remain independent of
any infrastructure or delivery mechanism, including the AI provider
that eventually produces an AIAnalysis.

See docs/domain-model.md for the conceptual description of AIAnalysis
and QualityScore.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QualityScore(Enum):
    """The quality indication produced by an AI analysis (FR-04).

    FR-04's acceptance criteria (report.md) only requires distinguishing
    "ready for validation" from "needs clarification" -- not a numeric
    score. A category is also more honest about what an AI judgement
    actually is: a qualitative signal, not a precise measurement.
    """

    READY_FOR_VALIDATION = "ready_for_validation"
    NEEDS_CLARIFICATION = "needs_clarification"


@dataclass(frozen=True)
class AIAnalysis:
    """The result of an AI-assisted analysis of a Requirement (FR-02, FR-04).

    Deliberately NOT persisted as its own aggregate at this stage: it is
    produced by the AI Gateway, used immediately to inform the
    /requirements/{id}/analyse response and to move the Requirement to
    Analyzed, and is not queried on its own later. If a future
    requirement needs analysis history, this can be revisited -- see
    domain-model.md's note on modeling assumptions left open.
    """

    quality_score: QualityScore
    issues: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        # Accept any iterable of strings (e.g. a list) at construction time,
        # but always store an immutable tuple internally -- consistent
        # with this being a value object.
        object.__setattr__(self, "issues", tuple(self.issues))
