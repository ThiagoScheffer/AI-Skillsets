# Changelog

## 1.0.1 - 2026-08-29

- Fixed pt-BR mojibake in PDF reports (for example `NÃ£o` -> `Não`).
- Enforced explicit UTF-8/UTF-8-SIG JSON I/O in report and audit helper scripts.
- Added conservative repair of common UTF-8 decoded as Latin-1/CP1252 at PDF render time.
- Audit JSON validation now rejects likely mojibake and Unicode replacement glyphs.
- PDF verification now fails when extracted text contains likely encoding corruption.
- Added regression coverage for Portuguese diacritics and mojibake input.

## 1.0.0 - 2026-08-29

- Initial production-ready Codex skill package.
- Five evidence-based audit categories: tenant isolation, trusted authorization, IDOR/BOLA, secrets, and XSS.
- Progressive-disclosure reference modules and stack adapters.
- Candidate discovery and repository metadata helpers.
- Canonical `audit-results.json` contract and validation.
- Reproducible pt-BR ReportLab/Matplotlib PDF generator.
- PDF structural verification and representative-page rasterization.
- User-level and repository-level installer.
- Smoke-tested finding and zero-finding report paths.
