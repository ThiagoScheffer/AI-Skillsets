# Token Economy

The objective is not minimum tokens; it is minimum context that preserves correctness.

## Context capsule order
1. current task + explicit acceptance criteria
2. project instructions and constraints
3. `git status` + relevant diff
4. symbols/files directly touched
5. test/build entry points
6. 3-8 relevant verified memory records
7. one compact evidence/reputation digest for the task family
8. only then, broader code search

Target ~1,200 tokens before implementation for ordinary tasks. Expand only when evidence shows the task needs more context.

## High-leverage rules
- Diff-first: inspect changed hunks before entire files.
- Index-first: search filenames/symbols before directory-wide reads.
- Evidence pointers: remember command + result summary + commit/file hash, not huge logs.
- Use `evidence_engine.py assess --compact` or `decision_engine.py --compact`; do not inject the full `.agent/evidence.jsonl` into model context.
- Summarize tool noise: retain failing assertion, stack root, counts, and exit status.
- Reuse verified commands from memory instead of rediscovering build/test syntax.
- Use fresh subagents/workers for isolated tasks when the harness supports them; pass a compact task packet rather than the whole conversation.
- After a milestone, create a short checkpoint summary and drop obsolete scratch context.

## Never optimize away
Do not save tokens by skipping tests, security checks, required files, user constraints, or review on risky work. Token economy is subordinate to correctness and safety.
