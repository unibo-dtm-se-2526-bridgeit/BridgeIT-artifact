from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from bridgeit.application.dto import RequirementCreateRequest, RequirementResponse
from bridgeit.domain.requirement import Requirement
from bridgeit.infrastructure.persistence.sqlite_requirement_repository import (
    SQLiteRequirementRepository,
)

app = FastAPI(title="BridgeIT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TEMPORARY: these routes call the repository directly instead of going
# through an Application Layer Use Case ("Sottometti requirement"), since
# that Use Case is @nikytresca's responsibility and isn't written yet.
# Flagged for refactor once it exists: the route should depend on the Use
# Case, not on infrastructure directly. Tracked as tech debt, same pattern
# as the earlier Any->Requirement note.
_db_path = Path(__file__).resolve().parents[3] / "bridgeit.db"
_repository = SQLiteRequirementRepository(_db_path)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint: confirms the service is up and responding."""
    return {"status": "ok"}


@app.post("/requirements", response_model=RequirementResponse, status_code=201)
def create_requirement(payload: RequirementCreateRequest) -> RequirementResponse:
    """Submit a new requirement (FR-01)."""
    requirement = Requirement.submit(payload.text)
    _repository.save(requirement.id, requirement)
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
        raise HTTPException(status_code=404, detail="Requirement not found")
    return RequirementResponse(
        id=requirement.id,
        text=requirement.text.content,
        status=requirement.status.value,
    )
