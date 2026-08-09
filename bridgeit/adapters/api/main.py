from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bridgeit.adapters.api.analysis_router import register_analysis_routes
from bridgeit.adapters.api.errors import ApiError, register_error_handlers
from bridgeit.application.dto import RequirementCreateRequest, RequirementResponse
from bridgeit.application.use_cases.submit_requirement import SubmitRequirementUseCase
from bridgeit.infrastructure.ai.gemini_ai_gateway import GeminiAIGateway
from bridgeit.infrastructure.persistence.sqlite_requirement_repository import (
    SQLiteRequirementRepository,
)

app = FastAPI(title="BridgeIT")
register_error_handlers(app)

# Allow the local frontend (served from a different origin than the API)
# to call this backend during development. Origins are listed explicitly
# rather than using "*", so this stays safe to tighten later for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null",  # allows requests from pages opened directly as local files
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

_db_path = Path(__file__).resolve().parents[3] / "bridgeit.db"
_repository = SQLiteRequirementRepository(_db_path)

# AI Gateway (Milestone 5): constructed once here, same style as
# _repository above. Reads GEMINI_API_KEY from the environment -- see
# infrastructure/ai/gemini_ai_gateway.py.
_ai_gateway = GeminiAIGateway()
register_analysis_routes(app, repository=_repository, ai_gateway=_ai_gateway)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint: confirms the service is up and responding."""
    return {"status": "ok"}


@app.post("/requirements", response_model=RequirementResponse, status_code=201)
def create_requirement(payload: RequirementCreateRequest) -> RequirementResponse:
    """Submit a new requirement (FR-01)."""
    # Built per-request (not once at module load) so this always uses
    # whatever _repository currently is -- including the swapped-in test
    # repository used by the test suite via monkeypatch.
    requirement = SubmitRequirementUseCase(_repository).execute(payload.text)
    return RequirementResponse(
        id=requirement.id,
        text=requirement.text.content,
        status=requirement.status.value,
    )


@app.get("/requirements/{requirement_id}", response_model=RequirementResponse)
def get_requirement(requirement_id: str) -> RequirementResponse:
    """Retrieve a requirement by id."""
    requirement = _repository.get_by_id(requirement_id)
    if requirement is None:
        raise ApiError(
            status_code=404,
            code="requirement_not_found",
            message="No requirement found with the given id.",
        )
    return RequirementResponse(
        id=requirement.id,
        text=requirement.text.content,
        status=requirement.status.value,
    )