# Research: Framework Governance & Fleet Initiative

As-built record — decisions reconstructed 2026-07-05 from v0.0.1–v0.0.3 history, `PATTERNS.md`,
and the `Project_Structure.md` changelog.

## Decision 1 — Constitution-first, not tooling-first

**Choice**: the framework's core artifact is a prose constitution (`GEMINI.md`) codifying
five lessons as non-negotiable procedure, read at the start of every session, with tooling
(scripts, gates) only as enforcement for the subset that can be mechanized.
**Why**: the failure mode being engineered against is context rot and re-litigated decisions
across agent sessions (`GEMINI.md:1,15`); the downstream PoC page records the retrospective
verdict — "Constitution-first beats tooling-first … Drift never accumulated"
(`docs/tradefleet_initiative.html:187-188`).
**Rejected**: encoding all governance in CI/tooling — most of the five lessons (pattern
integrity, 80/20 discipline, cost review) are judgment rules a gate cannot express.

## Decision 2 — The changelog table doubles as release history

**Choice**: `Project_Structure.md`'s Changelog table is both the file-accounting ledger
(parsed by the gate) and the human release narrative — BASELINE/V0.0.2/V0.0.3 rows carry the
release summaries (`Project_Structure.md:51,56,57`); there is no separate CHANGELOG.md.
**Why**: one docs-of-record surface; the gate forces the table to stay current, so the
release history rides along for free.
**Rejected**: a separate Keep-a-Changelog file (used by some consumer repos, e.g.
VoiceBridge) — redundant here where every change is a docs/tooling change.

## Decision 3 — Declared-but-empty Bruno and Terraform gates

**Choice**: ship `bruno/` and `terraform/` as README-only process declarations
(`bruno/README.md`, `terraform/README.md`) with no collections or configs.
**Why**: this repo is a template/methodology with no application stack; the gates must exist
as inheritable surface so replicated repos start with the rules in place. The v0.0.2 PoC
shows the inheritance worked: children run 76-request/151-assertion Bruno suites
(`docs/tradefleet_initiative.html:158`).
**Rejected**: deleting the empty dirs until needed — would break the template contract;
adding toy collections — would violate Pattern Reference Integrity (nothing real to test).

## Decision 4 — Fleet proof recorded as self-contained static HTML (v0.0.2)

**Choice**: document the TradeFleet initiative as one dependency-free HTML page
(`docs/tradefleet_initiative.html`, inline CSS, renders from the filesystem), and exclude
`docs/` from the structure gate (`scripts/verify_structure.py:57`).
**Why**: the audience includes non-developers (contractors, stakeholders); a browser-openable
single file needs no toolchain, and the gate exclusion keeps presentation assets from
polluting the file-accounting ledger (exclusion decision logged 2026-05-20,
`Project_Structure.md:50`).
**Rejected**: Markdown-only (weak for a diagram-heavy pitch); a docs site generator
(dependency + build step for two pages).

## Decision 5 — GitHub Spec Kit as the 80/20 implementation, with a subordinate distillation (v0.0.3)

**Choice**: adopt Specify CLI v0.12.5 with dual agent integrations (10 Claude Code skills,
10 Gemini CLI commands) and seed `.specify/memory/constitution.md` as a *distillation* of
`GEMINI.md` + `PATTERNS.md` that "never introduces rules of its own; on conflict, GEMINI.md
wins" (`GEMINI.md:41`; `.specify/memory/constitution.md:3-5`).
**Why**: the 80/20 planning phase previously produced output that died with the session (or
lived only as `bootstrap_prompts/` snapshots, spec 003); Spec Kit makes the 80% durable in
`specs/NNN-*/` (`GEMINI.md:38-40`). The distillation preserves single-source-of-truth: two
constitutions with equal authority would themselves be GIST debt.
**Rejected**: promoting the Spec Kit constitution to peer authority; single-CLI integration
(the fleet operates through both Gemini CLI and Claude Code, `README.md:30`).

## Decision 6 — Fleet replication seeds the CHILD's distillation, not a copy (v0.0.3)

**Choice**: when the framework replicates to a fleet child, the child's
`.specify/memory/constitution.md` is distilled from the child's own constitution
(`PATTERNS.md:15`).
**Why**: children deliberately diverge (naming, entities, domain rules —
`docs/tradefleet_initiative.html:179-181`); a copied parent distillation would gate the child
against the wrong constitution.
**Rejected**: verbatim copy on clone.
