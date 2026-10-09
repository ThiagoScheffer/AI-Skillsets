---
name: reliability-operations
description: Use for observability, SLOs, runbooks, production readiness, incident response hooks, capacity/dependency monitoring, and post-release review with feedback into product and engineering artifacts.
---

# Reliability and Operations

Design production feedback as part of the system, not as an afterthought.

## Canonical artifacts

- `.sdlc/operations/observability.md`
- `.sdlc/operations/slos.md`
- `.sdlc/operations/runbook.md`
- `.sdlc/operations/post-release-review.md`

## Consider

- service objectives and user-visible signals
- logs/metrics/traces
- alert conditions and ownership
- dependency health
- capacity/resource saturation
- backup/restore when relevant
- failure/degraded modes
- incident diagnostics
- safe operational actions
- data migration monitoring
- release health checks

Do not invent SLO targets. Derive them from product/business requirements or record the decision as unresolved.

Post-release findings should be able to update requirements, ADRs, threat models and test strategy.
