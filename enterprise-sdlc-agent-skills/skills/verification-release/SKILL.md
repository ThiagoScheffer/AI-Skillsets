---
name: verification-release
description: Use to derive and execute verification strategy, gather evidence against requirements, assess release readiness, validate rollback/deployment plans, and distinguish automated evidence from human approval.
---

# Verification and Release

Ask: what evidence demonstrates each requirement and control?

## Verification mapping

Typical mappings:
- pure domain rule -> unit/property test
- integration contract -> contract/integration test
- critical user journey -> end-to-end test
- authorization rule -> positive + negative security tests
- concurrency behavior -> concurrency test
- performance NFR -> load/performance test
- migration -> forward/rollback migration test
- accessibility -> automated + manual evidence as applicable

## Canonical artifacts

- `.sdlc/verification/test-plan.md`
- `.sdlc/verification/test-evidence/`
- `.sdlc/verification/acceptance-report.md`
- `.sdlc/release/release-plan.md`
- `.sdlc/release/rollback-plan.md`

Use `templates/TEST-PLAN.md` and `templates/RELEASE-PLAN.md`.

## Release readiness

A successful build is not equivalent to release readiness. Check applicable requirements, controls, migrations, observability, operational ownership and rollback capability.

Never mark a human release gate approved without explicit authority evidence.
