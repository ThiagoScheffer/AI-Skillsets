# Autonomy Policy

## Classification

| Class | Observable conditions | Default behavior |
| --- | --- | --- |
| `routine-proven` | Low blast radius, reversible, stable tests, repeated verified project precedent, no protected domain | Agent may proceed through local verified steps. Remote advancement still needs bounded standing approval or explicit approval. |
| `non-trivial` | Meaningful blast radius, cross-module behavior, new integration, incomplete track record, weak path overlap, recent failure, or review is valuable | Run automated checks plus targeted review before commit/push/merge/deploy. |
| `novel-high-risk` | Weak evidence plus novelty, high blast radius, unclear/irreversible rollback, protected domain, destructive effect, or production-critical impact | Human decides before the consequential action. |

Use `references/evidence-reputation.md` and `scripts/evidence_engine.py` when project evidence exists. A numerical score never overrides hard gates.

## Protected domains
Treat these as `novel-high-risk` unless a narrower, explicit standing policy exists:

- authentication, authorization, permissions, identity, secrets or key handling
- billing, payments, money movement, entitlements
- destructive data changes, migrations, backfills, retention/deletion
- production infrastructure, DNS, certificates, release controls
- privacy, legal/compliance, security boundary changes
- irreversible external API actions or customer-impacting bulk operations
- disabling tests, security checks, audit logs, branch protection, or safety controls

## Risk signals
Increase risk for: large or unclear diff, many files/modules, weak tests, flaky baseline, stale evidence, dependency upgrades, concurrency, persistence/schema changes, external side effects, poor rollback, incident pressure, or instruction to "just skip" a gate.

Decrease risk only with evidence: narrow diff, deterministic tests, known rollback, repeated successful precedent, isolated environment, independent review, and current verification.

## Operation gates

| Operation | Routine-proven | Non-trivial | Novel/high-risk |
| --- | --- | --- | --- |
| inspect / plan / test | auto | auto | auto |
| edit locally | auto | auto with checkpoints | human before protected-domain or otherwise consequential mutation |
| commit locally | auto after verification | verification + targeted review | human unless explicitly approved |
| push remote | standing approval OR explicit approval | targeted review + standing/explicit approval | explicit human approval |
| merge | standing approval + protections OR explicit approval | targeted review + explicit approval by default | explicit human approval |
| deploy / production action | explicit bounded standing policy or explicit approval + rollback/monitoring | human by default | explicit human approval |

A standing approval must be project-specific, explicit, revocable, and bounded by branch, operation, risk class, and protected paths. It does not apply to `novel-high-risk` work unless the human policy explicitly names that protected action.

## Evidence freshness
A past success is precedent, not proof. Re-run the smallest relevant verification after each material change. If code, dependencies, environment, requirements, or file scope changed substantially, downgrade stale precedent or use a new task family.
