# Category 2 - Privileged Authorization Enforced Only in the Client

## Goal

Verify function-level and field-level authorization in a trusted server/service layer.

OWASP ASVS 5.0 requires authorization at a trusted service layer rather than client-side controls. OWASP's Authorization Cheat Sheet recommends deny-by-default and permission validation on every request.

## Workflow

1. Enumerate frontend privilege gates.
2. Identify the API/server action/RPC/GraphQL mutation each gate invokes.
3. Identify alternate routes to the same business operation.
4. Verify trusted backend enforcement for the required role/permission on every path.
5. Review field/property-level authorization for privileged attributes.

## Sensitive operations

Include:

- admin consoles/actions;
- organization/workspace settings;
- membership/invitations;
- role/permission changes;
- owner transfer;
- writes/deletes/publish/approve/export;
- billing-sensitive settings;
- security configuration;
- feature management;
- support/impersonation capabilities.

## Field-level authorization

A caller authorized to edit an object is not automatically authorized to edit all fields. Review mass assignment / generic updates involving fields such as:

`role`, `permissions`, `owner_id`, `tenant_id`, `organization_id`, `workspace_id`, `status`, `approved`, `is_admin`, billing/security flags.

Prefer explicit writable DTO/schema fields or server-side assignment of protected properties.

## Finding threshold

Report only when a non-privileged caller can invoke a trusted backend operation requiring privileges they do not possess, or can modify a protected field without the required authorization.

Do not report UI hiding alone.

## Preferred remediation

- centralized policy/guard/middleware with deny-by-default semantics;
- explicit per-function permission requirements;
- server-side derivation of sensitive fields;
- regression tests calling the backend directly as a lower-privilege user;
- test alternate methods/routes, not only the UI path.
