"""Unit tests for AIAnalysis and QualityScore."""

from bridgeit.domain.ai_analysis import AIAnalysis, QualityScore


class TestQualityScore:
    def test_has_the_two_values_required_by_fr04(self) -> None:
        assert QualityScore.READY_FOR_VALIDATION.value == "ready_for_validation"
        assert QualityScore.NEEDS_CLARIFICATION.value == "needs_clarification"


class TestAIAnalysis:
    def test_stores_quality_score_and_issues(self) -> None:
        analysis = AIAnalysis(
            quality_score=QualityScore.NEEDS_CLARIFICATION,
            issues=("Missing a measurable acceptance criterion.",),
        )

        assert analysis.quality_score == QualityScore.NEEDS_CLARIFICATION
        assert analysis.issues == ("Missing a measurable acceptance criterion.",)

    def test_issues_defaults_to_empty(self) -> None:
        analysis = AIAnalysis(quality_score=QualityScore.READY_FOR_VALIDATION)

        assert analysis.issues == ()

    def test_issues_is_always_stored_as_a_tuple(self) -> None:
        # Constructed with a list, but stored as an immutable tuple --
        # AIAnalysis is a value object.
        analysis = AIAnalysis(
            quality_score=QualityScore.READY_FOR_VALIDATION,
            issues=("one", "two"),
        )

        assert isinstance(analysis.issues, tuple)
