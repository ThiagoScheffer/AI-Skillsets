# Category 4 - Hardcoded / Exposed Secrets

## Scope

Review current source/configuration and relevant Git history for privileged credentials such as:

- API keys/tokens;
- passwords/database credentials;
- JWT/session/signing secrets;
- webhook signing secrets;
- OAuth client secrets;
- private keys/certificates containing private material;
- cloud/service-account credentials;
- encryption keys;
- default administrative credentials;
- provider credentials with elevated data-plane/control-plane privileges.

Search source, configs, `.env*`, Docker/Compose, Kubernetes/Helm, Terraform/IaC, CI, scripts, seeds/fixtures, tests, docs/examples, and generated frontend bundles when available.

## False-positive control

Classify candidate values using actual provider semantics.

Examples:

- Supabase `sb_publishable_...` and legacy `anon` credentials are intended for public clients and rely on authorization/RLS; do not call them secret solely because they are visible.
- Supabase `sb_secret_...` and legacy `service_role` credentials are privileged and bypass RLS; keep server-side.
- `NEXT_PUBLIC_*` and `VITE_*` variables are client-exposed by design. The question is whether the contained value is permitted to be public.
- OAuth client IDs are usually public identifiers; client secrets are not.

When semantics cannot be established, do not label the value a confirmed secret leak.

## Default/fallback credentials

Review patterns like:

`${VAR:-default-secret}`

and code equivalents. Determine:

1. whether the default is privileged;
2. whether production can start using it;
3. whether startup validation fails closed;
4. whether docs/deploy files encourage real use of the default.

A clearly fake example placeholder is not automatically a vulnerability.

## Git history

If Git metadata exists:

- use an already-installed secret scanner when available;
- otherwise inspect history safely using Git commands and targeted patterns;
- record historical evidence as commit SHA + path + hunk/context;
- do not dump full historical secrets into logs/output.

If a real credential entered history, recommend revoke/rotate first. History rewriting does not invalidate a credential and may have collaboration side effects.

## Client bundles

For web/mobile clients, verify whether privileged values are bundled into artifacts. Understand framework public-env behavior and build-time substitution.

## Redaction

Never reproduce full real credentials. Preserve only enough characters for identification, e.g. `sk_live_abcd...wxyz`.

Do not test credential validity against external services without explicit authorization.

## Preferred remediation

- revoke/rotate exposed credentials first;
- move secrets to provider-supported secret stores/runtime env;
- fail startup for missing/insecure production secrets;
- remove privileged values from client builds;
- clean history when justified after rotation;
- enable secret scanning/push protection/pre-commit checks appropriate to the hosting environment.
