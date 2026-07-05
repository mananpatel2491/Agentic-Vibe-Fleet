# Project Structure: Agentic Vibe Fleet

This document provides a functional map of the codebase, enabling the Lead Agent (Gemini) to navigate and implement features with full architectural context.

## Core Framework (The 'Director' Layer)

| Path | Purpose |
| :--- | :--- |
| `GEMINI.md` | **Constitution**: The central nervous system and non-negotiable operating procedures. |
| `Project_Structure.md` | **Architecture Map**: This document. Functional mapping of the codebase. |
| `requirements.txt` | **Dependencies**: Python package requirements for the project. |
| `GEMINI_Getting_Started.md` | **Onboarding**: Auto-updated guide on using Gemini Code Assist features. |
| `PATTERNS.md` | **Pattern Registry**: Living document for established engineering patterns and design decisions. |
| `scripts/` | **Agentic Skills**: Maintenance and hygiene scripts accessible to agents. |
| `bruno/` | **API Validation**: Bruno collections and documentation for contract testing. |
| `bootstrap_prompts/` | **Plan Archive**: Systematic prompts generated from user intent to start new sessions. |
| `terraform/` | **Infrastructure-as-Code**: GCP/Terraform configuration for cost-gated deployments. |
| `.specify/` | **Spec Kit Core**: GitHub Spec Kit toolkit — constitution distillation (`memory/constitution.md`), spec/plan/tasks templates, PowerShell helpers, workflow registry. |
| `specs/` | **Feature Specs**: Durable per-feature artifacts (`NNN-feature/spec.md`, `plan.md`, `tasks.md`) produced by the Spec Kit chain. (Created on first `/speckit-specify` run.) |
| `.claude/` | **Claude Code Integration**: Spec Kit skills (`/speckit-*` dash-form commands) for Claude Code sessions. |
| `.gemini/` | **Gemini CLI Integration**: Spec Kit commands (`/speckit.*` dot-form TOML) for Gemini CLI sessions. |

## Application Layer (TBD)

| Path | Purpose |
| :--- | :--- |
| `src/` | Application source code. |
| `docs/architecture_overview.html` | **Visual Guide**: A 1-page HTML overview of the Agentic Vibe Fleet framework. (Excluded from `verify_structure.py` checks) |
| `Function_Mapping.md` | **Traceability Map**: Correlates frontend components with backend API functions. |

## Changelog

| Date | Action | Files Affected | Summary |
| :--- | :--- | :--- | :--- |
| 2026-05-19 | INITIALIZE | `Project_Structure.md`, `GEMINI.md`, `README.md`, `.gitignore`, `LICENSE`, `PATTERNS.md`, `scripts/README.md`, `bruno/README.md`, `terraform/README.md` | Initial architecture mapping and framework bootstrapping for the Director layer. |
| 2026-05-19 | ADD | `scripts/verify_structure.py` | Added hygiene script (Python) to enforce changelog consistency. |
| 2026-05-19 | DELETE | `scripts/verify-structure.ps1` | Removed PowerShell version in favor of cross-platform Python script. |
| 2026-05-20 | ADD | `GEMINI_Getting_Started.md`, `scripts/update_getting_started.py` | Added onboarding documentation and an automated skill to keep it updated via Gemini API. |
| 2026-05-20 | ADD | `requirements.txt` | Added dependency manifest to automate environment setup. |
| 2026-05-20 | UPDATE | `requirements.txt`, `scripts/update_getting_started.py` | Migrated from deprecated `google-generativeai` to `google-genai` SDK. |
| 2026-05-20 | UPDATE | `requirements.txt`, `scripts/update_getting_started.py` | Added `python-dotenv` support for more secure and portable API key management. |
| 2026-05-20 | UPDATE | `scripts/update_getting_started.py` | Refined .env loading logic to use absolute project root paths for better reliability. |
| 2026-05-20 | UPDATE | `scripts/update_getting_started.py` | Switched to `gemini-1.5-flash` to resolve 404 NOT_FOUND errors in the v1beta API. |
| 2026-05-20 | FIX | `scripts/update_getting_started.py` | Forced SDK to use `v1` API endpoint to resolve model-not-found errors. |
| 2026-05-20 | UPDATE | `scripts/update_getting_started.py` | Implemented dynamic model selection via `client.models.list()` to prevent future 404s. |
| 2026-05-20 | UPDATE | `PATTERNS.md`, `scripts/update_getting_started.py` | Codified automation patterns (Python-only, dynamic LLM, CLI arguments, and dry-run support). |
| 2026-05-20 | ADD | `scripts/optimize_changelog.py` | Added LLM-powered script to consolidate and clean the architectural changelog. |
| 2026-05-20 | UPDATE | `PATTERNS.md`, `Project_Structure.md`, `Function_Mapping.md` | Added patterns for Contract-First Bruno validation and Full-Stack Traceability Mapping. |
| 2026-05-20 | ADD | `scripts/generate_bootstrap_prompt.py`, `bootstrap_prompts/` | Added 'Prompt Architect' skill to automate context-aware session planning and plan archiving. |
| 2026-05-20 | MOVE | `architecture_overview.html` | Moved visual architecture overview to `docs/` folder and excluded `docs/` from `verify_structure.py` checks. |
| 2026-05-20 | BASELINE | ALL | **V0.0.1 Template Baseline**: Director Layer operational. Ready for autonomous vibe coding and replication. |
| 2026-05-20 | UPDATE | `PATTERNS.md` | Added patterns for Proactive Hardening, Production Readiness Gating, and Infrastructure Migration Advisory. |
| 2026-06-09 | FIX | `scripts/generate_bootstrap_prompt.py` | Made `--dry-run` a true short-circuit (no API call / no file write) so it works even when the Gemini API is unavailable; previously the dry-run preview sat after the live `generate_content` call and was skipped on any API error. Added a masked `GOOGLE_API_KEY loaded` confirmation and a clearer key-not-found message for debuggability. |
| 2026-06-09 | FIX | `scripts/generate_bootstrap_prompt.py` | `select_model` now offers an interactive picker (lists available models, prompts for an index, defaults to index 0) instead of silently auto-selecting index 0. Preserves the `--model` override and falls back to the default on empty/invalid or non-interactive (piped/CI) stdin. |

| 2026-06-12 | ADD | `docs/tradefleet_initiative.html` | **V0.0.2 — Proof of concept: the initiative works.** Added a self-contained HTML explainer documenting the TradeFleet initiative built on this framework: methodology (this repo) — template (TradeFleet, full base source + bootstrap/rollout prompt) — two LIVE production contractor sites (EcoHomeBuild, BullyBrickMI; Firebase Hosting + Cloud Run + Firestore at ~$0/mo, Bruno gates 76/151 green per child). Docs-only change — cost review: $0, no infra. |
| 2026-07-05 | ADD | `.specify/`, `.claude/`, `.gemini/`, `GEMINI.md`, `PATTERNS.md`, `Project_Structure.md`, `README.md`, `scripts/verify_structure.py` | **V0.0.3 — GitHub Spec Kit adoption.** Initialized Spec Kit (Specify CLI v0.12.5) with Claude Code (skills, `/speckit-*`) and Gemini CLI (commands, `/speckit.*`) integrations. Seeded `.specify/memory/constitution.md` as a distillation of GEMINI.md + PATTERNS.md (GEMINI.md remains supreme). Codified the Spec-Driven Feature Workflow: the specify→clarify→plan→tasks→implement chain is the concrete implementation of the 80/20 planning phase, with durable artifacts in `specs/NNN-*/`. Tooling-only change — cost review: $0, no infra. |