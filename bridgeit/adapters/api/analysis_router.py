"""Driving adapter: FastAPI routes for AI analysis and human validation.

Wire this into the app from main.py:

    from bridgeit.adapters.api.analysis_router import register_analysis_routes
    register_analysis_routes(app, repository=_repository, ai_gateway=_ai_gateway)

No business logic here -- routes only translate HTTP requests into use
case calls and use case results into HTTP responses, consistent with
architecture.md -- Adapter Responsibilities.

Uses the same shared ApiError from bridgeit.adapters.api.errors that
GET /requirements/{id} already uses, so every endpoint's error response
follows the same {"error": {"code", "message"}} shape.
"""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from bridgeit.adapters.api.errors import ApiError
from bridgeit.application.ports.ai_gateway import AIGateway, AIGatewayError
from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.application.use_cases.analyse_requirement import (
    AnalyseRequirementUseCase,
    RequirementNotFoundError,
)
from bridgeit.application.use_cases.validate_requirement import (
    InvalidValidationDecisionError,
    ValidateRequirementUseCase,
)
from bridgeit.domain.requirement import InvalidStateTransitionError


class AnalysisBody(BaseModel):
    quality_indication: str
    issues: list[str]


class AnalysisResponse(BaseModel):
    requirement_id: str
    status: str
    analysis: AnalysisBody


class ValidateRequest(BaseModel):
    decision: Literal["approve", "edit", "reject"]
    modified_text: str | None = None


class ValidateResponse(BaseModel):
    requirement_id: str
    status: str


def register_analysis_routes(
    app: FastAPI, repository: RequirementRepository, ai_gateway: AIGateway
) -> None:
    """Register /requirements/{id}/analyse and /validate on the given app.

    Mirrors the same "construct once, close over it" style already used
    in main.py for the repository -- consistent with the TEMPORARY note
    there: a proper Use Case-based dependency wiring can replace this
    once the rest of the routes are refactored too.
    """

    analyse_use_case = AnalyseRequirementUseCase(repository, ai_gateway)
    validate_use_case = ValidateRequirementUseCase(repository)

    @app.post(
        "/requirements/{requirement_id}/analyse",
        response_model=AnalysisResponse,
    )
    def analyse_requirement(requirement_id: str) -> AnalysisResponse:
        """Request an AI-assisted analysis of a requirement (FR-02, FR-04)."""
        try:
            analysis = analyse_use_case.execute(requirement_id)
        except RequirementNotFoundError as error:
            raise ApiError(
                status_code=404,
                code="requirement_not_found",
                message="No requirement found with the given id.",
            ) from error
        except InvalidStateTransitionError as error:
            raise ApiError(
                status_code=409, code="invalid_status_transition", message=str(error)
            ) from error
        except AIGatewayError as error:
            raise ApiError(
                status_code=502, code="ai_provider_error", message=str(error)
            ) from error

        return AnalysisResponse(
            requirement_id=requirement_id,
            status="Analyzed",
            analysis=AnalysisBody(
                quality_indication=analysis.quality_score.value,
                issues=list(analysis.issues),
            ),
        )

    @app.post(
        "/requirements/{requirement_id}/validate",
        response_model=ValidateResponse,
    )
    def validate_requirement(
        requirement_id: str, body: ValidateRequest
    ) -> ValidateResponse:
        """Record a human validation decision for a requirement (FR-05)."""
        try:
            requirement = validate_use_case.execute(
                requirement_id, body.decision, body.modified_text
            )
        except RequirementNotFoundError as error:
            raise ApiError(
                status_code=404,
                code="requirement_not_found",
                message="No requirement found with the given id.",
            ) from error
        except InvalidValidationDecisionError as error:
            raise ApiError(status_code=400, code="missing_field", message=str(error)) from error
        except InvalidStateTransitionError as error:
            raise ApiError(
                status_code=409, code="invalid_status_transition", message=str(error)
            ) from error

        return ValidateResponse(requirement_id=requirement_id, status=requirement.status.value)
