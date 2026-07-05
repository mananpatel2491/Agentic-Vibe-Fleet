# Data Model: Prompt Architect Skill

No database. Data surfaces are the CLI inputs, the assembled LLM request, and the archived
artifact.

## CLI inputs (`scripts/generate_bootstrap_prompt.py:125-131`)

| Input | Type | Required | Behavior |
|---|---|---|---|
| `intent` | positional str | yes | the English feature/bug description |
| `--model` | str | no | verbatim model ID, skips listing (`:18-19`) |
| `--dry-run` | flag | no | preview-only short-circuit (`:95-103`) |

## Assembled request

- **Context block**: `\n--- <filename> ---\n<content>\n` per governance doc, in fixed order
  `Project_Structure.md`, `PATTERNS.md`, `GEMINI.md`; absent files skipped silently
  (`scripts/generate_bootstrap_prompt.py:40-49`).
- **System prompt**: fixed Prompt-Architect instructions — standing gates (`:68-72`),
  feature protocol incl. the exact STATION CHECK sentence (`:74-77`), bug protocol (`:79-81`),
  "Output ONLY the final Markdown content" (`:83`).
- **User query**: `CONTEXT:\n{context}\n\nUSER INTENT: {intent}` (`:86`).
- **Client**: `genai.Client(api_key=..., http_options={'api_version': 'v1'})` (`:105`).

## Config/env keys

| Key | Source | Default | Notes |
|---|---|---|---|
| `GOOGLE_API_KEY` | env or `<root>/.env` (`:52-55`) | none — abort if missing | echoed masked only (`:59-60`); `.env` holds exactly this key |
| model fallback | constant | `models/gemini-1.5-flash` (`:23,25`) | used when listing fails/empty |

## Archived artifact

- **Path**: `<root>/bootstrap_prompts/prompt_<YYYYMMDD_HHMMSS>.md`
  (`scripts/generate_bootstrap_prompt.py:89-91`).
- **Content**: `response.text.strip()` — the LLM's Markdown bootstrap prompt, no wrapper
  added (`:114-118`).
- **Lifecycle**: directory created on demand (`:116`); excluded from the structure gate
  (`scripts/verify_structure.py:57`); currently absent on disk (no live run since last
  clean) — expected, not drift.
