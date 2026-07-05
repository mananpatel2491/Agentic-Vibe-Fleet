# Quickstart: Maintenance & Hygiene Skills

The gate needs nothing but Python; the two LLM skills need `GOOGLE_API_KEY` (env or root
`.env`).

## 1. Structure gate (credential-free)

```powershell
cd C:\Docs\Build\mananUtils\Agentic-Vibe-Fleet
python .\scripts\verify_structure.py
# SUCCESS: All files are accounted for in the changelog.   (exit 0)
```

Break it: `New-Item scratch.txt`, re-run → red CRITICAL listing ` - scratch.txt`, exit 1.
Delete the file to go green. (Files under `docs/`, `specs/`, `.specify/` etc. are excluded
and won't trip it.)

## 2. Changelog consolidation — preview, then apply, then re-verify

The documented workflow (`scripts/README.md:10-14`):

```powershell
pip install -r requirements.txt                       # google-genai + python-dotenv
python .\scripts\optimize_changelog.py --dry-run      # preview consolidated table
python .\scripts\optimize_changelog.py                # apply (integrity-checked write)
python .\scripts\verify_structure.py                  # must stay green
```

If the LLM's consolidation would drop any accounted filename, the apply step refuses and
lists the files — nothing is written.

## 3. Regenerate the onboarding guide

```powershell
python .\scripts\update_getting_started.py --dry-run   # preview full doc
python .\scripts\update_getting_started.py --model models/gemini-flash-latest   # non-interactive
```

Without `--model` on an interactive terminal you get a numbered model picker (Enter = index
0). Output overwrites `GEMINI_Getting_Started.md`.

## 4. What's inert without credentials

Steps 2–3 abort early with `Error: GOOGLE_API_KEY not found at <root>\.env` when the key is
missing; step 1 always works.
