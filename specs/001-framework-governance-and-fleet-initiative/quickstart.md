# Quickstart: Framework Governance & Fleet Initiative

Everything in this capability is offline-readable — no credentials, no build step.

## 1. Read the governance layer the way an agent does

```powershell
cd C:\Docs\Build\mananUtils\Agentic-Vibe-Fleet
# Session-start reading order (GEMINI.md:10,14):
#   GEMINI.md → PATTERNS.md → Project_Structure.md
```

Sanity checks that you absorbed it: the Bruno exception string is at `GEMINI.md:25`; the
maintenance skills live in `scripts/` per `Project_Structure.md:14`.

## 2. Verify the map matches the tree (the enforced part)

```powershell
python .\scripts\verify_structure.py
# SUCCESS: All files are accounted for in the changelog.   (exit 0)
```

Break it on purpose: create any file at repo root and re-run — exit 1 names the file
(mechanics in spec 002).

## 3. View the fleet proof-of-concept

Open in any browser (no server needed):

- `docs\architecture_overview.html` — the framework one-pager
- `docs\tradefleet_initiative.html` — three-tier fleet, live child URLs, 151/151 Bruno
  numbers, replication modes

## 4. Exercise the Spec Kit chain (v0.0.3)

From Claude Code in this repo: `/speckit-specify <feature description>`
From Gemini CLI: `/speckit.specify <feature description>`

Either produces `specs/NNN-<slug>/spec.md` from `.specify/templates/spec-template.md`; the
subsequent `/speckit-plan` gates against `.specify/memory/constitution.md` (GEMINI.md wins on
conflict). Prereqs for regenerating the toolkit itself: `uv` + Specify CLI (`README.md:36`).

## 5. Confirm the precedence rule

```powershell
Get-Content .specify\memory\constitution.md -TotalCount 5
# > **Precedence**: GEMINI.md is the Project Constitution of record ...
```
