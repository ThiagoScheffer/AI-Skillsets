# Artifact Contract

Each material artifact should record:

- status: draft/review/approved/superseded where meaningful
- last updated date or commit when available
- authoritative inputs
- unresolved assumptions/questions
- linked identifiers (requirements, ADRs, threats, tests)

Avoid copy-pasting the same decision into multiple artifacts. Prefer references so drift is visible.

Canonical locations:

- `.sdlc/product/PRD.md`
- `.sdlc/requirements/requirements.yaml`
- `.sdlc/requirements/traceability.yaml`
- `.sdlc/design/SYSTEM-DESIGN.md`
- `.sdlc/design/adr/ADR-###-*.md`
- `.sdlc/security/threat-model.md`
- `.sdlc/planning/tasks.yaml`
- `.sdlc/verification/test-plan.md`
- `.sdlc/release/release-plan.md`
- `.sdlc/operations/runbook.md`
