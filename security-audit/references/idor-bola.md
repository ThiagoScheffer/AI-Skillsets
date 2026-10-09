# Category 3 - IDOR / BOLA

## Goal

Verify object-level authorization for every backend handler that uses an untrusted object identifier.

OWASP API1:2023 notes that identifiers may appear in paths, queries, headers, or request payloads and can be integers, UUIDs, strings, or other keys. Unguessable identifiers reduce discovery but are not authorization.

## Inventory

Enumerate handlers receiving or deriving identifiers from:

- path params;
- query params;
- request bodies/forms;
- GraphQL arguments;
- RPC parameters;
- headers;
- filenames/slugs/usernames;
- nested resource identifiers;
- decoded tokens or state objects containing resource IDs.

For every read/update/delete/action determine how the object is constrained to the caller's allowed scope.

## Secure patterns

Prefer lookups such as:

- object queried through caller-owned/tenant-scoped relation;
- policy/permission evaluation against the loaded object;
- repository method that requires trusted tenant/user context;
- DB row policy that applies to the effective database role, with no privileged bypass.

A later ownership check can be correct, but verify it occurs before sensitive data/action and is applied on every code path.

## Nested resources

For `/organizations/:orgId/projects/:projectId`, verify the caller is allowed into the organization and the project belongs to/relates to that organization as intended. Checking that both IDs independently exist is insufficient.

## Finding threshold

Report only when changing/supplying an identifier can access, mutate, delete, or invoke an action on an unauthorized object.

Do not report simply because an ID originates from the client.

## Preferred remediation

- scope the lookup itself to allowed objects;
- centralize object policies where supported;
- avoid trusting `user_id`/`tenant_id` supplied in request bodies;
- add negative tests using two users/two tenants and object IDs from the other principal.
