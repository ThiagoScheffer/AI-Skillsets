---
name: implementation-planning
description: Use after requirements/design are sufficiently stable to decompose work into dependency-aware, vertically coherent, testable implementation slices with traceability and rollback considerations.
---

# Implementation Planning

Create an executable delivery plan, not a generic checklist.

## Canonical artifacts

- `.sdlc/planning/implementation-plan.md`
- `.sdlc/planning/tasks.yaml`
- `.sdlc/planning/dependencies.yaml`

## Task design

Prefer vertical slices that produce a verifiable increment. Avoid decompositions such as "build backend / build frontend / add tests" when a feature can be sliced through the stack.

Each material task should include:
- `TASK-###`
- objective
- requirement IDs
- acceptance criteria
- dependencies
- impacted components
- expected tests/evidence
- security/privacy implications
- migration/rollout notes if applicable
- definition of complete

Sequence high-risk unknowns early when an experiment or spike can reduce risk.
