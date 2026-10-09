# Memory Contract

Durable memory is a verified project artifact, not a transcript archive and not a substitute for tests.

## Store
Store short records that improve future decisions: accepted architectural decisions, verified project commands, stable local conventions, recurring failure causes, successful rollback patterns, and known risk boundaries. Each record needs a summary, kind, tags/files, evidence, timestamp, and confidence.

## Do not store
Do not persist secrets, tokens, passwords, private keys, full environment dumps, raw customer/user data, speculative diagnoses, temporary stack traces without a reusable lesson, or model chain-of-thought.

## Write rule
Write L1 memory only when one of these is true:
1. relevant verification passed and the lesson is directly supported by it; or
2. a human explicitly confirmed the decision/outcome.

## Retrieval rule
Retrieve narrowly using changed files, symbols, tags, task terms, and recent decisions. Prefer 3-8 high-signal records. If a record conflicts with current code or current instructions, current evidence wins and the record should be superseded.

## Promotion rule
Promote a project lesson to reusable L2 guidance only after multiple independent successful uses, no contradictory evidence, and regression scenarios. Policy or autonomy changes require human review.

## Forgetting / compaction
Merge duplicates, mark superseded records, and prune low-confidence or stale operational trivia. Keep the evidence pointer and decision rationale concise; never keep entire chats just for memory.
