# Usage examples

## Full audit

```text
$security-audit Audit this repository across all five categories. Generate the structured results and pt-BR PDF, verify the PDF, and return verified findings plus strengths and limitations.
```

## Authorization-focused

```text
$security-audit Focus on tenant isolation, function authorization, and IDOR/BOLA. Still detect the full stack first and make route coverage explicit. Do not generate speculative findings.
```

## Re-run after fixes

```text
$security-audit Re-audit the previous security findings against the current repository state. Confirm which issues are fixed with exact evidence, check for regressions in equivalent routes, update audit-results.json, and regenerate the PDF.
```

## Secrets only

```text
$security-audit Audit current source, deploy/CI configuration, frontend bundles if present, and available Git history for real privileged secrets. Distinguish public/publishable keys from secrets and redact all values in output.
```
