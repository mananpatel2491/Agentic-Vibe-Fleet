# Governance Contract — what consumers of this framework can rely on

This capability exposes no network API. Its contract surface is the set of documents and
rules that agent sessions and fleet-replicated repos consume.

## 1. Session-start contract (any agent, any session)

| Obligation | Source of truth |
|---|---|
| Read `Project_Structure.md` before proposing changes | `GEMINI.md:10` |
| Consult `PATTERNS.md` at session start; inherit, don't re-litigate | `GEMINI.md:14-15` |
| Log every file add/remove in the Changelog table immediately | `GEMINI.md:12` |
| 80% plan / 20% execute; one testable change per session | `GEMINI.md:34-36` |
| Ask before acting on ambiguity; justify every line | `GEMINI.md:43-46` |

## 2. Gate contract

| Gate | Rule | Escape hatch |
|---|---|---|
| Structure | `python scripts/verify_structure.py` exit 0 required after commits | none |
| Bruno | no backend API feature is complete until the Bruno pipeline passes; gates all commits | exact string: `"I understand bruno validation is failing and I allow the exception to have the code committed to github repo"` (`GEMINI.md:25`, `PATTERNS.md:9`) |
| IaC/cost | Terraform update + `terraform plan` + cost projection before any GitHub tagging; tagging triggers deployment | none — tagging prohibited until reviews finalized (`GEMINI.md:27-30`) |

## 3. Spec Kit contract (since v0.0.3)

- Entry points: `/speckit-specify|clarify|plan|tasks|implement|analyze|checklist|constitution|converge|taskstoissues`
  (Claude Code, `.claude/skills/`) and the dot-form equivalents (Gemini CLI,
  `.gemini/commands/*.toml`).
- Artifacts land in `specs/NNN-<slug>/`; templates from `.specify/templates/`.
- Constitution gate: `.specify/memory/constitution.md` — a distillation only; `GEMINI.md`
  wins on conflict (`.specify/memory/constitution.md:3-5`); regenerate on material change
  (`GEMINI.md:41`).

## 4. Replication contract (fleet children)

- The Director layer (constitution + map + registry + `scripts/` + gate dirs) is the
  template surface cloned into consumer repos (`Project_Structure.md:51` — "Ready for
  autonomous vibe coding and replication").
- A child's Spec Kit distillation is seeded from the CHILD's own constitution, never copied
  from the parent (`PATTERNS.md:15`).
- Evidence the contract holds: TradeFleet (Tier 2) and two live Tier-3 children shipped
  under these rules (`docs/tradefleet_initiative.html:114-152,156-167`).

## 5. Stability notes

- Changelog "Files Affected" (column 3) is machine-parsed — see spec 002's
  `contracts/structure-gate-contract.md` for the exact parse/exclusion semantics.
- `docs/` and the Spec Kit payload dirs are outside the structure gate; do not rely on the
  gate to detect drift there.
