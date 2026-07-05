# Feature Specification: Maintenance & Hygiene Skills

**Feature Branch**: `retro/002-maintenance-hygiene-skills` (as-built record — no branch created)

**Created**: 2026-07-05

**Status**: Shipped (v0.0.1; verify-gate exclusions extended in v0.0.3)

**Input**: retro-spec conversion of the 2026-05-19/20 `scripts/` work (changelog rows `Project_Structure.md:36-48`) and the v0.0.3 gate-exclusion update (999d30f)

## Why

The constitution's Lesson 1 ("log every file immediately") and Lesson 3 ("automated
maintenance via agentic skills", `GEMINI.md:9-20`) are only credible if a machine can catch
drift and an agent can run the upkeep. This capability is the `scripts/` skill set that does
both: a credential-free **structure gate** (`verify_structure.py`) that fails when the file
tree and the `Project_Structure.md` changelog disagree, an LLM-powered **changelog
consolidator** (`optimize_changelog.py`) that compacts the ledger without losing a single
accounted file, and an LLM-powered **onboarding refresher** (`update_getting_started.py`)
that regenerates `GEMINI_Getting_Started.md`. All three embody the registry's automation
patterns: Python-only, `argparse`, `--dry-run`, `--model` bypass, dynamic model selection
(`PATTERNS.md:6-8,18,21`).

## User Scenarios & Testing

### User Story 1 - Catch unlogged files before they become drift (Priority: P1)

After any change, the agent (or a human) runs the structure gate; if a file exists on disk
but is absent from the changelog's "Files Affected" history, the gate fails and names it.

**Why this priority**: This is the only *mechanically enforced* rule in the methodology repo —
every other skill and doc depends on the map staying truthful.

**Independent Test**: `python scripts/verify_structure.py` on a clean checkout exits 0 with
`SUCCESS: All files are accounted for in the changelog.` (`scripts/verify_structure.py:73-74`);
add a stray root file and it exits 1 listing it.

**Acceptance Scenarios**:

1. **Given** the repo root, **When** the gate runs, **Then** it locates the root by walking
   up to the nearest `Project_Structure.md` (`scripts/verify_structure.py:6-12`), parses
   every changelog row's "Files Affected" cell (column index 3, split on commas, backticks
   stripped, POSIX-normalized — `scripts/verify_structure.py:26-37`), and compares against an
   `rglob` of the actual tree.
2. **Given** exclusion-listed paths — `.git/`, `__pycache__/`, `.env`, `bootstrap_prompts/`,
   `docs/`, `Project_Structure.md` itself (`scripts/verify_structure.py:57`) and the Spec Kit
   payload dirs `.specify/ .claude/ .gemini/ specs/` (`scripts/verify_structure.py:59-62`,
   added v0.0.3) — **When** files exist there, **Then** the gate ignores them by design.
3. **Given** unlogged files, **When** the gate runs, **Then** it prints them in red and exits
   1 (`scripts/verify_structure.py:67-71`), blocking the post-commit hygiene step mandated by
   the bootstrap standing instructions (`scripts/generate_bootstrap_prompt.py:69`).

---

### User Story 2 - Consolidate a noisy changelog without losing accountability (Priority: P2)

As the changelog accumulates micro-rows (nine rows landed on 2026-05-20 alone,
`Project_Structure.md:38-50`), the agent asks Gemini to merge same-date rows — but the merge
is rejected if even one filename would vanish from the ledger.

**Why this priority**: Keeps the P1 gate's source of truth readable long-term; valuable but
not load-bearing (the gate works on a noisy table too).

**Independent Test**: `python scripts/optimize_changelog.py --dry-run` prints the proposed
consolidated table without writing (`scripts/optimize_changelog.py:124-127`).

**Acceptance Scenarios**:

