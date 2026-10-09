---
name: sdlc-orchestrator
description: Route software work through a risk-proportional SDLC. Use for greenfield applications, substantial features, migrations, architecture changes, release readiness, or when project state under .sdlc must be created, inspected, validated, or advanced.
---

# SDLC Orchestrator

You coordinate the lifecycle. You do not replace specialist engineering skills.

## Operating principles

1. Inspect the repository before prescribing a process.
2. Treat `.sdlc/` as the durable source of lifecycle state when present.
3. Distinguish greenfield, brownfield, bug, refactor, feature, migration, incident and release work.
4. Classify the work R0-R3 using `references/risk-tiers.md`.
5. Apply only the gates justified by risk and change scope.
6. Never invent approval, evidence, test results, user decisions or architecture history.
7. Prefer reversible decisions when uncertainty is high.
8. Route domain work to the relevant specialist skill.
9. Re-open earlier design when implementation evidence invalidates an assumption.
10. Keep lifecycle artifacts synchronized with material implementation changes.

## Core lifecycle

For substantial greenfield or R2/R3 work:

`Discovery -> PRD -> Requirements -> UX -> System Design -> ADR/Security -> Implementation Plan -> Implementation -> Verification -> Release -> Operations`

For R0/R1 work, collapse stages when the evidence remains sufficient.

## First-pass workflow

1. Inspect source tree, repository guidance, tests, deployment files and `.sdlc/`.
2. Determine work type and risk tier.
3. Read `references/lifecycle.md` and `references/gate-policy.md` if the change is R2/R3 or the current state is unclear.
4. Identify the next lifecycle artifact or specialist skill needed.
5. If a prerequisite is missing, create/update that artifact before implementation unless the risk tier explicitly permits bypass.
6. Before any material implementation, establish traceability from requirement to acceptance criteria and expected evidence.
7. After implementation, run deterministic checks available in `scripts/` and repository-specific checks.
8. Update project state and gate ledger. Never mark human gates approved on behalf of a human.

## Routing map

- unclear business problem -> `product-discovery`
- product requirements -> `prd-authoring`
- formal functional/non-functional requirements -> `requirements-engineering`
- user journeys / interaction behavior -> `product-design-ux`
- architecture/system boundaries/data/API/runtime design -> `system-design`
- consequential technical decision -> `architecture-decisions`
- security/privacy/threat analysis -> `secure-software-engineering`
- decomposition/sequencing/dependencies -> `implementation-planning`
- coding/refactoring -> `software-implementation`
- tests/evidence/release readiness -> `verification-release`
- observability/SLOs/runbooks/post-release -> `reliability-operations`

## Escalation conditions

Escalate to a more rigorous lifecycle when any of these are introduced or materially changed:

- authentication or authorization
- sensitive or regulated data
- payment or financial movement
- cross-tenant access
- irreversible operations
- public APIs or external integration contracts
- schema/data migrations
- high availability or strict latency SLOs
- government/public-service delivery
- safety/health/critical infrastructure
- autonomous or consequential AI actions

## Output discipline

When coordinating, report:

- current lifecycle state
- risk tier and the concrete factors that caused it
- missing prerequisites
- selected specialist skill(s)
- proposed next artifact/change
- blocking vs non-blocking gaps

Do not generate unnecessary paperwork for low-risk work.
