# API Review Rubric

Use this rubric to prioritize defects. Do not fabricate a numeric score when the reviewed evidence does not cover a category; mark it `N/A` and state the evidence gap.

## Severity

- **P0 — Critical:** likely auth bypass, cross-tenant exposure, credential leakage, destructive unauthenticated mutation, or a contract defect causing catastrophic data/security impact.
- **P1 — High:** broken authorization boundary, unsafe retry/payment duplication risk, severe compatibility break, incorrect method semantics causing side effects on safe requests, or systematic error handling that misleads clients.
- **P2 — Medium:** meaningful integration/reliability problem, inconsistent status/error contract, weak pagination/filtering semantics, avoidable token/security weakness without immediate exploit evidence, or hard-to-migrate design debt.
- **P3 — Low:** naming inconsistency, documentation mismatch, ergonomics issue, or non-breaking cleanup with limited operational impact.

## Scorecard

Score only categories supported by evidence.

| Category | Weight | Questions |
| --- | ---: | --- |
| Resource/interface modeling | 15 | Are targets and operations understandable and stable? Are command endpoints used intentionally? |
| HTTP/RPC semantics | 15 | Are methods, safety, idempotency, retries, streaming, and deadlines correct? |
| Status and error model | 15 | Do protocol status and machine-readable details agree? Is validation actionable and stable? |
| Collections/query behavior | 10 | Are filters, sorting, pagination, limits, and ordering consistent? |
| Compatibility/evolution | 10 | Are breaking changes controlled, deprecated, and migratable? |
| Authentication/authorization | 20 | Are credentials protected, claims validated, authorization enforced, and revocation/storage appropriate? |
| Protocol fit | 10 | Does REST/GraphQL/gRPC match the actual clients and workloads? |
| Validation/operability | 5 | Are contracts tested, observable, and failure/retry behaviors verified? |

## Review method

1. Find concrete evidence before asserting a defect.
2. Report security and correctness issues before style.
3. Separate standards violations from organization preferences.
4. Distinguish a theoretical risk from an observed exploit path.
5. For every P0/P1/P2 finding, state impact and exact remediation.
6. For implementation requests, add or update tests that would fail before the fix and pass after it when practical.
7. State what was not reviewed: infrastructure, gateway config, identity provider, client storage, production headers, etc.
