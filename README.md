# BridgeIT

![Status](https://img.shields.io/badge/status-active%20development-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey)

> AI-Supported Requirements Engineering Platform — University of Bologna Software Engineering Project (A.Y. 2025/2026)

## Project Overview

BridgeIT is a **Requirements Engineering platform** that helps business stakeholders and software engineers analyse and validate natural-language requirements through an explicit, human-controlled lifecycle. Its architecture is designed to support future traceability between a requirement and derived artifacts, although those stretch features are not part of the current implementation.

Requirements Engineering is one of the most critical and error-prone disciplines in software development: requirements originate as informal, ambiguous natural-language statements, and translating that informal intent into structured, unambiguous, traceable engineering artifacts is a well-documented source of project failure. BridgeIT uses Artificial Intelligence to assist this translation — flagging ambiguity, proposing structure, and suggesting revisions — but AI in BridgeIT never decides autonomously. Every AI-generated suggestion is a proposal that requires explicit human validation before it can affect the authoritative state of a requirement.

This distinction is what separates BridgeIT from a generic AI chatbot: BridgeIT is built around an explicit domain model, a defined workflow, and an architecture that keeps every AI-assisted suggestion reviewable, attributable, and traceable to its origin.

The platform is designed around four cardinal engineering principles:

- **Domain-Driven Design (DDD)** — an explicit domain model (Requirement, Artifact, AI Analysis, Traceability Link) expressed in terms meaningful to the Requirements Engineering domain, not to any particular storage or delivery technology.
- **Hexagonal Architecture (Ports and Adapters)** — the domain and application logic are isolated from external technical concerns (web framework, persistence, AI provider) behind explicit ports, so the domain remains independently testable and technology-agnostic.
- **SOLID principles**, most notably the **Dependency Inversion Principle** — dependencies always point inward, toward the domain; adapters depend on abstractions defined by the layers they serve, never the reverse.
- **AI isolated through an AI Gateway** — access to the AI provider (the Gemini API) is mediated entirely through a dedicated gateway abstraction invoked by the application layer, so the domain has no dependency on any AI provider, and the provider itself remains replaceable in principle.

## Current Status

**BridgeIT's core Requirement → AI Analysis → Human Validation flow is now implemented and merged into `master` through PR #23.** The project currently has **58 automated tests**, while the local Pytest suite and static checks complete successfully. BridgeIT remains in active development while final acceptance testing, report completion, and optional stretch features are addressed.

**Completed:**
- Domain layer: the `Requirement` entity, its value objects, lifecycle transitions, `AIAnalysis`, and the binary `QualityScore`.
- Persistence: `SQLiteRequirementRepository`, implemented with Python's standard `sqlite3` module and verified with integration tests.
- Requirement APIs: `POST /requirements` and `GET /requirements/{requirement_id}` (FR-01), with a shared structured API error format.
- AI integration: the `AIGateway` port and `GeminiAIGateway` adapter, using `gemini-3.5-flash-lite` and retrying transient 429/503 provider errors.
- Analysis and validation: `POST /requirements/{requirement_id}/analyse` (FR-02/FR-04) and `POST /requirements/{requirement_id}/validate` (FR-05), backed by dedicated application use cases.
- Frontend: six plain HTML/CSS/JavaScript pages covering health, Requirement creation and visualization, AI Analysis, Business Analyst validation, and help/guidance.
- Quality and infrastructure: automated tests, coverage measurement, Ruff, Mypy, GitHub Actions, Docker, Docker Compose, and releases through `semantic-release`.

**Remaining / finalization work:**
- Run and document the final end-to-end and manual acceptance tests for the complete Requirement → AI Analysis → Human Validation workflow.
- Complete and align the remaining course-report chapters, user/developer guidance, and individual AI-tool-usage disclosures.
- Reconcile the operational roadmap and local technical documents with the implementation now present in `master`.
- Traceability links and derived artifacts (FR-06/FR-07) remain optional stretch goals and are not currently implemented.
- Authentication/user management, AI-analysis persistence, and AI-response caching are not part of the current implementation.

The operational plan remains available in [`docs/RoadMap.md`](./docs/RoadMap.md). The authoritative course report is published at [unibo-dtm-se-2526-bridgeit.github.io/report](https://unibo-dtm-se-2526-bridgeit.github.io/report/).

## Repository Organization

This repository (`artifact`) is part of the [`unibo-dtm-se-2526-bridgeit`](https://github.com/unibo-dtm-se-2526-bridgeit) GitHub organization, consistent with the structure recommended for the University of Bologna Software Engineering course: this repository holds the implementation, while the documentation (Project Report, Architecture, Domain Model, and Roadmap) lives in the dedicated [`report`](https://github.com/unibo-dtm-se-2526-bridgeit/report) repository.

## Project Documentation

The authoritative course report lives in the dedicated [`report`](https://github.com/unibo-dtm-se-2526-bridgeit/report) repository and is published through [GitHub Pages](https://unibo-dtm-se-2526-bridgeit.github.io/report/).

A working copy of the roadmap and implementation-oriented technical documents is also kept under [`docs/`](./docs) in this repository for development convenience. Separate ADR files are not currently maintained; implemented architectural decisions are documented in the report's Design and Development chapters and reflected in the roadmap.

## Architecture & Documentation

Full project documentation lives under [`docs/`](./docs). Each document has a distinct, non-overlapping scope:

| Document | Summary |
|---|---|
| [**Report**](./docs/report.md) | Project vision, problem statement, functional and non-functional requirements, user stories, workflow, methodology, roadmap, and current development status. |
| [**Architecture**](./docs/architecture.md) | The Hexagonal Architecture layering (driving adapters → application layer → domain / AI Gateway → driven adapters), the dependency rules that govern it, the AI Gateway's isolation from the domain, the proposed package structure, and the illustrative API design. |
| [**Domain Model**](./docs/domain-model.md) | The Domain-Driven Design model: entities (Requirement, Artifact, AI Analysis, Traceability Link), value objects, domain rules, the Requirement aggregate root and the invariants it protects, and the project's ubiquitous language. |

All three documents are kept consistent with one another and are updated incrementally as the project progresses, following the same Conventional Commits discipline used for the codebase.

## Development Setup

BridgeIT is built in Python and managed with [Poetry](https://python-poetry.org/).

```bash
# Clone the repository
git clone https://github.com/unibo-dtm-se-2526-bridgeit/BridgeIT-artifact.git
cd BridgeIT-artifact

# Install dependencies (creates/uses the project's virtual environment)
poetry install
```

**Alternatively, using Docker** (no local Python or Poetry installation required):

```bash
docker compose up
```

Once dependencies are installed, the FastAPI service and the six-page frontend under [`web/`](./web) can be run locally. See [`docs/RoadMap.md`](./docs/RoadMap.md) for the operational plan and the [published report](https://unibo-dtm-se-2526-bridgeit.github.io/report/) for the authoritative project documentation.

## Quality Assurance

Project tasks are run through [`poe`](https://github.com/nat-n/poethepoet) (Poe the Poet), configured as the project's task runner on top of Poetry.

```bash
# Run the automated test suite (Pytest)
poetry run poe test

# Run static analysis (Ruff for linting, Mypy for type checking)
poetry run poe static-checks
```

Both commands run automatically in the project's CI/CD pipeline (GitHub Actions) on every commit, alongside automatic releases via `semantic-release` (see [`docs/report.md` — Continuous Integration and Continuous Delivery](./docs/report.md#continuous-integration-and-continuous-delivery)).

## License

This project is licensed under the **Apache License 2.0** (see [`docs/report.md` — License](./docs/report.md#license) for details on the current licensing status).
