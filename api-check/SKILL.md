---
name: api-check
description: Review, design, implement, and refactor application APIs and API contracts, including REST/OpenAPI, GraphQL, gRPC, authentication/token handling, resource and URL modeling, HTTP methods and idempotency, status codes, structured errors, filtering/pagination, compatibility/versioning, and format consistency. Use when Codex is asked to check or audit an API, review an OpenAPI specification or endpoint code, design backend interfaces, choose REST vs GraphQL vs gRPC, fix API semantics, or assess Basic, opaque bearer-token, or JWT authentication.
---
# API Check

Use this skill to make an API predictable, semantically correct, secure-by-default, and easy for clients to integrate with. Treat the user's requirements and the repository's established contract as primary evidence; do not rewrite working public contracts merely to satisfy stylistic preferences.

## Workflow

1. **Identify the task mode.**
   - For an audit/review request, inspect and report findings. Do not change files unless the user also asks to fix or implement.
   - For a design request, produce a concrete contract before implementation.
   - For an implementation/refactor request, inspect the existing architecture, modify the smallest coherent surface, and run relevant tests/lint/type checks.
   - For protocol selection, compare REST, GraphQL, and gRPC against the actual workload rather than picking by trend.

2. **Establish the contract surface.**
   Inspect API routes, controllers/handlers, OpenAPI documents, GraphQL schemas/resolvers, `.proto` files, auth middleware, client SDKs, tests, and public documentation when present. Identify whether the API is public, browser-facing, mobile-facing, internal service-to-service, or mixed.

3. **Review interface semantics.**
   Read [references/rest-design.md](references/rest-design.md) for REST/HTTP work. Check resource modeling, paths, methods, safety/idempotency, status codes, query parameters, pagination, structured errors, consistency, and compatibility.

4. **Select or verify the protocol.**
   Read [references/protocol-choice.md](references/protocol-choice.md) when choosing or comparing REST, GraphQL, or gRPC. Do not claim one protocol is universally faster or superior.

5. **Review authentication and authorization.**
   Read [references/auth-security.md](references/auth-security.md) for Basic auth, opaque bearer tokens, JWT/JWS/JWE, cookie storage, refresh tokens, CSRF, and revocation. Distinguish authentication from authorization. Distinguish bearer-token semantics from token format: a JWT can itself be a bearer token.

6. **Run deterministic contract checks when OpenAPI is available.**
   Execute `python scripts/check_openapi.py <openapi-file>`. Treat its output as heuristic evidence, not as a substitute for semantic review. For OpenAPI 3.2.x, preserve valid 3.2 features rather than downgrading the document to older tooling assumptions.

7. **Prioritize findings.**
   Use [references/review-rubric.md](references/review-rubric.md). Rank concrete defects above stylistic preferences. Cite exact file paths and line numbers whenever available.

8. **Resolve standards-sensitive questions.**
   Read [references/standards.md](references/standards.md) when a finding depends on normative HTTP, JWT/OAuth, OpenAPI, GraphQL, gRPC, or browser-security semantics. Verify current versions when the user explicitly asks for the latest standard.

9. **Validate changes.**
   Run the repository's existing tests first. Then run relevant contract validation, generated-client checks, schema checks, type checks, and focused integration tests. Add tests for changed behavior, especially retries/idempotency, authentication failures, authorization boundaries, validation errors, and backward compatibility.

## Engineering Rules

- Let the URI identify the target resource or domain concept and let the HTTP method carry standard operation semantics when using HTTP APIs.
- Permit command/action resources when a domain operation does not map cleanly to CRUD; avoid forcing awkward noun-only designs.
- Treat GET and HEAD as safe. Treat safe methods, PUT, and DELETE as idempotent in their intended effect. Do not assume POST is inherently non-idempotent; an application can make it retry-safe with explicit semantics such as idempotency keys.
- Treat PUT as create-or-replace at a known target URI; treat PATCH as a partial modification whose semantics depend on the patch media type/contract.
- Do not report repeated DELETE responses as a violation merely because the second response differs; idempotency concerns intended server effect, not identical response bytes.
- Use HTTP status codes as protocol-level outcomes. Do not return `200` for an operation that semantically failed merely to carry an error object.
- Prefer RFC 9457 `application/problem+json` for HTTP API problem details unless the existing public contract has a stable alternative error envelope.
- Use query parameters for optional filtering, sorting, search, sparse fieldsets, and pagination. Do not encode state-changing commands as `GET ?action=...`.
- Preserve backward compatibility by default. Classify changes as additive-compatible, conditionally compatible, or breaking; do not assume every added field is harmless to every client.
- Do not describe HTTP itself as meaning the server has “zero memory.” HTTP request semantics are stateless across requests, but applications can and often do maintain server-side state.
- Do not equate bearer tokens with opaque tokens. “Bearer” describes how possession authorizes use; opaque versus JWT/self-contained describes token representation.
- Do not say JWTs eliminate database/cache access or “scale infinitely.” Local signature verification can reduce token introspection, but authorization state, revocation, key distribution, tenancy, and account status may still require external state.
- Do not claim all JWTs have exactly three parts. A compact JWS commonly has three segments; a compact JWE has five.
- Do not claim a JWT payload is always merely Base64URL-readable. Signed/MACed JWS payloads are readable; JWE provides encryption.
- Never place secrets or credentials in JWT claims merely because the token is signed.
- Prefer asymmetric signing when many services verify tokens but should not gain signing authority. Do not call it mandatory without architectural evidence.
- For browser sessions, prefer `Secure` + `HttpOnly` cookies or a BFF pattern when appropriate; treat `SameSite` as defense in depth, not a complete CSRF solution.
- Never recommend storing session identifiers, refresh tokens, or equivalent credentials in `localStorage` as a default pattern.
- For OAuth-style refresh tokens in public clients, require replay defenses such as refresh-token rotation or sender-constrained tokens according to current security best practice.
- Pin accepted JWT algorithms and validate issuer, audience, expiration/not-before as required by the trust model. Do not trust claims before cryptographic validation.
- Never invent performance claims. If performance determines REST vs GraphQL vs gRPC, request or run workload-representative measurements when possible.

## Output Contract

For **reviews**, return:

1. Verdict and scope.
2. Findings ordered by `P0`, `P1`, `P2`, `P3`, each with evidence, impact, and exact remediation.
3. A compact scorecard using the rubric.
4. Contract examples only where they clarify a finding.
5. Validation performed and residual risks.

For **design/implementation**, return:

1. Chosen protocol and why it fits the workload.
2. Contract summary: resources/services, methods/RPCs, status/error model, auth, pagination/filtering, and versioning policy.
3. Files changed and tests/validation run.
4. Any intentional compatibility trade-off or unresolved risk.

Do not bury critical correctness or security issues behind style commentary.
