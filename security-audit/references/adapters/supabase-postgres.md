# Adapter - Supabase / PostgreSQL

Load when Supabase or PostgreSQL RLS is part of the security boundary.

## Detect

Look for `@supabase/supabase-js`, Supabase CLI/config, migrations under `supabase/`, SQL policies, `auth.uid()`, `auth.jwt()`, `create policy`, `enable row level security`, Storage policies, edge functions, and Supabase environment keys.

## Isolation

Inventory exposed tables/views/functions and determine which roles can access them. Review both grants and RLS policies. Check select/insert/update/delete semantics, including `USING` and `WITH CHECK` where appropriate.

Trace privileged server clients. A secret/service-role credential can bypass RLS, so a user-request path using it must enforce authorization in the trusted application layer.

Review `SECURITY DEFINER` functions, RPCs, views, custom roles with `BYPASSRLS`, and Storage policies.

## Secret semantics

Do not flag `sb_publishable_...` or legacy anon keys solely for client exposure. Treat `sb_secret_...` and legacy service-role keys as privileged. Re-check current Supabase docs for the exact credential generation in the project.

## Regression tests

Use two users and preferably two tenants. Test list/search/export and object actions with one tenant attempting to reference another tenant's rows. If testing RLS directly, exercise the effective unprivileged role/JWT rather than only an owner/admin DB connection.
