---
name: system-design
description: Use to create or update the technical system design for a substantial software feature or application, including boundaries, runtime interactions, data, APIs, failure modes, scalability, security, observability and deployment.
---

# System Design

Translate approved product/requirements into an implementable technical design.

## Canonical artifact

`.sdlc/design/SYSTEM-DESIGN.md`

Use `templates/SYSTEM-DESIGN.md` as a menu, not as a requirement to fill every section.

## Design from drivers

Start with:
- requirements covered
- architecture drivers
- constraints
- risk tier
- current system context

Then design only what is needed:
- boundaries/components
- runtime flows
- domain/data model
- API/event contracts
- auth/authz and trust boundaries
- consistency/transactions/idempotency
- failure/degraded behavior
- concurrency/background work
- caching/performance/capacity
- security/privacy
- observability
- deployment/configuration/secrets
- migration/rollback

## Diagrams

Prefer versionable diagrams (Mermaid, PlantUML, Structurizr DSL). Use C4 concepts for context/container/component views when helpful.

## Rules

Do not hide major trade-offs. Consequential choices with meaningful alternatives should become ADRs. Do not create ADRs for trivial coding decisions.
