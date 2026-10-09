#!/usr/bin/env python3
from pathlib import Path
import sys
from _common import project_root

root=project_root(sys.argv[1] if len(sys.argv)>1 else '.')
s=root/'.sdlc'
artifacts=[
 ('Discovery',s/'product'/'discovery.md'),
 ('PRD',s/'product'/'PRD.md'),
 ('Requirements',s/'requirements'/'requirements.yaml'),
 ('System design',s/'design'/'SYSTEM-DESIGN.md'),
 ('Threat model',s/'security'/'threat-model.md'),
 ('Implementation plan',s/'planning'/'implementation-plan.md'),
 ('Tasks',s/'planning'/'tasks.yaml'),
 ('Test plan',s/'verification'/'test-plan.md'),
 ('Release plan',s/'release'/'release-plan.md'),
 ('Runbook',s/'operations'/'runbook.md')]
print('SDLC STATUS')
for name,p in artifacts:
    print(f'{name:22} {"PRESENT" if p.exists() else "MISSING"}')
