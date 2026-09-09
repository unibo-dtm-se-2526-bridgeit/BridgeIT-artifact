# BridgeIT

![Status](https://img.shields.io/badge/status-core%20workflow%20implemented-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Release](https://img.shields.io/badge/release-bridgeit--v1.0.2-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey)

> AI-Supported Requirements Engineering Platform — University of Bologna Software Engineering Project (A.Y. 2025/2026)

## Project Overview

BridgeIT is a Requirements Engineering platform that supports the lifecycle of natural-language software requirements through AI-assisted quality analysis and explicit human validation.

The project follows a **human-in-the-loop** principle: Google Gemini can identify quality issues and support requirement refinement, but it cannot autonomously approve, modify, reject, or otherwise determine the authoritative state of a requirement. The final decision remains under explicit Business Analyst control.

## Current Status

The core BridgeIT workflow is implemented and has been validated end-to-end.

A requirement starts in:

`Submitted` → `Analyzed` → explicit Business Analyst decision

The human decision can then produce one of three outcomes:

- `Approve` → `Validated`
- `Edit` → `Clarified`
- `Reject` → `Rejected`

A requirement in `Clarified` state can be analysed again:

`Clarified` → `Analyzed`

The `Edit` → `Clarified` → `Analyse` refinement cycle can be repeated before a final validation decision is recorded.

### Implemented capabilities

- Requirement creation and retrieval;
- explicit Requirement lifecycle and domain rules;
- SQLite persistence through the `RequirementRepository` port and Python's standard `sqlite3` module;
- AI-assisted requirement analysis through an abstract `AIGateway`;
- Google Gemini integration through `GeminiAIGateway`;
- explicit Business Analyst approval, clarification/editing, and rejection;
- lifecycle enforcement for invalid state transitions;
- shared structured API error handling;
- six-page HTML/CSS/JavaScript frontend:
  - Health
  - Create
  - Requirements
  - Analyse
  - Validate
  - Guide
- Docker and Docker Compose support;
- automated testing;
- Ruff linting and formatting checks;
- Mypy static type checking;
- GitHub Actions CI/CD and automated releases.

## Architecture

BridgeIT follows **Hexagonal Architecture (Ports and Adapters)** together with **Domain-Driven Design**.

The domain and application logic remain independent from external technical concerns such as the database, AI provider, and HTTP framework.

Key abstraction boundaries include:

- `RequirementRepository` for persistence;
- `AIGateway` for AI-provider interaction.

Current adapters include:

- SQLite persistence through Python's standard `sqlite3`;
- Google Gemini through the `google-genai` client;
- FastAPI as the HTTP driving adapter;
- a vanilla HTML/CSS/JavaScript web client.

This architecture keeps infrastructure dependencies outside the core domain and allows the Requirement lifecycle to remain independently testable.

## Core API

The implemented core HTTP operations include:

- `POST /requirements`
- `GET /requirements/{requirement_id}`
- `POST /requirements/{requirement_id}/analyse`
- `POST /requirements/{requirement_id}/validate`

FastAPI also exposes automatically generated OpenAPI documentation while the backend is running.

## AI Integration

BridgeIT currently integrates Google Gemini behind the `AIGateway` abstraction.

The configured model is:

`gemini-3.5-flash-lite`

Transient provider failures associated with HTTP `429` and `503` responses are handled through a bounded retry policy.

AI output is used to support human review. It does not directly determine the authoritative final state of a Requirement.

## Frontend

The lightweight frontend is implemented in vanilla HTML, CSS, and JavaScript and communicates with the FastAPI backend through REST APIs.

It contains six pages:

1. **Health** — check backend connectivity;
2. **Create** — submit a new Requirement;
3. **Requirements** — retrieve and inspect a Requirement;
4. **Analyse** — request AI-assisted quality analysis;
5. **Validate** — record the Business Analyst decision;
6. **Guide** — provide workflow guidance and help.

## Development Setup

BridgeIT uses Poetry for dependency and environment management.

Install the project dependencies with:

```bash
poetry install
```

Run the automated test suite with:

```bash
poetry run poe test
```

Run static verification with:

```bash
poetry run poe static-checks
```

Alternatively, the application can be started using Docker Compose:

```bash
docker compose up
```

Complete installation, configuration, and deployment instructions are available in the report's [**Developer Guide**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/10-devguide/index.md) and [**Deployment**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/07-deployment/index.md) chapters.

## Validation

BridgeIT has been verified through automated tests and a manual end-to-end acceptance session.

The manual acceptance checks cover:

- Requirement creation;
- AI-assisted analysis;
- human clarification and editing;
- human approval;
- human rejection;
- re-analysis after clarification;
- repeated refinement cycles;
- rejection of an invalid analysis request after a Requirement has reached `Validated`;
- availability of the frontend Guide.

Detailed validation evidence is available in the report's [**Validation**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/05-validation/index.md) chapter.

## Current Scope

The current implementation prioritizes the complete:

**Requirement → AI Analysis → Human Validation**

workflow together with its architecture, persistence, frontend, testing, deployment, and CI/CD support.

The following capabilities are outside the implemented core version and remain possible future extensions:

- authentication and user management;
- authorization policies;
- persistence and caching of AI-analysis results;
- richer traceability-link management;
- derived artifact generation.

This prioritization reflects the scope implemented and validated to date. The team is awaiting instructor feedback on whether any additional capabilities should be included before final submission. See the report's [**Future Work**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/12-future/index.md) chapter for the documented extension opportunities.

## Release

Latest release:

**`bridgeit-v1.0.3`**

The release process is automated through GitHub Actions and semantic-release.

## Project Documentation

The authoritative Software Engineering report is maintained in the dedicated report repository:

- [Published report](https://unibo-dtm-se-2526-bridgeit.github.io/report/)
- [Report repository](https://github.com/unibo-dtm-se-2526-bridgeit/report)
- [GitHub organization](https://github.com/unibo-dtm-se-2526-bridgeit)

The report documents the project concept, requirements, architecture, implementation, validation, release process, deployment, CI/CD, user workflow, developer setup, and future work.

Useful direct links:

- [**Design**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/03-design/index.md)
- [**Development**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/04-development/index.md)
- [**Validation**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/05-validation/index.md)
- [**User Guide**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/09-userguide/index.md)
- [**Developer Guide**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/10-devguide/index.md)
- [**Future Work**](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/main/sections/12-future/index.md)

## License

BridgeIT is distributed under the **Apache License 2.0**.
