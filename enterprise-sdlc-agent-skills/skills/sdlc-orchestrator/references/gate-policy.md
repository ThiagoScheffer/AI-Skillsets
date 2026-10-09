# Gate Policy

## Gate categories

### Automated gates
May be marked by deterministic evidence, for example:
- schema validation
- build
- type checking
- lint/static analysis
- unit/integration/contract/e2e tests
- security scanners
- dependency checks
- traceability validation
- artifact consistency checks

### Human/authority gates
Must never be fabricated by the agent:
- product scope approval
- material architecture approval where required
- privacy/security risk acceptance
- exception approval
- production release authorization

## Gate states

- `not_required`
- `pending`
- `ready_for_review`
- `approved`
- `rejected`
- `blocked`
- `superseded`

## Rule

A gate is only `approved` when its configured approval source exists. Passing tests does not imply human approval. Human approval does not imply passing automated verification.
