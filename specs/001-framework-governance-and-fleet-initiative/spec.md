# Feature Specification: Framework Governance & Fleet Initiative

**Feature Branch**: `retro/001-framework-governance-and-fleet-initiative` (as-built record — no branch created)

**Created**: 2026-07-05

**Status**: Shipped (v0.0.1, v0.0.2, v0.0.3)

**Input**: retro-spec conversion of v0.0.1 (Director-layer template baseline, commits 5c7886b…2f7ca6c/839517e), v0.0.2 (TradeFleet initiative proof-of-concept docs, 5faa89e), and v0.0.3 (GitHub Spec Kit adoption, 999d30f)

## Why

Agentic-Vibe-Fleet is the **methodology repo itself** — the Tier-1 "operating system" that
governs how autonomous agents build software across the fleet (`docs/tradefleet_initiative.html:116-121`).
Without a durable, repo-resident constitution, every agent session re-litigates resolved
decisions and loses architectural context ("context rot", `GEMINI.md:1`). This capability is
the governance layer of record: the constitution codifying five hard-won lessons
(`GEMINI.md:8-30`), the pattern registry (`PATTERNS.md`), the self-verifying architecture map
(`Project_Structure.md` + changelog table), the traceability map (`Function_Mapping.md`),
declared-but-unfilled Bruno/Terraform gates, the visual explainers under `docs/`, the v0.0.2
proof that the methodology shipped a real three-tier fleet (TradeFleet → EcoHomeBuild +
BullyBrickMI live), and — since v0.0.3 — the GitHub Spec Kit chain that makes the 80/20
planning phase produce durable `specs/NNN-*/` artifacts.

