# Data Model: Framework Governance & Fleet Initiative

No database, no application storage. The "data" of this capability is structured Markdown
whose shapes are contracts consumed by agents and by the structure gate (spec 002).

## Architecture map tables (`Project_Structure.md`)

- **Core Framework table** (`Project_Structure.md:7-21`): `| Path | Purpose |` rows for the
  Director layer — governance docs, `scripts/`, `bruno/`, `bootstrap_prompts/`, `terraform/`,
  and the Spec Kit payload dirs (`.specify/`, `specs/`, `.claude/`, `.gemini/`).
- **Application Layer table** (`Project_Structure.md:23-29`): `src/` (TBD — not on disk),
  `docs/architecture_overview.html`, `Function_Mapping.md`.
- **Changelog table** (`Project_Structure.md:33-57`): `| Date | Action | Files Affected |
  Summary |`. Column 3 ("Files Affected") is machine-parsed by the gate; Action vocabulary in
  use: INITIALIZE, ADD, DELETE, UPDATE, FIX, MOVE, BASELINE. Release rows carry bolded
  version markers (**V0.0.1**/**V0.0.2**/**V0.0.3**) and, post-baseline, an explicit cost
  note. Full parse semantics: spec 002 `data-model.md`.

## Constitution shapes

- **`GEMINI.md`** (47 lines): role definitions (`:3-5`) → Five Core Lessons (`:8-30`) →
  Operational Protocols: 80/20 (`:34-36`), Spec-Driven Feature Workflow (`:38-41`),
  Communication Guidelines (`:43-46`).
- **`.specify/memory/constitution.md`** (41 lines): precedence header (`:3-5`) → five Core
  Principles I–V mirroring the five lessons (`:9-22`) → Operational Constraints (`:24-29`) →
  Development Workflow (`:31-35`) → Governance + version stamp
  `Version 1.0.0 | Ratified 2026-07-05` (`:37-41`).

## Pattern registry shape (`PATTERNS.md`)

Three numbered sections: `1. Architectural Patterns` (9 bold-titled bullets,
`PATTERNS.md:5-15`), `2. Coding Standards` (`:17-18`), `3. Tooling Conventions` (`:20-21`).
Convention: each entry is a **named pattern** + rule sentence(s); entries must reflect the
actual codebase (`GEMINI.md:16`).

## Traceability map shape (`Function_Mapping.md`)

`| Frontend Component | Action | Backend Endpoint / Function | Documentation/Contract |`
(`Function_Mapping.md:5-7`; single illustrative row today) + four maintenance rules
Add/Update/Delete/Audit (`:9-13`).

## Config/env keys

None read by the governance texts themselves. (`GOOGLE_API_KEY` belongs to the scripts —
specs 002/003.)

## docs/ pages

Self-contained HTML with inline CSS, zero external assets:
`docs/architecture_overview.html` (141 lines) and `docs/tradefleet_initiative.html`
(207 lines; three-tier diagram `:114-152`, stats grid `:154-168`, replication modes
`:170-182`). Not parsed by any tool; excluded from the gate.
