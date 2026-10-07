# BridgeIT — Domain Model

**Status:** Current conceptual domain model, aligned with the implementation at the latest release (see `CHANGELOG.md`).

This document describes the domain concepts that are currently implemented and distinguishes them from concepts that remain part of the planned future scope.

---

## Ubiquitous Language

| Term | Meaning | Current status |
|---|---|---|
| **Requirement** | A natural-language statement of intent managed through its lifecycle in BridgeIT. | Implemented |
| **AI Analysis** | The result of an AI-assisted evaluation of a Requirement, including a qualitative indication and identified issues. | Implemented |
| **Artifact** | A structured engineering-facing object derived from a validated Requirement. | Conceptual / future |
| **Traceability Link** | An explicit relationship connecting a Requirement to a derived Artifact. | Conceptual / future |
| **Quality Indication** | The non-binding quality result produced by an AI analysis. | Implemented as `QualityScore` |
| **Human Validation** | The explicit approve, edit, or reject decision performed by a human reviewer. | Implemented in application/domain workflow |
| **RequirementText** | Immutable value object containing the current requirement text. | Implemented |
| **RequirementStatus** | Enumeration representing the requirement lifecycle state. | Implemented |

---

## Domain Entities

### Requirement

**Purpose:** Represents a single requirement expressed in natural language and managed through the BridgeIT lifecycle.

**Implementation:** `bridgeit/domain/requirement.py`

**Main attributes:**

- unique identifier;
- current `RequirementText`;
- current `RequirementStatus`.

The current implementation does not store a submission timestamp or a version-history collection.

### Lifecycle

The actual state machine implemented by `Requirement` is:

```text
Submitted → Analyzed

Analyzed → Validated
Analyzed → Clarified
Analyzed → Rejected

Clarified → Analyzed

Validated → terminal
Rejected → terminal
```

The `Requirement` entity enforces these transitions through its domain methods. Invalid transitions raise `InvalidStateTransitionError`.

When a requirement is clarified, its current text is replaced by a new `RequirementText` while the identifier remains unchanged.

---

### AI Analysis

**Purpose:** Represents the outcome of one AI-assisted analysis of a requirement.

**Implementation:** `bridgeit/domain/ai_analysis.py`

The current implementation contains:

- `quality_score: QualityScore`;
- `issues: tuple[str, ...]`.

`QualityScore` has two values:

- `ready_for_validation`;
- `needs_clarification`.

The AI Analysis object does not currently contain an independent identifier, a suggested-revision field, or a human decision field. It is produced by the AI Gateway, returned by the analysis endpoint, and not persisted as an independent database record.

---

## Value Objects

### RequirementText

`RequirementText` is an immutable value object containing the current natural-language requirement.

An empty or whitespace-only value is rejected. When the requirement is edited, a new `RequirementText` instance is created instead of mutating the old value object.

The implementation preserves only the **current** value. Previous versions are not retrievable from the database.

### QualityScore

`QualityScore` is an enumeration used to represent the qualitative result of an AI-assisted analysis:

```text
READY_FOR_VALIDATION
NEEDS_CLARIFICATION
```

It is a value rather than a numeric measurement and is intended to guide human review.

### RequirementStatus

`RequirementStatus` is implemented as an enumeration with the following values:

```text
Submitted
Analyzed
Clarified
Validated
Rejected
```

### ValidationDecision

A human validation decision exists in the application workflow as one of the values:

```text
approve
edit
reject
```

At present it is represented by the API request rather than by a dedicated domain `ValidationDecision` class. The authenticated identity of the reviewer is also not stored, because authentication and user management are outside the current implementation scope.

---

## Domain Rules

The current domain enforces the following rules:

1. A new Requirement always starts in `Submitted`.
2. Only a Requirement in `Submitted` or `Clarified` can be analysed through the corresponding state transition.
3. An AI analysis moves an eligible Requirement to `Analyzed`, but the AI does not choose a final human validation outcome.
4. Only an explicit human validation action can move an `Analyzed` Requirement to `Validated`, `Clarified`, or `Rejected`.
5. `Validated` and `Rejected` are terminal in the current implementation.
6. An edited Requirement keeps the same identifier and moves to `Clarified`.
7. A `Clarified` Requirement must be analysed again before it can be validated.

Traceability-link and derived-artifact constraints remain conceptual because those features are not implemented in the current release.

---

## Conceptual Future Domain Concepts

### Artifact

An `Artifact` is a planned engineering-facing object derived from a validated Requirement, such as a future backlog item or development artifact.

The current artifact does **not** implement an `Artifact` class, repository, database table, or API endpoint. It therefore remains a future domain concept documented for FR-07.

### Traceability Link

A `TraceabilityLink` is a planned first-class relationship between a Requirement and a derived Artifact.

The current artifact does **not** implement this entity, its persistence, or its endpoints. It remains part of the future scope described for FR-06.

---

## Aggregate Boundary

`Requirement` is the only implemented aggregate root in the current domain model. Its responsibility is to protect its own text and lifecycle state.

`AIAnalysis` is a separate immutable result object produced by the application-level analysis workflow rather than a persisted aggregate. `Artifact` and `TraceabilityLink` remain conceptual future objects and therefore do not currently participate in a runtime aggregate boundary.

---

## Modeling Boundaries

The following decisions are intentional current limitations:

- **Requirement history:** only the current text is stored; previous revisions are not persisted.
- **AI analysis history:** analyses are not persisted independently and are not queryable after the analysis response.
- **Authentication:** no `User` or identity entity is implemented.
- **Artifact taxonomy:** no concrete derived-artifact type has been implemented.
- **Traceability:** links are conceptual only and are not currently stored.

These boundaries keep the implemented domain model consistent with the functionality actually present in the artifact.

