# Feature Specification: Prompt Architect Skill

**Feature Branch**: `retro/003-prompt-architect-skill` (as-built record — no branch created)

**Created**: 2026-07-05

**Status**: Shipped (v0.0.1 baseline; hardened 2026-06-09 via fix/dry-run-bootstrap-prompt 2d7f6b1 and fix/interactive-model-select af8a13d)

**Input**: retro-spec conversion of the Prompt Architect skill (`Project_Structure.md:49,53,54`; commit 7b13bde)

## Why

The framework's 80/20 protocol demands that every session start from a high-context plan —
but writing that plan by hand re-introduces the very context loss the framework fights. The
Prompt Architect (`scripts/generate_bootstrap_prompt.py`) turns a one-line English intent
into a systematic **Bootstrap Prompt** for a fresh Lead Agent session: it ingests the three
governance docs as context, bakes in the standing gate instructions
(verify_structure/Bruno/changelog), forces a reuse analysis for features and a
hypothesis-first protocol for bugs, and archives every generated plan under
`bootstrap_prompts/` (`README.md:9-14`). Two 2026-06-09 fixes hardened it: a true no-network
`--dry-run` short-circuit and an interactive model picker with a non-interactive fallback.
Since v0.0.3, Spec Kit (spec 001) supersedes it as the *primary* planning artifact chain;
the Prompt Architect remains the session-bootstrap on-ramp.

## User Scenarios & Testing

### User Story 1 - Intent → context-grounded bootstrap prompt (Priority: P1)

The Director types one English sentence; the skill emits a Markdown bootstrap prompt that a
fresh agent session can execute with full architectural context and the standing gates
pre-wired.

**Why this priority**: This is the skill's whole purpose — the "Generate Plan" step 1 of the
vibe-coding workflow (`README.md:11`).

**Independent Test**: With `GOOGLE_API_KEY` set, run
`python scripts/generate_bootstrap_prompt.py "Add a health endpoint"`; a
`bootstrap_prompts/prompt_<timestamp>.md` file is created and the console instructs you to
copy it into a new session (`scripts/generate_bootstrap_prompt.py:116-120`).

**Acceptance Scenarios**:

1. **Given** an intent, **When** the skill runs, **Then** the request context contains the
   full text of `Project_Structure.md`, `PATTERNS.md`, and `GEMINI.md`
   (`scripts/generate_bootstrap_prompt.py:40-49`) so the generated plan can reference real
   files and patterns.
2. **Given** any generated prompt, **Then** its standing instructions require: run
   `python ./scripts/verify_structure.py` after every commit, run Bruno for backend changes,
   no commit without Bruno success absent the owner exception string, and immediate
   `Project_Structure.md` updates (`scripts/generate_bootstrap_prompt.py:68-72`).
3. **Given** a feature intent with no reusable components, **Then** the generated prompt
   must open with `STATION CHECK: This appears to be a brand-new feature with no reusable
   components. Confirm to proceed.` (`scripts/generate_bootstrap_prompt.py:74-77`).
4. **Given** a bug intent, **Then** the generated prompt enforces Create Hypothesis → Ask for
   Confirmation → Report Findings → Implementation
   (`scripts/generate_bootstrap_prompt.py:79-81`).
5. **Given** success, **Then** the output lands in `bootstrap_prompts/prompt_YYYYMMDD_HHMMSS.md`
   (dir created on demand, `scripts/generate_bootstrap_prompt.py:89-91,116-118`).

---

### User Story 2 - True dry-run: preview with zero cost, zero network (Priority: P2)

The Director previews exactly what would be sent and written — even when the Gemini API is
down or the key is absent from quota — because `--dry-run` short-circuits before any client
is constructed.

**Why this priority**: Shipped as a dedicated fix (2d7f6b1) after the original dry-run sat
*after* the live `generate_content` call and was skipped on any API error
(`Project_Structure.md:53`).

**Independent Test**: `python scripts/generate_bootstrap_prompt.py "x" --dry-run` prints the
`--- DRY RUN: no API call made, no file written ---` banner, the resolved output path, and
the full request preview, then exits — no `bootstrap_prompts/` write occurs
(`scripts/generate_bootstrap_prompt.py:95-103`).

**Acceptance Scenarios**:

1. **Given** `--dry-run`, **When** the skill runs, **Then** it returns before
   `genai.Client(...)` is ever constructed (`scripts/generate_bootstrap_prompt.py:95-105`) —
   the preview works offline (key presence is still checked first, `:55-60`).
2. **Given** no `--model` with `--dry-run`, **Then** the model line prints
   `<resolved dynamically at run time>` rather than guessing
   (`scripts/generate_bootstrap_prompt.py:97`).
3. **Given** a loaded key, **Then** only a masked confirmation is echoed
   (`GOOGLE_API_KEY loaded (xxxx...xxxx)`, `scripts/generate_bootstrap_prompt.py:59-60`) —
   never the secret.

---

### User Story 3 - Deliberate model choice, automation-safe (Priority: P3)

On an interactive terminal the Director picks the Gemini model from a live numbered list; in
CI/piped contexts the skill never blocks and uses the default.

**Why this priority**: Shipped as a dedicated fix (af8a13d) replacing silent index-0
auto-selection (`Project_Structure.md:54`); ergonomics, not core function.

**Independent Test**: run without `--model` on a terminal → numbered list + index prompt with
`[Enter for default 0: <name>]`; run with stdin closed → default selected without hanging.

