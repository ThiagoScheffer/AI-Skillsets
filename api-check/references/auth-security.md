# Authentication and API Security Reference

## 1. Separate authentication from authorization

Authentication establishes the caller's identity or credential context. Authorization decides what that caller may do. Enforce both at the appropriate boundary; successful authentication must never imply broad authorization.

HTTP being stateless does not mean an application cannot maintain sessions or server-side state. Cookies, session stores, token stores, caches, and databases can all participate in authentication.

## 2. Basic authentication

HTTP Basic transmits a Base64-encoded username/password credential in the `Authorization` header. Base64 is encoding, not encryption. Require HTTPS/TLS and protect credentials at rest, in logs, traces, crash dumps, CI configuration, and secret stores.

Use Basic only when its simplicity fits the threat model and operational context. Do not label it automatically safe merely because a system is “internal.” Prefer scoped, rotatable machine credentials/tokens when they provide better containment.

## 3. Bearer tokens: representation vs usage

A bearer token grants access to whoever possesses it. The token may be opaque or self-contained. A JWT is often used *as a bearer token*, so “bearer token vs JWT” is not a clean type distinction.

Opaque tokens can be validated through a session/token store, cache, authorization server introspection, or another service. Do not assume each request requires a direct database query.

Self-contained access tokens can reduce introspection by allowing local cryptographic validation, but callers may still need external state for revocation, account disablement, tenant policy, dynamic permissions, or key discovery.

## 4. JWT details

JWT is a claims container represented using JWS and/or JWE constructions.

- A compact JWS normally has three dot-separated segments and provides integrity/authenticity when correctly verified; its payload is generally readable.
- A compact JWE has five segments and provides encryption.
- `typ` is not universally mandatory and must not be described as “always JWT.”
- Registered claims such as `iss`, `sub`, `aud`, `exp`, `nbf`, and `iat` are context-dependent; define which are required by the trust model.

For signed JWT access tokens:
- verify the cryptographic signature before trusting claims;
- pin/allowlist acceptable algorithms rather than accepting whatever the token header requests;
- validate issuer and audience where multiple issuers/resources exist;
- enforce expiration and not-before semantics with carefully bounded clock skew;
- validate key identifiers and JWKS/key selection safely;
- keep sensitive secrets out of readable claims;
- keep token lifetime no longer than the actual risk model justifies.

Prefer asymmetric signing when one authority should sign and many services should verify without receiving signing capability. Symmetric HMAC can be appropriate in smaller trust domains where all verifiers are allowed to sign; sharing an HMAC key expands signing authority.

## 5. Revocation and refresh

JWT revocation is not impossible; it is less inherently centralized than deleting an opaque server-side session. Available controls include short access-token lifetimes, deny/revocation lists, token-version checks, account/session state checks, key rotation for scoped incidents, and introspection-based designs.

Refresh-token design is independent of whether the access token is a JWT. Keep refresh tokens more protected than ordinary API access tokens because they mint new access. For public OAuth clients, use sender-constrained refresh tokens or refresh-token rotation/replay detection in line with current OAuth security best current practice.

Do not hard-code “15 minutes” or “7 days” as universal lifetimes. Select lifetimes from threat model, device/client type, revocation capability, user experience, and regulatory requirements.

## 6. Browser token storage

Do not default to `localStorage`/`sessionStorage` for session IDs, refresh tokens, or equivalent bearer credentials: any JavaScript executing in the origin can read them.

For browser sessions, `Secure; HttpOnly` cookies or a Backend-for-Frontend pattern are often safer defaults because JavaScript cannot directly read HttpOnly cookies. This mitigates token theft through XSS but does not make XSS harmless; malicious script can still act as the user while it executes.

Treat `SameSite=Strict` or `Lax` as CSRF defense in depth, not a complete CSRF strategy. Depending on the application, also use CSRF tokens, Origin/Referer validation, Fetch Metadata, non-simple request patterns, or equivalent framework defenses. Evaluate subdomain trust because same-site is broader than same-origin.

## 7. Authorization controls

Check authorization on the server for every protected operation and object boundary. Look specifically for:
- BOLA/IDOR: user can access another user's object by changing an ID;
- broken function-level authorization: low-privilege user can invoke admin operations;
- tenant boundary bypass;
- stale role/permission claims in long-lived self-contained tokens;
- mass assignment of privileged fields;
- authorization enforced only in the UI/client.

Prefer policy decisions based on trusted server context, not arbitrary client-supplied role or tenant fields.

## 8. Failure handling

Use `401` for missing/invalid authentication where appropriate and `403` for authenticated/known callers that are not authorized, while allowing deliberate `404` concealment policies when justified. Avoid account enumeration, secret-bearing logs, raw token logging, and detailed cryptographic failure messages to untrusted clients.
