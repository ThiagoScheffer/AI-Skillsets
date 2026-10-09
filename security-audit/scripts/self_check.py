#!/usr/bin/env python3
"""Check skill packaging and Python syntax."""
from __future__ import annotations
import json, py_compile, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['SKILL.md','agents/openai.yaml','references/methodology.md','references/stack-detection.md','references/tenant-isolation.md','references/authorization.md','references/idor-bola.md','references/secrets.md','references/xss.md','references/severity.md','references/evidence-standard.md','references/report-spec.md','assets/audit-results.schema.json','scripts/generate_report.py','scripts/verify_report.py']

def main():
    errs=[]
    for r in REQUIRED:
        if not (ROOT/r).exists(): errs.append('missing '+r)
    sm=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---',sm,re.S)
    if not m: errs.append('SKILL.md missing YAML frontmatter')
    else:
        fm=m.group(1)
        if not re.search(r'^name:\s*security-audit\s*$',fm,re.M): errs.append('SKILL.md name invalid')
        dm=re.search(r'^description:\s*(.+)$',fm,re.M)
        if not dm or len(dm.group(1))>1024: errs.append('SKILL.md description missing or >1024 chars')
    oy=(ROOT/'agents/openai.yaml').read_text(encoding='utf-8')
    if '$security-audit' not in oy: errs.append('openai.yaml default prompt must mention $security-audit')
    try: json.loads((ROOT/'assets/audit-results.schema.json').read_text(encoding='utf-8'))
    except Exception as e: errs.append('schema JSON invalid: '+str(e))
    for p in (ROOT/'scripts').glob('*.py'):
        try: py_compile.compile(str(p),doraise=True)
        except Exception as e: errs.append(f'{p.name} syntax: {e}')
    if errs:
        print('SELF-CHECK FAILED'); [print('ERROR:',e) for e in errs]; return 1
    print('SELF-CHECK OK')
    print(f'root={ROOT}')
    print(f'files={sum(1 for p in ROOT.rglob("*") if p.is_file())}')
    return 0
if __name__=='__main__': sys.exit(main())
