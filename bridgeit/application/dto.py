from pydantic import BaseModel, Field


class RequirementCreateRequest(BaseModel):
    """Request body for submitting a new requirement (FR-01).

    This is a Data Transfer Object (DTO): it validates and shapes data
    coming from the HTTP boundary. It is intentionally distinct from the
    domain `Requirement` entity (see architecture.md — Dependency Rules):
    the API must never expose domain objects directly.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="The natural-language text of the requirement being submitted.",
    )


class RequirementResponse(BaseModel):
    """Response body representing a Requirement's current state to API clients.

    Distinct from the domain `Requirement` entity for the same reason as
    `RequirementCreateRequest` above: it is the API's own view of a
    requirement, shaped for HTTP clients, not the domain's internal
    representation.
    """

    id: str = Field(..., description="Unique identifier of the requirement.")
    text: str = Field(..., description="Current text of the requirement.")
    status: str = Field(
        ...,
        description="Current lifecycle status of the requirement "
        "(e.g. Submitted, Analyzed, Clarified, Validated, Rejected).",
    )
