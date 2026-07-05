---
description: "As-built task record for the AVF governance layer, fleet PoC docs, and Spec Kit adoption"
---

# Tasks: Framework Governance & Fleet Initiative

As-built record — reconstructed 2026-07-05 from v0.0.1 (5c7886b…2f7ca6c, 839517e), v0.0.2
(5faa89e), v0.0.3 (999d30f). `[X]` = shipped, with the shipping release; `[ ]` = genuinely open.

## Phase 1: Director-layer scaffold (US1)

- [X] T001 [US1] Author `GEMINI.md` constitution — roles, five core lessons, 80/20 protocol,
  communication guidelines (v0.0.1, 2026-05-19)
- [X] T002 [US1] Author `PATTERNS.md` pattern registry, grown through the 2026-05-20 script
  work (automation patterns, Bruno/traceability patterns, hardening/readiness/migration
  advisories — `Project_Structure.md:46,48,52`) (v0.0.1)
- [X] T003 [US1] Author `Project_Structure.md` — Core Framework + Application Layer tables +
  Changelog table (v0.0.1)
- [X] T004 [P] [US1] Author `Function_Mapping.md` traceability map + maintenance rules (v0.0.1)
- [X] T005 [P] [US1] Seed declared gates: `bruno/README.md`, `terraform/README.md` (v0.0.1)
- [X] T006 [P] [US1] Add `README.md`, `LICENSE` (MIT), `.gitignore` (v0.0.1)
- [X] T007 [US1] Add `architecture_overview.html`, then MOVE to `docs/` and exclude `docs/`
  from hygiene checks (`Project_Structure.md:50`; commit 839517e) (v0.0.1)
- [X] T008 [US1] Declare the baseline: BASELINE changelog row "Director Layer operational.
  Ready for autonomous vibe coding and replication." (`Project_Structure.md:51`; commit
  2f7ca6c) (v0.0.1)

## Phase 2: Fleet initiative proof of concept (US3)

- [X] T009 [US3] Author `docs/tradefleet_initiative.html` — three-tier fleet diagram, live
  child URLs, 151/151 Bruno stats, Mode 1/Mode 2 replication, lessons baked in (v0.0.2,
  5faa89e, 2026-06-12)
- [X] T010 [US3] Log the docs-only release with explicit $0 cost review
  (`Project_Structure.md:56`); merge `--no-ff` to main (b001b24) (v0.0.2)

## Phase 3: Spec Kit adoption (US2)

- [X] T011 [US2] Initialize Specify CLI v0.12.5 payload: `.specify/` (templates ×5,
  PowerShell helpers, workflows registry, memory) (v0.0.3, 999d30f, 2026-07-05)
- [X] T012 [P] [US2] Install 10 Claude Code skills `.claude/skills/speckit-*/` and 10 Gemini
  CLI commands `.gemini/commands/speckit.*.toml` (v0.0.3)
- [X] T013 [US2] Seed `.specify/memory/constitution.md` as a GEMINI.md+PATTERNS.md
  distillation with explicit precedence header, v1.0.0 ratified 2026-07-05 (v0.0.3)
- [X] T014 [US2] Codify the Spec-Driven Feature Workflow in `GEMINI.md:38-41`,
  `PATTERNS.md:15`, `README.md:27-36`; map rows `Project_Structure.md:18-21`; extend
  `verify_structure.py` exclusions for the payload dirs (`scripts/verify_structure.py:59-62`)
  (v0.0.3)

## Open follow-ups (genuinely pending)

- [ ] T015 `src/` is mapped as Application Layer TBD (`Project_Structure.md:27`) but absent
  on disk — populate or re-scope the table when/if this repo gains application code
- [ ] T016 `Function_Mapping.md:7` still holds the illustrative placeholder row; replace with
  real rows when the first endpoint exists, per its own maintenance rules
- [ ] T017 Populate `bruno/collections/` + the visual HTML flow (`bruno/README.md:9-11`
  names subdirs that don't exist yet) when the first backend API ships
- [ ] T018 Populate `terraform/environments|modules/` (`terraform/README.md:11-13`, same
  gap) when the first infra-dependent feature ships
- [ ] T019 Regenerate `.specify/memory/constitution.md` next time `GEMINI.md`/`PATTERNS.md`
  materially change (`GEMINI.md:41`)
- [ ] T020 `GEMINI.md:1-30` carries residual citation artifacts from its source conversation
  ("[790, 811, conversation history]") — cosmetic cleanup candidate for a future docs pass
