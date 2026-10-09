---
name: architecture-decisions
description: Use to record, review, or supersede consequential architecture decisions with alternatives, trade-offs, consequences, risks and revisit conditions.
---

# Architecture Decisions

Create an ADR only when the decision is consequential, has meaningful alternatives, is costly to reverse, or future maintainers need the reasoning.

## Canonical artifact

`.sdlc/design/adr/ADR-###-short-title.md`

Use `templates/ADR.md`.

## Required reasoning

- context
- decision drivers
- considered options
- selected decision
- trade-offs
- positive/negative consequences
- risks/mitigations
- revisit conditions
- linked requirements/design sections

## Statuses

`proposed`, `accepted`, `superseded`, `deprecated`, `rejected`

Never rewrite history to make an old ADR look current. Supersede it with a new ADR.
