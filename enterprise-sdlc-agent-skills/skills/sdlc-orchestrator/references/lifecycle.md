# Lifecycle Reference

## States

1. `discovery`
2. `prd`
3. `requirements`
4. `ux`
5. `system-design`
6. `architecture-security`
7. `implementation-plan`
8. `implementation`
9. `verification`
10. `release`
11. `operations`

A project may revisit previous states. Lifecycle progression is not strictly linear.

## Minimum evidence by risk

### R0
- change intent is clear
- appropriate local verification exists

### R1
- bounded requirement/acceptance criteria
- implementation plan or task note
- regression evidence

### R2
- PRD or equivalent product requirement source
- requirement registry
- system design
- material ADRs
- security/privacy analysis when applicable
- implementation plan
- verification plan and evidence
- release/rollback thinking

### R3
Everything in R2 plus:
- explicit human gates for product/design/security/release as appropriate
- higher assurance profile
- deeper failure, resilience and operational analysis
- compliance mappings required by the selected profile
