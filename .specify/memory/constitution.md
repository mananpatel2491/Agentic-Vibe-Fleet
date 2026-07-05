# Agentic Vibe Fleet Constitution

> **Precedence**: `GEMINI.md` is the Project Constitution of record for this repository.
> This file is its Spec Kit–facing distillation, consumed by the `/speckit.*` workflow.
> On any conflict, `GEMINI.md` (and `PATTERNS.md` for design decisions) wins.

## Core Principles

### I. Context-First Architecture Map
Before proposing any change, read `Project_Structure.md` and use its functional descriptions to decide how a feature lands. Every file addition or removal is logged in the Changelog table immediately — no deferred bookkeeping.

### II. Pattern Reference Integrity
Consult `PATTERNS.md` at the start of every session. Inherit prior design decisions instead of re-litigating them; never record aspirational designs — every pattern entry must reflect the actual codebase.

### III. Automated Maintenance via Agentic Skills
Project hygiene runs through the `scripts/` folder (Python, cross-platform, `argparse`, `--dry-run` support). When a file is expected but missing or environment state is drift-prone, run the maintenance scripts rather than hand-editing. Tedious mechanical work may be delegated to local models to preserve API quota.

### IV. Continuous API Validation — NON-NEGOTIABLE
No backend API feature is complete until the Bruno pipeline is updated and passing. Successful Bruno execution gates all commits; the only exception requires the exact acknowledgment string recorded in `PATTERNS.md`. A feature is "done" only when automated validation passes and its visual flow is verified.

### V. Infrastructure-as-Code & Cost Gating
Every infra-dependent feature requires a Terraform update. Projected costs are calculated and `terraform plan` is reviewed before any GitHub tagging; tagging (which triggers deployment) is prohibited until cost and infra reviews are finalized.

## Operational Constraints

- **80/20 Surgical Strike**: 80% of a session is read-only planning, 20% execution; one testable change per session to prevent cascade damage. The Spec Kit chain (`specify → clarify → plan → tasks → implement`) is the concrete implementation of the planning phase — specs in `specs/NNN-*/` are the durable artifacts of the 80%.
- **Roles**: The Director (user) owns intent, arbitration, and final review. The Lead Agent owns autonomous reasoning, planning, and error-free execution.
- **Proactive hardening**: when touching an existing file, audit for security risks and leaks; patch immediately.
- **Production readiness**: temporary/mock markers (`TODO: temp`, `fix later`) must be flagged to the Director before proceeding.

## Development Workflow

- Version-branch git flow: work on a `vX.Y.Z` branch, `merge --no-ff` to `main`; local only unless the Director asks to push.
- Clarify ambiguous prompts before acting; if a line of code cannot be justified, it is not implemented.
- Start fresh sessions frequently to avoid context rot; durable memory lives in `Project_Structure.md`, `PATTERNS.md`, `GEMINI.md`, and `specs/`.

## Governance

This distillation is regenerated whenever `GEMINI.md` or `PATTERNS.md` materially changes. Amendments to the actual constitution happen in `GEMINI.md` under Director approval; this file never introduces rules of its own. All spec/plan/task artifacts produced by `/speckit.*` must be verified for compliance against the principles above.

**Version**: 1.0.0 | **Ratified**: 2026-07-05 | **Last Amended**: 2026-07-05
