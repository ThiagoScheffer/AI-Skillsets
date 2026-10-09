---
name: adaptive-agent-autonomy
description: Use when an AI coding agent must decide how far it may proceed, reuse verified project knowledge, minimize context cost, or request approval before push, merge, deployment, migrations, permission changes, financial actions, or other high-impact work.
---

# Adaptive Agent Autonomy

## Core principle
Autonomy is earned by verified evidence for the current task. It is never a permanent property of the model or agent.

**REQUIRED COMPANION:** Use `superpowers` process skills when available for brainstorming, planning, TDD, debugging, code review, and verification. This skill adds memory, token economy, evidence reputation, risk classification, and approval gates; it does not replace those workflows.

## Operating loop
1. **Build a context capsule.** Read the task, `git status`, relevant diffs/files, project instructions, test entry points, relevant verified memories, and one compact task-evidence digest. Prefer indexes/diffs over full-tree reads. Target <= 1,200 tokens before implementation.
2. **Classify from evidence.** Use `references/evidence-reputation.md` and `scripts/evidence_engine.py`. Reputation is scoped to this project/task family; old evidence decays and failures reduce autonomy. Hard risk conditions override the score.
3. **Execute the smallest verified step.** Use the relevant Superpowers workflow if installed. Otherwise require plan -> implement -> test -> review -> verify. Never weaken tests to manufacture success.
4. **Gate the exact operation.** Prefer `scripts/decision_engine.py`, which combines evidence classification with `scripts/autonomy_gate.py`. Inspection/planning/testing may continue; commit/push/merge/deploy require fresh evidence and their operation-specific gates.
5. **Learn from outcomes.** Record verified successes, failures, and rollbacks in `.agent/evidence.jsonl`. Persist reusable lessons in `.agent/memory.jsonl` only after verification or explicit human confirmation. Never store secrets, credentials, raw private data, or guesses.
6. **Improve by proposal.** Repeated verified success may produce a promotion candidate, but never silently relax policy. Run regression scenarios before L2 promotion; autonomy-policy changes require human approval.

## Memory hierarchy
- **L0 session:** disposable scratch/context.
- **L1 project:** concise evidence-linked decisions/patterns plus task outcome evidence.
- **L2 reusable:** promoted cross-project rules/skills only after repeated evidence and review.

## Hard human gates
Human decision is required for novel/high-risk consequential work and, unless a narrowly explicit policy says otherwise, authentication/authorization, permissions, secrets, money/billing, destructive data operations, migrations, production infrastructure, legal/compliance boundaries, irreversible actions, and bypassing security/test controls.

## Completion contract
Before advancing project state, report: task family, classification + confidence, current verification, review status, learned evidence/memory, gate decision, and exact next operation. If approval is required, stop before that operation.
