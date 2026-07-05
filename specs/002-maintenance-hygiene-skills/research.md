# Research: Maintenance & Hygiene Skills

As-built record — decisions reconstructed 2026-07-05 from the 2026-05-19/20 changelog rows
(`Project_Structure.md:36-48`), `PATTERNS.md`, and the scripts at HEAD.

## Decision 1 — Python-only, PowerShell deleted

**Choice**: the first gate implementation `scripts/verify-structure.ps1` was deleted the same
day in favor of the Python version (`Project_Structure.md:36-37`), codified as the
Cross-Platform Automation pattern (`PATTERNS.md:6`).
**Why**: the fleet targets Windows/macOS/Linux; PowerShell is not portable enough for a
template meant to replicate.
**Rejected**: dual-maintained ps1+py scripts (double drift surface).

## Decision 2 — Machine-verified changelog instead of trust

**Choice**: parse the human-facing changelog table itself
(`scripts/verify_structure.py:14-39`) rather than keeping a separate manifest.
**Why**: one source of truth — the doc agents already must update (`GEMINI.md:12`) is the
same artifact the machine checks; a second manifest would drift from the first.
**Rejected**: a JSON manifest (drift), git-hook-only enforcement (skippable, and the fleet
runs across shells).

## Decision 3 — `google-generativeai` → `google-genai` SDK migration

**Choice**: migrate both LLM scripts to the `google-genai` SDK
(`Project_Structure.md:40`; imports `scripts/optimize_changelog.py:6`).
**Why**: the old SDK was deprecated; staying would violate the framework's own
future-proofing stance.
**Rejected**: pinning the deprecated SDK.

## Decision 4 — Root-pinned `.env` via python-dotenv

**Choice**: `load_dotenv(dotenv_path=root / ".env")` with `root` derived from
`Path(__file__).resolve().parent.parent` (`scripts/optimize_changelog.py:57-59`), added for
"more secure and portable API key management" then refined to absolute root paths
(`Project_Structure.md:41-42`).
**Why**: scripts must work regardless of the caller's CWD (agents invoke from anywhere);
relative `.env` lookup silently failed.
**Rejected**: requiring an exported env var only (Windows friction), CWD-relative dotenv
(the bug that prompted the refinement).

## Decision 5 — Force `v1` API version

**Choice**: `genai.Client(api_key=..., http_options={'api_version': 'v1'})`
(`scripts/optimize_changelog.py:66`; comment block
`scripts/update_getting_started.py:54-56`).
**Why**: the SDK default (v1beta) returned 404 NOT_FOUND for model aliases; two changelog
iterations (switch model → force v1) landed on this fix (`Project_Structure.md:43-44`).
**Rejected**: chasing alias names inside v1beta.

## Decision 6 — Dynamic model selection with hard fallback

**Choice**: list `generateContent`-capable models at runtime; `--model` bypasses; a hardcoded
fallback covers list failures (`scripts/update_getting_started.py:13-39`;
`Project_Structure.md:45`; pattern `PATTERNS.md:7`).
**Why**: a prior hardcoded model 404'd when deprecated; runtime listing prevents recurrence.
**Rejected**: hardcoded model IDs as primary path.
**Superseded-risk note (2026-07-05)**: the *fallback* strings still hardcode
`gemini-1.5-flash`-family IDs (`scripts/update_getting_started.py:28,39`;
`scripts/optimize_changelog.py:25,31`) — by now themselves deprecation candidates; the
fallback path is the one place the pattern is not fully honored (reported as a finding, not
fixed in this docs-only retro).

## Decision 7 — LLM output is untrusted: integrity check before write

**Choice**: `optimize_changelog.py` diffs the accounted-file set before/after consolidation
and refuses to write on any loss (`scripts/optimize_changelog.py:111-119`), using the same
parse rules as the gate.
**Why**: the changelog is the structure gate's source of truth; a lossy LLM "cleanup" would
break `verify_structure.py` for every file it dropped. The prompt also forbids "various
files" summaries (`scripts/optimize_changelog.py:94`), but prompt instructions alone are not
a guarantee — the post-hoc check is.
**Rejected**: trusting the model, or hand-consolidating the table (the tedium this skill
exists to remove).
