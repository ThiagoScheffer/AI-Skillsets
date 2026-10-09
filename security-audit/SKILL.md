---
name: security-audit
description: Perform evidence-based repository security audits for tenant or owner isolation, server-side authorization, IDOR/BOLA, exposed or hardcoded secrets, and XSS. Detect the actual stack and security model first, systematically inventory relevant routes and privilege gates, report verified findings only with exact file/line evidence, record verified strengths and coverage, recommend stack-native fixes and regression tests, and generate a professional pt-BR PDF with ready-to-use GitHub issues. Use when asked to audit, review, assess, or harden a repository for access control, RLS/tenant isolation, authorization, IDOR, credentials/secrets, XSS, or these five security categories.
---

# Security Audit

Perform a defensive, evidence-based source-code security audit. The objective is to assess five risk categories, not to manufacture a fixed number of vulnerabilities. A category may contain zero, one, or multiple verified findings.

## Mandatory workflow

1. Read `references/methodology.md` and `references/stack-detection.md`.
2. Detect the repository architecture, authentication, authorization, tenant-isolation model, frontend, data layer, and deployment/configuration surface from code evidence.
3. Load only the stack adapters that match the detected project from `references/adapters/`.
4. Build the coverage inventories required by `references/methodology.md` before classifying findings.
5. Audit all five categories. Before finalizing each category, read its reference:
   - tenant/owner isolation -> `references/tenant-isolation.md`
   - privileged/function authorization -> `references/authorization.md`
   - IDOR/BOLA -> `references/idor-bola.md`
   - exposed/hardcoded secrets -> `references/secrets.md`
   - XSS/unsafe rendering -> `references/xss.md`
6. Validate every proposed finding against `references/evidence-standard.md`.
7. Assign severity using `references/severity.md`.
8. Write the canonical result to `docs/security-audit/audit-results.json` as UTF-8 (no legacy ANSI/Latin-1 encoding) and validate it with `scripts/validate_audit_results.py`. Fix any encoding/mojibake validation error before report generation.
9. Generate the pt-BR PDF according to `references/report-spec.md`. Copy the reusable report generator to `docs/security-audit/generate_report.py` so the report remains reproducible without this installed skill.
10. Verify the PDF with `scripts/verify_report.py` and visually inspect rendered representative pages when a renderer is available.
11. Return the stack/security model, coverage, verified findings, verified strengths, limitations, and all generated paths.

## Non-negotiable evidence rules

- Report verified vulnerabilities only. Do not speculate.
- Do not claim complete coverage unless the relevant attack surface was systematically enumerated.
- Treat authentication, function-level authorization, object-level authorization, field-level authorization, and tenant isolation as distinct controls.
- A frontend gate is not a security control and is not by itself a vulnerability. A finding exists only when the trusted backend lacks the required authorization.
- An endpoint accepting an ID is not automatically IDOR/BOLA. Prove the authorization failure.
- A client-visible key is not automatically a leaked secret. Classify the key using provider/framework semantics and actual privileges.
- Generic input validation is not sufficient proof of XSS prevention. Trace an untrusted source to a rendering/execution sink and evaluate the control in that output context.
- Do not duplicate one root cause across categories. Report it once and cross-reference related categories.
- Record meaningful secure implementations as strengths to demonstrate reviewed coverage.
- Use exact current line numbers from the final repository state. For historical-only Git evidence, use `commit <SHA> | <path> | <hunk/context>` instead of inventing a current line.
- Never print complete real secrets in chat, JSON, PDF, Markdown issues, logs, or test output. Redact them.

## Safe execution

This is primarily a source/configuration audit. Existing local tests, linters, static analyzers, repository scripts, and already-installed secret scanners may be used when safe.

Do not attack production systems, perform destructive requests, alter production data, authenticate to third-party services with discovered credentials, exfiltrate secrets, or install software globally. If a local service may point to production, do not exercise it until its target is proven safe.

The bundled scanner is candidate discovery only. Pattern matches are never proof of a vulnerability.

## Required outputs

Create inside the audited repository:

- `docs/security-audit/audit-results.json`
- `docs/security-audit/generate_report.py`
- `docs/security-audit/relatorio-auditoria-seguranca.pdf`

Optional supporting artifacts such as chart images or verification renders may be generated under `docs/security-audit/`, but remove disposable intermediates before delivery unless they are useful for reproducibility.

## Final response format

Return:

1. detected stack and security model;
2. coverage summary;
3. verified findings, file by file and line by line;
4. verified strengths;
5. audit limitations/manual follow-up;
6. paths of every generated artifact.

For each chat finding use:

`Severity - file:line - description - exploitability condition`

Never claim a vulnerability, route coverage, credential validity, dynamic verification, or successful PDF verification unless it was actually established.
