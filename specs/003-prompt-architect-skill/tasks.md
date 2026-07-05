---
description: "As-built task record for the Prompt Architect session-bootstrap skill"
---

# Tasks: Prompt Architect Skill

As-built record — reconstructed 2026-07-05 from 7b13bde (initial), 2d7f6b1 (true dry-run),
af8a13d (interactive picker), changelog rows `Project_Structure.md:49,53,54`.
`[X]` = shipped; `[ ]` = genuinely open.

## Phase 1: Initial skill (US1)

- [X] T001 [US1] Implement `scripts/generate_bootstrap_prompt.py` — intent → Gemini →
  archived bootstrap prompt, with governance-doc context ingestion
  (`scripts/generate_bootstrap_prompt.py:40-49`) (7b13bde, 2026-05-20)
- [X] T002 [US1] Encode the Prompt-Architect system prompt: standing gate instructions,
  feature reuse / STATION CHECK protocol, bug hypothesis protocol (`:64-84`) (7b13bde)
- [X] T003 [US1] Archive outputs to timestamped `bootstrap_prompts/` and map the dir at
  directory level, gate-excluded (`Project_Structure.md:16,49`;
  `scripts/verify_structure.py:57`) (7b13bde)
- [X] T004 [US1] Document as step 1 of the vibe-coding workflow (`README.md:9-14`) and
  request its coverage in onboarding (`scripts/update_getting_started.py:66`) (v0.0.1)

## Phase 2: Dry-run hardening (US2)

- [X] T005 [US2] Move `--dry-run` to a true pre-network short-circuit with request preview
  and resolved-path echo (`scripts/generate_bootstrap_prompt.py:93-103`)
  (2d7f6b1, fix/dry-run-bootstrap-prompt, merged 327e8ed, 2026-06-09)
- [X] T006 [US2] Add masked `GOOGLE_API_KEY loaded` confirmation + clearer key-not-found
  message (`:55-60`) (2d7f6b1)

## Phase 3: Model-picker hardening (US3)

- [X] T007 [US3] Interactive numbered model picker with `[Enter for default 0]`, preserving
  `--model` bypass (`scripts/generate_bootstrap_prompt.py:27-38`)
  (af8a13d, fix/interactive-model-select, merged dae87c6, 2026-06-09)
- [X] T008 [US3] Non-interactive safety: `EOFError` → default without blocking; invalid
  index → default (`:33-38`) (af8a13d)

## Open follow-ups (genuinely pending)

- [X] T009 Key check precedes the dry-run short-circuit
  (`scripts/generate_bootstrap_prompt.py:55-60` vs `:95`) — a fully offline machine with no
  `.env` cannot even preview; consider allowing keyless dry-runs (v0.0.5 — dry-run
  short-circuit moved BEFORE the GOOGLE_API_KEY check; keyless `--dry-run` verified)
- [X] T010 API errors print and exit 0 (`:122-123`) — nonzero exit would serve CI better
  (same class as spec 002 T018) (v0.0.5 — API/listing/key failures now `sys.exit(1)`)
- [X] T011 Back-port the EOFError-hardened picker to `update_getting_started.py:34` (three
  `select_model` variants have diverged across `scripts/`) (v0.0.5 — backported; all
  pickers now dynamic-only with EOF-safe default)
- [X] T012 `scripts/README.md:16-20` inventory omits this script entirely — add a row
  (shared with spec 002 T015) (v0.0.5 — row added with usage)
- [ ] T013 Missing governance docs are skipped silently during context assembly (`:44-48`) —
  consider a warning so degraded prompts are visible
- [ ] T014 Decide the long-term relationship with Spec Kit (spec 001): keep as session
  on-ramp, or fold bootstrap generation into `/speckit-specify` (no decision on file)
