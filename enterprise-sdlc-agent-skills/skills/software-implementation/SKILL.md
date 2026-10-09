---
name: software-implementation
description: Use to implement a defined software task while preserving architecture, requirements traceability, tests, security controls, documentation and project-specific repository conventions.
---

# Software Implementation

Implement the defined task without silently redesigning the system.

## Before editing

Identify:
- task ID
- requirements/acceptance criteria
- impacted architecture sections/ADRs
- expected verification
- security/privacy controls
- repository-specific instructions and commands

## Workflow

1. inspect relevant existing code and tests
2. identify the smallest coherent change
3. implement following local conventions
4. update/add proportionate tests
5. run targeted checks, then broader checks as justified
6. inspect the resulting diff for unintended effects
7. update documentation/contracts/traceability affected by the change

## Design feedback loop

If implementation reveals that the approved design is invalid, unsafe, or materially incomplete, stop normal coding, record the contradiction, update/review the design or ADR, then resume.

Do not fabricate successful command output or claim a test ran when it did not.
