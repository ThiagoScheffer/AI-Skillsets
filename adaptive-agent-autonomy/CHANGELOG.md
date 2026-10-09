# Changelog

## 0.2.0 — Evidence & Reputation Engine

- Added project-local, task-scoped evidence/reputation scoring with recency decay and failure penalties.
- Added deterministic promotion criteria for `routine-proven` work: >=3 verified successes, stable tests, low blast radius, known rollback, no recent failure, and score >=82.
- Added `decision_engine.py` to combine classification and operation gating into one machine-readable next-step decision.
- Added explicit `--human-approved` handling so approval can unlock an exact operation without weakening verification requirements.
- Corrected safe-step behavior: inspect/plan/test remain autonomous even when the eventual mutation is high-risk.
- Added compact assessment output to reduce context/token usage.
- Added regression tests for earned autonomy, demotion after failures, protected domains, and approval semantics.
- Added portable Superpowers ensure/install helper.
