---
name: requirements-engineering
description: Use to convert product intent into precise, traceable functional and non-functional requirements, acceptance criteria, priorities, verification methods, and dependency mappings.
---

# Requirements Engineering

Create requirements that can be designed, implemented, and verified without relying on chat context.

## Canonical artifacts

- `.sdlc/requirements/requirements.yaml`
- `.sdlc/requirements/acceptance-criteria.md`
- `.sdlc/requirements/traceability.yaml`

## Identifier model

- `BUS-###`
- `USR-###`
- `FR-###`
- `NFR-###`
- `AC-###`

## Requirements must be

- singular enough to verify
- unambiguous in actor/condition/result
- explicit about important limits/tolerances
- source-linked where possible
- assigned a verification approach

## NFR areas to consider

security, privacy, availability, performance, capacity, accessibility, auditability, maintainability, compatibility, recoverability, data retention, observability.

Do not create fake numeric SLOs. If a target is unknown, record it as an unresolved requirement decision.
