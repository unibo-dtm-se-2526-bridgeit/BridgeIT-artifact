"""Unit tests for AnalyseRequirementUseCase."""

from unittest.mock import MagicMock

import pytest

from bridgeit.application.use_cases.analyse_requirement import (
    AnalyseRequirementUseCase,
    RequirementNotFoundError,
)
from bridgeit.domain.ai_analysis import AIAnalysis, QualityScore
from bridgeit.domain.requirement import Requirement, RequirementStatus
from tests.application.fakes import InMemoryRequirementRepository


def _fake_ai_gateway(analysis: AIAnalysis) -> MagicMock:
    gateway = MagicMock()
    gateway.analyse.return_value = analysis
    return gateway


class TestAnalyseRequirementUseCase:
    def test_marks_the_requirement_as_analyzed(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall do X.")
        repository.save(requirement.id, requirement)

        analysis = AIAnalysis(quality_score=QualityScore.READY_FOR_VALIDATION)
        use_case = AnalyseRequirementUseCase(repository, _fake_ai_gateway(analysis))

        use_case.execute(requirement.id)

        retrieved = repository.get_by_id(requirement.id)
        assert retrieved is not None
        assert retrieved.status == RequirementStatus.ANALYZED

    def test_returns_the_ai_analysis(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall do X.")
        repository.save(requirement.id, requirement)

        analysis = AIAnalysis(
            quality_score=QualityScore.NEEDS_CLARIFICATION,
            issues=("Ambiguous actor.",),
        )
        use_case = AnalyseRequirementUseCase(repository, _fake_ai_gateway(analysis))

        result = use_case.execute(requirement.id)

        assert result is analysis

    def test_raises_when_requirement_does_not_exist(self) -> None:
        repository = InMemoryRequirementRepository()
        use_case = AnalyseRequirementUseCase(
            repository,
            _fake_ai_gateway(
                AIAnalysis(quality_score=QualityScore.READY_FOR_VALIDATION)
            ),
        )

        with pytest.raises(RequirementNotFoundError):
            use_case.execute("does-not-exist")
