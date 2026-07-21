# Project Roadmap and Task Assignment

This roadmap defines the weekly goals for the team and **puts into practice the Milestones already defined in `report.md` (Roadmap section)**: it is not an alternative plan, but the translation of those milestones into weekly tasks assigned per person, with beginner-level subtasks.

**Team:**
- `@nikytresca` — Domain and AI developer (Domain Layer, AI Gateway)
- `@marthinaf03` — Data and API developer (Persistence, FastAPI, Frontend)

**Duration:** 4 weeks.

---

## Review Note (regarding the draft proposed by Gemini)

I corrected/integrated a few points to align them with `report.md`, `architecture.md`, and `domain-model.md`:

1. **Typo fixed:** "Aggregate Root Requiremente" → **Requirement**.
2. **AI provider:** the current documentation plans for **a single AI provider (Gemini)** behind the AI Gateway, not "Gemini/OpenRouter". If you really want to plan for a second provider as a fallback, it should first be added as an explicit requirement in `report.md` (a new NFR) — for now I've left it out, consistent with the project's principle of not implementing anything that isn't documented first.
3. **AI cache:** this is not currently a documented requirement (it doesn't appear among the FR/NFR). I've left it as an **optional/stretch** task in Week 2, clearly flagged as such, not as a core task.
4. **Missing from the original draft, added here:** the task for **FR-05 (Human Validation)** in Week 3. This is an important omission: FR-05 is the mechanism that makes the project's core principle true ("AI suggests, the human validates" — see `report.md` — AI Philosophy). Without it, the prototype would not honor BridgeIT's central idea, no matter how well everything else works.
5. **Week 4 corrected:** the original draft assumed the Report had to be "written" from scratch. In reality, `report.md`, `architecture.md`, and `domain-model.md` are **already written in detail** and available in the documentation repository (https://github.com/nikytresca-pixel/report). The real work for Week 4 is not to write, but to **update** these documents to reflect what has actually been implemented (in particular the "Current Development Status" and "Current Limitations and Future Challenges" sections).
6. Every task now explicitly references the **FR-xx / NFR-xx** and the **endpoints** already defined in `architecture.md` — so every subtask is traceable to a requirement already written, not invented on the spot.

---

## Update 1 — GitHub Organization and New Requests from the Professor

1. **The GitHub organization already exists**: [`unibo-dtm-se-2526-bridgeit`](https://github.com/unibo-dtm-se-2526-bridgeit). It contains (or will contain) both the `artifact` repository (code) and the `report` repository (documentation). The task is no longer "create the organization", but **migrate the documentation already written in `artifact/docs/` into the `report` repository**, following its official 12-numbered-section structure.
2. **Preliminary request from the professor** during the review of the Concept section: (a) include user management in the project's scope; (b) specify SQLite as the concrete persistence technology. Point (b) has been **confirmed and made official** (see Update 2). Point (a), user management, **did not appear in the official approval communication** — it therefore remains an open hypothesis, not a confirmed requirement at this stage. It has not been added to `domain-model.md`/`architecture.md`/`report.md` for this reason: if the professor confirms it later, it will be picked up separately.

### A. Documentation migration into the `report` repository

- [ ] **01-concept** — ✅ Content already ready: `Concept.md`, already refined with the professor's guidance (user management not included, SQLite persistence made explicit).
- [x] **02-requirements** — ✅ Drafted into the `report` repository by `@marthinaf03` (see Update 8). Source: `report.md` (Problem Statement, Domain Terminology, Project Objectives/FR/NFR, User Stories, Scope, Stakeholders).
- [x] **03-design** — ✅ Drafted into the `report` repository by `@marthinaf03` (see Update 8). Source: `architecture.md` and `domain-model.md`.
- [ ] **04-development** — ⚠️ Partially ready: `report.md` (Development Methodology) and `architecture.md` (Proposed Package Structure, now including the `frontend/` folder) cover the principles; needs to be integrated with the practical setup instructions from the README.
- [x] **05-validation** — ✅ Drafted into the `report` repository by `@marthinaf03` (see Update 8). Source: `report.md` — Testing Strategy, now also reflecting the real 26-test suite at 95% coverage.
- [x] **06-release** — ✅ Drafted into the `report` repository by `@marthinaf03` (see Update 8). Source: `report.md` — Version Control Convention and License.
- [x] **07-deployment** — ✅ **No longer empty**: Docker support (`Dockerfile`, `docker-compose.yml`) added by `@marthinaf03` (see Update 8) directly fills this gap.
- [ ] **08-cicd** — ✅ Content ready: `report.md` — Continuous Integration and Continuous Delivery. *(The pipeline itself is now reported fully functional — see Update 8 — but the section's migration into `report` is not yet explicitly confirmed.)*
- [ ] **09-user-guide** — ❌ To be written: requires at least the minimal frontend (Milestone 7) to be implemented.
- [ ] **10-devguide** — ⚠️ Partially ready: the `artifact` repository's README already contains the backend setup instructions (now rewritten to match real progress — see Update 8); frontend and Docker instructions still need to be added.
- [ ] **11-self-assessment** — ❌ To be written at the end of the project.
- [ ] **12-future** — ✅ Content ready: `report.md` — Current Limitations and Future Challenges.

### B. Substantive changes — updated status

- [x] **`report.md`** — Scope, Technologies, Roadmap, and Current Development Status updated with SQLite and the minimal frontend. *(Done)*
- [x] **`architecture.md`** — Repository Pattern, Adapter Responsibilities, and Proposed Package Structure now explicitly name SQLite (via `sqlite3`); the `frontend/` folder added as an external client to the hexagon. *(Done)*
- [ ] **`domain-model.md`** — No change needed: neither persistence nor the frontend introduce new domain concepts (exactly the benefit of Hexagonal Architecture). This remains valid **only if and when** user management is confirmed by the professor (in which case a new `User` entity would be needed).

---

## Update 2 — Official Approval: Persistence and Frontend

The project received official approval from the professor, with two additional technical requirements tied to the team growing from one to two people:

1. **Persistence**: SQLite, with **SQLAlchemy** as the ORM, behind the Repository pattern.
2. **Frontend**: a minimal web application, consuming the REST APIs exposed by FastAPI — no specific page or feature beyond what is already implicit in the requirements (FR-01 → FR-07).

These two points have already been integrated into `report.md` and `architecture.md` (see checklist B above). What follows is the practical impact on the operational roadmap: the single "Requirement Management" Milestone has been split into two distinct Milestones (Persistence and API), and a Milestone for the Frontend has been added — which is **new** work, not just a re-framing of already-planned tasks.

**Honest note on workload:** adding an entire frontend, while keeping the one-month constraint, is ambitious for a two-person team new to this. The plan below handles this by starting the frontend in Week 3 (not Week 4), in parallel with the rest, instead of piling it all up at the end. If time gets tight, the first thing to cut is the frontend's own scope (a single page covering the whole flow, without styling or multiple pages) — not its architectural foundations (it must still remain an external client that only consumes the REST API, never direct access to the backend).

---

## Update 3 — Official Feedback from the Professor After Approval

The project has been **officially approved** by the instructor. With the second person joining the team, the professor explicitly requested two additional technical requirements:

1. **A DBMS** — SQLite is sufficient. This was already the choice made in Update 2; here it is confirmed as an explicit requirement from the professor, not just our own technical decision.
2. **A frontend** (web or desktop) — also already planned in Update 2; the professor now makes it an explicit requirement.

**This update supersedes what is written in Update 1, point 2:** **user management** (minimal user handling) was no longer "an open hypothesis" — it is now **confirmed** as part of the required persistence work. As a consequence, `domain-model.md` will need a new `User` entity (see the updated checklist B below); it is not added here because this roadmap, per these instructions, only updates itself, not the other documents.

The feedback translates into these new work packages, distributed across the existing weeks (details in each week's section below):

- **Persistence:** SQLite repository via `sqlite3` for `Requirement` (already implemented — see PR #6 and ADR-0001 in Update 4), **+ user persistence** (minimal authentication), **+ backlog persistence** (the `Derived Artifacts`), with corresponding integration tests for each.
- **Frontend:** confirmed **React + TypeScript** as the stack (no technical reason to choose otherwise, since the frontend remains a lightweight external client — see `architecture.md` — Adapter Responsibilities). The work now explicitly breaks down into: project setup, communication with the FastAPI APIs, requirement submission, requirement visualization, AI Analysis visualization, human validation workflow, traceability visualization, and UI polishing in the last week.

### Checklist B — update to `domain-model.md`'s status

- [ ] **`domain-model.md`** — **Now requires a change** (no longer "no change needed"): a new `User` entity needs to be added (identity, role), since user management has been confirmed by the professor (see above). This change is not included in this roadmap: it is only tracked here as work to be done, consistent with the instruction to update only the roadmap at this stage.

---

## Update 4 — Final Decision on Persistence: Plain `sqlite3`, Not SQLAlchemy

During the implementation of the first persistence adapter (`SQLiteRequirementRepository`, PR #6), the work was done using Python's standard `sqlite3` module directly, with hand-written SQL — **not SQLAlchemy**, as instead planned in `report.md`, `architecture.md`, and the earlier weeks of this roadmap.

After review, this choice was **confirmed as final**: the `RequirementRepository` port isolates the domain and Application Layer from any concrete technology regardless, so plain `sqlite3` is fully consistent with the architecture, simply different from the originally planned technology. This is exactly the kind of decision that `architecture.md` — Architecture Decision Records promised to record "once it is actually made": the project's first real ADR has therefore been created, [`docs/adr/0001-sqlite-persistence-without-orm.md`](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/master/docs/adr/0001-sqlite-persistence-without-orm.md).

As a result:
- `report.md`, `architecture.md`, and this roadmap have been updated to describe **SQLite via `sqlite3`**, no longer SQLAlchemy.
- Every **not-yet-completed** task that mentioned SQLAlchemy (`User` persistence in Week 2, `Artifact`/backlog persistence in Week 3) has been updated accordingly below, to give correct instructions to whoever carries them out.
- No impact on `domain-model.md`: the choice between `sqlite3` and SQLAlchemy is a detail of the driven adapter, it doesn't touch the domain.

---

## Update 5 — Final Decision on the Frontend: HTML/CSS/JavaScript, Not React + TypeScript

During the implementation of the first piece of frontend (PR #7, the backend health-check page), the work was done with plain HTML, CSS, and JavaScript, with no framework and no build system — **not React + TypeScript**, as instead declared "confirmed" in Update 3.

After review, this choice was **confirmed as final**: the frontend still remains an external client that talks to the backend only through `fetch()` calls to the REST API — exactly the boundary required by `architecture.md` — regardless of React or TypeScript. For a project the professor wants to keep "intentionally lightweight" on the frontend, a static site with no build system is just as consistent (if not more so) as an entire React + TypeScript toolchain. As with persistence, a second ADR has been created: [`docs/adr/0002-vanilla-html-css-js-frontend.md`](https://github.com/unibo-dtm-se-2526-bridgeit/report/blob/master/docs/adr/0002-vanilla-html-css-js-frontend.md).

As a result:
- `report.md` — Technologies updated to describe HTML/CSS/JavaScript instead of "framework to be selected".
- Every **not-yet-completed** task that mentioned React + TypeScript has been updated below.
- No impact on `domain-model.md`.
- **Side note, not yet resolved:** the frontend lives in the `web/` folder, while `architecture.md` — Proposed Package Structure still names `frontend/`. This has not been touched in this update (it concerns only `report.md`/`RoadMap.md`); if `web/` is confirmed as the final name, it will need to be aligned there too in a later step.

---

## Update 6 — Removal of User Management: the Source Was Never Verified

After a more thorough discussion within the team, it emerged that the "confirmation" of user management cited in Update 3 never had a verifiable source — not even in the original message that reported it. Update 1, written earlier, had already correctly treated this point as "an open hypothesis, not a confirmed requirement"; Update 3 reversed that without any real confirmation ever coming from an official communication from the professor.

Weighing pros and cons carefully: the main pro — avoiding a failing grade for missing requirements — depends entirely on clarifying a source that was never clarified. The cons, on the other hand, are concrete and immediate: real workload in a month that is already tight for two people (new entity, password hashing, endpoints, tests); the risk of implementing rushed authentication, which would be perceived worse at evaluation time than an honestly declared omission; and above all, time taken away from the project's actual core (Requirement → AI Analysis → Human Validation), which remains the most likely evaluation criterion (see `report.md` — AI Philosophy).

**Decision:** User Management is removed from the operational roadmap. All tasks concerning it (the `User` entity in Week 1, user persistence and the `/users`/`/login` endpoints in Week 2) have been removed from the weeks below.

**Concrete action, not to be postponed:** explicitly verify in writing with the professor whether user management is genuinely required, before spending any development time on it. If a real confirmation arrives, it will be treated as a new work package starting from that point — not retroactively recovered from this update.

This restores as valid the line already written in **Checklist B** above ("no change needed to `domain-model.md`... this remains valid only if and when user management is confirmed") — that caution was correct from the start.

---

## Update 7 — Frontend CRUD Completed and Common Error Format (`ApiError`)

During Week 3, `@marthinaf03` has already completed, ahead of schedule:

- The **basic frontend CRUD pages** (create/view requirement), marked as completed above.
- A **common error format for the API**, `ApiError` — `{"error": {"code": "...", "message": "..."}}` — already applied to `GET /requirements/{id}`. This is the same structure discussed and agreed with `@nikytresca` in the exchange about the JSON contract for `/analyse` and `/validate`.

**Practical consequence:** the endpoints still to be written (`/analyse`, `/validate`) must reuse this same `ApiError` structure, not define their own — consistency already agreed, now also tracked here.

---

## Update 8 — Backend, Testing, CI/CD, and Documentation Confirmed Complete by `@marthinaf03`

`@marthinaf03` has reported substantial, verified progress that goes beyond what this roadmap had tracked so far.

**Backend — Persistence and API**
- `POST /requirements` and `GET /requirements/{id}` (FR-01) implemented and verified, both manually (Swagger UI) and with automated tests.
- The shared `ApiError` format (Update 7) is now confirmed applied to both application errors and input-validation errors, not just some of them.

**Testing and code quality**
- API endpoint integration tests added (via FastAPI's `TestClient`).
- Test coverage measurement properly configured (previously present but misconfigured): **95%** coverage on production code.
- The project now has **26 automated tests** in total, across domain, application, persistence, and API.

**Frontend**
- Create and view requirement pages now connected to the real backend endpoints (not placeholders).
- A coherent, deliberate visual direction (not generic) has been defined and applied — a professional technical-console aesthetic, with intentional animations (loading state, visual confirmation) designed to be reused in the upcoming AI Analysis / Validation pages `@nikytresca` is building.

**CI/CD and infrastructure — new, not previously tracked in this roadmap**
- Diagnosed and fixed a systematic CI/CD failure on the release job (misconfigured GitHub token, never resolved before).
- Diagnosed and fixed a second, related issue about conditional PyPI publishing.
- **Docker support added** (`Dockerfile`, `docker-compose.yml`): the project can now be started with a single command, without installing Python or Poetry locally. This directly fills the gap flagged in checklist A for **07-deployment** (previously "to be written: no real deployment planned yet" — updated below).
- The CI/CD pipeline is now **fully functional**, including automatic release via `semantic-release`.

**Documentation and project quality**
- README fully rewritten to match the project's real current state (it previously described a much earlier phase).
- Drafted the **Requirements, Design, Validation, and Release** sections for the course documentation repository — substantially completes checklist A's items 02, 03, 05, and 06 (updated below).
- Project metadata reviewed and fixed (author info, description, license, changelog), including a non-trivial oversight inherited from the course template: dependency-update PRs were being assigned to the professor instead of the team.
- **Drafted an AI-tool-usage disclosure statement** for her share of the work, per the course template's transparency guidance.

**Overall status, per `@marthinaf03`:** backend (persistence, API, testing), infrastructure (CI/CD, containerization), the basic frontend, and project documentation are complete and verified. What remains is AI Gateway integration and the human validation mechanism for AI-generated analyses (FR-05), currently in progress by `@nikytresca`.

**Action for `@nikytresca`, not to be skipped:** the course template expects an AI-tool-usage disclosure statement per person, not just one for the team. Since a substantial share of the domain modeling and documentation work was AI-assisted, a similar disclosure should be drafted for this side of the work too, matching the transparency standard `@marthinaf03` has already set.

---

## Week-to-Milestone Map (from `report.md`, 8-milestone version)

| Week | Milestones covered |
|---|---|
| 1 ✅ | Milestone 2 (Domain Model) — completed |
| 2 | Milestone 3 (Persistence Layer) + Milestone 5 (AI Gateway Integration) + **start of** Milestone 7 (Frontend) |
| 3 | Milestone 4 (Requirement Management APIs, including FR-05) + main frontend development + **possible** Milestone 6 (Traceability & Derived Artifacts, if time allows) |
| 4 | Milestone 8 (Testing, CI/CD and Release) + frontend polish |

---

## Week 1 — Domain and Setup ✅ (completed)

*(Actual status, no longer a plan: this week is complete.)*

### `@nikytresca`

- [x] **Migrate the documentation into the `report` repository**, under the [`unibo-dtm-se-2526-bridgeit`](https://github.com/unibo-dtm-se-2526-bridgeit) organization, following the *A. Documentation migration* checklist above.
- [x] **Develop the entire Domain Layer in Python** (see `domain-model.md` — Domain Entities, Value Objects, Aggregate Boundary).
  - [x] Value objects: `RequirementText`, `RequirementStatus` (enumeration: `Submitted`, `Analyzed`, `Clarified`, `Validated`, `Rejected`).
  - [x] `Requirement` entity (identity, text, status), with allowed state transitions as methods — pure Python only.
  - [x] Unit tests for entities and value objects (creation, valid/invalid transitions, value-object equality).

### `@marthinaf03`

- [x] **Basic FastAPI project setup with Poetry**, `/health` endpoint.
- [x] `application/` package with the `RequirementRepository` port (abstract), and Pydantic models (DTOs) for request/response, distinct from the domain.
- [x] Fake in-memory repository, with conformance tests against the port.
- [x] **Refactor `Any` → `Requirement`** once `@nikytresca`'s Domain Layer was integrated (closed the tech debt tracked in the dedicated issue).

---

## Week 2 — SQLite Persistence and Frontend Kickoff

### `@marthinaf03` — Milestone 3: Persistence Layer

- [ ] **`SQLiteRequirementRepository` adapter**, conforming to the already-defined port. *(Implemented in PR #6 using plain `sqlite3` — see Update 4 and ADR-0001.)*
  - [ ] `infrastructure/persistence/` module, database connection handling (local file).
  - [ ] Tests: saving and retrieving a `Requirement`; no data loss/alteration between write and read.

### `@nikytresca` — Milestone 5: AI Gateway Integration

- [ ] **AI adapter (Gemini)**, corresponding to FR-02.
  - [ ] `infrastructure/ai/` module; `AIGateway` port (abstract interface) in the Application Layer.
  - [ ] Implementation translating Gemini's response into a domain `AIAnalysis`.
  - [ ] Tests with a **mocked** Gemini client (never the real API in automated tests).

*If time allows:*
- [ ] *(Optional/stretch — not currently a documented requirement)* Cache for AI calls, only if first documented as a technical note in `report.md`.

### New — Frontend (kickoff, both)

Confirmed stack: **plain HTML, CSS, and JavaScript, with no framework and no build system** — see Update 5 and ADR-0002.

- [x] **`web/` folder with minimal structure**, CORS on the FastAPI side where needed, static test page calling `/health` to confirm the end-to-end connection. *(Already implemented in PR #7.)*
- [ ] **Wireframe/sketch of the screens** for AI Analysis + Human Validation (just a sketch on paper or a lightweight tool — no code needed), to give `@nikytresca` a clear starting point before Week 3.
- [ ] **Shared JSON data contract between the two**, for the exchange between frontend and backend on Week 3's endpoints (shape of requests/responses for analysis and validation) — agreed together, so each person's pages can be developed in parallel without blocking each other.

---

## Week 3 — Use Cases, Integration, Frontend

### `@nikytresca` — Application Layer + Frontend (AI Analysis and Validation)

- [ ] Use case "Submit requirement" (FR-01).
- [ ] Use case "Request AI analysis" (FR-02).
- [ ] Use case "Clarify requirement" (FR-03).
- [ ] Use case "Get Quality Indication" (FR-04).
- [ ] **FR-05 — Human Validation** (fundamental, non-negotiable — it's the mechanism that makes "AI suggests, the human validates" true).
  - [ ] `ValidationDecision` use case (approve / edit / reject).
  - [ ] Explicit guarantee, with dedicated tests: no `AIAnalysis` changes a `Requirement`'s status without a human decision.
- [ ] High-coverage application/domain logic tests.
- [ ] **Use the common `ApiError` error format** (`{"error": {"code": ..., "message": ...}}`) for `/analyse` and `/validate`, already implemented by `@marthinaf03` and applied to `GET /requirements/{id}` — do not define a different one (see Update 7).
- [ ] **Frontend — AI Analysis + Human Validation pages**, calling `POST /requirements/{id}/analyse` and `POST /requirements/{id}/validate` (JSON contract agreed in Week 2).

### `@marthinaf03` — API + Frontend (basic CRUD)

- [x] `POST /requirements` (FR-01), `GET /requirements/{id}`. *(Implemented and verified — manually via Swagger UI and with automated tests. See Update 8.)*
- [ ] `POST /requirements/{id}/analyse` (FR-02), `POST /requirements/{id}/validate` (FR-05).
- [x] Manual verification via Swagger UI for the endpoints above. *(Full end-to-end verification, including `/analyse` and `/validate`, still pending until those are implemented.)*
- [x] **Frontend — basic CRUD pages**: create/view requirement (calling `POST /requirements`, `GET /requirements/{id}`), minimal HTTP error handling, navigation/linking between both people's pages. *(Completed by `@marthinaf03` — see Update 7.)*

*If time allows (not core):*
- [ ] `GET /requirements/{id}/traceability-links` (FR-06) and `POST /requirements/{id}/artifacts` (FR-07), with the corresponding use case and persistence for `Artifact`.

---

## Week 4 — Report and Final Polish

### `@nikytresca`

- [ ] **Update `architecture.md` and `domain-model.md`** — only real deviations from what was planned, without rewriting; no entry on `User` is needed anymore (removed in Update 6).
- [x] **Set up/review the CI/CD pipeline (GitHub Actions)**: install dependencies → `poetry run poe static-checks` → `poetry run poe test`. *(Completed ahead of schedule by `@marthinaf03`, including automatic release via `semantic-release` and a fix for a previously-unresolved token misconfiguration — see Update 8.)*

### `@marthinaf03`

- [ ] **Update `report.md`** — Testing Strategy, Current Development Status, Technologies (HTML/CSS/JavaScript confirmed). No user management entry to add to Scope (see Update 6).
- [ ] Document the chosen frontend stack and the `web/` structure in `report.md`.

### Together

- [ ] **Full end-to-end test**: Requirement → AI Analysis → Human Validation (+ Traceability/Artifact, if implemented in Week 3) — run also through the frontend, not only from Swagger UI.
- [ ] **Update `report.md` — "Current Limitations and Future Challenges" and "Conclusion"** with the real state reached, without declaring anything implemented that isn't — including an honest note that user management is not implemented, pending verification with the professor (Update 6).
- [ ] Verify all cross-links between `report.md`, `architecture.md`, `domain-model.md`.
- [ ] **Frontend polish** (light, lowest priority): minimal loading/error states, basic visual consistency. This is not a design exercise — keep it intentionally light.

---

## Functional Requirement Coverage After This Update

Verifies that every FR has at least one roadmap activity covering it, after the removal of User Management and the frontend restructuring:

| FR | Coverage in this roadmap |
|---|---|
| FR-01 (Requirement Creation) | Week 1 ✅ (`Requirement.submit`), Week 3 (`POST /requirements`) |
| FR-02 (AI-Assisted Analysis) | Week 2 (Gemini adapter), Week 3 (`POST /requirements/{id}/analyse`) |
| FR-03 (Requirement Clarification) | Week 1 ✅ (`clarify()` method), Week 3 ("Clarify requirement" use case) |
| FR-04 (Requirement Quality Evaluation) | Week 3 (`QualityScore` produced by the Gemini adapter, "Get Quality Indication" use case) |
| FR-05 (Human Validation) | Week 3 (`ValidationDecision`, `POST /requirements/{id}/validate`) — **fundamental, non-negotiable** |
| FR-06 (Traceability Link Management) | Week 3, **if time allows** (no longer guaranteed as core — see the workload note) |
| FR-07 (Derived Artifact Creation) | Week 3, **if time allows** (same) |

All seven Functional Requirements remain covered by at least one planned activity. FR-06 and FR-07 have been **downgraded to "if time allows"** in this update, in line with the choice to prioritize the core cycle (Requirement → AI Analysis → Human Validation) over additional features, now that User Management no longer absorbs time but the margin still remains tight for one month with two people. No FR has been removed.
