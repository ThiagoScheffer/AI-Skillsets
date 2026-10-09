#!/usr/bin/env python3
import sys, re
from _common import project_root

root = project_root(sys.argv[1] if len(sys.argv) > 1 else '.')
sdlc = root/'.sdlc'
if not sdlc.exists():
    print('ERROR: .sdlc missing'); raise SystemExit(1)

texts = {}
for p in sdlc.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.yaml','.yml','.json','.txt'}:
        try: texts[p] = p.read_text(encoding='utf-8')
        except Exception: pass

requirements=set(); task_refs=set(); test_refs=set()
for p, t in texts.items():
    requirements.update(re.findall(r'\b(?:FR|NFR)-\d{3,}\b', t) if 'requirements' in str(p) else [])
    if '/planning/' in str(p).replace('\\','/'):
        task_refs.update(re.findall(r'\b(?:FR|NFR)-\d{3,}\b', t))
    if '/verification/' in str(p).replace('\\','/'):
        test_refs.update(re.findall(r'\b(?:FR|NFR)-\d{3,}\b', t))

missing_task = sorted(requirements-task_refs)
missing_test = sorted(requirements-test_refs)
print(f'Requirements found: {len(requirements)}')
print(f'Not referenced in planning: {missing_task or "none"}')
print(f'Not referenced in verification: {missing_test or "none"}')
if missing_task or missing_test:
    print('RESULT: INCOMPLETE TRACEABILITY')
    raise SystemExit(2)
print('RESULT: TRACEABILITY PASS')
