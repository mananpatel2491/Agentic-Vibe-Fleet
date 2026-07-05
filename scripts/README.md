# Agentic Skills (scripts/)

This directory contains maintenance and hygiene scripts designed to be executed by agents to ensure project health and environment consistency.

## Usage
Agents should use Shell Mode to execute these scripts when:
- A file is expected but missing.
- Environment state has drifted.
- Repetitive boilerplate tasks need to be performed.

### Maintenance Workflow
1. **Preview**: Run `python .\scripts\optimize_changelog.py --dry-run` to see how Gemini suggests consolidating duplicate entries.
2. **Apply**: Run `python .\scripts\optimize_changelog.py` to update the `Project_Structure.md`.
3. **Verify**: Run `python .\scripts\verify_structure.py` to ensure project hygiene and changelog integrity.

## Inventory
| Script | Description |
| :--- | :--- |
| `verify_structure.py` | Python-based hygiene script for cross-platform (Win/Mac/Linux) changelog validation. Usage: `python .\scripts\verify_structure.py` (exit 0 = all files accounted for; `--dry-run` prints a read-only notice). |
| `optimize_changelog.py` | Uses Gemini to consolidate and clean up the Project_Structure.md changelog table. Usage: `python .\scripts\optimize_changelog.py` (add `--dry-run` to preview the optimized table without writing; `--model <id>` to bypass dynamic selection). |
| `generate_bootstrap_prompt.py` | The 'Prompt Architect': turns an English intent into a context-aware bootstrap prompt archived to `bootstrap_prompts/` for starting a new session. Usage: `python .\scripts\generate_bootstrap_prompt.py "your intent"` (add `--dry-run` to preview the request keylessly — no API call, no file write; `--model <id>` to bypass the interactive picker). |
| `update_getting_started.py` | Regenerates the `GEMINI_Getting_Started.md` onboarding guide via the Gemini API. Usage: `python .\scripts\update_getting_started.py` (add `--dry-run` to preview without writing; `--model <id>` to bypass the interactive picker). |

All scripts follow the Automation-First CLI pattern (`PATTERNS.md`): `argparse` interface, `--dry-run` support, `--model` override, and dynamic (non-hardcoded) LLM model selection. LLM scripts exit non-zero on API or model-listing failures so CRON/CI callers can detect them.