1. **Given** the current table, **When** the LLM returns a consolidated version, **Then** the
   script re-parses both tables with the same parser the gate uses and refuses to write if
   `original_files - new_files` is non-empty, printing the files that would be lost and the
   warning that it "would break verify_structure.py"
   (`scripts/optimize_changelog.py:111-119`).
2. **Given** LLM output wrapped in markdown fences, **When** sanitizing, **Then** the fences
   are stripped before validation (`scripts/optimize_changelog.py:108-109`).
3. **Given** no `## Changelog` heading, **Then** the script aborts with an error instead of
   corrupting the file (`scripts/optimize_changelog.py:79-86`).

---

### User Story 3 - Regenerate the onboarding guide on demand (Priority: P3)

The agent refreshes `GEMINI_Getting_Started.md` by querying Gemini for current Code Assist
guidance (agent mode, preview models, the fleet's maintenance skills, the Prompt Architect
workflow) and overwriting the doc with a stamped footer.

**Why this priority**: Convenience documentation; nothing gates on it, and its content is
LLM-authored prose rather than repo ground truth.

**Independent Test**: `python scripts/update_getting_started.py --dry-run` previews the full
output without writing (`scripts/update_getting_started.py:81-84`).

**Acceptance Scenarios**:

1. **Given** a valid `GOOGLE_API_KEY`, **When** the script runs, **Then** it writes
   `GEMINI_Getting_Started.md` with the auto-updated header and the
   `*Last updated via scripts/update_getting_started.py*` footer
   (`scripts/update_getting_started.py:76-88`).
2. **Given** no `--model` flag on an interactive terminal, **When** selecting a model,
   **Then** the script lists `generateContent`-capable models and prompts for an index with
   default 0 (`scripts/update_getting_started.py:19-36`) — the Non-Hardcoded LLM Selection
   pattern (`PATTERNS.md:7`).

### Edge Cases

- **Missing Python deps**: both LLM scripts catch `ImportError` at import time and exit with
  `pip install -r requirements.txt` guidance instead of a traceback
  (`scripts/optimize_changelog.py:5-11`; `scripts/update_getting_started.py:4-11`).
- **Missing `GOOGLE_API_KEY`**: LLM scripts abort with the checked `.env` path named
  (`scripts/optimize_changelog.py:61-64`); `verify_structure.py` needs no credentials at all.
- **Model listing fails** (quota/network): `select_model` falls back to a hardcoded default
  (`scripts/optimize_changelog.py:29-31`; `scripts/update_getting_started.py:37-39`) — see
  Findings: the fallback IDs are stale-model risks and one lacks the `models/` prefix.
- **`Project_Structure.md` missing entirely**: the gate exits 1 CRITICAL
  (`scripts/verify_structure.py:43-45`); the optimizer likewise aborts
  (`scripts/optimize_changelog.py:69-72`).
- **`--dry-run` on the gate**: accepted for fleet CLI consistency but purely cosmetic — the
  script is read-only either way (`scripts/verify_structure.py:79-83`; the `dry_run`
  parameter is unused inside `verify()`).
- **Known-unhandled (non-goals)**: the gate is one-directional — it flags files missing from
  the changelog but NOT changelog entries whose files no longer exist (deleted files stay in
  history legitimately); `update_getting_started.py`'s `input()` has no dedicated EOF branch —
  non-interactive stdin lands in the broad `except` and uses the default model with a
  misleading "Could not list models" warning (`scripts/update_getting_started.py:34-39`).

## Requirements

### Functional Requirements

- **FR-001**: The structure gate MUST derive the accounted-file set exclusively from the
  changelog's "Files Affected" column (index 3) using comma-split, backtick-strip, POSIX
  normalization (`scripts/verify_structure.py:26-37`).
- **FR-002**: The gate MUST exit 0 when every non-excluded file on disk is accounted for, and
  exit 1 listing each unaccounted file otherwise (`scripts/verify_structure.py:65-74`).
