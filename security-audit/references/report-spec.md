# PDF Report Specification

## Deliverables in the audited repository

- `docs/security-audit/audit-results.json` - canonical structured result
- `docs/security-audit/generate_report.py` - copied reusable generator
- `docs/security-audit/relatorio-auditoria-seguranca.pdf` - final report

Copy this skill's `scripts/generate_report.py` into the audit directory unless a project-local generator already exists and is better suited. The copied generator must run independently of the installed skill when its Python dependencies are available.

## Language and layout

- Brazilian Portuguese (`pt-BR`)
- A4
- approximately 2 cm margins
- consistent header/footer with report name and page number
- readable typography, code, tables and legends
- no reliance on color alone
- UTF-8 text end-to-end; `audit-results.json` must be saved as UTF-8 (UTF-8 BOM is accepted on input)
- no mojibake such as `NÃ£o`, `organizaÃ§Ãµes`, `â€“`, or Unicode replacement glyphs (`�`)

Severity palette:

- Critical: `#B91C1C`
- High: `#EA580C`
- Medium: `#D97706`
- Low: `#2563EB`
- Informational: neutral gray
- Strength: `#059669`

## Required sections

### 1. Cover

Title:

`Relatório de Auditoria de Segurança - <nome do projeto>`

Include date, repository/project, scope, key exclusions/limitations, detected stack, and a methodological note explaining how the five categories map to the detected architecture.

### 2. Executive summary

Include:

- total verified findings;
- counts by severity;
- counts by category;
- donut chart by severity when findings exist;
- bar chart by category;
- concise central risk themes.

If there are zero findings, do not render a misleading empty donut. Clearly state zero verified findings within the reviewed scope.

### 3. Stack, scope and coverage

Summarize architecture, authn/authz/isolation, route coverage, privilege-gate coverage, Git-history availability, deployment/config review, and limitations.

### 4. Strengths and weaknesses

`Pontos fortes`: verified secure controls with evidence.

`Pontos fracos`: central verified risk patterns. If no findings exist, say so and avoid inventing weaknesses.

### 5. Detailed findings

Group by category. Use a table with:

`Severidade | Arquivo:linha | Descrição`

Use a colored severity cell/chip. Follow table rows with sufficient detail for exploitability, impact, conditions, remediation, tests, and mappings.

### 6. Prioritized recommendations

`P1`, `P2`, `P3`... ordered by risk and remediation dependencies.

### 7. Audit limitations / manual follow-up

Only meaningful unresolved coverage limitations. Do not mix speculative items into findings.

### 8. ISSUES PARA O GITHUB

Final major section. For every actionable finding or sensible root-cause group, provide a complete Markdown issue between:

`--- ISSUE n ---`

and

`--- FIM ISSUE n ---`

Each issue contains:

- title `[Segurança] <descrição curta>`;
- suggested labels `security` + severity;
- problem/exploitability;
- redacted exact evidence;
- impact;
- stack-specific fix;
- verifiable acceptance checklist including regression testing where practical.

Group related trivial findings when the same root cause/fix applies.

## Generation and verification

Do not install globally. Use an isolated venv if report packages are missing.

After generation:

1. validate `audit-results.json` (validation rejects likely text-encoding mojibake);
2. run `scripts/verify_report.py` against the PDF;
3. render the first, a representative middle, and the final page when `pdftoppm` or equivalent exists;
4. visually inspect renders for clipping, overlap, broken glyphs, unreadable tables/charts, and bad page breaks;
5. correct defects and regenerate before delivery.

Do not claim visual verification if only structural checks ran.
