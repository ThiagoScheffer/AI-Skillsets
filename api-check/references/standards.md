# Standards Basis

Use these as the normative/authoritative starting points when a review turns on protocol semantics or security details. Prefer the repository's declared contract version and do not upgrade a public API merely because a newer specification exists.

- HTTP semantics and method/idempotency rules: RFC 9110 — https://www.rfc-editor.org/rfc/rfc9110
- Problem Details for HTTP APIs: RFC 9457 — https://www.rfc-editor.org/rfc/rfc9457
- HTTP Basic authentication: RFC 7617 — https://www.rfc-editor.org/rfc/rfc7617
- OAuth 2.0 Bearer Token Usage: RFC 6750 — https://www.rfc-editor.org/rfc/rfc6750
- JSON Web Token: RFC 7519 — https://www.rfc-editor.org/rfc/rfc7519
- JWT Best Current Practices: RFC 8725 — https://www.rfc-editor.org/rfc/rfc8725
- OAuth 2.0 Security Best Current Practice: RFC 9700 — https://www.rfc-editor.org/rfc/rfc9700
- OpenAPI Specification: use the version declared by the document; the current published branch is available at https://spec.openapis.org/oas/latest.html
- GraphQL specification: https://spec.graphql.org/
- gRPC official documentation: https://grpc.io/docs/
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP CSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

When external lookup is available and the user asks for compliance with the latest standard, verify the latest published version/date before making version-specific claims.
