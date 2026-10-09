#!/usr/bin/env python3
from pathlib import Path
import sys, re
from _common import project_root

root = project_root(sys.argv[1] if len(sys.argv) > 1 else '.')
sdlc = root/'.sdlc'
errors=[]; warnings=[]

if not sdlc.exists():
    errors.append('.sdlc directory is missing')
else:
    required = ['project.yaml','status.yaml','gate-ledger.yaml']
    for name in required:
        if not (sdlc/name).exists(): errors.append(f'missing .sdlc/{name}')
    gate = sdlc/'gate-ledger.yaml'
    if gate.exists():
        txt = gate.read_text(encoding='utf-8')
        if re.search(r'approved_by:\s*(ai|agent|codex|claude)\b', txt, re.I):
            errors.append('gate ledger records an AI agent as approval authority')
    prd = sdlc/'product'/'PRD.md'
    req = sdlc/'requirements'/'requirements.yaml'
    design = sdlc/'design'/'SYSTEM-DESIGN.md'
    tasks = sdlc/'planning'/'tasks.yaml'
    if design.exists() and not req.exists():
        warnings.append('system design exists but requirements registry is missing')
    if tasks.exists() and not design.exists():
        warnings.append('implementation tasks exist but system design is missing; acceptable only for low-risk work')

print('SDLC validation')
for w in warnings: print('WARN:', w)
for e in errors: print('ERROR:', e)
if errors:
    print('RESULT: FAIL')
    raise SystemExit(1)
print('RESULT: PASS')
