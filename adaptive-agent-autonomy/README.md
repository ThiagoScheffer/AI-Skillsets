# Adaptive Agent Autonomy — v0.2

Portable skill for coding agents that need evidence-based autonomy, concise project memory, token-efficient context, and explicit approval gates.

It is designed to **compose with Superpowers** rather than duplicate it. Superpowers supplies disciplined planning/TDD/debugging/review workflows; this layer adds task-scoped reputation, memory, context budgeting, and operation gates.

## What v0.2 adds

The Evidence & Reputation Engine learns only from outcomes in the current project. Repeated verified success can earn `routine-proven`; failures, stale evidence, weak path overlap, flaky tests, unknown rollback, or larger blast radius reduce confidence. The score is never a permanent reputation for the model.

The one-shot flow is:

```text
Task -> context capsule -> evidence assessment -> classify -> implement/verify
     -> operation gate -> proceed / review / human approval -> record outcome
```

## Install

```bash
mkdir -p ~/.agents/skills
cp -R adaptive-agent-autonomy ~/.agents/skills/
```

Or:

```bash
./install.sh
```

To **check for Superpowers and add a portable copy if missing**:

```bash
./install.sh --ensure-superpowers
```

The curated source is:
`https://github.com/openai/plugins/tree/main/plugins/superpowers`

## Initialize project memory

```bash
python ~/.agents/skills/adaptive-agent-autonomy/scripts/memory_store.py init --repo .
```

Record only verified reusable lessons:

```bash
python ~/.agents/skills/adaptive-agent-autonomy/scripts/memory_store.py record \
  --repo . --kind command \
  --summary "Focused unit tests run with: npm test -- path/to/test" \
  --evidence "exit 0 on current branch" --tags tests --verified
```

Retrieve a compact context slice:

```bash
python ~/.agents/skills/adaptive-agent-autonomy/scripts/memory_store.py context \
  --repo . --query "authentication tests" --files src/auth.ts --max-tokens 1200
```

## Record project evidence

After a successful verified instance of a repeatable task:

```bash
python ~/.agents/skills/adaptive-agent-autonomy/scripts/evidence_engine.py record \
  --repo . \
  --task-family generated-client-refresh \
  --operation commit --outcome success --verified --reviewed \
  --blast-radius low --rollback known \
  --files src/generated/client.ts \
  --verification "focused tests: exit 0"
```

Failures and rollbacks should also be recorded; they reduce future autonomy.

## Classify + decide next operation

```bash
python ~/.agents/skills/adaptive-agent-autonomy/scripts/decision_engine.py \
  --repo . \
  --task-family generated-client-refresh \
  --operation push \
  --files src/generated/client.ts \
  --blast-radius low --test-stability stable --rollback known \
  --verified --reviewed
```

Possible gates are:

- `AUTO_PROCEED`
- `GATED_REVIEW`
- `HUMAN_REQUIRED`
- `BLOCKED`

For token-constrained agents, add `--compact` to emit a one-line decision digest.

Explicit approval for the exact change/operation can be represented with `--human-approved`; it does **not** bypass fresh verification.

## Routine-proven threshold

By default, routine autonomy requires at least 3 verified prior successes for the same task family, no failure in the five most recent matching outcomes, stable current tests, low blast radius, known rollback, no protected domain or uncontrolled external effect, and evidence score >=82/100.

Remote push/merge/deploy still follow their own approval policy even if the task is routine.

## Validation

```bash
python -m pytest tests/test_contract.py tests/test_evidence_engine.py
```

Behavioral eval prompts are in `tests/pressure-scenarios.md`.
