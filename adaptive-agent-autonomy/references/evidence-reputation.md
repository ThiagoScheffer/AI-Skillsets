# Evidence & Reputation Engine

The engine tracks **project-local precedent for a task family**. It does not assign a permanent reputation to the model or agent. Autonomy remains task- and operation-specific.

## What earns autonomy
A task becomes `routine-proven` only when current safeguards and repeated project evidence agree. The default threshold requires:

- at least 3 verified prior successes for the same task family;
- no failure among the five most recent matching outcomes;
- stable current tests;
- low blast radius;
- a known rollback;
- relevant file/path overlap with precedent when paths are supplied;
- no protected domain, novelty flag, or uncontrolled external side effect; and
- evidence score >= 82/100.

A high score alone cannot override any hard condition above.

## Evidence score
`scripts/evidence_engine.py` combines recency-weighted outcomes, sample volume, review history, current test stability, rollback quality, blast radius, verification quality, and precedent freshness. Old evidence decays. Failures penalize confidence faster than successes increase it.

The output is intentionally compact: classification, confidence, history digest, reasons, and next verification step. Agents should consume the digest instead of replaying the full evidence log into context.

## Recording outcomes
Store successful outcomes only when freshly verified. Failures and rollbacks should also be recorded because negative evidence must reduce autonomy.

Example:

```bash
python scripts/evidence_engine.py record \
  --repo . \
  --task-family generated-client-refresh \
  --operation commit \
  --outcome success --verified --reviewed \
  --blast-radius low --rollback known \
  --files src/generated/client.ts,tests/generated-client.test.ts \
  --verification "pytest tests/generated-client.test.ts: exit 0"
```

Then assess a future instance:

```bash
python scripts/evidence_engine.py assess \
  --repo . \
  --task-family generated-client-refresh \
  --operation push \
  --blast-radius low --test-stability stable --rollback known \
  --files src/generated/client.ts \
  --compact
```

## Failure handling
A new failure does not erase useful history, but it immediately reduces confidence and prevents `routine-proven` until sufficient fresh evidence is rebuilt. If requirements, dependencies, architecture, or affected paths change materially, treat old precedent as weaker or create a new task family.

## Promotion and self-improvement
When the engine marks `promotion_candidate=true`, the agent may propose a concise L1 memory or skill improvement. It must not silently relax policy. Promotion to reusable L2 guidance requires repeated success, regression scenarios, and review. Changes to protected-domain or approval rules always require human approval.

## Separation of concerns
- `evidence_engine.py` answers: **How proven is this task pattern here?**
- `autonomy_gate.py` answers: **May this exact operation proceed now?**
- `decision_engine.py` combines both and returns the exact next action.

Remote push, merge, and deploy remain operation-gated even when the task pattern is routine.
