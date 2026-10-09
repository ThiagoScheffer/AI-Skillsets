# Security Reference Register

Last reviewed: 2026-08-29.

Use these references to calibrate reasoning. Prefer current official project/provider documentation when repository dependencies or provider behavior differ from these notes.

## Authorization / tenant isolation / IDOR

- OWASP ASVS 5.0 V8 Authorization: https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md
  - function-level, data-specific, field-level authorization;
  - trusted service-layer enforcement;
  - cross-tenant controls.
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - deny by default;
  - validate permissions on every request.
- OWASP API1:2023 Broken Object Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- OWASP API5:2023 Broken Function Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
- CWE-639 Authorization Bypass Through User-Controlled Key: https://cwe.mitre.org/data/definitions/639.html
- CWE-862 Missing Authorization: https://cwe.mitre.org/data/definitions/862.html

## XSS

- OWASP ASVS 5.0 V1 Encoding and Sanitization: https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
- OWASP Cross Site Scripting Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP DOM based XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
- CWE-79 Cross-site Scripting: https://cwe.mitre.org/data/definitions/79.html

## Secrets

- GitHub: Removing sensitive data from a repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
  - revoke/rotate credentials before considering history rewriting.
- GitHub Push Protection: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- GitHub Secret Scanning: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
- Gitleaks: https://github.com/gitleaks/gitleaks

## Supabase / PostgreSQL

- Supabase Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase API keys: https://supabase.com/docs/guides/getting-started/api-keys
- Supabase secure data guidance: https://supabase.com/docs/guides/database/secure-data
- Supabase Storage access control: https://supabase.com/docs/guides/storage/security/access-control

Important provider detail as of this review: Supabase publishable/legacy anon keys are intended for public clients; secret/legacy service-role credentials are privileged and bypass RLS. Re-check provider docs when auditing because product semantics can change.

## Configuration

- OWASP ASVS 5.0 V13 Configuration: https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md

## Codex skill packaging

- Codex skills documentation: https://developers.openai.com/codex/skills
- OpenAI skills catalog / skill creator: https://github.com/openai/skills
- Agent Skills specification: https://agentskills.io/specification
