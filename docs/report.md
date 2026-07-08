# BridgeIT

## Project Vision

Requirements Engineering remains one of the most critical and error-prone disciplines in software development. Requirements originate as informal, natural-language statements produced by business stakeholders who reason in terms of goals, needs, and expectations rather than formal, verifiable specifications. The translation of this informal intent into structured, unambiguous, and traceable engineering artifacts is widely recognized as a major source of software project failure: a substantial proportion of defects and costly rework can be traced back to requirements that were incomplete, ambiguous, or misunderstood at the point of hand-off between business and engineering.

Artificial Intelligence, and Large Language Models in particular, can help mitigate this problem: by reading unstructured text, flagging ambiguity or incompleteness, and proposing more structured representations — without replacing the judgment of requirements engineers and business analysts, who remain responsible for final interpretation and validation.

BridgeIT is built on this distinction. Unlike a general-purpose AI chatbot, which offers no persistent structure and no accountability for what it produces, BridgeIT is a **Requirements Engineering platform** with an explicit domain model, a defined workflow, and an architecture that keeps every AI-assisted suggestion reviewable, attributable, and traceable to its origin. Its purpose is to help business stakeholders and software engineers turn natural-language requirements into structured, traceable software artifacts, with AI as a means to that end, not the end itself.

---

## Academic Context

BridgeIT is developed as a Software Engineering project for the University of Bologna. Beyond its function as a Requirements Engineering platform, the project is intended to demonstrate practical command of principles central to the course: Domain-Driven Design, Hexagonal Architecture, automated testing practices, and Continuous Integration/Continuous Delivery. Its documentation and architecture are structured so that each of these principles can be directly inspected and evaluated as the implementation progresses, rather than only described in the abstract.

---

## Problem Statement

The problem BridgeIT addresses can be summarized along four dimensions, each of which motivates a specific aspect of the platform's design:

- **Manual requirements management does not scale.** In most software projects, requirements are collected and maintained manually across disconnected documents, spreadsheets, and messaging threads. This manual process is time-consuming, error-prone, and difficult to keep synchronized as a project evolves.

- **Natural language is inherently ambiguous.** Requirements are almost always first expressed in natural language, which is flexible for communication but poorly suited to precise specification. Ambiguity that is not caught early is expensive to correct later.

- **Information is lost between business and development.** As a requirement moves from a business stakeholder's original statement to the engineering team's interpretation of it, informal context and intent are frequently lost or distorted, particularly when no structured intermediate artifact captures that translation.

- **Traceability is difficult to maintain without dedicated tooling.** Without an explicit mechanism linking requirements to the artifacts derived from them, it becomes difficult to answer basic but essential questions such as "why does this backlog item exist?" or "which requirements are not yet covered by any implementation artifact?".

BridgeIT is designed as a direct response to these four problems: it provides a structured, AI-assisted, and traceable environment for managing the full lifecycle of a requirement, from its initial natural-language formulation to the artifacts derived from it.

---

## Domain Terminology

