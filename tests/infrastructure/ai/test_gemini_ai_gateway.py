"""Unit tests for GeminiAIGateway.

The Gemini client is always mocked here -- the real API is never called
in automated tests, consistent with report.md -- Testing Strategy.
"""

from unittest.mock import MagicMock

import pytest

from bridgeit.application.ports.ai_gateway import AIGatewayError
from bridgeit.domain.ai_analysis import QualityScore
from bridgeit.infrastructure.ai.gemini_ai_gateway import GeminiAIGateway


def _mocked_client(response_text: str) -> MagicMock:
    client = MagicMock()
    client.models.generate_content.return_value = MagicMock(text=response_text)
    return client


class TestGeminiAIGatewayAnalyse:
    def test_returns_needs_clarification_when_gemini_reports_issues(self) -> None:
        client = _mocked_client(
            '{"quality_indication": "needs_clarification", '
            '"issues": ["Missing a measurable acceptance criterion."]}'
        )
        gateway = GeminiAIGateway(client=client)

        analysis = gateway.analyse("The system shall be fast.")

        assert analysis.quality_score == QualityScore.NEEDS_CLARIFICATION
        assert analysis.issues == ("Missing a measurable acceptance criterion.",)

    def test_returns_ready_for_validation_with_no_issues(self) -> None:
        client = _mocked_client('{"quality_indication": "ready_for_validation", "issues": []}')
        gateway = GeminiAIGateway(client=client)

        analysis = gateway.analyse("The system shall respond within 200ms for 95% of requests.")

        assert analysis.quality_score == QualityScore.READY_FOR_VALIDATION
        assert analysis.issues == ()

    def test_calls_the_client_with_the_configured_model(self) -> None:
        client = _mocked_client('{"quality_indication": "ready_for_validation", "issues": []}')
        gateway = GeminiAIGateway(client=client, model="gemini-2.0-flash")

        gateway.analyse("Some requirement text.")

        _, kwargs = client.models.generate_content.call_args
        assert kwargs["model"] == "gemini-2.0-flash"
        assert "Some requirement text." in kwargs["contents"]

    def test_raises_ai_gateway_error_on_malformed_json(self) -> None:
        client = _mocked_client("this is not JSON")
        gateway = GeminiAIGateway(client=client)

        with pytest.raises(AIGatewayError):
            gateway.analyse("Some requirement text.")

    def test_raises_ai_gateway_error_on_unexpected_quality_indication_value(self) -> None:
        client = _mocked_client('{"quality_indication": "maybe", "issues": []}')
        gateway = GeminiAIGateway(client=client)

        with pytest.raises(AIGatewayError):
            gateway.analyse("Some requirement text.")

    def test_raises_ai_gateway_error_when_quality_indication_is_missing(self) -> None:
        client = _mocked_client('{"issues": []}')
        gateway = GeminiAIGateway(client=client)

        with pytest.raises(AIGatewayError):
            gateway.analyse("Some requirement text.")


class TestGeminiAIGatewayLazyInitialization:
    def test_construction_never_fails_even_without_a_key_or_client(self) -> None:
        # Must never raise, even with GEMINI_API_KEY unset -- constructing
        # this at app startup (main.py) must not be able to take down the
        # whole app over a missing AI key.
        GeminiAIGateway()

    def test_analyse_raises_a_clear_error_when_no_key_and_no_client(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        gateway = GeminiAIGateway()

        with pytest.raises(AIGatewayError):
            gateway.analyse("Some requirement text.")
