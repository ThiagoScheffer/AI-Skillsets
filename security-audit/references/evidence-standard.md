# Finding Evidence Standard

A finding is acceptable only when another engineer can reproduce the reasoning from repository evidence.

## Required fields

Every finding must include:

- unique ID such as `SEC-001`;
- one primary category;
- severity;
- concise title;
- affected component;
- exact current `file:line` references;
- minimal redacted code evidence;
- attacker-controlled source or missing authorization boundary;
- control/data-flow explanation;
- attacker prerequisites;
- exploitability conditions;
- concrete impact;
- why current defenses do not prevent exploitation;
- stack-native remediation;
- a regression/security test;
- relevant OWASP/CWE mapping when appropriate.

## Line accuracy

Obtain line numbers from the final checked-out source after any audit-generated files are written. Do not estimate.

For a historical-only secret no longer present in current files, use:

`commit <SHA> | <path> | <hunk/context>`

## Code snippets

Use the smallest snippet that proves the point. Never include full real credentials. Redact sensitive values before writing any artifact.

## Proof rules by category

### Tenant isolation

Show the data operation, trusted tenant source, and missing/bypassed scope.

### Function authorization

Show the privileged operation and the missing/insufficient trusted backend check. A client role gate can be supporting evidence, not the sole proof.

### IDOR/BOLA

Show the untrusted identifier and the lookup/action lacking object authorization. Explain how an ID belonging to a different authorized principal would pass.

### Secrets

Establish that the value is genuinely privileged based on provider semantics or repository use. Do not call examples/placeholders secrets without evidence.

### XSS

Show source-to-sink flow and why escaping/sanitization/URL validation is absent or ineffective in the sink context.

## Reject or downgrade candidates when

- the route is dead/generated/test-only and cannot affect relevant environments;
- a lower trusted layer provably enforces the missing check;
- a value is public by provider design;
- framework auto-escaping makes the alleged XSS path non-executable;
- exploitability depends on configuration that is explicitly prevented;
- the evidence is incomplete.

Important unresolved items belong under `limitations` or `manual_follow_up`, not under `findings`.

## Strength evidence

Strengths should identify what was actually checked, e.g.:

- router/controller family where every handler used the same ownership policy;
- RLS migration/policies protecting an exposed table set;
- backend guard mirroring all discovered admin UI gates;
- sanitizer applied at every discovered rich-text sink;
- startup validation rejecting default secrets.

Avoid vague praise.
