# Category 1 - Tenant / Owner Isolation

## Goal

Verify that data operations cannot cross the authenticated caller's permitted user/organization/workspace/account boundary.

OWASP ASVS 5.0 explicitly requires cross-tenant controls and data-specific authorization. Treat isolation as a system invariant, not just an endpoint concern.

## First determine the project's isolation mechanism

Examples:

- PostgreSQL/Supabase RLS policies;
- tenant-aware DB session/context;
- global ORM/query scopes;
- repository/service wrappers that always inject tenant scope;
- middleware that establishes a trusted tenant from membership;
- manual predicates such as `tenant_id = authenticatedTenantId`;
- ACL/relationship-based filters.

Do not assume a missing `user_id` predicate is vulnerable if a lower trusted layer already applies the correct scope.

## Systematic checks

Pay special attention to operations that commonly bypass object-by-object checks:

- lists and feeds;
- search/autocomplete;
- pagination;
- aggregates/counts/statistics;
- dashboards;
- reports;
- CSV/PDF/export endpoints;
- bulk mutation/deletion;
- background jobs;
- admin/support queries;
- joins/subqueries/views that reintroduce cross-tenant rows;
- cache keys that omit tenant identity.

For each data path ask:

1. Where does the tenant/user scope originate?
2. Can the caller supply or override it?
3. Is membership validated before using an organization/workspace ID?
4. Does the data-access layer constrain every relevant table/relationship?
5. Can a privileged server credential bypass lower-layer policies?

## Supabase/Postgres-specific

When applicable verify:

- RLS is enabled for exposed tables;
- grants and policies both match intended operations;
- `USING` protects row visibility/target rows;
- `WITH CHECK` prevents writes that move/create rows outside allowed scope where relevant;
- views/functions/RPCs do not unintentionally execute with elevated privileges;
- `SECURITY DEFINER`, owner roles, `BYPASSRLS`, service-role/secret credentials are understood;
- backend clients with RLS-bypassing credentials apply equivalent authorization before querying;
- Storage policies are reviewed separately when user files are in scope.

## Finding threshold

Report when there is a concrete reachable operation that can read/affect another unauthorized tenant/user scope, or a verified policy/configuration condition directly enabling that access.

Do not duplicate a single object-by-ID issue here when Category 3 is the precise root cause. Cross-reference instead.

## Preferred remediation patterns

- derive tenant identity from authenticated membership, not arbitrary request fields;
- use scoped repository/queryset APIs that require trusted tenant context;
- make the DB policy a defense-in-depth boundary when feasible;
- avoid privileged DB credentials in user-request paths unless the service enforces equivalent scope;
- add cross-tenant negative tests for list/search/report/export and bulk operations.