The terms below are used consistently throughout this report. They are defined here briefly, for readability; their full treatment as domain concepts (entities, value objects, and the reasoning behind each) is maintained in [domain-model.md](domain-model.md#ubiquitous-language).

- **Requirement** — A single unit of business or system intent, originally expressed in natural language, tracked through its lifecycle from submission to validation.
- **AI Analysis** — The outcome of an AI-assisted evaluation of a Requirement's text, including a Quality Indication and, where applicable, a suggested revision. It is always a proposal, never an automatic change.
- **Derived Artifact** — A structured, engineering-facing object (for example, a backlog item) created from a validated Requirement, retaining an explicit reference back to it. Referred to as "Artifact" in the domain model.
- **Traceability Link** — An explicit, inspectable relationship connecting a Requirement to a Derived Artifact or another object derived from it.
- **Quality Indication** — A non-binding assessment of a Requirement's clarity, completeness, and freedom from ambiguity, produced by an AI Analysis, intended to guide — not replace — human judgment about whether a Requirement is ready for validation.

---

## Project Objectives

### Functional Requirements

**FR-01 Requirement Creation**

*Description:* The system shall allow a stakeholder to submit a requirement expressed in natural language and have it represented as a structured, persistent artifact within the platform.

*Acceptance Criteria:*
- Given a non-empty natural-language description, when it is submitted, then the system stores it as a Requirement with a unique identifier and an initial status.
- Given a previously submitted Requirement, when it is retrieved by its identifier, then its stored text is returned unchanged.

**FR-02 AI-Assisted Requirement Analysis**

*Description:* The system shall use the AI Gateway to analyze a submitted requirement's text and identify potential quality issues, such as ambiguity or incompleteness.

*Acceptance Criteria:*
- Given a Requirement eligible for analysis, when an analysis is requested, then the system produces an AI Analysis associated with that Requirement's identifier.
- Given an AI Analysis has been produced, when the Requirement is subsequently retrieved, then its stored text and status are unchanged from before the analysis.

**FR-03 Requirement Clarification**

*Description:* The system shall allow a stakeholder to revise a requirement's wording in response to issues identified during AI-assisted analysis.

*Acceptance Criteria:*
- Given a Requirement that has been analyzed, when its text is revised, then the Requirement keeps the same identifier while its stored text is updated.
- Given a revised Requirement, when its history is inspected, then the relationship between the original submission and the revision remains identifiable.

**FR-04 Requirement Quality Evaluation**

*Description:* The system shall produce a Quality Indication for a requirement, based on defined criteria, to help stakeholders judge its readiness for validation.

*Acceptance Criteria:*
- Given a Requirement that has been analyzed, when its Quality Indication is requested, then a result distinguishing at least "ready for validation" from "needs clarification" is returned.
- Given a Quality Indication has been produced, when the Requirement's status is checked, then the status has not changed as a direct, automatic result of that indication.

**FR-05 Human Validation of AI Suggestions**

*Description:* The system shall require an explicit human decision (approve, edit, or reject) before any AI-generated suggestion affects the authoritative state of a requirement.

*Acceptance Criteria:*
- Given an AI Analysis awaiting review, when no human decision has been recorded, then the Requirement's authoritative state remains unaffected by that analysis.
- Given a human reviewer approves, edits, or rejects an AI Analysis, when the decision is recorded, then it includes a reference to who made it and is retrievable together with the Requirement.

**FR-06 Traceability Link Management**

*Description:* The system shall allow the creation and inspection of traceability links between a requirement and the artifacts derived from it.

*Acceptance Criteria:*
- Given a Requirement and a Derived Artifact, when a Traceability Link is created between them, then the link is retrievable by querying either the Requirement or the Artifact.
- Given a Requirement with one or more Traceability Links, when those links are requested, then all of them are returned.

**FR-07 Derived Artifact Creation**

*Description:* The system shall allow a validated requirement to be used as the basis for creating a derived, structured artifact (e.g., a backlog item), while preserving its link to the source requirement.

*Acceptance Criteria:*
- Given a Requirement whose status is "Validated," when a Derived Artifact is created from it, then the Artifact retains an explicit, retrievable reference to that Requirement.
- Given a Requirement whose status is not "Validated," when creation of a Derived Artifact from it is attempted, then no Artifact is created.

### Non-Functional Requirements

**NFR-01 Maintainability** — The codebase shall be organized so that changes to one concern (e.g., persistence, AI provider) do not require changes to unrelated parts of the system.

**NFR-02 Testability** — The architecture shall allow domain and application logic to be verified through automated tests independently of external infrastructure (database, AI provider, web framework).

**NFR-03 Modularity** — The system shall be composed of clearly bounded modules with explicit responsibilities, consistent with Domain-Driven Design and Hexagonal Architecture.

**NFR-04 Replaceable AI Provider** — The AI capability shall be accessed through an abstraction (the AI Gateway) that allows the underlying provider to be replaced without affecting domain or application logic.

**NFR-05 Security** — Access to external AI provider credentials and any future persisted data shall be handled through configuration mechanisms that avoid embedding secrets in source code or version control.

**NFR-06 Extensibility** — The domain and application layers shall be designed so that new requirement-derived artifact types or additional AI-assisted capabilities can be introduced without restructuring existing modules.

**NFR-07 Reliability** — The system shall ensure that failures originating in an external dependency (e.g., AI provider unavailability) do not corrupt or lose previously stored Requirement data.

**NFR-08 Error Handling** — The system shall handle failures in external dependencies gracefully, surfacing a clear, actionable indication rather than an unhandled failure, and without leaving a Requirement in an inconsistent state.

**NFR-09 Configuration Management** — Environment-specific settings (e.g., AI provider credentials, persistence configuration) shall be externalized from the codebase and managed through configuration mechanisms appropriate to each environment, consistent with NFR-05 (Security).

**NFR-10 Observability and Logging** — The system shall produce sufficient logging of significant domain events (e.g., an analysis requested, a validation decision recorded) to support debugging and future monitoring, without logging sensitive content in plaintext.

---

## Scope

### In Scope
- Modeling of the core Requirements Engineering domain concepts needed to support the platform's purpose (e.g., a requirement and its lifecycle, and its relationship to derived artifacts).
- A backend implementation in Python, architected according to Hexagonal Architecture and Domain-Driven Design.
- Integration with an AI provider (Gemini API) through a dedicated, abstracted AI Gateway, used to support — not replace — human decision-making in the requirements process.
- Mechanisms to establish and inspect traceability links between a requirement and the artifacts derived from it.
- A testing strategy and tooling setup (Pytest, static analysis) supporting continuous verification of the codebase as it grows.
- Project documentation that evolves alongside the implementation throughout the course.

### Out of Scope
- Multi-tenancy, enterprise-scale deployment, and organizational hierarchy management.
- Full compliance/regulatory features (e.g., audit certification, regulatory export formats).
- Integration with third-party Application Lifecycle Management tools (e.g., Jira, Azure DevOps).
- Real-time collaborative editing and presence features.
- A fully configurable workflow engine; any lifecycle/state handling implemented during the course is expected to remain intentionally minimal.
- Any user interface beyond what is strictly necessary to demonstrate and verify backend behavior; frontend scope, if any, will be defined separately and incrementally.
- Any specific class designs or database schemas beyond what has been explicitly decided at each stage of the project — these are not anticipated in this document and will be introduced only once designed.

---

## Stakeholders

- **Business Stakeholder / Domain Expert** — Represents the source of natural-language requirements. Interested in having their intent captured accurately and in being able to review how it has been interpreted, without needing to understand technical artifacts directly.

- **Requirements Engineer / Business Analyst** — Uses the platform to structure, refine, and validate requirements. Interested in tools that reduce ambiguity and manual effort while keeping them in control of the final interpretation.

- **Software Engineer / Developer** — Consumes structured requirements and traceability information to understand what must be built and why. Interested in requirements that are unambiguous, structured, and traceable to their origin.

- **Project Author (Student/Developer)** — Designs and implements BridgeIT as a university project, responsible for ensuring the system embodies the architectural and engineering principles the course requires, and for evolving both the implementation and this documentation incrementally.

- **Course Instructor / Academic Evaluator (University of Bologna)** — Evaluates the project against the Software Engineering course requirements, including architectural soundness, adherence to engineering principles, code quality, and documentation quality.

---

## User Stories

The user stories below translate the functional requirements into concrete usage scenarios, expressed from the perspective of the platform's primary actors (see [Stakeholders](#stakeholders)). Each story is linked to the functional requirement(s) it operationalizes, with one exception (US-08) that addresses the project's documentation process rather than a product feature.

**US-01 — Submitting a requirement** *(→ FR-01)*
> As a **Business Stakeholder**,
> I want to submit a requirement in natural language,
> So that my intent is captured as a structured artifact I can later review.

*Acceptance Criteria:* The stakeholder can submit free-text content and later retrieve it unchanged as a stored requirement.

**US-02 — Requesting AI-assisted analysis** *(→ FR-02)*
> As a **Requirements Engineer**,
> I want the platform to analyze a requirement for ambiguity or incompleteness,
> So that I can identify issues before the requirement is validated.

*Acceptance Criteria:* An analysis can be requested for any stored requirement, and its result is visible alongside the requirement's current text, without altering it.

**US-03 — Clarifying a requirement after analysis** *(→ FR-03)*
> As a **Business Stakeholder or Requirements Engineer**,
> I want to revise a requirement's wording after an analysis has surfaced an issue,
> So that the requirement can be improved before it is validated.

*Acceptance Criteria:* A requirement's text can be revised after it has been analyzed, the requirement keeps the same identifier, and the relationship between the original submission and the revision remains identifiable.

**US-04 — Reviewing requirement quality** *(→ FR-04)*
> As a **Requirements Engineer**,
> I want to see a quality indication for a requirement,
> So that I can decide whether it needs further clarification before proceeding.

*Acceptance Criteria:* A quality indication is retrievable for a requirement and clearly distinguishable from a final approval status.

**US-05 — Validating an AI suggestion** *(→ FR-05)*
> As a **Business Stakeholder or Requirements Engineer**,
> I want to explicitly approve, edit, or reject any AI-generated suggestion,
> So that no interpretation of my requirement becomes authoritative without my consent.

*Acceptance Criteria:* Every AI suggestion presented to a user offers an explicit approve/edit/reject action, and the resulting decision is recorded.

**US-06 — Inspecting traceability** *(→ FR-06)*
> As a **Software Engineer**,
> I want to inspect which artifacts are linked to a given requirement,
> So that I can understand the origin and justification of the artifacts I am implementing.

*Acceptance Criteria:* For any requirement, the set of linked derived artifacts can be listed and inspected.

**US-07 — Creating a derived artifact** *(→ FR-07)*
> As a **Software Engineer**,
> I want to create a derived artifact from a validated requirement,
> So that I can begin implementation work with a clear, traceable link back to its source.

*Acceptance Criteria:* A derived artifact created from a requirement is persisted together with an explicit reference to that requirement.

**US-08 — Tracing project documentation and design evolution** *(→ Development Methodology, Version Control Convention)*
> As a **Course Instructor / Academic Evaluator**,
> I want to trace how BridgeIT's documentation and architectural decisions evolved over time,
> So that I can evaluate the project's engineering discipline, not only its current state.

*Acceptance Criteria:* Changes to architecture and domain-model documentation are traceable through Git history following the project's Conventional Commits convention, so that the project's evolution can be reviewed independently of its final form.

---

## Requirements Engineering Workflow

BridgeIT is designed around an explicit, human-governed workflow. This section describes the workflow that the platform is intended to support; it is a description of expected behavior, not a record of implemented functionality (see [Current Development Status](#current-development-status)).

1. **Requirement submission** — A stakeholder submits a requirement in natural-language form. *(FR-01)*
2. **AI-assisted analysis** — The system uses the AI Gateway to analyze the submitted text, identifying potential issues such as ambiguity or incompleteness. *(FR-02)*
3. **Requirement clarification** — Where the analysis surfaces issues, the system presents them to the stakeholder, who may revise the requirement's wording. *(FR-03)*
4. **Requirement quality evaluation** — The requirement's structural and textual quality is assessed against defined criteria, producing a quality indication rather than a pass/fail gate. *(FR-04)*
5. **Human validation** — A human reviewer (business stakeholder, requirements engineer, or software engineer, depending on context) examines the AI-assisted output and explicitly approves, edits, or rejects it. *(FR-05)*
6. **Traceability generation** — Once validated, the requirement is linked to any artifacts derived from it, establishing a traceable relationship that can later be inspected. *(FR-06)*
7. **Creation of derived artifacts** — Structured artifacts (e.g., backlog items) are created from the validated requirement, always retaining their trace back to the originating requirement. *(FR-07)*

Every step above that involves an AI-generated output is governed by the same underlying principle, detailed in [AI Philosophy](#ai-philosophy): AI output is always a proposal, never an authoritative change.

---

## Architecture

BridgeIT's architecture follows Hexagonal Architecture (Ports and Adapters) and Domain-Driven Design, with a dedicated AI Gateway abstraction isolating the domain from any specific AI provider. To avoid duplicating architectural content across documents, the full architectural description — including the layering diagram, the AI Architecture explanation, and the illustrative API design — is maintained as a single authoritative reference in **[architecture.md](architecture.md)**.

The preliminary domain model referenced by that architecture (entities, value objects, aggregate boundary, and domain rules) is likewise maintained as a single authoritative reference in **[domain-model.md](domain-model.md)**, rather than being repeated here.

This report focuses on project vision, requirements, workflow, methodology, and project status; readers seeking architectural or domain-modeling detail should consult those two documents directly.

---

## AI Philosophy

AI plays a deliberately bounded role within BridgeIT: it exists to **support** the Requirements Engineering process, not to automate it away from human judgment.

Three principles govern how AI is used throughout the platform:

1. **AI supports, it does not decide.** Every AI-generated output — whether a quality assessment, a suggested rewrite, or a suggested traceability link — is treated as a proposal. It is presented to a human for review and requires explicit human confirmation before it becomes part of the authoritative project data.

2. **AI never replaces human validation.** No AI-generated artifact is permitted to change the state of the domain autonomously. The responsibility for interpreting business intent and for accepting or rejecting any AI suggestion remains with the human stakeholders using the platform.

3. **Every AI-assisted artifact remains traceable.** Any structured artifact that originates from, or is influenced by, an AI suggestion must retain a clear link back to the original natural-language requirement it was derived from. Traceability is treated as a first-class architectural concern, not an afterthought layered on top of AI-generated content.

This philosophy is intended to remain stable throughout the project, even as the specific AI capabilities implemented evolve.

---

## Technologies

| Technology | Role in the Project |
|---|---|
| **Python** | Primary implementation language for the entire backend. |
| **Poetry** | Dependency management and packaging, based on the official project template provided for the course. |
| **FastAPI** | Web framework used to expose the application's functionality through an HTTP interface. |
| **Gemini API** | External AI provider, accessed exclusively through the AI Gateway abstraction. |
| **Git** | Version control system used to track the incremental evolution of the codebase and documentation. |
| **GitHub** | Hosting platform for the project repository, enabling collaboration, change history, and (planned) CI/CD automation. |
| **Pytest** | Testing framework used to verify the correctness of the domain, application, and infrastructure layers. |
| **Ruff** | Static analysis and linting tool used to enforce code quality and style consistency. |
| **Mypy** | Static type checker used to verify type correctness across the codebase. |
| **Markdown** | Format used for all project documentation, including this report. |

---

## Development Methodology

BridgeIT is developed following an incremental engineering methodology, consistent with the academic and architectural goals of the project:

- **Incremental iterations** — The system is built in small, well-defined increments, each adding a bounded piece of functionality rather than attempting large, monolithic implementation steps.
- **Small commits** — Changes are committed to version control in small, focused units, each representing a coherent and reviewable step in the project's evolution.
- **Continuous testing** — Automated tests are introduced alongside the code they verify, rather than being deferred to the end of the project, so that the codebase remains verifiable at every stage.
- **Continuous documentation** — This document, and any documentation that follows it, evolves together with the implementation. Sections are updated, expanded, or corrected as architectural and implementation decisions are actually made, rather than being written speculatively in advance.
- **Git versioning** — All source code and documentation changes are tracked through Git, providing a complete history of how the project — including its architecture and its documentation — has evolved over time.

---

## Testing Strategy

BridgeIT's testing strategy is aligned with its Hexagonal Architecture: each architectural layer is expected to be verifiable in relative isolation. The categories below describe the testing strategy **planned** for the project; tests will be introduced incrementally as each corresponding layer is implemented, not all at once.

- **Unit Testing** — Verifies individual domain and application components in isolation (e.g., a single domain rule or service method), with external dependencies replaced by test doubles.
- **Integration Testing** — Verifies that adapters correctly implement their corresponding ports when connected to real or realistic infrastructure (e.g., persistence, AI Gateway adapter), and that application-layer use cases behave correctly when orchestrating domain objects and ports together.
- **Acceptance Testing** — Verifies that the system, as a whole, satisfies the functional expectations described in this document, from the perspective of a user of the platform.

These three categories are intended to follow the **test pyramid** principle: a large base of fast, isolated Unit Tests, a smaller layer of Integration Tests, and a minimal set of Acceptance Tests covering only the most significant end-to-end scenarios. This distribution is intended to keep the test suite fast to run and inexpensive to maintain as the codebase grows, consistent with NFR-02 (Testability); no specific proportion between the three categories is fixed at this stage, since no tests yet exist to measure it against.

Each test category is intended to trace back to the requirements it verifies, following the chain:

```
Requirement (FR-xx) → User Story (US-xx) → Test Case
```

This traceability chain is intended to ensure that every implemented test can be justified by a specific functional requirement and user story, and, conversely, that every functional requirement and user story is eventually covered by at least one test.

Test coverage will be monitored as the codebase grows, using tooling compatible with the Pytest setup already in place. **No coverage percentage has been achieved or measured at this stage**; coverage reporting will be introduced and reported truthfully as tests are added alongside implementation.

---

## Continuous Integration and Continuous Delivery

A Continuous Integration and Continuous Delivery pipeline is planned using **GitHub Actions**, to automatically verify code quality and, later, to automate releases. As with the rest of this document, the description below reflects planned configuration; it is not yet implemented (see [Current Development Status](#current-development-status)).

**CI pipeline (planned):**
- Install project dependencies via Poetry.
- Run static analysis with Ruff.
- Run type checking with Mypy.
- Run the automated test suite with Pytest.

**Release pipeline (planned):**
- Apply **Semantic Versioning** (MAJOR.MINOR.PATCH) to releases, consistent with the versioning convention described under [Version Control Convention](#version-control-convention).
- Produce and publish a versioned package release once the CI pipeline passes.

---

## Version Control Convention

BridgeIT's Git history follows the **Conventional Commits** convention, chosen to keep the project's evolution traceable and to make the purpose of each change explicit without needing to inspect its full diff.

Commits are kept small and coherent: each commit is expected to represent a single, self-contained change (e.g., one configuration step, one test, one small piece of functionality), rather than bundling unrelated changes together. This supports traceability of changes — both for the author, when reviewing the project's history, and for the course evaluator, when assessing how the project evolved over time.

Commit messages follow the pattern `<type>: <short description>`, using the following types:

| Prefix | Meaning |
|---|---|
| `feat:` | Introduces a new feature or capability. |
| `fix:` | Corrects a defect in existing functionality. |
| `docs:` | Changes to documentation only (e.g., this report). |
| `test:` | Adds or modifies automated tests. |
| `refactor:` | Restructures existing code without changing its external behavior. |

Examples:
```
feat: initialize bridgeit package structure
docs: add Requirements Engineering Workflow section
test: configure pytest environment
refactor: reorganize poetry project layout
```

Package releases, once introduced, will follow **Semantic Versioning**, as described in [Continuous Integration and Continuous Delivery](#continuous-integration-and-continuous-delivery).

---

## License

The project currently adopts the **Apache License 2.0**, inherited from the official Poetry project template provided for the course. No alternative license has been evaluated or applied at this stage.

The final version of this report will include a dedicated discussion of the license choice, including the rationale for retaining or changing it, once that decision is deliberately made rather than inherited by default.

---

## Repository Structure

The project repository is generated from the official Python Poetry project template provided by the course instructor. At this stage, the repository reflects only the structure produced by that template and the initialization work completed so far: standard Poetry project configuration, a Python package layout (renamed to `bridgeit`), and a location for automated tests, as established by the template itself.

No additional folders, modules, or files beyond what the template and the completed initialization actually contain are described here. As the project's domain, application, and infrastructure layers are implemented, this section will be expanded to accurately reflect the real, current structure of the repository — not an anticipated or planned one.

---

## Roadmap

The project is planned to progress through the following incremental milestones. Milestones are cumulative and are expected to be completed in sequence; only Milestone 1 is complete at the time of writing (see [Current Development Status](#current-development-status)).

- **Milestone 1 — Project Initialization** *(completed)*
  Repository setup from the official Poetry template, package renaming, testing environment, and static analysis configuration.
  *Deliverable:* An initialized Git repository with Poetry configuration, the `bridgeit` package, a configured test runner, and static analysis tooling — the current state of this repository.

- **Milestone 2 — Domain Model**
  Implementation of the core domain entities, value objects, and business rules identified in [domain-model.md](domain-model.md).
  *Deliverable:* Domain entities and value objects implemented as plain Python objects, with no persistence or API dependency, covered by unit tests.

- **Milestone 3 — Requirement Management**
  Implementation of the application-layer use cases and (initially in-memory or minimal) persistence needed to support requirement creation, retrieval, and clarification.
  *Deliverable:* Application-layer use cases for FR-01 and FR-03, backed by an initial persistence adapter, covered by application-level tests.

- **Milestone 4 — AI Gateway**
  Implementation of the AI Gateway abstraction and its adapter for the Gemini API, supporting AI-assisted requirement analysis.
  *Deliverable:* An AI Gateway port and a Gemini adapter implementing FR-02 and FR-04 end-to-end, together with the human validation mechanism required by FR-05 to act on the resulting AI Analysis, with the adapter covered by integration tests.

- **Milestone 5 — Traceability**
  Implementation of traceability link management and derived artifact creation.
  *Deliverable:* FR-06 and FR-07 implemented and exposed through the application layer, with acceptance tests demonstrating the full Requirement → AI Analysis → Human Validation → Traceability Link → Derived Artifact flow.

- **Milestone 6 — Testing and Deployment**
  Consolidation of the automated test suite across all layers, and introduction of the CI/CD pipeline described in [Continuous Integration and Continuous Delivery](#continuous-integration-and-continuous-delivery).
  *Deliverable:* A consolidated test suite across unit, integration, and acceptance levels, and a working CI/CD pipeline executing linting, type checking, and tests on every commit, with a first versioned package release.

---

## Current Development Status

This section reflects the actual, current state of the repository at the time of writing, and will be updated as the project progresses.

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
- Persistence layer (repository implementations and storage).
- CI/CD pipeline (GitHub Actions).
- Frontend (no user interface has been designed or built).

This document will be revised at each meaningful project milestone so that it remains an accurate reflection of BridgeIT's implementation status, rather than a description of its intended end state.