Unlike consumer repos (e.g. VoiceBridge's `specs/001`), which *apply* this framework, this
spec documents the framework at its origin: the governance texts here are the product.

## User Scenarios & Testing

### User Story 1 - Session bootstrap with full architectural context (Priority: P1)

A fresh Lead Agent session reads `GEMINI.md`, `PATTERNS.md`, and `Project_Structure.md` and
can navigate the repo, inherit all prior design decisions, and know the non-negotiable gates
without the Director re-explaining anything.

**Why this priority**: Context-rot prevention is the framework's stated reason to exist
(`GEMINI.md:1`); the five lessons are the product.

**Independent Test**: Open a fresh agent session with only the three governance docs; ask it
(a) where maintenance skills live and (b) what string is required to commit with a failing
Bruno gate. It should answer `scripts/` (`Project_Structure.md:14`) and the exact exception
string (`GEMINI.md:25`) without a codebase search.

**Acceptance Scenarios**:

1. **Given** a fresh clone, **When** the agent reads `GEMINI.md`, **Then** it finds the five
   core lessons — context-first architecture map, pattern reference integrity, agentic
   maintenance skills, continuous Bruno validation, IaC + cost gating (`GEMINI.md:8-30`) —
   plus the Director/Lead-Agent role split (`GEMINI.md:3-5`) and the 80/20 plan-first
   protocol (`GEMINI.md:34-36`).
2. **Given** any file addition or removal, **When** it is not logged in the Changelog table,
   **Then** `python scripts/verify_structure.py` exits 1 naming the missing files
   (`scripts/verify_structure.py:67-71`) — the map is machine-verified, not trusted
   (enforcement mechanics are spec 002's scope).
3. **Given** a design question already settled (e.g. "should scripts be PowerShell?"),
   **When** the agent consults `PATTERNS.md`, **Then** the decision is present as a grounded
   pattern (Cross-Platform Automation, `PATTERNS.md:6`) and is not re-litigated.

---

### User Story 2 - Spec-driven feature workflow (Priority: P2)

Any feature beyond a trivial fix runs the Spec Kit chain (specify → clarify → plan → tasks →
implement), producing durable artifacts under `specs/NNN-*/`, gated by a constitution
distillation that never overrides `GEMINI.md`.

**Why this priority**: Adopted in v0.0.3 as "the concrete implementation of the 80/20
planning phase" (`GEMINI.md:38-41`); it governs all future work but arrived after the
baseline shipped.

**Independent Test**: Run `/speckit-specify` (Claude Code) or `/speckit.specify` (Gemini CLI)
in-repo; a numbered `specs/NNN-*/spec.md` is produced from `.specify/templates/spec-template.md`.

**Acceptance Scenarios**:

1. **Given** the repo root, **When** listing Spec Kit integrations, **Then** ten Claude Code
   skills exist under `.claude/skills/speckit-*/` and ten Gemini CLI commands under
   `.gemini/commands/speckit.*.toml` (shipped in 999d30f, v0.0.3; mapped at
   `Project_Structure.md:20-21`).
2. **Given** a plan is produced, **When** its Constitution Check runs, **Then** it gates
   against `.specify/memory/constitution.md`, whose precedence header declares `GEMINI.md`
   supreme on conflict (`.specify/memory/constitution.md:3-5`) and which "never introduces
   rules of its own" (`GEMINI.md:41`; `.specify/memory/constitution.md:39`).

---

### User Story 3 - Fleet initiative proof-of-concept record (Priority: P3)

The Director (or any stakeholder) opens the self-contained `docs/` pages and sees the
methodology's architecture and its end-to-end validation: the three-tier fleet (methodology →
TradeFleet template → live contractor children) with real production numbers.

**Why this priority**: Evidence, not machinery — v0.0.2 is a docs-only release
(`Project_Structure.md:56`) whose value is proving "the initiative works" to justify further
investment in the framework.

**Independent Test**: Open `docs/tradefleet_initiative.html` in a browser; it renders
standalone (no build step, inline CSS) and names both live child URLs.

**Acceptance Scenarios**:

1. **Given** `docs/tradefleet_initiative.html`, **When** rendered, **Then** it documents the
   three tiers — Tier 1 methodology (this repo, `docs/tradefleet_initiative.html:116-121`),
   Tier 2 TradeFleet template with BOOTSTRAP.md + Fleet Registry (`:124-132`), Tier 3 live
   children EcoHomeBuild (ecohomebuild-afee5.web.app) and BullyBrickMI (bullybrickmi.web.app)
   (`:134-151`) — plus the proof numbers: 151/151 Bruno assertions per child (76 requests, 7
   collections), ~$0/mo per site (`:156-161`).
2. **Given** `docs/architecture_overview.html`, **When** rendered, **Then** it presents the
   framework's vibe-coding workflow as a one-page visual guide
   (`docs/architecture_overview.html:88-112`), and both `docs/` files are excluded from the
   structure gate by design (`Project_Structure.md:28`; `scripts/verify_structure.py:57`).

### Edge Cases

- **Constitution/distillation conflict**: resolved by explicit precedence — `GEMINI.md` (and
  `PATTERNS.md` for design decisions) wins (`.specify/memory/constitution.md:3-5`).
- **Bruno gate with no backend**: the gate is declared (`GEMINI.md:21-26`,
  `bruno/README.md:5-7`) but `bruno/` contains only its README — there is no application
  stack yet, so there is nothing to validate. Explicitly a declared-forward rule, not dead
  policy: consumer repos (TradeFleet children) enforce it for real
  (`docs/tradefleet_initiative.html:158`).
- **Terraform/cost gate with no infra**: same posture — process codified
  (`terraform/README.md:5-9`), directory holds only the README, cost posture $0/mo (both
  v0.0.2 and v0.0.3 changelog rows end with an explicit "cost review: $0, no infra" note,
  `Project_Structure.md:56-57`).
- **Bruno-gate exception path**: commits with failing Bruno validation require the exact
  owner acknowledgment string, verbatim in two places (`GEMINI.md:25`, `PATTERNS.md:9`).
- **Explicit non-goal**: `src/` is mapped as "Application Layer (TBD)"
  (`Project_Structure.md:23-27`) but does not exist on disk — this repo intentionally ships
  no application code; the application layers live in the consumer repos.

## Requirements

### Functional Requirements

- **FR-001**: The repo MUST carry a supreme constitution (`GEMINI.md`) codifying the five
  core lessons as non-negotiable operating procedures (`GEMINI.md:8-30`) and the
  Director/Lead-Agent role definition (`GEMINI.md:3-5`).
- **FR-002**: Every file addition/removal MUST be logged immediately in the
  `Project_Structure.md` Changelog table (`GEMINI.md:12`), which doubles as the release
  history — INITIALIZE → V0.0.1 BASELINE → V0.0.2 → V0.0.3 rows
  (`Project_Structure.md:35,51,56,57`).
- **FR-003**: `PATTERNS.md` MUST record only patterns that reflect the actual codebase, never
  aspirational designs (`GEMINI.md:16`), spanning architectural patterns, coding standards,
  and tooling conventions (`PATTERNS.md:5-21`).
- **FR-004**: Sessions MUST follow the 80/20 surgical-strike protocol — 80% read-only
  planning, one testable change per session (`GEMINI.md:34-36`).
- **FR-005**: Features beyond trivial fixes MUST run the Spec Kit chain with artifacts
  persisted in `specs/NNN-*/` (`GEMINI.md:38-41`; `PATTERNS.md:15`; `README.md:27-36`).
- **FR-006**: The Spec Kit constitution (`.specify/memory/constitution.md`) MUST be a
  distillation of `GEMINI.md` + `PATTERNS.md` with an explicit precedence header; on
  conflict `GEMINI.md` wins, and the distillation is regenerated when the source docs
  materially change (`GEMINI.md:41`; `.specify/memory/constitution.md:3-5,39`).
- **FR-007**: When replicating the framework to a fleet child, the child's distillation MUST
  be seeded from the CHILD's constitution, never copied from the parent (`PATTERNS.md:15`).
- **FR-008**: Cross-layer traceability MUST be maintained in `Function_Mapping.md` per its
  Add/Update/Delete/Audit rules (`Function_Mapping.md:9-13`); rows today are illustrative
  placeholders because no endpoints exist (`Function_Mapping.md:7`).
- **FR-009**: The Bruno and IaC/cost gates MUST be declared with their process rules
  (`bruno/README.md`, `terraform/README.md`; `GEMINI.md:21-30`) even while empty, so consumer
  repos inherit them on replication.
- **FR-010**: The fleet proof-of-concept record MUST be self-contained static HTML under
  `docs/`, excluded from the structure gate (`scripts/verify_structure.py:57`;
  `Project_Structure.md:50` MOVE row).

### Key Entities

- **Constitution (`GEMINI.md`)**: supreme operating procedure — five lessons, roles, 80/20
  protocol, Spec Kit workflow, communication guidelines.
- **Constitution distillation (`.specify/memory/constitution.md`)**: Spec Kit-facing five
  Core Principles, v1.0.0, ratified 2026-07-05 (`.specify/memory/constitution.md:41`).
- **Pattern registry (`PATTERNS.md`)**: 3 sections — Architectural Patterns (9 entries),
  Coding Standards, Tooling Conventions.
- **Architecture map (`Project_Structure.md`)**: Core Framework ("Director Layer") table +
  Application Layer table + Changelog table (the structure-gate source of truth and release
  ledger).
- **Traceability map (`Function_Mapping.md`)**: frontend-component → backend-endpoint →
  Bruno-contract table with maintenance rules.
- **Fleet PoC page (`docs/tradefleet_initiative.html`)**: three-tier diagram, replication
  modes 1/2, production numbers, lessons baked in.

## Success Criteria

- **SC-001**: A clean checkout passes the structure gate: `python scripts/verify_structure.py`
  exits 0 — re-verified in this retro run (see spec 002 for the gate itself).
- **SC-002**: Three releases are each traceable end-to-end: a Changelog-table row
  (`Project_Structure.md:51,56,57`), a `vX.Y.Z` (or baseline) commit, and a `--no-ff` merge
  to main (git: 2f7ca6c/839517e, 5faa89e→b001b24, 999d30f→5143308).
- **SC-003**: The methodology is proven downstream: two production contractor sites live at
  ~$0/mo each with 151/151 Bruno assertions green per child, replicated from one template
  (`docs/tradefleet_initiative.html:156-161`) — evidence recorded 2026-06-12.
- **SC-004**: Spec Kit is operational in both agent CLIs: 10 skills + 10 commands +
  templates + PowerShell helpers shipped in v0.0.3 at $0 cost (`Project_Structure.md:57`).

## Assumptions

- The Lead Agent honors the read-first rules (`GEMINI.md:10,14`); the only mechanical
  enforcement in this repo is the structure gate (spec 002) — pattern integrity and 80/20
  discipline are procedural.
- `docs/` pages are hand-maintained snapshots: the TradeFleet numbers (151/151, live URLs)
  were accurate as of 2026-06-12 and are not auto-synced with the downstream repos.
- Bruno/Terraform gates remain declared-only until this repo (or a template consuming it)
  gains an application stack; children enforce them today.
- Local-Ollama delegation for tedious tasks (`GEMINI.md:20`) is an operating instruction to
  the agent, not implemented tooling in this repo.
