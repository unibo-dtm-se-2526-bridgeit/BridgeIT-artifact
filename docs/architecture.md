# BridgeIT — Architecture

**Status:** Preliminary — reflects intended design direction, not implemented code (see [report.md — Current Development Status](report.md#current-development-status))

This document is the single authoritative reference for BridgeIT's architecture. It is referenced, not duplicated, by [report.md](report.md) and [domain-model.md](domain-model.md), consistent with the project's documentation structure.

Unless explicitly marked otherwise, the descriptions below are written as design commitments — statements of how the architecture is intended to behave — not as claims that this behavior is already implemented. For what currently exists in the repository, see [report.md — Current Development Status](report.md#current-development-status).

---

## Architectural Principles

BridgeIT's architecture is planned around a small set of well-established architectural principles, described here at a conceptual level. No implementation classes are included at this stage; the architecture will be documented in greater depth as it is actually implemented.

- **Hexagonal Architecture (Ports and Adapters)** — The core application logic is isolated from external technical concerns (web framework, database, AI provider) behind explicit ports, with adapters implementing those ports for specific technologies. This is what allows the domain to be tested and reasoned about independently of any particular infrastructure choice. It is also the primary mechanism through which BridgeIT satisfies the Dependency Inversion Principle (the "D" in SOLID); the precise dependency direction this implies is stated in full in [Dependency Rules](#dependency-rules) below.

- **Domain-Driven Design** — The system is organized around an explicit domain model representing the core concepts of the Requirements Engineering process, rather than around technical or database-driven structures. Domain logic is expressed in terms meaningful to the Requirements Engineering domain itself. The full domain model — entities, value objects, the aggregate boundary, and domain rules — is documented in [domain-model.md](domain-model.md).

- **Repository Pattern** — Persistence concerns are abstracted behind a repository interface (a port), expressed in terms meaningful to the domain, so that persistence technology never leaks into business logic. Consistent with the Application Layer below, it is that layer — not the domain layer itself — that depends on and invokes this repository port; the domain layer remains free of any outgoing dependency, including to its own persistence abstraction.

- **Application Layer (Service Layer pattern)** — Application-level use cases are coordinated through a service layer that orchestrates domain objects and repositories, keeping orchestration logic distinct from both the domain model and the infrastructure adapters. This separation is also what keeps each layer independently testable, per NFR-02 (Testability).

- **AI Gateway** — Access to AI capabilities (e.g., the Gemini API) is mediated through a dedicated gateway abstraction, invoked by the application layer rather than the domain, and detailed further in [AI Architecture](#ai-architecture) below.

---

## Dependency Rules

BridgeIT's layering is governed by a small set of dependency rules, consistent with Hexagonal Architecture and the Dependency Inversion Principle introduced above:

- **Dependencies point inward.** Outer layers (driving adapters, driven adapters) depend on inner layers (application, domain) — never the reverse. A driven adapter (e.g., a persistence or Gemini adapter) depends on the port it implements; it is never depended upon by the layer that port belongs to.
- **The domain layer is independent.** The domain layer depends on nothing outside itself — no web framework, no persistence technology, no AI provider. It expresses business rules only, in terms meaningful to the Requirements Engineering domain (see [domain-model.md](domain-model.md)).
- **Infrastructure adapters depend on abstractions, not the other way around.** Both driving and driven adapters depend on ports defined by the application or domain layer. Neither the domain nor the application layer imports or references a specific adapter implementation (e.g., FastAPI, a specific persistence library, or the Gemini SDK).

These rules are what make the AI Gateway's positioning in [AI Architecture](#ai-architecture) possible: because dependencies only point inward, the domain remains wholly unaware that AI-assisted analysis exists as a capability, while the application layer — one step further out — is the one permitted to depend on it.

This section states a principle to be upheld during implementation; how it will be enforced (e.g., through code review, import-linting, or module boundaries) is a decision left open for when Milestone 2 (Domain Model) begins.

---

## Layered View (Conceptual Diagram)

The diagram below illustrates how the architectural principles above relate to one another. It shows architectural layers and their direction of dependency only — no classes, modules, or implementation details are implied.

```
 ┌──────────────────────────────────────────────────────────┐
 │                     DRIVING ADAPTERS                       │
 │            (inbound — e.g. future FastAPI controllers)     │
 └──────────────────────────┬───────────────────────────────┘
                             │  calls, via an inbound port
                             ▼
 ┌──────────────────────────────────────────────────────────┐
 │                     APPLICATION LAYER                      │
 │       (use cases / service-layer orchestration)            │
 └──────┬─────────────────────┬─────────────────────┬───────┘
        │ uses, via a          │ uses, via a          │ uses, via the
        │ domain port          │ repository port      │ AI Gateway port
        ▼                      ▼                      ▼
 ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
 │    DOMAIN LAYER      │  │  DRIVEN ADAPTERS     │  │     AI GATEWAY        │
 │ (aggregate root,     │  │ (e.g. future         │  │ (abstraction over     │
 │  entities, value      │  │  Database Adapter)   │  │  an external AI       │
 │  objects, business    │  └───────────────────┘  │  provider)            │
 │  rules — see           │                          └──────────┬────────────┘
 │  domain-model)          │                                     │ delegates, via
 └───────────────────┘                                          │ an adapter
                                                                    ▼
                                                        ┌───────────────────┐
                                                        │  DRIVEN ADAPTERS     │
                                                        │ (e.g. future Gemini  │
                                                        │  Adapter)            │
                                                        └───────────────────┘
```

- **Driving adapters** (e.g., future FastAPI controllers) are the entry points that trigger application behavior. They depend on the application layer, never the reverse.
- **Application layer** coordinates use cases (e.g., "submit a requirement", "request an analysis") by orchestrating domain objects and invoking ports — including the repository port and the AI Gateway port; it contains no business rules of its own.
- **Domain layer** holds the aggregate root, entities, value objects, and business rules that define what a requirement and its lifecycle actually mean, independent of any technical detail. It has no outgoing dependency of its own: persistence and AI access are invoked by the application layer, not by the domain. Its full conceptual model is documented in [domain-model.md](domain-model.md), not repeated here.
- **Driven adapters** (e.g., a future Database Adapter, a future Gemini Adapter) implement the ports required by the application layer, and are the only layer aware of specific external technologies.

This layering reflects intended design direction only. None of the boxes shown above currently exist as implemented code; see [report.md — Current Development Status](report.md#current-development-status) for what has actually been built so far.

---

## AI Architecture

A recurring risk in AI-augmented systems is allowing an external AI provider to become an implicit dependency of the domain itself — for example, by shaping domain entities around a specific provider's response format, or by letting the provider's output directly mutate domain state. BridgeIT's architecture is explicitly designed to avoid this.

Three points follow directly from the Hexagonal Architecture principles above:

- **Gemini API is an infrastructure concern.** The Gemini API is treated as an external technical detail, on the same architectural footing as a database or a message broker — not as part of the domain.
- **The domain model must remain independent from Gemini — and from the AI Gateway itself.** No domain entity, value object, or business rule (see [domain-model.md](domain-model.md)) references Gemini, the AI Gateway, or any provider-specific concept. Requesting an AI-assisted analysis is a use case coordinated by the **application layer**, not a capability the domain invokes on its own; the domain only ever sees the resulting `AI Analysis` once it is presented back for human validation.
- **The AI Gateway is the abstraction boundary between the application and external AI providers.** The application layer depends on the AI Gateway port, not on Gemini directly. The Gemini Adapter is one possible implementation of that port.
- **Future AI providers could replace Gemini without changing domain or application-layer logic.** Because the dependency runs from the Gemini Adapter toward the AI Gateway port (and not the reverse), replacing Gemini with a different provider is expected to require only a new adapter implementing the same port.

This relationship can be summarized as a simple dependency chain:

```
Application Layer
        |
        |  depends on (via an abstraction)
        v
AI Gateway Port
        |
        |  implemented by
        v
Gemini Adapter
```

The **Application Layer** depends only on the AI Gateway Port; the Gemini Adapter depends on that same port from the other side, fulfilling it. The **Domain Layer has no dependency on the AI Gateway at all** — it is the application layer's responsibility to invoke the port when orchestrating a use case (e.g., "analyze a requirement"), and to apply the resulting AI Analysis to the Requirement only through the explicit human-validation operation described in [domain-model.md](domain-model.md#aggregate-boundary).

This keeps the domain focused purely on business rules, and makes the AI provider replaceable in principle without touching either the domain or the application layer's use-case logic — only the adapter changes. This design is consistent with the project's [AI Philosophy](report.md#ai-philosophy): AI is treated as a replaceable, external capability, never as an autonomous decision-maker embedded in the domain.

---

## Proposed Package Structure

The structure below is a **proposed** organization for the `bridgeit` Python package, illustrating how the [Dependency Rules](#dependency-rules) above could be reflected in the codebase. It is **not implemented**: the current repository contains only the initialized package with no internal structure yet (see [report.md — Current Development Status](report.md#current-development-status)). The actual structure may differ once Milestone 2 begins, and this section will be corrected to match it at that point.

```
bridgeit/
├── domain/            # Entities, value objects, business rules — no external imports
├── application/        # Use cases, service-layer orchestration, port interfaces
├── infrastructure/
│   ├── persistence/    # Repository adapter(s) implementing a persistence port
│   └── ai/             # Gemini adapter implementing the AI Gateway port
├── adapters/
│   └── api/            # FastAPI driving adapter (routes, request/response translation)
└── tests/
    ├── unit/            # Domain and application logic in isolation
    ├── integration/      # Adapters against real or realistic infrastructure
    └── acceptance/       # End-to-end scenarios against the full application
```

`domain/` and `application/` contain no dependency on `infrastructure/` or `adapters/`; the reverse dependency is what the Dependency Rules above require. This structure is deliberately shallow and avoids additional enterprise-style subdivision (e.g., separate command/query modules, or a dedicated "core" package) beyond what the project's current scope justifies.

---

## Adapter Responsibilities

The table below describes the intended responsibility of each adapter identified so far. None of these adapters are implemented yet; responsibilities are expected to be realized starting with Milestone 3 (Requirement Management) and Milestone 4 (AI Gateway) (see [report.md — Roadmap](report.md#roadmap)).

| Adapter | Kind | Responsibility |
|---|---|---|
| **FastAPI driving adapter** | Driving | Translates incoming HTTP requests into calls to application-layer use cases, and use-case results back into HTTP responses. Performs request/response translation and transport-level input validation only — it contains no business rules. |
| **Repository persistence adapter** | Driven | Implements the persistence port defined by the application/domain layer, translating a Requirement (and related objects) to and from whatever storage mechanism is chosen, without leaking that mechanism's details back into the domain. |
| **Gemini AI adapter** | Driven | Implements the AI Gateway port by translating an analysis request into a call to the Gemini API, and the provider's response back into a domain-meaningful `AI Analysis` (see [domain-model.md](domain-model.md)). All Gemini-specific request/response handling is contained here; no other layer is aware of it. |

---

## API Design

The platform is expected to expose its functional capabilities through an HTTP API, once the application and driving-adapter layers are implemented. The following endpoints are illustrative examples of the intended API surface, aligned with the functional requirements in [report.md](report.md#functional-requirements) — they represent design intent, not an implemented or finalized contract.

```
POST /requirements
GET  /requirements/{id}
POST /requirements/{id}/analyse
POST /requirements/{id}/validate
GET  /requirements/{id}/traceability-links
POST /requirements/{id}/artifacts
```

- `POST /requirements` is expected to correspond to **FR-01** (Requirement Creation).
- `GET /requirements/{id}` is expected to support retrieval of a requirement's current state, including its quality indication and traceability links.
- `POST /requirements/{id}/analyse` is expected to correspond to **FR-02** (AI-Assisted Requirement Analysis).
- `POST /requirements/{id}/validate` is expected to correspond to **FR-05** (Human Validation of AI Suggestions), recording an explicit approve/edit/reject decision on a pending AI Analysis.
- `GET /requirements/{id}/traceability-links` is expected to correspond to **FR-06** (Traceability Link Management), returning the Traceability Links associated with a Requirement.
- `POST /requirements/{id}/artifacts` is expected to correspond to **FR-07** (Derived Artifact Creation), creating a Derived Artifact from a validated Requirement.

Formal API documentation (OpenAPI/Swagger, generated automatically once FastAPI routes are implemented) will be introduced during development and referenced from this section once available. No API is implemented at the current stage of the project.

---

## Architecture Decision Records

Significant architectural decisions — for example, choosing a specific persistence technology, or revisiting the placement of the AI Gateway — will be captured as lightweight Architecture Decision Records (ADRs) once such decisions are actually made, rather than documented speculatively in advance.

Each ADR is expected to follow a minimal, standard structure: a short title, the context that motivated the decision, the decision itself, and its consequences. ADRs will be stored under `docs/adr/`, numbered sequentially (e.g., `0001-adoption-of-hexagonal-architecture.md`), and are not rewritten after acceptance — superseding an earlier decision means adding a new ADR that references it, preserving a historical record of how the architecture evolved.

No ADR exists yet, consistent with the project's current Milestone 1 (initialization only) status (see [report.md — Current Development Status](report.md#current-development-status)). The first ADR is expected once an architectural decision is actually made, during Milestone 2 or later.

---

## Relationship to Other Documents

- [report.md](report.md) — project vision, requirements, workflow, methodology, and current status.
- [domain-model.md](domain-model.md) — the conceptual domain model (entities, value objects, aggregate boundary, domain rules) referenced by the Domain Layer above.

This document will be revised, rather than duplicated, whenever architectural decisions evolve; significant changes are additionally expected to be captured as an [Architecture Decision Record](#architecture-decision-records), per the section above.