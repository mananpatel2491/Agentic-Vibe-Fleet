# Implementation Plan: Prompt Architect Skill

**Branch**: `retro/003-prompt-architect-skill` | **Date**: 2026-07-05 | **Spec**: [spec.md](./spec.md)

**Input**: As-built reconstruction from commit 7b13bde (initial skill), 2d7f6b1
(fix/dry-run-bootstrap-prompt), af8a13d (fix/interactive-model-select), and changelog rows
`Project_Structure.md:49,53,54`.

## Summary

Single Python script `scripts/generate_bootstrap_prompt.py`: load `.env` from the resolved
repo root → verify + mask-echo `GOOGLE_API_KEY` → concatenate the three governance docs into
a context block → if `--dry-run`, print model/path/request preview and return before any
client exists → else construct a `google-genai` v1 client, resolve the model
(override → interactive picker → default), call `generate_content` with a fixed
Prompt-Architect system prompt (standing gate instructions, feature-reuse and bug-hypothesis
protocols), and write the result to `bootstrap_prompts/prompt_<timestamp>.md`.

## Technical Context

**Language/Version**: Python 3, stdlib `argparse`/`pathlib`/`datetime`

**Primary Dependencies**: `google-genai`, `python-dotenv` (`requirements.txt:1-2`)

**Storage**: filesystem archive `bootstrap_prompts/` (git-excluded from the structure gate,
`scripts/verify_structure.py:57`; not present until first live run — `mkdir(exist_ok=True)`
at `scripts/generate_bootstrap_prompt.py:116`)

**Testing**: no automated tests; `--dry-run` is the manual harness (prints the exact request
that would be sent)

**Target Platform**: cross-platform CLI (`PATTERNS.md:6`)

**Project Type**: dev tooling / session planning

**Performance Goals**: N/A — one API call per invocation

**Constraints**: $0 infra; API spend only on live runs (dry-run guaranteed free by
construction)

**Scale/Scope**: 1 script, 131 lines; one prompt artifact per session start

## Constitution Check

Gated against `.specify/memory/constitution.md` (distillation of `GEMINI.md`, which is supreme).

- **I. Context-First Architecture Map — PASS.** The skill mechanizes the principle for new
  sessions: `Project_Structure.md` is force-fed into every generated plan
  (`scripts/generate_bootstrap_prompt.py:43`), and all three of its own changes were logged
  same-day (`Project_Structure.md:49,53,54`).
- **II. Pattern Reference Integrity — PASS.** `PATTERNS.md` is part of the generation
  context, so generated plans inherit the registry; the skill itself follows the registry's
  automation patterns (argparse/dry-run/model-bypass, `PATTERNS.md:8,18,21`).
- **III. Automated Maintenance via Agentic Skills — PASS.** Lives in `scripts/`, Python,
  cross-platform, CI-safe (EOFError fallback keeps it non-blocking when piped,
  `scripts/generate_bootstrap_prompt.py:33-35`).
- **IV. Continuous API Validation — PASS (propagated, not applicable locally).** The script
  exposes no API; instead it *propagates* the Bruno gate into every bootstrap prompt's
  standing instructions verbatim (`scripts/generate_bootstrap_prompt.py:70-71`).
- **V. Infrastructure-as-Code & Cost Gating — PASS.** No infra; the dry-run fix is itself a
  cost-gating measure (guaranteed-zero-spend preview path,
  `scripts/generate_bootstrap_prompt.py:93-103`).

**Operational constraints**: both 2026-06-09 fixes were one-testable-change branches
(`fix/dry-run-bootstrap-prompt`, `fix/interactive-model-select`) merged separately — 80/20
compliant; note they used `fix/*` branch names rather than `vX.Y.Z` (pre-dating the strict
version-branch convention now distilled at `.specify/memory/constitution.md:33`).

## Project Structure

### Documentation (this feature)

```text
specs/003-prompt-architect-skill/
├── spec.md
├── plan.md              # this file
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md
└── contracts/
    └── cli-contract.md
```

### Source Code (repository root)

```text
scripts/generate_bootstrap_prompt.py   # the skill                       (7b13bde; hardened 2d7f6b1 + af8a13d)
bootstrap_prompts/                     # plan archive (runtime-created)  (mapped Project_Structure.md:16)
requirements.txt                       # shared deps                     (spec 002)
.env                                   # GOOGLE_API_KEY                  (git-ignored)
```

**Structure Decision**: one self-contained script in the constitution's `scripts/` skill
surface; generated artifacts quarantined in `bootstrap_prompts/`, deliberately outside both
the structure gate and (in practice) version control so plan archives never pollute the
file-accounting ledger.

## Complexity Tracking

No violations. One duplication note: `select_model` exists in three variants across the
scripts (this one is the only EOFError-hardened, prompt-defaulting version,
`scripts/generate_bootstrap_prompt.py:13-38`; the interactive-picker fix was NOT back-ported
to `update_getting_started.py:34`) — recorded as drift in tasks.md, acceptable at current
scale.
