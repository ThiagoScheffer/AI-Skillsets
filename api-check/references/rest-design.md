# REST and HTTP Design Reference

## 1. Resource and URI modeling

Prefer stable identifiers for resources and domain concepts. A collection such as `/users` and an item such as `/users/{userId}` is predictable, but plural nouns are a convention rather than a REST law. Follow the repository's established naming convention unless it is internally inconsistent or materially harmful.

Avoid action-heavy routes such as `/getUsers` or `/deleteProduct/{id}` when normal HTTP methods already express the operation. For operations that are genuine domain commands, model a command/action resource or subordinate resource when that produces clearer semantics, for example `POST /orders/{id}/cancellations`. Do not distort a domain model merely to avoid every verb in every URI.

Paths identify the target. Query parameters refine retrieval or processing: filters, sorting, search, pagination, sparse fieldsets, expansions, and similar optional criteria. Do not use `GET /resource?action=delete` for a state change.

## 2. Method semantics

- `GET`: retrieve a representation; safe and idempotent by intended semantics.
- `HEAD`: same retrieval semantics as GET without response content; safe and idempotent.
- `POST`: process content according to target-resource semantics; often creates a subordinate resource, but may represent commands or processing. Not defined as idempotent by HTTP, though an application can design a POST operation to be retry-safe.
- `PUT`: create or replace the state of the known target resource. Idempotent by intended effect.
- `PATCH`: apply partial modifications according to the patch document/media type. Do not assume every PATCH format has identical conflict or idempotency properties.
- `DELETE`: remove the association/functionality of the target URI. Idempotent by intended effect; repeated requests may return different status codes while remaining idempotent.

For retry-sensitive POST operations such as payments or order creation, consider an idempotency-key contract with defined key scope, retention window, replay behavior, and response reuse.

## 3. Status codes

Use the status line to communicate the protocol-level outcome.

Common success cases:
- `200 OK`: successful request with a response representation.
- `201 Created`: one or more resources created; provide `Location` when there is a canonical URI that benefits the client.
- `202 Accepted`: accepted but not completed; expose a way to observe eventual status when asynchronous processing matters.
- `204 No Content`: successful request with no response content.

Common client-error cases:
- `400 Bad Request`: malformed or otherwise invalid request at the HTTP/application parsing layer.
- `401 Unauthorized`: authentication credentials are missing, invalid, or otherwise insufficient to establish the required authentication; include the relevant challenge semantics when applicable.
- `403 Forbidden`: the request is understood but the authenticated/identified principal is not permitted, or policy intentionally denies it.
- `404 Not Found`: target resource is not found or is intentionally concealed as such.
- `409 Conflict`: request conflicts with current resource state, version, uniqueness, or concurrent transition.
- `412 Precondition Failed`: conditional request precondition failed; useful with ETags and optimistic concurrency.
- `422 Unprocessable Content`: request content is syntactically understood but cannot be processed semantically. Do not use it as a catch-all for every domain error.
- `429 Too Many Requests`: rate limit or quota enforcement; include retry metadata where useful.

Choose between 409 and 422 from semantics, not house style alone: 409 is usually about conflict with current state; 422 is usually about the submitted content being semantically unprocessable.

## 4. Structured errors

Prefer RFC 9457 problem details for new HTTP APIs unless compatibility requires another stable envelope. Use `application/problem+json` and keep the core fields semantically correct. Add extension members for stable machine-readable error codes and field violations when useful.

A validation response should identify actionable fields/paths without leaking secrets, internal stack traces, SQL fragments, signing details, or private topology.

Keep authentication failures intentionally non-enumerative where revealing whether an account exists would increase risk.

## 5. Collections, filters, and pagination

Use one consistent convention across collection endpoints. Define:
- filter syntax and supported fields;
- sort field syntax and default order;
- pagination model (cursor/keyset preferred for large mutable datasets; offset can be fine for simpler stable datasets);
- page-size limits;
- response metadata or links;
- deterministic ordering when pagination requires it.

Do not silently change pagination semantics between endpoints.

## 6. Compatibility and versioning

Classify every contract change:
- **Additive-compatible:** usually a new optional operation, optional request field with safe default, or response field for clients that tolerate unknown fields.
- **Conditionally compatible:** behavior depends on generated clients, strict decoders, validation, enums, schema settings, or documented assumptions.
- **Breaking:** removed/renamed fields, changed types/meaning, narrower accepted inputs, changed requiredness, incompatible auth, changed identifiers, changed status/error semantics, or behavior that invalidates existing client assumptions.

Do not version reflexively. Prefer additive evolution and explicit deprecation when possible. When a breaking version is necessary, use one consistent mechanism and publish a migration path and deprecation window appropriate to the API's consumers.

## 7. Representation consistency

Keep stable conventions for:
- JSON property casing;
- nullability versus omission;
- identifiers and identifier types;
- timestamps and time zones;
- monetary values and currency representation;
- enum evolution;
- pagination and error envelopes;
- correlation/request identifiers;
- content types and charset behavior.

JSON is common, not mandatory. Respect content negotiation and existing media-type contracts where applicable.
