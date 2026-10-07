# BridgeIT — Architecture

**Status:** Current implementation architecture — updated to reflect the artifact at release `bridgeit-v1.0.3`.

This document describes the architecture that is actually present in the repository. The final course report contains the broader project discussion; this file focuses on the implementation structure of the artifact.

---

## Architectural Principles

BridgeIT follows **Hexagonal Architecture (Ports and Adapters)** together with **Domain-Driven Design**.

The main goal is to keep the Requirements Engineering domain independent from technical concerns such as HTTP, SQLite, and the external AI provider.

The implementation is organized around the following principles:

- **Domain independence** — the domain layer contains the `Requirement` aggregate root and its value objects and has no dependency on FastAPI, SQLite, or the Gemini SDK.
- **Application orchestration** — application use cases coordinate domain objects, persistence, and AI capabilities through explicit ports.
- **Ports and adapters** — persistence and AI-provider details are implemented by driven adapters, while FastAPI acts as the driving adapter for HTTP requests.
- **Dependency inversion** — the application layer depends on abstractions such as `RequirementRepository` and `AIGateway`; concrete infrastructure implementations depend on those abstractions.
- **Human-in-the-loop** — AI analysis is advisory. The AI provider never directly records the authoritative human validation outcome.

---

## Dependency Rules

The current codebase follows these dependency rules:

- `bridgeit/domain/` does not import infrastructure or framework-specific code.
- `bridgeit/application/` depends on domain objects and abstract ports, not on concrete adapters.
- `bridgeit/infrastructure/` implements application-layer ports using concrete technologies such as `sqlite3` and `google-genai`.
- `bridgeit/adapters/api/` translates HTTP requests into application-layer operations and translates results and errors back into HTTP responses.

This structure allows the domain logic to be tested without requiring a database or a live Gemini connection.

---

## Layered View

The implemented dependency structure can be summarized as follows:

```text
                 HTTP client / browser
                         |
                         v
              +------------------------+
              | FastAPI API adapter    |
              | adapters/api/          |
              +-----------+------------+
                          |
                          v
              +------------------------+
              | Application layer      |
              | use_cases/ + ports/    |
              +-----+-------------+----+
                    |             |
             domain |             | ports
                    v             v
          +----------------+   +----------------------+
          | Domain layer   |   | Driven adapters      |
          | Requirement    |   | SQLite repository    |
          | value objects  |   | Gemini AI gateway    |
          +----------------+   +----------------------+
```

The frontend in `web/` is a separate static client. It communicates with the FastAPI service through HTTP requests and does not contain domain logic.

---

## Actual Package Structure

The repository currently contains the following relevant structure:

```text
bridgeit/
├── domain/
│   ├── requirement.py
│   └── ai_analysis.py
├── application/
│   ├── dto.py
│   ├── ports/
│   │   ├── ai_gateway.py
│   │   └── requirement_repository.py
│   └── use_cases/
│       ├── submit_requirement.py
│       ├── analyse_requirement.py
│       └── validate_requirement.py
├── adapters/
│   └── api/
│       ├── main.py
│       ├── analysis_router.py
│       └── errors.py
└── infrastructure/
    ├── ai/
    │   └── gemini_ai_gateway.py
    └── persistence/
        └── sqlite_requirement_repository.py

tests/
├── domain/
├── application/
├── infrastructure/
└── adapters/

web/
├── index.html
├── create.html
├── requirements.html
├── analyse.html
├── validate.html
└── help.html
```

The test suite mirrors the main implementation areas rather than being split into separate `unit/`, `integration/`, and `acceptance/` directories.

---

## Domain Layer

The domain layer is implemented in pure Python.

The main aggregate root is `Requirement`. It contains:

- a unique identifier;
- the current `RequirementText`;
- the current `RequirementStatus`.

The requirement lifecycle is explicitly enforced by the domain state machine:

```text
Submitted
    |
    v
Analyzed -----> Validated
    |
    +---------> Rejected
    |
    v
Clarified
    |
    v
Analyzed
```

`Validated` and `Rejected` are terminal states in the current implementation.

