# Structure Gate & Hygiene CLI Contract

No network API. The contract surfaces are CLI invocations, exit codes, and the changelog
parse rules that other tools (and fleet copies) rely on.

## 1. `verify_structure.py` — the gate

```
python scripts/verify_structure.py [--model IGNORED] [--dry-run]
```

| Aspect | Contract | Source |
|---|---|---|
| Root discovery | nearest ancestor dir containing `Project_Structure.md`; CRITICAL + exit 1 if none | `scripts/verify_structure.py:6-12,43-45` |
| Accounted set | union of all changelog "Files Affected" cells (column index 3); comma-split, backticks stripped, POSIX-normalized | `:26-37` |
| Scanned set | `rglob("*")` files minus exclusions `.git/ __pycache__/ .env bootstrap_prompts/ docs/ Project_Structure.md .specify/ .claude/ .gemini/ specs/` | `:52-63` |
| PASS | scanned ⊆ accounted → green `SUCCESS` line, **exit 0** | `:73-74` |
| FAIL | red `CRITICAL` + one ` - <path>` line per missing file, **exit 1** | `:67-71` |
| Direction | one-way only: disk→changelog. Rows for deleted files stay valid history | by construction |
| `--dry-run` | banner only; behavior identical (read-only script) | `:82-83` |

Consumers: bootstrap standing instructions ("After every commit, run …",
`scripts/generate_bootstrap_prompt.py:69`), the fleet's replicated copies, and this retro
run's docs-of-record gate.

## 2. `optimize_changelog.py` — integrity-checked writer

```
python scripts/optimize_changelog.py [--model MODEL_ID] [--dry-run]
```

- Reads/writes `Project_Structure.md` in place (preamble preserved, table replaced —
  `scripts/optimize_changelog.py:79-86,121,128-131`).
- **Write precondition**: `original_files ⊆ new_files` under the same parse rules as the
  gate; violation → refusal with per-file listing (`:111-119`).
- LLM prompt contract: keep `| Date | Action | Files Affected | Summary |`, no generic file
  descriptions, table-only output (`:90-101`); ```markdown fences stripped defensively
  (`:108-109`).
- Error mode: API/env failures print and return with **exit 0** (known limitation — spec
  tasks.md T018).

## 3. `update_getting_started.py` — doc regenerator

```
python scripts/update_getting_started.py [--model MODEL_ID] [--dry-run]
```

- Overwrites `GEMINI_Getting_Started.md` with header + LLM body + footer marker
  (`scripts/update_getting_started.py:76-88`).
- Model resolution: `--model` → interactive picker over `generateContent`-capable models →
  fallback constant (`:13-39`).

## 4. Env contract

| Variable | Required by | Effect when missing |
|---|---|---|
| `GOOGLE_API_KEY` (env or root `.env`) | scripts 2–3 | abort before any API call, path named |
| none | script 1 | gate is credential-free by design |
