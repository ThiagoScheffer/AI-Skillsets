# Security Audit Skill for Codex

A reusable Codex skill for evidence-based repository security audits across five high-risk areas:

1. tenant/owner isolation;
2. server-side function/role authorization;
3. IDOR / BOLA;
4. hardcoded or exposed secrets;
5. XSS / unsafe rendering.

It discovers the actual stack first, inventories the attack surface, distinguishes verified findings from candidates, records secure controls as strengths, creates structured audit data, and renders a professional Brazilian Portuguese PDF with ready-to-paste GitHub issues.

## Install

### User-level: available across repositories

From the extracted skill directory:

```bash
python scripts/install_skill.py --user
```

Equivalent manual install:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R security-audit "$HOME/.agents/skills/security-audit"
```

### Repository-level: version with one repository

```bash
python /path/to/security-audit/scripts/install_skill.py --repo /path/to/repository
```

This installs to:

```text
<repo>/.agents/skills/security-audit/
```

Codex currently discovers skills from `.agents/skills` locations and from `$HOME/.agents/skills`. If a newly installed or changed skill is not visible, restart Codex.

## Invoke

Explicit invocation:

```text
$security-audit Audit this repository and generate the complete security report.
```

The skill also permits implicit invocation for clearly matching security-audit requests.

## Report dependencies

The discovery/validation helpers use the Python standard library. PDF generation uses ReportLab and Matplotlib; PDF verification uses pypdf and optionally `pdftoppm`.

Do not install these globally. In the audited repository, if needed:

```bash
python -m venv docs/security-audit/.venv
. docs/security-audit/.venv/bin/activate
python -m pip install -r /path/to/security-audit/requirements-report.txt
```

On Windows PowerShell, activate the venv with:

```powershell
.\docs\security-audit\.venv\Scripts\Activate.ps1
```

## Architecture

```text
security-audit/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── methodology.md
│   ├── stack-detection.md
│   ├── tenant-isolation.md
│   ├── authorization.md
│   ├── idor-bola.md
│   ├── secrets.md
│   ├── xss.md
│   ├── severity.md
│   ├── evidence-standard.md
│   ├── report-spec.md
│   ├── sources.md
│   └── adapters/
├── scripts/
│   ├── collect_repo_metadata.py
│   ├── scan_security_patterns.py
│   ├── init_audit_output.py
│   ├── validate_audit_results.py
│   ├── generate_report.py
│   ├── verify_report.py
│   ├── install_skill.py
│   └── self_check.py
├── assets/
│   ├── audit-results.schema.json
│   └── report-config.json
├── examples/
│   ├── audit-results.example.json
│   └── usage-prompts.md
└── requirements-report.txt
```

## Design principles

- **Evidence first:** pattern scanning finds candidates; Codex proves or rejects exploitability.
- **No forced finding count:** zero findings is a valid result.
- **Coverage is explicit:** route and privilege inventories are part of the audit evidence.
- **Provider-aware secrets:** public/publishable keys are distinguished from privileged credentials.
- **Source-to-sink XSS analysis:** dangerous APIs are not findings without an attacker-controlled path and ineffective defenses.
- **Deterministic reporting:** `audit-results.json` is the canonical result and the PDF is rendered from it.
- **UTF-8-safe reporting:** canonical JSON is written/read explicitly as UTF-8; the renderer repairs common legacy UTF-8/Latin-1 mojibake defensively and the verifier rejects corrupted PDF text.
- **Safe by default:** no production attacks or credential validation against third-party services.

## Self-check

```bash
python scripts/self_check.py
```

A complete audit remains a reasoning task; these scripts intentionally do not auto-label pattern matches as vulnerabilities.