A clarification replaces the current requirement text and moves the requirement to `Clarified`; the next valid operation is a new AI analysis, which moves it back to `Analyzed`.

---

## Application Layer and Ports

The application layer contains the main use cases:

- `SubmitRequirementUseCase`
- `AnalyseRequirementUseCase`
- `ValidateRequirementUseCase`

The main ports are:

- `RequirementRepository` — persistence abstraction;
- `AIGateway` — abstraction over the AI provider.

The application layer therefore orchestrates the following flow:

```text
Requirement
    |
    +--> repository
    |
    +--> AI Gateway
    |
    +--> human validation decision
```

Requirement retrieval through `GET /requirements/{id}` is currently implemented as a small API-level read operation directly against the repository instead of a dedicated application use case. This is intentionally lightweight but remains a possible future refactoring.

---

## Persistence Adapter

The current persistence adapter is `SQLiteRequirementRepository` and uses Python's standard `sqlite3` module directly.

The database table stores the current requirement state:

| Column | Meaning |
|---|---|
| `id` | Unique requirement identifier |
| `text` | Current requirement text |
| `status` | Current lifecycle status |

The previous versions of a requirement are not persisted. When `Edit` is selected, the current text is replaced and the same requirement id is retained.

Persistence is hidden behind the `RequirementRepository` port, so the rest of the application is independent from SQLite.

---

## AI Architecture

BridgeIT integrates Google Gemini through `GeminiAIGateway`, which implements the `AIGateway` port.

The dependency chain is:

```text
Application Layer
       |
       v
AIGateway port
       |
       v
GeminiAIGateway
       |
       v
Google Gemini API
```

The Gemini adapter translates the external provider response into the domain-level `AIAnalysis` object. The current `AIAnalysis` contains a qualitative `QualityScore` and a tuple of textual issues.

AI analysis is **not persisted** as an independent database record. It is returned to the client as part of the analysis response and causes the Requirement to enter the `Analyzed` state. The final validation decision is still made explicitly through the validation use case.

Transient provider failures such as HTTP `429` and `503` responses are handled through the bounded retry policy implemented in the Gemini adapter.

---

## API Design

The current HTTP API exposes these operations:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check that the backend is running |
| `POST` | `/requirements` | Create a requirement |
| `GET` | `/requirements/{id}` | Retrieve a requirement |
| `POST` | `/requirements/{id}/analyse` | Request an AI analysis |
| `POST` | `/requirements/{id}/validate` | Record a human decision |

FastAPI also generates OpenAPI documentation automatically while the backend is running.

The following endpoints are **not implemented** in the current release:

- `GET /requirements/{id}/traceability-links`
- `POST /requirements/{id}/artifacts`

These correspond to the future Traceability and Derived Artifact capabilities discussed in the final report.

---

## Error Handling

API errors use a common `ApiError` structure:

```json
{
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

The same format is used for requirement-not-found errors, invalid state transitions, invalid validation data, and AI-provider failures.

---

## Frontend

The frontend is implemented in **plain HTML, CSS, and JavaScript**, with no framework and no build system.

The six available pages are:

1. Health
2. Create
3. Requirements
4. Analyse
5. Validate
6. Guide

The frontend communicates with the backend through the REST endpoints using `fetch()` and does not directly access the persistence layer or Gemini.

---

## CI/CD and Release

GitHub Actions currently performs:

1. dependency installation through Poetry;
2. syntax compilation;
3. Ruff static checks;
4. Mypy static type checking;
5. formatting verification;
6. the automated test suite with coverage;
7. a cross-platform test matrix on Ubuntu, Windows, and macOS using Python 3.10–3.13;
8. the semantic-release process after successful checks.

The current release format is:

`bridgeit-v<version>`

The latest artifact release is `bridgeit-v1.0.3`.

---

## Architecture Limitations

The current architecture intentionally leaves several capabilities outside the implemented core:

- authentication and authorization;
- persistent AI-analysis history;
- traceability links;
- derived artifacts;
- structured domain-event logging for observability;
- a dedicated application use case for requirement retrieval.

These are documented as future improvements rather than as implemented features.
