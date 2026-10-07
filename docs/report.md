# BridgeIT — Artifact Documentation Snapshot

This file summarizes the **current state of the artifact** at the latest release (see `CHANGELOG.md`). The authoritative course report is maintained in the dedicated `report` repository; this document is kept here so that the artifact does not contain outdated implementation claims.

---

## Project Vision

BridgeIT is a Requirements Engineering platform that supports the lifecycle of natural-language software requirements through AI-assisted quality analysis and explicit human validation.

The system follows a **human-in-the-loop** principle: Google Gemini provides quality feedback, but the final authoritative decision remains under explicit Requirements Engineer control.

---

## Current Workflow

The implemented lifecycle is:

```text
Submitted → Analyzed → Validated
                   ├→ Clarified → Analyzed
                   └→ Rejected
```

A human reviewer chooses `Approve`, `Edit`, or `Reject` from the Validate page.

An edited requirement keeps its identifier, replaces its current text, enters `Clarified`, and must be analysed again before another final decision can be recorded.

---

## Implemented Functional Capabilities

| Capability | Status |
|---|---|
| Requirement creation | Implemented |
| Requirement retrieval | Implemented |
| AI-assisted analysis | Implemented |
| Quality indication (`ready_for_validation` / `needs_clarification`) | Implemented |
| Human approve/edit/reject workflow | Implemented |
| SQLite persistence | Implemented |
| Common API error format | Implemented |
| Vanilla HTML/CSS/JavaScript frontend | Implemented |
| Docker / Docker Compose | Implemented |
| Automated tests and coverage tooling | Implemented |
| Ruff linting and formatting | Implemented |
| Mypy static type checking | Implemented |
| GitHub Actions CI/CD | Implemented |
| Semantic-release | Implemented |
| Traceability link management | Future work |
| Derived artifact creation | Future work |
| Authentication and authorization | Future work |
| Persistent AI-analysis history | Future work |
| Structured domain-event logging | Future work |

---

## Functional Requirements Mapping

The current implementation covers the core requirements as follows:

| Requirement | Current status | Implementation evidence |
|---|---|---|
| FR-01 Requirement Creation | Implemented | `POST /requirements`, `SubmitRequirementUseCase`, SQLite repository |
| FR-02 AI-Assisted Requirement Analysis | Implemented | `POST /requirements/{id}/analyse`, `AIGateway`, `GeminiAIGateway` |
| FR-03 Requirement Clarification | Implemented | `Requirement.clarify()`, `ValidateRequirementUseCase` with `edit` |
| FR-04 Requirement Quality Evaluation | Implemented | `QualityScore`, Gemini analysis response |
| FR-05 Human Validation | Implemented | `ValidateRequirementUseCase`, `POST /requirements/{id}/validate` |
| FR-06 Traceability Link Management | Not implemented | Planned future capability |
| FR-07 Derived Artifact Creation | Not implemented | Planned future capability |

---

## Architecture

BridgeIT uses Hexagonal Architecture and Domain-Driven Design.

The domain layer contains the `Requirement` aggregate root and value objects. The application layer contains use cases and the `RequirementRepository` and `AIGateway` ports. The FastAPI API is a driving adapter, while SQLite and Gemini are driven adapters.

The frontend is a separate static HTML/CSS/JavaScript client that communicates with the backend through the REST API.

For the detailed implementation architecture, see [`architecture.md`](architecture.md).

---

## Persistence

The current persistence implementation uses Python's standard `sqlite3` module.

The database stores only the current requirement state:

```text
id | text | status
```

Previous requirement revisions are not persisted. An edit replaces the current text while preserving the requirement identifier.

AI analyses are also not stored as independent database records.

---

## API

The implemented HTTP endpoints are:

```text
GET  /health
POST /requirements
GET  /requirements/{id}
POST /requirements/{id}/analyse
POST /requirements/{id}/validate
```

FastAPI provides generated OpenAPI documentation when the backend is running.

The Traceability and Derived Artifact endpoints are not implemented in the current release.

---

## Frontend

The frontend contains six pages:

1. **Health** — verify backend connectivity.
2. **Create** — submit a requirement.
3. **Requirements** — retrieve and inspect a requirement.
4. **Analyse** — request an AI-assisted analysis.
5. **Validate** — record the human decision.
6. **Guide** — explain the workflow and answer common questions.

No frontend framework or build system is used.

---

## Testing and Quality

The repository contains **61 automated tests**, organized by domain, application, infrastructure, and API concerns.

The configured quality tools are:

- Pytest for automated tests;
- Coverage.py for coverage measurement;
- Ruff for linting and formatting;
- Mypy for static type checking;
- Python compilation checks.

The GitHub Actions workflow also runs the test suite on Ubuntu, Windows, and macOS for Python 3.10, 3.11, 3.12, and 3.13.

The exact coverage value should be read from the latest successful CI artifact rather than inferred from the repository text.

---

## CI/CD and Release

The repository uses GitHub Actions for continuous integration and release automation.

The pipeline performs syntax checks, static checks, formatting checks, automated tests, and then invokes semantic-release after the cross-platform test matrix succeeds.

Release tags follow:

```text
bridgeit-v<version>
```

The current version is the one recorded in `pyproject.toml` and `CHANGELOG.md`, tagged as `bridgeit-v<version>`.

The release configuration updates `pyproject.toml` and `CHANGELOG.md` and creates a GitHub Release. Public PyPI publication is conditional on the presence of `PYPI_TOKEN`.

---

## Current Limitations and Future Work

The following capabilities are deliberately outside the current core implementation:

- authentication and authorization;
- persistent AI-analysis results and history;
- traceability-link management;
- derived artifact creation;
- structured logging of significant domain events;
- a dedicated application-level retrieval use case;
- richer frontend component reuse.

These limitations are documented as future work rather than being presented as implemented functionality.

---

## Documentation Policy

The dedicated course report repository is the authoritative source for the final academic report. This artifact-side document is a technical snapshot and should be updated whenever implementation changes materially affect the description above.