**Acceptance Scenarios**:

1. **Given** `--model <id>`, **Then** it is used verbatim, skipping listing entirely
   (`scripts/generate_bootstrap_prompt.py:18-19`) — the Automation-First CLI bypass
   (`PATTERNS.md:8`).
2. **Given** an interactive session, **Then** `generateContent`-capable models are listed
   with indices and Enter selects index 0 (`scripts/generate_bootstrap_prompt.py:21-38`).
3. **Given** non-interactive stdin, **When** `input()` raises `EOFError`, **Then** the
   default is used without blocking (`scripts/generate_bootstrap_prompt.py:33-35`).
4. **Given** an invalid/out-of-range entry, **Then** the default is used
   (`scripts/generate_bootstrap_prompt.py:36-38`).

### Edge Cases

- **Deps missing**: `ImportError` guard prints the `pip install -r requirements.txt` remedy
  and exits (`scripts/generate_bootstrap_prompt.py:5-11`).
- **Key missing**: abort naming both lookup locations (env and `<root>/.env`)
  (`scripts/generate_bootstrap_prompt.py:55-57`); this runs *before* the dry-run
  short-circuit, so even previews require a key on file.
- **Model listing fails / returns empty**: hard fallback `models/gemini-1.5-flash`
  (`scripts/generate_bootstrap_prompt.py:20-25`) — same stale-fallback risk noted in spec 002.
- **Governance doc missing**: `get_context_content` skips absent files silently
  (`scripts/generate_bootstrap_prompt.py:44-48`) — a degraded prompt is generated rather
  than an error (known behavior, not a crash).
- **API error during generation**: caught and printed; no file written, exit 0
  (`scripts/generate_bootstrap_prompt.py:122-123`).
- **Explicit non-goal**: the skill does not validate or execute the generated plan; quality
  control is the Director's copy-review step (`README.md:12-13`).

## Requirements

### Functional Requirements

- **FR-001**: The skill MUST accept a positional English `intent` plus `--model` and
  `--dry-run` flags via `argparse` (`scripts/generate_bootstrap_prompt.py:125-131`).
- **FR-002**: The generation context MUST include the current contents of
  `Project_Structure.md`, `PATTERNS.md`, and `GEMINI.md`
  (`scripts/generate_bootstrap_prompt.py:43`).
- **FR-003**: Generated prompts MUST embed the standing gate instructions
  (verify_structure after every commit; Bruno for backend changes; exception-string rule;
  immediate map updates) (`scripts/generate_bootstrap_prompt.py:68-72`).
- **FR-004**: Feature intents MUST trigger reuse analysis with file references, or the
  STATION CHECK opener when nothing is reusable
  (`scripts/generate_bootstrap_prompt.py:74-77`); bug intents MUST produce the
  hypothesis-confirmation-findings-implementation protocol (`:79-81`).
- **FR-005**: `--dry-run` MUST short-circuit before any network call or file write, printing
  model, target path, and the full request preview
  (`scripts/generate_bootstrap_prompt.py:93-103`).
- **FR-006**: The API key MUST never be printed in full; confirmation output is masked to
  first/last 4 characters (`scripts/generate_bootstrap_prompt.py:59-60`).
- **FR-007**: Model selection MUST follow the priority order override → interactive pick →
  default index 0, degrading safely on EOF/invalid input
  (`scripts/generate_bootstrap_prompt.py:13-38`).
- **FR-008**: Outputs MUST be archived as timestamped Markdown under `bootstrap_prompts/`
  (`scripts/generate_bootstrap_prompt.py:89-91,116-118`), which is excluded from the
  structure gate (`scripts/verify_structure.py:57`) and mapped at directory level
  (`Project_Structure.md:16`).

### Key Entities

- **Prompt Architect script (`scripts/generate_bootstrap_prompt.py`)**: the skill; 131 lines,
  `google-genai` + `python-dotenv`.
- **Bootstrap Prompt**: generated Markdown artifact — standing instructions + plan for one
  feature/bug session.
- **Plan Archive (`bootstrap_prompts/`)**: timestamped prompt history; created on first live
  run.

## Success Criteria

- **SC-001**: A preview is obtainable with zero API spend: the dry-run banner explicitly
  asserts "no API call made, no file written" and the code path constructs no client
  (`scripts/generate_bootstrap_prompt.py:95-105`) — verified by the 2026-06-09 fix rationale
  ("works even when the Gemini API is unavailable", `Project_Structure.md:53`).
- **SC-002**: Both hardening fixes shipped through the repo's convention: dedicated branches
  merged to main (327e8ed, dae87c6) with same-day changelog rows
  (`Project_Structure.md:53-54`).
- **SC-003**: The skill is wired into the documented workflow as step 1 of vibe coding
  (`README.md:9-14`) and into onboarding as the "Prompt Architect workflow" section request
  (`scripts/update_getting_started.py:66`).

## Assumptions

- `GOOGLE_API_KEY` present in env or root `.env` even for dry-runs (checked before the
  short-circuit).
- The three governance docs exist at repo root (silently degraded context otherwise).
- Generated prompts are consumed by copy-paste into a fresh agent session
  (`scripts/generate_bootstrap_prompt.py:120`); no direct session-spawning integration.
- Since v0.0.3, feature planning of record is the Spec Kit chain (spec 001); the Prompt
  Architect complements rather than replaces it (no deprecation decision on file).
