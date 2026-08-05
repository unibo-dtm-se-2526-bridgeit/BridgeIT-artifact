"""Integration tests for the analyse/validate routes, using FastAPI's
TestClient. No real Gemini call, no real database -- both replaced with
fakes/mocks passed directly to register_analysis_routes.
"""

from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from bridgeit.adapters.api.analysis_router import register_analysis_routes
from bridgeit.adapters.api.errors import register_error_handlers
from bridgeit.domain.ai_analysis import AIAnalysis, QualityScore
from bridgeit.domain.requirement import Requirement
from tests.application.fakes import InMemoryRequirementRepository


def _build_client(repository: InMemoryRequirementRepository) -> TestClient:
    app = FastAPI()
    register_error_handlers(app)

    fake_ai_gateway = MagicMock()
    fake_ai_gateway.analyse.return_value = AIAnalysis(
        quality_score=QualityScore.NEEDS_CLARIFICATION, issues=("Ambiguous actor.",)
    )

    register_analysis_routes(app, repository=repository, ai_gateway=fake_ai_gateway)
    return TestClient(app)


class TestAnalyseRoute:
    def test_returns_200_with_the_analysis(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall be fast.")
        repository.save(requirement.id, requirement)
        client = _build_client(repository)

        response = client.post(f"/requirements/{requirement.id}/analyse")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "Analyzed"
        assert body["analysis"]["quality_indication"] == "needs_clarification"
        assert body["analysis"]["issues"] == ["Ambiguous actor."]

    def test_returns_404_with_api_error_shape_when_requirement_missing(self) -> None:
        repository = InMemoryRequirementRepository()
        client = _build_client(repository)

        response = client.post("/requirements/does-not-exist/analyse")

        assert response.status_code == 404
        assert response.json()["error"]["code"] == "requirement_not_found"


class TestValidateRoute:
    def test_approve_returns_200_with_validated_status(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall be fast.")
        requirement.mark_analyzed()
        repository.save(requirement.id, requirement)
        client = _build_client(repository)

        response = client.post(
            f"/requirements/{requirement.id}/validate", json={"decision": "approve"}
        )

        assert response.status_code == 200
        assert response.json()["status"] == "Validated"

    def test_edit_without_modified_text_returns_400_with_api_error_shape(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall be fast.")
        requirement.mark_analyzed()
        repository.save(requirement.id, requirement)
        client = _build_client(repository)

        response = client.post(
            f"/requirements/{requirement.id}/validate", json={"decision": "edit"}
        )

        assert response.status_code == 400
        assert response.json()["error"]["code"] == "missing_field"

    def test_approve_on_submitted_requirement_returns_409(self) -> None:
        repository = InMemoryRequirementRepository()
        requirement = Requirement.submit("The system shall be fast.")
        repository.save(requirement.id, requirement)
        client = _build_client(repository)

        response = client.post(
            f"/requirements/{requirement.id}/validate", json={"decision": "approve"}
        )

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "invalid_status_transition"
