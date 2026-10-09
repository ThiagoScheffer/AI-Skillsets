# Adapter - Java / Kotlin

Applicable to Spring/Spring Boot, Jakarta/JAX-RS, Micronaut, Quarkus, and similar stacks.

## Authorization

Inventory controller mappings and security configuration. In Spring, examine filter chains, request matchers, method security (`@PreAuthorize`, etc.), service checks, and whether method security is enabled. Verify sensitive routes are not accidentally matched by broader permit rules.

## Data/object access

Review JPA/Hibernate/Spring Data repository calls, specifications, query annotations, and native SQL for tenant/object scope. Check that user-supplied tenant IDs are validated against authenticated memberships.

## Field authorization

Generic request-to-entity binding can expose protected fields. Prefer explicit request DTOs and server-assigned privilege/ownership fields.

## XSS

Review template escaping, raw response construction, HTML email generation, sanitizer usage, and frontend modules separately.