- **FR-003**: The gate MUST exclude `.git/`, `__pycache__/`, `.env`, `bootstrap_prompts/`,
  `docs/`, `Project_Structure.md`, `.specify/`, `.claude/`, `.gemini/`, `specs/`
  (`scripts/verify_structure.py:55-62`).
- **FR-004**: The changelog optimizer MUST validate that the consolidated table preserves the
  union of all previously-accounted filenames, and MUST refuse to write on any loss
  (`scripts/optimize_changelog.py:111-119`).
- **FR-005**: The optimizer's LLM prompt MUST require the exact
  `| Date | Action | Files Affected | Summary |` structure and forbid generic
  file descriptions (`scripts/optimize_changelog.py:90-101`).
- **FR-006**: All three scripts MUST be Python with `argparse`, exposing `--model` and
  `--dry-run` (`scripts/verify_structure.py:76-83`; `scripts/optimize_changelog.py:136-142`;
  `scripts/update_getting_started.py:93-98`), per `PATTERNS.md:6-8,18,21`.
- **FR-007**: LLM-backed scripts MUST resolve their model dynamically from
  `client.models.list()` filtered to `generateContent` support, with `--model` as automation
  bypass (`scripts/optimize_changelog.py:13-31`; `scripts/update_getting_started.py:13-39`).
- **FR-008**: LLM-backed scripts MUST load `GOOGLE_API_KEY` from the environment or the repo
  `.env` via `python-dotenv`, pinning the `.env` path to the project root
  (`scripts/optimize_changelog.py:57-63`; changelog rationale `Project_Structure.md:41-42`).
- **FR-009**: LLM-backed scripts MUST force the `v1` API version to avoid v1beta 404s
  (`scripts/optimize_changelog.py:66`; `scripts/update_getting_started.py:54-56`; decision
  history `Project_Structure.md:44`).
- **FR-010**: The skill inventory and preview→apply→verify workflow MUST be documented in
  `scripts/README.md` (`scripts/README.md:10-14`) — see Findings for its stale inventory table.

### Key Entities

- **Structure gate (`scripts/verify_structure.py`)**: stdlib-only; changelog↔tree diff; exit
  code is the contract.
- **Changelog optimizer (`scripts/optimize_changelog.py`)**: Gemini-backed table
  consolidation with a no-file-loss integrity check.
- **Onboarding refresher (`scripts/update_getting_started.py`)**: Gemini-backed regeneration
  of `GEMINI_Getting_Started.md`.
- **Skill inventory (`scripts/README.md`)**: usage triggers + maintenance workflow.
- **Dependency manifest (`requirements.txt`)**: `google-genai`, `python-dotenv`
  (`requirements.txt:1-2`, unpinned).

## Success Criteria

- **SC-001**: `python scripts/verify_structure.py` exits 0 on a clean checkout — re-verified
  in this retro run (2026-07-05).
- **SC-002**: The gate has survived two structural evolutions without false positives by
  design updates logged in the changelog: the `docs/` move (`Project_Structure.md:50`) and
  the Spec Kit payload adoption (`Project_Structure.md:57`).
- **SC-003**: The optimizer's integrity check makes LLM output safe-by-construction: a
  consolidation that would drop any accounted file is rejected before write
  (`scripts/optimize_changelog.py:111-119`).
- **SC-004**: `GEMINI_Getting_Started.md` exists and carries the script's footer marker
  (`GEMINI_Getting_Started.md:1` header; footer per
  `scripts/update_getting_started.py:78`) — the skill has been exercised for real.

## Assumptions

- Python 3 on PATH; `pip install -r requirements.txt` done for the two LLM scripts
  (`requirements.txt:1-2`); `verify_structure.py` runs with stdlib only.
- A `GOOGLE_API_KEY` in env or `.env` at repo root (`.env` is git-ignored, `.gitignore:25`).
- The changelog table's column order is stable (`Date | Action | Files Affected | Summary`);
  both the gate and the optimizer hard-code column index 3.
- Gemini API `v1` endpoint remains available; fallback model IDs are best-effort only.
