# BridgeIT

AI-Supported Requirements Engineering Platform — Software Engineering project, University of Bologna.

## Project Overview

BridgeIT is a Requirements Engineering platform that helps business stakeholders and software engineers transform natural-language requirements into structured software artifacts, while preserving complete traceability between a requirement and everything derived from it.

Requirements Engineering is one of the most critical and error-prone disciplines in software development: requirements originate as informal, ambiguous natural-language statements, and translating that informal intent into structured, unambiguous, traceable engineering artifacts is a well-documented source of project failure. BridgeIT uses Artificial Intelligence to assist this translation, flagging ambiguity, proposing structure, and suggesting revisions, but AI in BridgeIT never decides autonomously. Every AI-generated suggestion is a proposal that requires explicit human validation before it can affect the authoritative state of a requirement.

This distinction is what separates BridgeIT from a generic AI chatbot: BridgeIT is built around an explicit domain model, a defined workflow, and an architecture that keeps every AI-assisted suggestion reviewable, attributable, and traceable to its origin.

The platform is designed around four cardinal engineering principles:

- **Domain-Driven Design (DDD)** — an explicit domain model (`Requirement`, `Artifact`, `AI Analysis`, `Traceability Link`) expressed in terms meaningful to the Requirements Engineering domain, not to any particular storage or delivery technology.
- **Hexagonal Architecture (Ports and Adapters)** — the domain and application logic are isolated from external technical concerns (web framework, persistence, AI provider) behind explicit ports, so the domain remains independently testable and technology-agnostic.
- **SOLID principles**, most notably the Dependency Inversion Principle — dependencies always point inward, toward the domain; adapters depend on abstractions defined by the layers they serve, never the reverse.
- **AI isolated through an AI Gateway** — access to the AI provider (the Gemini API) is mediated entirely through a dedicated gateway abstraction invoked by the application layer, so the domain has no dependency on any AI provider, and the provider itself remains replaceable in principle.

## Current Status

BridgeIT has completed its Domain Layer, initial Persistence Layer, and initial API/Frontend layers. Development is currently in progress on the remaining Application Layer use cases and AI integration.

**Completed:**

- Domain model: `Requirement` aggregate root, `RequirementText` and `RequirementStatus` value objects, with explicit lifecycle state transitions (Submitted → Analyzed → Clarified → Validated/Rejected).
- Application Layer scaffolding: the `RequirementRepository` port, Pydantic DTOs for the API boundary, and an in-memory fake repository used to verify the port's contract in tests.
- Persistence Layer: `SQLiteRequirementRepository`, a concrete adapter for `RequirementRepository`, backed by Python's standard-library `sqlite3` (see `docs/adr/0001-sqlite-persistence-without-orm.md` for the decision record).
- API layer (FastAPI): `GET /health`, `POST /requirements`, `GET /requirements/{id}`, with a shared structured error format (`{"error": {"code": ..., "message": ...}}`) applied consistently across endpoints and validation errors.
- Frontend: a minimal HTML/CSS/JavaScript web client (no framework or build system — see `docs/adr/0002-vanilla-html-css-js-frontend.md`), with pages to submit and view a requirement, wired to the live API.
- Automated testing: unit tests for the domain and application layers, integration tests for the persistence layer and API endpoints.
- CI/CD pipeline (GitHub Actions): dependency install, static analysis (`ruff`, `mypy`), automated tests, and release automation on `master`.

**Not yet implemented:**

- AI Gateway and Gemini API integration.
- Remaining Application Layer use cases (AI-assisted analysis, clarification, quality evaluation, human validation).
- `POST /requirements/{id}/analyse` and `POST /requirements/{id}/validate` endpoints, and their corresponding frontend pages.
- Traceability Link and Derived Artifact management (planned as best-effort, time permitting).

The current `POST /requirements` and `GET /requirements/{id}` routes are a deliberately temporary implementation: they call the persistence adapter directly rather than going through an Application Layer use case, since that use case is still in development. This will be refactored once available, without requiring any change to already-persisted data.

The full, up-to-date status is maintained in `docs/report.md` and is expected to evolve incrementally, milestone by milestone, alongside this README.

## Repository Organization

At this stage, this repository contains both the implementation and the full project documentation (`docs/`). Keeping the two together simplifies iteration while the codebase and documentation are still evolving in step with one another.

The project is intended to adopt a two-repository organization, consistent with the structure recommended for the University of Bologna Software Engineering course: this repository will become the implementation (artifact) repository, while the documentation (Project Report, Architecture, and Domain Model) will reside in a dedicated `report` repository. This is a matter of repository structure only — no documentation content will be lost or altered as part of it.

## Project Documentation

The project's documentation is currently available in two places:

- locally, under `docs/`, as referenced throughout this README; and
- in a dedicated documentation repository: `nikytresca-pixel/report`.

The dedicated repository is intended to become the canonical location for the project's documentation, consistent with the repository organization recommended for the University of Bologna Software Engineering course. The local copy under `docs/` will eventually be migrated there without any change to its contents; until that migration is complete, the links in this README continue to point to the local copy.

## Architecture & Documentation

Full project documentation lives under `docs/`. Each document has a distinct, non-overlapping scope:

| Document | Summary |
|---|---|
| Report | Project vision, problem statement, functional and non-functional requirements, user stories, workflow, methodology, roadmap, and current development status. |
| Architecture | The Hexagonal Architecture layering (driving adapters → application layer → domain / AI Gateway → driven adapters), the dependency rules that govern it, the AI Gateway's isolation from the domain, the proposed package structure, and the illustrative API design. |
| Domain Model | The Domain-Driven Design model: entities (`Requirement`, `Artifact`, `AI Analysis`, `Traceability Link`), value objects, domain rules, the `Requirement` aggregate root and the invariants it protects, and the project's ubiquitous language. |

All three documents are kept consistent with one another and are updated incrementally as the project progresses, following the same Conventional Commits discipline used for the codebase.

## Development Setup

BridgeIT is built in Python and managed with Poetry.

```bash
# Clone the repository
git clone <repository-url>
cd BridgeIT-artifact

# Install dependencies (creates/uses the project's virtual environment)
poetry install
```

### Running the API server

Once dependencies are installed, start the FastAPI development server:

```bash
poetry run uvicorn bridgeit.adapters.api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

### Running the frontend

With the API server running, open `web/index.html` (or any page under `web/`) directly in a browser. The frontend is a static HTML/CSS/JavaScript client with no build step required.

## Quality Assurance

Project tasks are run through `poe` (Poe the Poet), configured as the project's task runner on top of Poetry.

```bash
# Run the automated test suite (Pytest)
poetry run poe test

# Run static analysis (Ruff for linting, Mypy for type checking)
poetry run poe static-checks

# Check code formatting (Ruff)
poetry run poe format-check
```

All three commands are expected to be run locally before every commit, and are also enforced automatically in the project's Continuous Integration pipeline (see `docs/report.md` — Continuous Integration and Continuous Delivery).

## License

This project is licensed under the Apache License 2.0 (see `docs/report.md` — License for details on the current licensing status).
