# Data Model: Maintenance & Hygiene Skills

No database. The data surfaces are the parsed changelog table, the exclusion list, and the
scripts' config inputs.

## Changelog table parse contract (shared by gate + optimizer)

Source: `Project_Structure.md` under `## Changelog`. Parsed by
`scripts/verify_structure.py:14-39` and (same rules, string input)
`scripts/optimize_changelog.py:33-53`:

| Column (index) | Meaning | Machine use |
|---|---|---|
| Date (1 after split) | ISO date | ignored |
| Action (2) | INITIALIZE / ADD / UPDATE / DELETE / FIX / MOVE / BASELINE | ignored |
| **Files Affected (3)** | comma-separated, backticked paths | **parsed**: split on `,`, backticks stripped, `strip('/')`, POSIX-normalized via `Path(...).as_posix()` |
| Summary (4) | prose | ignored (LLM rewrites it during consolidation) |

Header/separator rows are skipped by substring heuristics (`"Files Affected"`, `"---"`,
`"Action"`, `"Date"` — `scripts/verify_structure.py:34`). Consequence: a literal file named
e.g. `Dates.md` in the cell would be mis-skipped — accepted limitation at current scale.

## Gate exclusion set (`scripts/verify_structure.py:55-62`)

```
.git/**  __pycache__/**  .env  bootstrap_prompts/**  docs/**  Project_Structure.md
.specify/**  .claude/**  .gemini/**  specs/**        # added v0.0.3
```

Everything else under the repo root must appear in the union of all "Files Affected" cells.

## Exit-code contract

| Script | 0 | 1 |
|---|---|---|
| `verify_structure.py` | all files accounted (`:73-74`) | missing files listed, or no `Project_Structure.md` found (`:43-45,67-71`) |
| `optimize_changelog.py` | always (errors print + return, no nonzero exit) | never — see finding: failures are not signaled via exit code |
| `update_getting_started.py` | always (same pattern) | never |

## Config/env keys

| Key | Read by | Default/behavior |
|---|---|---|
| `GOOGLE_API_KEY` | both LLM scripts, from env or root `.env` (`scripts/optimize_changelog.py:57-63`) | absent → abort with checked path named |
| `--model` | all three (`verify_structure.py` ignores it, self-documented `:78`) | LLM scripts: bypass dynamic selection |
| `--dry-run` | all three | optimizer/updater: preview, no write; gate: cosmetic banner (`:82-83`) |

Fallback model constants when listing fails: `models/gemini-1.5-flash`
(`scripts/optimize_changelog.py:25,31`; `scripts/update_getting_started.py:39`) and bare
`gemini-1.5-flash` (`scripts/update_getting_started.py:28`).

## Generated artifact shape

`GEMINI_Getting_Started.md` = fixed header `# Getting Started with Gemini Code Assist
(Auto-Updated)` + LLM body + footer `*Last updated via scripts/update_getting_started.py*`
(`scripts/update_getting_started.py:78`).
