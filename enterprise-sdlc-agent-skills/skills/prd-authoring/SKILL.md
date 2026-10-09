---
name: prd-authoring
description: Use to create or revise a Product Requirements Document from validated discovery or product direction, keeping product intent separate from implementation architecture.
---

# PRD Authoring

Write the product contract: what is needed and why. Avoid technology choices unless they are genuine external constraints.

## Canonical artifact

`.sdlc/product/PRD.md`

Use `templates/PRD.md` as the baseline.

## Required content for substantial work

- problem statement
- target users/stakeholders
- objectives and measurable outcomes
- in scope / out of scope
- capabilities and journeys
- business rules
- constraints
- data and integration expectations
- security/privacy/accessibility expectations
- dependencies
- assumptions/open questions
- release intent

## Quality bar

A PRD is not ready when:
- success cannot be evaluated
- scope boundaries are unclear
- material assumptions are hidden
- requirements depend on undefined actors/data
- non-goals are needed to prevent obvious scope creep but are absent

Do not choose database/framework/API style unless product context truly mandates it.
