# Risk Tiers

Risk tier controls process depth. It is not a judgment of developer skill or product value.

## R0 - trivial

Examples: copy edit, visual spacing, comment, safe refactor with no observable behavior change.

Default: implement with proportionate checks.

## R1 - bounded

Examples: simple CRUD endpoint, isolated UI state, low-risk feature with no sensitive data or trust-boundary change.

Default: lightweight requirement + acceptance criteria + implementation/verification.

## R2 - significant

Indicators include:
- authentication/authorization
- personal information
- payments
- tenant boundaries
- external APIs/webhooks
- new persistent data model
- migrations
- materially new subsystem
- externally observable compatibility contract
- significant performance/availability requirement

Default: full design lifecycle.

## R3 - high assurance

Indicators include:
- government/public-service systems
- health/safety/critical infrastructure
- high-impact financial processing
- broad privileged access
- high-value secrets or identity infrastructure
- severe availability consequences
- consequential autonomous AI actions
- explicit regulatory/high-assurance mandate

Default: full lifecycle plus authority gates and high-assurance controls.

## Classification method

Use the highest justified tier after considering:
- confidentiality
- integrity
- availability
- privacy
- financial impact
- external contract impact
- reversibility
- blast radius
- regulatory exposure
- operational complexity

Document the concrete factors; do not merely output a tier label.
