# BridgeIT

![Status](https://img.shields.io/badge/status-architecture%20%26%20setup%20phase-yellow)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey)

> AI-Supported Requirements Engineering Platform — Software Engineering project, University of Bologna.

## Project Overview

BridgeIT is a **Requirements Engineering platform** that helps business stakeholders and software engineers transform natural-language requirements into structured software artifacts, while preserving complete traceability between a requirement and everything derived from it.

Requirements Engineering is one of the most critical and error-prone disciplines in software development: requirements originate as informal, ambiguous natural-language statements, and translating that informal intent into structured, unambiguous, traceable engineering artifacts is a well-documented source of project failure. BridgeIT uses Artificial Intelligence to assist this translation — flagging ambiguity, proposing structure, and suggesting revisions — but AI in BridgeIT never decides autonomously. Every AI-generated suggestion is a proposal that requires explicit human validation before it can affect the authoritative state of a requirement.

This distinction is what separates BridgeIT from a generic AI chatbot: BridgeIT is built around an explicit domain model, a defined workflow, and an architecture that keeps every AI-assisted suggestion reviewable, attributable, and traceable to its origin.

The platform is designed around four cardinal engineering principles:

- **Domain-Driven Design (DDD)** — an explicit domain model (Requirement, Artifact, AI Analysis, Traceability Link) expressed in terms meaningful to the Requirements Engineering domain, not to any particular storage or delivery technology.
- **Hexagonal Architecture (Ports and Adapters)** — the domain and application logic are isolated from external technical concerns (web framework, persistence, AI provider) behind explicit ports, so the domain remains independently testable and technology-agnostic.
- **SOLID principles**, most notably the **Dependency Inversion Principle** — dependencies always point inward, toward the domain; adapters depend on abstractions defined by the layers they serve, never the reverse.
- **AI isolated through an AI Gateway** — access to the AI provider (the Gemini API) is mediated entirely through a dedicated gateway abstraction invoked by the application layer, so the domain has no dependency on any AI provider, and the provider itself remains replaceable in principle.

## Current Status

**BridgeIT is currently in its Architecture & Design Setup Phase.** Only project initialization has been completed to date. No domain logic, application services, infrastructure adapters, or AI integration have been implemented yet.

**Completed:**
- Repository initialization from the official Poetry project template.
- Poetry project configuration.
- Renaming of the project package to `bridgeit`.
- Automated testing environment set up with Pytest.
- Static analysis configuration with Ruff and Mypy.
- Git versioning established through GitHub.

**Not yet implemented:**
- Domain model (Requirements Engineering core concepts).
- AI integration (Gemini API and AI Gateway abstraction).
- APIs (FastAPI service layer and endpoints).
- Persistence layer.
- CI/CD pipeline.
- Frontend.

The full, up-to-date status is maintained in [`docs/report.md`](./docs/report.md#current-development-status) and is expected to evolve incrementally, milestone by milestone, alongside this README.

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
git clone <repository-url>
cd bridgeit

# Install dependencies (creates/uses the project's virtual environment)
poetry install
```

Once dependencies are installed, the application (once implemented) is intended to run as a **FastAPI** service. Instructions for running the API server will be added here once the corresponding milestone (see [`docs/report.md` — Roadmap](./docs/report.md#roadmap)) is implemented.

## Quality Assurance

Project tasks are run through [`poe`](https://github.com/nat-n/poethepoet) (Poe the Poet), configured as the project's task runner on top of Poetry.

```bash
# Run the automated test suite (Pytest)
poetry run poe test

# Run static analysis (Ruff for linting, Mypy for type checking)
poetry run poe static-checks
```

Both commands are expected to be run locally before every commit, and will later be wired into the project's Continuous Integration pipeline (see [`docs/report.md` — Continuous Integration and Continuous Delivery](./docs/report.md#continuous-integration-and-continuous-delivery)).

## License

This project is licensed under the **Apache License 2.0** (see [`docs/report.md` — License](./docs/report.md#license) for details on the current licensing status).