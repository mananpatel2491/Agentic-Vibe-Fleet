# Implementation Plan: Maintenance & Hygiene Skills

**Branch**: `retro/002-maintenance-hygiene-skills` | **Date**: 2026-07-05 | **Spec**: [spec.md](./spec.md)

**Input**: As-built reconstruction from the 2026-05-19/20 changelog rows
(`Project_Structure.md:36-48`) and the v0.0.3 exclusion update (999d30f).

## Summary

Three Python skills under `scripts/`. `verify_structure.py` (stdlib-only) walks up to the
project root, parses the `Project_Structure.md` changelog's "Files Affected" cells into a
normalized set, `rglob`s the real tree minus a fixed exclusion list, and exits 1 naming any
unaccounted file. `optimize_changelog.py` sends the changelog table to Gemini for same-date
consolidation, then re-parses the result with the gate's own parser and refuses any write
that would lose a filename. `update_getting_started.py` regenerates
`GEMINI_Getting_Started.md` from a fixed prompt. Both LLM scripts share the conventions
hard-won during 2026-05-20 (nine changelog rows): `google-genai` SDK (migrated from
deprecated `google-generativeai`), `python-dotenv` with root-pinned `.env`, forced `v1` API
version, dynamic model listing, `argparse` + `--model` + `--dry-run`.

## Technical Context

**Language/Version**: Python 3, stdlib `argparse`/`pathlib`/`re`

**Primary Dependencies**: `google-genai`, `python-dotenv` (`requirements.txt:1-2`, unpinned)
— LLM scripts only; the gate imports nothing beyond stdlib

**Storage**: none — reads/writes tracked Markdown (`Project_Structure.md`,
`GEMINI_Getting_Started.md`)

**Testing**: no pytest suite; the gate *is* the test (exit-code contract), and `--dry-run`
serves as the manual safety harness for the writers (`PATTERNS.md:21`)

**Target Platform**: cross-platform (Windows primary) — the PowerShell predecessor was
deleted for this reason (`Project_Structure.md:37`; `PATTERNS.md:6`)

**Project Type**: dev tooling / repo hygiene

**Performance Goals**: N/A — sub-second local scans; LLM latency dominated by API

**Constraints**: $0 infra; only cost is Gemini API usage on the two LLM scripts

**Scale/Scope**: 3 scripts, ~330 lines total, one repo (plus fleet copies downstream)

## Constitution Check

Gated against `.specify/memory/constitution.md` (distillation of `GEMINI.md`, which is supreme).

- **I. Context-First Architecture Map — PASS.** This capability is the principle's
  enforcement arm: "no deferred bookkeeping" is machine-checked
  (`scripts/verify_structure.py:65-74`), and every script change was itself logged as a
  changelog row the same day (`Project_Structure.md:36-48`).
- **II. Pattern Reference Integrity — PASS.** The automation patterns were codified FROM this
  work, not aspirationally: the Python-only, dynamic-LLM, CLI-arguments, and dry-run patterns
  were added to `PATTERNS.md` in the same 2026-05-20 batch that implemented them
  (`Project_Structure.md:46`; `PATTERNS.md:6-8,18,21`).
- **III. Automated Maintenance via Agentic Skills — PASS.** This capability *is* Principle
  III: `scripts/` hygiene, Python/cross-platform/argparse/dry-run
  (`.specify/memory/constitution.md:15-16` describes exactly these scripts).
- **IV. Continuous API Validation — PASS (not applicable in substance).** No backend API is
  exposed by local Python scripts; the Bruno gate has no surface here. `bruno/` remains the
  declared gate for future API work (spec 001).
- **V. Infrastructure-as-Code & Cost Gating — PASS.** No infra touched; the only external
  spend is per-call Gemini usage, kept low by `--dry-run` previews and the `--model` bypass
  (no accidental interactive loops in CI).

**Operational constraints**: each 2026-05-20 refinement was a single testable change with its
own row (SDK migration, dotenv, root-pinning, v1 forcing, dynamic listing) — 80/20 compliant.

## Project Structure

### Documentation (this feature)

```text
specs/002-maintenance-hygiene-skills/
├── spec.md
├── plan.md              # this file
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md
└── contracts/
    └── structure-gate-contract.md
```

### Source Code (repository root)

```text
scripts/
├── README.md                    # skill inventory + preview→apply→verify workflow (v0.0.1)
├── verify_structure.py          # structure gate; stdlib-only                     (2026-05-19; Spec Kit exclusions v0.0.3)
├── optimize_changelog.py        # Gemini changelog consolidation + integrity check (2026-05-20)
└── update_getting_started.py    # Gemini onboarding-doc regenerator                (2026-05-20)
requirements.txt                 # google-genai, python-dotenv                      (2026-05-20)
GEMINI_Getting_Started.md        # generated output of update_getting_started.py    (2026-05-20)
.env                             # GOOGLE_API_KEY (git-ignored, .gitignore:25)
```

**Structure Decision**: all skills live flat in `scripts/` (the constitution's designated
hygiene surface, `GEMINI.md:18`); generated docs land at repo root where agents read them;
secrets stay in a root `.env` that both the gate (exclusion) and git (ignore) refuse to track.

## Complexity Tracking

No violations. Non-obvious choices: (1) the optimizer reuses the gate's parsing logic as a
duplicated function rather than a shared module (`get_logged_files` /
`get_logged_files_from_table`) — acceptable at 3 scripts, a refactor candidate if a fourth
parser appears; (2) `verify_structure.py` accepts `--model`/`--dry-run` it doesn't need,
purely for fleet CLI consistency (`scripts/verify_structure.py:78-79`, self-documented).
