---
description: "As-built task record for the scripts/ maintenance and hygiene skills"
---

# Tasks: Maintenance & Hygiene Skills

As-built record — reconstructed 2026-07-05 from the 2026-05-19/20 changelog rows
(`Project_Structure.md:36-48`) and v0.0.3 (999d30f). `[X]` = shipped; `[ ]` = genuinely open.

## Phase 1: Structure gate (US1)

- [X] T001 [US1] Implement `scripts/verify_structure.py` — root discovery, changelog parse,
  tree diff, exit-code contract (2026-05-19, v0.0.1 baseline)
- [X] T002 [US1] Delete `scripts/verify-structure.ps1` in favor of cross-platform Python
  (`Project_Structure.md:37`) (2026-05-19)
- [X] T003 [US1] Exclude `docs/` from the gate when `architecture_overview.html` moved
  (`Project_Structure.md:50`; commit 839517e) (v0.0.1)
- [X] T004 [US1] Extend exclusions for the Spec Kit payload dirs `.specify/ .claude/ .gemini/
  specs/` (`scripts/verify_structure.py:59-62`) (v0.0.3, 999d30f)

## Phase 2: LLM script platform conventions (US2/US3 shared)

- [X] T005 Add `requirements.txt` (`google-genai`, `python-dotenv`)
  (`Project_Structure.md:39-40`) (2026-05-20)
- [X] T006 Migrate from deprecated `google-generativeai` to `google-genai` SDK
  (`Project_Structure.md:40`) (2026-05-20)
- [X] T007 Add `python-dotenv` key loading, then pin `.env` lookup to the absolute project
  root (`Project_Structure.md:41-42`) (2026-05-20)
- [X] T008 Resolve v1beta 404s: model switch, then force `v1` API endpoint
  (`Project_Structure.md:43-44`; `scripts/update_getting_started.py:54-56`) (2026-05-20)
- [X] T009 Implement dynamic model selection via `client.models.list()`
  (`Project_Structure.md:45`) (2026-05-20)
- [X] T010 Codify the conventions in `PATTERNS.md` (Python-only, dynamic LLM, CLI args,
  dry-run) in the same batch (`Project_Structure.md:46`; `PATTERNS.md:6-8,18,21`) (2026-05-20)

## Phase 3: Changelog optimizer (US2)

- [X] T011 [US2] Implement `scripts/optimize_changelog.py` — section split, consolidation
  prompt, fence sanitization (`Project_Structure.md:47`) (2026-05-20)
- [X] T012 [US2] Integrity check: refuse writes that would drop accounted files
  (`scripts/optimize_changelog.py:111-119`) (2026-05-20)

## Phase 4: Onboarding refresher (US3)

- [X] T013 [US3] Implement `scripts/update_getting_started.py` + generate
  `GEMINI_Getting_Started.md` (`Project_Structure.md:38`) (2026-05-20)
- [X] T014 [US3] Document the preview→apply→verify workflow + inventory in
  `scripts/README.md` (v0.0.1)

## Open follow-ups (genuinely pending)

- [X] T015 `scripts/README.md:16-20` inventory lists only 2 of the 4 scripts — add
  `generate_bootstrap_prompt.py` (spec 003) and `update_getting_started.py` (v0.0.5 — all
  4 scripts documented with usage)
- [X] T016 Fallback model IDs are stale-risk hardcodes and inconsistently prefixed
  (`scripts/update_getting_started.py:28` bare vs `:39` `models/`-prefixed) — refresh or
  derive the fallback (v0.0.5 — static fallbacks REMOVED from all three LLM scripts;
  dynamic `client.models.list()` is now the only path, listing failure exits non-zero)
- [X] T017 Dead code in `scripts/verify_structure.py`: unused `import re` (`:2`) and unused
  `dry_run` parameter inside `verify()` (`:41`) (v0.0.5 — both removed; `--dry-run` CLI
  flag still prints its read-only notice)
- [X] T018 LLM scripts return silently (exit 0) on API errors
  (`scripts/optimize_changelog.py:133-134`) — consider nonzero exits for CI use, per the
  Automation-First CLI pattern's CRON/CI intent (`PATTERNS.md:8`) (v0.0.5 — API/listing/
  key/integrity failures now `sys.exit(1)` with clear messages in all three LLM scripts)
- [X] T019 `.gitignore` is a Dynamics 365/AL template plus `.env` (`.gitignore:1-25`); it
  ignores neither `__pycache__/` nor `bootstrap_prompts/` — replace with a Python-appropriate
  ignore set (v0.0.5 — `__pycache__/` and `bootstrap_prompts/` added; existing entries
  incl. `.env` kept)
- [X] T020 `update_getting_started.py:34` `input()` has no explicit non-interactive branch
  (EOFError falls into the broad except with a misleading warning) — mirror the EOFError
  handling from `generate_bootstrap_prompt.py:33-35` (v0.0.5 — EOF-safe picker backported:
  non-interactive stdin → default index 0, no misleading warning)
