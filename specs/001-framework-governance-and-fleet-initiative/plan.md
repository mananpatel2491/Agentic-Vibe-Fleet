# Implementation Plan: Framework Governance & Fleet Initiative

**Branch**: `retro/001-framework-governance-and-fleet-initiative` | **Date**: 2026-07-05 | **Spec**: [spec.md](./spec.md)

**Input**: As-built reconstruction from v0.0.1 (5c7886b…2f7ca6c, 839517e), v0.0.2 (5faa89e), v0.0.3 (999d30f).

## Summary

v0.0.1 established the Director layer as a reusable template baseline: `GEMINI.md`
constitution (five lessons), `PATTERNS.md` registry, `Project_Structure.md` map with a
machine-verifiable Changelog table, `Function_Mapping.md`, declared Bruno/Terraform gate
directories (README-only), `docs/architecture_overview.html`, and the `scripts/` skills
(specs 002/003). v0.0.2 added `docs/tradefleet_initiative.html` — the docs-only
proof-of-concept record that the methodology shipped a real three-tier fleet. v0.0.3 layered
GitHub Spec Kit on top (Specify CLI v0.12.5): `.specify/` toolkit, `.claude/skills/speckit-*`
and `.gemini/commands/speckit.*.toml` dual integrations, and the constitution distillation at
`.specify/memory/constitution.md` with explicit `GEMINI.md` precedence.

## Technical Context

**Language/Version**: Markdown governance docs + self-contained static HTML (`docs/`, inline
CSS, no build step); no application code in this capability

**Primary Dependencies**: none for the governance texts (Python scripts are specs 002/003;
`requirements.txt:1-2` serves them)

**Storage**: none — all governance state lives in tracked Markdown/HTML files

**Testing**: `scripts/verify_structure.py` gates the map↔tree consistency (spec 002); the
governance texts themselves are Director-reviewed

**Target Platform**: any agent CLI (Gemini CLI + Claude Code both integrated since v0.0.3)
and any browser for `docs/`

**Project Type**: methodology / repo governance (Tier 1 of the fleet)

**Performance Goals**: N/A — offline documents

**Constraints**: $0/mo — v0.0.2 and v0.0.3 changelog rows each carry an explicit "cost
review: $0, no infra" note (`Project_Structure.md:56-57`)

**Scale/Scope**: 1 methodology repo governing a fleet of consumer repos (TradeFleet template
+ 2 live children as of 2026-06-12; more adopters since)

## Constitution Check

Gated against `.specify/memory/constitution.md` (distillation of `GEMINI.md`, which is supreme).

- **I. Context-First Architecture Map — PASS.** This capability *implements* the principle:
  the Core Framework / Application Layer tables (`Project_Structure.md:7-29`) plus the
  Changelog table give every session its map, and each of the three releases logged its rows
  immediately (`Project_Structure.md:35-57`) — no deferred bookkeeping.
- **II. Pattern Reference Integrity — PASS.** `PATTERNS.md` was seeded in v0.0.1 and grew
  only alongside shipped behavior (e.g. the Spec Kit workflow bullet, `PATTERNS.md:15`,
  landed with v0.0.3; the automation patterns, `PATTERNS.md:6-8`, landed with the 2026-05-20
  script work per `Project_Structure.md:46`).
- **III. Automated Maintenance via Agentic Skills — PASS (delegated).** The principle is
  codified here (`GEMINI.md:17-20`); the skills themselves are specs 002/003. No hand-edit
  was used where a script existed (the changelog rows for script fixes were logged, not
  regenerated).
- **IV. Continuous API Validation — PASS (declared, gate seeded).** The Bruno rules and the
  exact exception string are codified (`GEMINI.md:21-26`, `PATTERNS.md:9`,
  `bruno/README.md:5-7`); `bruno/` holds only its README because this repo exposes no API.
  The gate is enforced for real downstream (151/151 assertions per child,
  `docs/tradefleet_initiative.html:158`).
- **V. Infrastructure-as-Code & Cost Gating — PASS.** The cost-gated deployment process is
  codified (`GEMINI.md:27-30`, `terraform/README.md:5-9`); no infra-dependent feature has
  shipped here, and both post-baseline releases recorded explicit $0 cost reviews
  (`Project_Structure.md:56-57`).

**Operational constraints**: all three releases were single-concern (baseline / one docs page
/ one tooling adoption) per the 80/20 one-testable-change rule; version-branch flow with
`--no-ff` merges is visible in git history (b001b24, 5143308).

## Project Structure

### Documentation (this feature)

```text
specs/001-framework-governance-and-fleet-initiative/
├── spec.md
├── plan.md              # this file
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md
└── contracts/
    └── governance-contract.md
```

### Source Code (repository root)

```text
GEMINI.md                            # constitution of record             (v0.0.1; Spec Kit section v0.0.3)
PATTERNS.md                          # pattern registry                   (v0.0.1; Spec Kit bullet v0.0.3)
Project_Structure.md                 # architecture map + changelog       (v0.0.1; rows every release)
Function_Mapping.md                  # cross-layer traceability map       (v0.0.1)
README.md                            # onboarding + workflow              (v0.0.1; Spec Kit section v0.0.3)
LICENSE                              # MIT                                (v0.0.1)
docs/architecture_overview.html      # visual 1-pager                     (v0.0.1, moved to docs/ pre-baseline)
docs/tradefleet_initiative.html      # fleet PoC record                   (v0.0.2)
bruno/README.md                      # API-validation gate (declared)     (v0.0.1)
terraform/README.md                  # IaC/cost gate (declared)           (v0.0.1)
.specify/                            # Spec Kit toolkit + templates + constitution distillation (v0.0.3)
.claude/skills/speckit-*/            # 10 Claude Code skills              (v0.0.3)
.gemini/commands/speckit.*.toml      # 10 Gemini CLI commands             (v0.0.3)
```

**Structure Decision**: governance lives at repo root as flat Markdown so any agent reads it
on session start; visual evidence is segregated into `docs/` (excluded from the structure
gate, `scripts/verify_structure.py:57`); the Spec Kit payload is mapped at directory level
(`Project_Structure.md:18-21`) and likewise excluded (`scripts/verify_structure.py:60-62`)
rather than logged file-by-file.

## Complexity Tracking

No violations. Two non-obvious choices: (1) whole-directory gate exclusions for `docs/` and
the Spec Kit payload instead of row-by-row logging — justified by the in-code comment
(`scripts/verify_structure.py:59-61`) and the directory-level map rows; (2) keeping empty
Bruno/Terraform gates as README-only declarations rather than deleting them — they are the
template surface consumer repos inherit.
