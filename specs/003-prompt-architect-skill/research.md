# Research: Prompt Architect Skill

As-built record — decisions reconstructed 2026-07-05 from commits 7b13bde, 2d7f6b1, af8a13d
and changelog rows `Project_Structure.md:49,53,54`.

## Decision 1 — Generate the plan, don't wing the session

**Choice**: session planning is itself an agentic skill: intent + governance docs → LLM →
archived bootstrap prompt (`scripts/generate_bootstrap_prompt.py:51-121`), wired as step 1
of the vibe-coding workflow (`README.md:11`).
**Why**: the 80/20 protocol requires plan-first sessions; hand-written kickoff prompts lose
the architecture map and the standing gates — exactly the drift the constitution targets.
**Rejected**: a static prompt template (no repo-state awareness); planning inside the work
session (plan dies with the context window — later solved more durably by Spec Kit, spec 001).

## Decision 2 — Standing instructions baked into every plan

**Choice**: the system prompt hard-codes the gates (verify_structure after every commit,
Bruno for backend, exception-string rule, immediate map updates) into all generated prompts
(`scripts/generate_bootstrap_prompt.py:68-72`), plus intent-type protocols: feature → reuse
analysis / STATION CHECK; bug → hypothesis → confirmation → findings → implementation
(`:74-81`).
**Why**: fresh sessions cannot be trusted to remember procedure; embedding it in the
bootstrap makes the constitution self-propagating.
**Rejected**: relying on the new session to re-read GEMINI.md unprompted.

## Decision 3 — True dry-run short-circuit (2026-06-09, 2d7f6b1)

**Choice**: move the `--dry-run` branch BEFORE client construction and file writes,
previewing the exact request and resolved output path
(`scripts/generate_bootstrap_prompt.py:93-103`).
**Why**: the original dry-run ran *after* the live `generate_content` call, so it was
skipped whenever the API errored — a preview flag that cost quota and failed offline
(`Project_Structure.md:53`). A masked key confirmation was added in the same fix for
debuggability without leakage (`:59-60`).
**Rejected**: keeping preview-after-call; mocking the client (needless complexity for a
print-only path).

## Decision 4 — Interactive model picker with non-interactive fallback (2026-06-09, af8a13d)

**Choice**: replace silent index-0 auto-selection with a numbered live-model picker;
preserve `--model` bypass; default to index 0 on Enter, invalid input, or `EOFError`
(piped/CI stdin) (`scripts/generate_bootstrap_prompt.py:13-38`; `Project_Structure.md:54`).
**Why**: silent auto-selection hid which model produced a plan; but automation must never
block on `input()` — the EOFError branch keeps the Automation-First CLI pattern intact
(`PATTERNS.md:8`).
**Rejected**: mandatory `--model` (hostile ergonomics); interactive-only (breaks CI).
**Drift note**: this hardened picker was not back-ported to
`update_getting_started.py:34` (no EOFError branch) — the three `select_model` variants
have diverged (see tasks.md).

## Decision 5 — Timestamped archive outside the gate

**Choice**: write plans to `bootstrap_prompts/prompt_YYYYMMDD_HHMMSS.md`
(`scripts/generate_bootstrap_prompt.py:89-91`), with the directory mapped at directory level
(`Project_Structure.md:16`) and excluded from `verify_structure.py`
(`scripts/verify_structure.py:57`).
**Why**: plans are per-session ephemera with archival value; logging each in the changelog
would bury real file history under generated noise.
**Rejected**: changelog-tracked prompt files; discarding prompts after use (loses the
plan-audit trail).

## Decision 6 — Superseded-in-part by Spec Kit (2026-07-05, v0.0.3)

**Status note, not a removal**: since v0.0.3 the durable planning artifact of record is the
Spec Kit chain (`GEMINI.md:38-41`); the Prompt Architect remains the documented session
on-ramp (`README.md:9-14`) and its bootstrap prompts remain useful for kicking off
implementation sessions. No deprecation decision exists in the repo; the two coexist.
