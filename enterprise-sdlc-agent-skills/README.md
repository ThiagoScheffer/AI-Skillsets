# Enterprise SDLC Agent Skills

Provider-neutral software engineering skills for Codex, Claude Code, and other AI coding agents that support the open `SKILL.md` pattern.

The project is designed to convert an idea or PRD into an auditable software delivery lifecycle:

`Discovery -> PRD -> Requirements -> UX -> System Design -> Architecture Decisions -> Security/Privacy -> Implementation Plan -> Implementation -> Verification -> Release -> Operations`

It is intentionally **not** a one-shot "generate an app" prompt. The repository separates reusable engineering knowledge from project-specific SDLC state, uses risk-tiered gates, preserves traceability, and makes human approvals explicit.

## Design goals

- Provider-neutral core skills.
- Progressive disclosure: keep each `SKILL.md` focused and load references only when needed.
- Risk-proportional process: tiny changes do not need enterprise ceremony.
- Durable project state under `.sdlc/`.
- End-to-end requirement traceability.
- Explicit architecture decisions and design drift detection.
- Security and privacy by design.
- NZ private-sector and NZ government policy profiles.
- Deterministic validation scripts where an LLM should not be trusted to self-certify.
- Portable installation into Codex, Claude Code, or another agent host.

## Repository layout

```text
skills/                 Reusable Agent Skills
profiles/               Policy/compliance overlays
schemas/                JSON Schemas for project-side SDLC state
templates/              Human-readable artifact templates
scripts/                Deterministic validators and status generators
adapters/                Provider-specific installation notes
examples/                Example `.sdlc/` project state
```

## Core skills

1. `sdlc-orchestrator`
2. `product-discovery`
3. `prd-authoring`
4. `requirements-engineering`
5. `product-design-ux`
6. `system-design`
7. `architecture-decisions`
8. `secure-software-engineering`
9. `implementation-planning`
10. `software-implementation`
11. `verification-release`
12. `reliability-operations`

## Policy profiles

- `baseline`
- `nz-private`
- `nz-government`
- `high-assurance`
- `ai-enabled-application`

Profiles are overlays. They add requirements or gates without changing the provider-neutral lifecycle.

## Install for Codex

Copy or symlink the skill directories into your Codex-compatible skills directory, for example:

```text
.agents/skills/
```

You can either install all skills or only the orchestrator and the specialists you want. Keep this repository somewhere versioned and copy the `skills/*` directories into the target project or global skills location supported by your host.

See `adapters/codex/INSTALL.md`.

## Install for Claude Code

Copy the skill directories into:

```text
.claude/skills/
```

See `adapters/claude-code/INSTALL.md`.

## Start a project

Copy the example project state:

```bash
cp -R examples/sample-project/.sdlc ./.sdlc
```

Then edit `.sdlc/project.yaml`.

A substantial project should progress through stateful gates rather than relying on chat memory.

## Risk tiers

| Tier | Meaning | Typical examples | Process |
|---|---|---|---|
| R0 | Trivial / low risk | typo, copy tweak, safe refactor | direct implementation + appropriate checks |
| R1 | Bounded change | CRUD screen, small API, simple feature | lightweight requirements + implementation plan |
| R2 | Significant | auth, payments, PII, new subsystem | full design/security/verification lifecycle |
| R3 | High assurance | government, health, finance, critical services, high-risk autonomy | full lifecycle + explicit human approvals |

Risk classification is a routing decision, not a quality score.

## Project-side state

The reusable skills live here. Each application stores its own evidence under `.sdlc/`:

```text
.sdlc/
  project.yaml
  status.yaml
  gate-ledger.yaml
  product/
  requirements/
  design/
  security/
  planning/
  verification/
  release/
  operations/
```

This prevents an agent from inventing or losing project history.

## Traceability model

Recommended identifiers:

- `BUS-###` business objective
- `USR-###` user need
- `FR-###` functional requirement
- `NFR-###` non-functional requirement
- `AC-###` acceptance criterion
- `ADR-###` architecture decision
- `THR-###` threat
- `CTRL-###` control
- `TASK-###` implementation task
- `TEST-###` verification evidence
- `REL-###` release requirement

## Deterministic validation

Run:

```bash
python scripts/validate_sdlc.py .
python scripts/trace_requirements.py .
python scripts/detect_drift.py .
python scripts/generate_status.py .
```

These scripts intentionally validate structure and traceability rather than pretending to prove the application is correct.

## Human approvals

The agent must never invent a human approval. Human/authority gates belong in `.sdlc/gate-ledger.yaml` with an explicit actor and status.

## Engineering philosophy

The system should ask, in order:

1. What problem is being solved?
2. Which requirements are authoritative?
3. What evidence will prove them?
4. Which design decisions are consequential?
5. What can fail or be abused?
6. What is the smallest coherent implementation slice?
7. What evidence exists after implementation?
8. What changed in production and what should feed back into requirements?

The goal is disciplined engineering with AI acceleration, not AI-generated paperwork.
