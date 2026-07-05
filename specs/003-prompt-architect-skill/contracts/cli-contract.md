# CLI Contract — generate_bootstrap_prompt.py

No network API is exposed; the contract is the CLI surface, the generated-prompt guarantees,
and the archive layout.

## Invocation

```
python scripts/generate_bootstrap_prompt.py "<intent>" [--model MODEL_ID] [--dry-run]
```

| Argument | Contract | Source |
|---|---|---|
| `intent` (positional, required) | English feature/bug description; becomes `USER INTENT:` in the request | `scripts/generate_bootstrap_prompt.py:86,127` |
| `--model` | used verbatim; disables listing and picker | `:18-19,128` |
| `--dry-run` | zero network, zero writes; prints model, target path, full request preview | `:93-103,129` |

## Precondition sequence (order matters)

1. deps importable, else exit 1 with pip remedy (`:5-11`)
2. `GOOGLE_API_KEY` present (env or `<root>/.env`), else abort — applies to dry-runs too (`:52-57`)
3. masked key echo `GOOGLE_API_KEY loaded (xxxx...xxxx)` (`:59-60`)
4. dry-run short-circuit (`:95-103`) — client construction only after this point (`:105`)

## Generated-prompt guarantees (LLM-instructed)

Every bootstrap prompt is instructed to contain:

- Standing instructions: `python ./scripts/verify_structure.py` after every commit; Bruno
  validation for backend changes; no commit on Bruno failure without the owner exception
  string; immediate `Project_Structure.md` updates (`:68-72`).
- Feature intents: reuse analysis with file references, or first line
  `STATION CHECK: This appears to be a brand-new feature with no reusable components.
  Confirm to proceed.` (`:74-77`).
- Bug intents: Create Hypothesis → Ask for Confirmation → Report Findings → Implementation
  (`:79-81`).
- Markdown-only output (`:83`).

(These are prompt-level guarantees — enforced by instruction, not post-validated; the
Director reviews before use.)

## Archive contract

| Aspect | Value |
|---|---|
| Path | `<root>/bootstrap_prompts/prompt_<YYYYMMDD_HHMMSS>.md` (`:89-91`) |
| Creation | dir `mkdir(exist_ok=True)` on first live run (`:116`) |
| Gate status | excluded from `verify_structure.py` (`scripts/verify_structure.py:57`); mapped at `Project_Structure.md:16` |
| Dry-run | path is computed and printed but never written (`:97-98`) |

## Exit codes

| Condition | Exit |
|---|---|
| success / dry-run / handled abort (missing key, API error) | 0 |
| missing dependencies | 1 (`:9-11`) |
| bad CLI usage | 2 (argparse) |
