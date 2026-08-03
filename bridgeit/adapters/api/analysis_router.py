"""Driving adapter: FastAPI routes for AI analysis and human validation.

Wire this router into the existing FastAPI app
(bridgeit/adapters/api/main.py):

    from bridgeit.adapters.api.analysis_router import router as analysis_router
    app.include_router(analysis_router)

No business logic here -- every route only translates HTTP requests into
use case calls and use case results into HTTP responses, consistent
with architecture.md -- Adapter Responsibilities.

NOTE on ApiError: @marthinaf03 already defined and applied this shared
error model to GET /requirements/{id} (see bridgeit/application/dto.py
in the real repository). Import and reuse that one instead of the
ApiError/ApiErrorBody classes below -- they are only included here so
this skeleton file is self-contained and independently testable.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from bridgeit.application.ports.ai_gateway import AIGatewayError
from bridgeit.application.use_cases.analyse_requirement import (
    AnalyseRequirementUseCase,
    RequirementNotFoundError,
)
from bridgeit.application.use_cases.validate_requirement import (
    InvalidValidationDecisionError,
    ValidateRequirementUseCase,
)
from bridgeit.domain.requirement import InvalidStateTransitionError

router = APIRouter()


# --- Request/response models -------------------------------------------


class ApiErrorBody(BaseModel):
    code: str
    message: str


class ApiError(BaseModel):
    error: ApiErrorBody


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


# --- Dependencies ---------------------------------------------------------
# Placeholders: replace with however @marthinaf03 already wires the real
# SQLiteRequirementRepository instance into the existing POST /requirements
# endpoint (likely a FastAPI `Depends` returning a shared repository
# instance). get_analyse_use_case additionally needs a GeminiAIGateway
# instance (constructed once, e.g. at app startup, using GEMINI_API_KEY).


def get_analyse_use_case() -> AnalyseRequirementUseCase:
    raise NotImplementedError("Wire this to the real repository and AI gateway instances.")


def get_validate_use_case() -> ValidateRequirementUseCase:
    raise NotImplementedError("Wire this to the real repository instance.")


# --- Routes ----------------------------------------------------------------


@router.post(
    "/requirements/{requirement_id}/analyse",
    response_model=AnalysisResponse,
    responses={404: {"model": ApiError}, 409: {"model": ApiError}, 502: {"model": ApiError}},
)
def analyse_requirement(
    requirement_id: str,
    use_case: AnalyseRequirementUseCase = Depends(get_analyse_use_case),  # noqa: B008
) -> AnalysisResponse:
    try:
        analysis = use_case.execute(requirement_id)
    except RequirementNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=ApiError(
                error=ApiErrorBody(code="requirement_not_found", message=str(error))
            ).model_dump(),
        ) from error
    except InvalidStateTransitionError as error:
        raise HTTPException(
            status_code=409,
            detail=ApiError(
                error=ApiErrorBody(code="invalid_status_transition", message=str(error))
            ).model_dump(),
        ) from error
    except AIGatewayError as error:
        raise HTTPException(
            status_code=502,
            detail=ApiError(
                error=ApiErrorBody(code="ai_provider_error", message=str(error))
            ).model_dump(),
        ) from error

    return AnalysisResponse(
        requirement_id=requirement_id,
        status="Analyzed",
        analysis=AnalysisBody(
            quality_indication=analysis.quality_score.value, issues=list(analysis.issues)
        ),
    )


@router.post(
    "/requirements/{requirement_id}/validate",
    response_model=ValidateResponse,
    responses={400: {"model": ApiError}, 404: {"model": ApiError}, 409: {"model": ApiError}},
)
def validate_requirement(
    requirement_id: str,
    body: ValidateRequest,
    use_case: ValidateRequirementUseCase = Depends(get_validate_use_case),  # noqa: B008
) -> ValidateResponse:
    try:
        requirement = use_case.execute(requirement_id, body.decision, body.modified_text)
    except RequirementNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=ApiError(
                error=ApiErrorBody(code="requirement_not_found", message=str(error))
            ).model_dump(),
        ) from error
    except InvalidValidationDecisionError as error:
        raise HTTPException(
            status_code=400,
            detail=ApiError(error=ApiErrorBody(code="missing_field", message=str(error))).model_dump(),
        ) from error
    except InvalidStateTransitionError as error:
        raise HTTPException(
            status_code=409,
            detail=ApiError(
                error=ApiErrorBody(code="invalid_status_transition", message=str(error))
            ).model_dump(),
        ) from error

    return ValidateResponse(requirement_id=requirement_id, status=requirement.status.value)
