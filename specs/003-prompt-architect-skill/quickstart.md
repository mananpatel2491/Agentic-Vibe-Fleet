# Quickstart: Prompt Architect Skill

Requires `GOOGLE_API_KEY` in env or the repo-root `.env` — even for dry-runs (the key check
precedes the short-circuit).

## 1. Free preview (no API call, no file)

```powershell
cd C:\Docs\Build\mananUtils\Agentic-Vibe-Fleet
pip install -r requirements.txt
python .\scripts\generate_bootstrap_prompt.py "Add a health endpoint to the API" --dry-run
```

Expected output: masked `GOOGLE_API_KEY loaded (...)`, the `--- DRY RUN: no API call made,
no file written ---` banner, `Model : <resolved dynamically at run time>`, the resolved
`bootstrap_prompts\prompt_<timestamp>.md` target, and the full system-prompt + context
preview. Confirm `bootstrap_prompts/` was NOT created.

## 2. Live generation with model picker

```powershell
python .\scripts\generate_bootstrap_prompt.py "Fix: verify_structure misses nested files"
```

Pick a model from the numbered list (Enter = default 0). Output lands in
`bootstrap_prompts\prompt_YYYYMMDD_HHMMSS.md`; console says
`Action: Copy the content of this file to start your new session.`

## 3. Automation form (no prompts, pinned model)

```powershell
python .\scripts\generate_bootstrap_prompt.py "your intent" --model models/gemini-flash-latest
```

Piped/CI stdin also works without `--model` — the picker falls back to the default instead
of blocking.

## 4. Use the artifact

Open the generated file, copy its whole content into a fresh Lead Agent session, and verify
the session obeys the embedded standing instructions (it must run
`python ./scripts/verify_structure.py` after every commit). For a bug intent, the first
agent turn should be a hypothesis + confirmation request, not code.
