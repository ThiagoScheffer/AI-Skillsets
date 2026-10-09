# Audit Methodology

## Objective

Assess five security categories against the repository's actual architecture. Do not search for a predetermined number of vulnerabilities. Report only issues supported by concrete code/configuration evidence.

The audit is inspired by OWASP ASVS 5.0, OWASP API Security Top 10, OWASP Cheat Sheet Series, and relevant CWE definitions. Use them as verification guidance, not as a substitute for understanding the application's intended access model.

## Phase A - Establish the security model

Determine:

- repository/project boundaries and monorepo structure;
- backend languages/frameworks and exposed APIs;
- ORM/query builder/database client and databases;
- authentication provider/session/token mechanisms;
- authorization architecture: RBAC, ABAC, policies, ACLs, ownership, memberships, relationships;
- tenant/user isolation mechanism and where it is enforced;
- frontend frameworks and privilege-gating patterns;
- webhooks, workers, queues, serverless/edge functions, scheduled jobs;
- deployment, CI/CD, Docker, Kubernetes/Helm, Terraform/IaC, environment and secret configuration.

Authentication answers "who is the caller?" Authorization answers "may this caller perform this action on this resource/field?" Tenant isolation answers "which data universe may this caller ever reach?" Keep these concepts separate.

## Phase B - Build coverage inventories

### Backend inventory

Systematically enumerate application-controlled endpoints/entry points such as:

- REST routes/controllers;
- GraphQL queries/mutations/resolvers;
- RPC procedures;
- server actions;
- edge/serverless functions;
- webhooks;
- admin endpoints;
- report/export endpoints;
- background-job entry points that consume user-supplied identifiers or tenant context.

For each relevant handler record:

`Method/action | Route/function | Authn | Function authz | Tenant scope | Object authz | Data operation | Evidence`

### Frontend privilege inventory

Search for role/permission gates such as `isAdmin`, `isOwner`, `role`, `permission`, `canEdit`, `canDelete`, route guards, protected menus, disabled controls, and equivalent framework patterns.

Map every security-relevant client gate to the trusted backend operation it triggers. Confirm that the backend enforces an equivalent or stronger rule.

### Sensitive sinks and secret surface

Inventory:

- HTML/DOM/code-evaluation sinks;
- Markdown/rich-text renderers;
- user-controlled URL sinks;
- server-side HTML email/template paths;
- configuration, scripts, CI, Docker, Compose, Helm/Kubernetes, Terraform/IaC, docs/examples;
- frontend public environment behavior and produced bundles when available;
- Git history availability.

## Phase C - Verify, do not infer

A candidate becomes a finding only after establishing:

1. the affected code path is reachable or relevant;
2. the attacker-controlled input or missing authorization boundary;
3. the current control that should prevent abuse;
4. why that control is absent, bypassed, or insufficient;
5. the resulting impact and necessary exploitability conditions.

If one of these cannot be established from available evidence, either reject the candidate or place it in Manual Follow-up with the missing evidence clearly identified.

## Phase D - Remediation

Prefer fixes that make unsafe states hard to represent:

- centralized deny-by-default authorization;
- tenant-scoped repositories/querysets instead of scattered predicates;
- object lookup through the caller's allowed scope;
- allowlisted writable fields/DTOs for field-level authorization;
- provider-supported secret stores and fail-closed startup validation;
- safe rendering APIs and context-specific output handling;
- regression tests that reproduce the authorization/security boundary.

Do not provide vague advice such as "sanitize input" or "add authorization" when a stack-native control is identifiable.

## Phase E - Reporting

The canonical output is `audit-results.json`. The PDF and GitHub issue text are derived from it.

The report must distinguish:

- verified findings;
- verified strengths;
- audit coverage;
- limitations/manual follow-up.

A clean audit means "no verified findings within the reviewed scope," not "the application is secure."
