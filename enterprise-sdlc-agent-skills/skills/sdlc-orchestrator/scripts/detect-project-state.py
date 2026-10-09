#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
sdlc = root / '.sdlc'
checks = [
    ('project', sdlc/'project.yaml'),
    ('prd', sdlc/'product'/'PRD.md'),
    ('requirements', sdlc/'requirements'/'requirements.yaml'),
    ('system_design', sdlc/'design'/'SYSTEM-DESIGN.md'),
    ('threat_model', sdlc/'security'/'threat-model.md'),
    ('tasks', sdlc/'planning'/'tasks.yaml'),
    ('test_plan', sdlc/'verification'/'test-plan.md'),
    ('release_plan', sdlc/'release'/'release-plan.md'),
    ('runbook', sdlc/'operations'/'runbook.md'),
]
for name, path in checks:
    print(f'{name}: {"present" if path.exists() else "missing"}')
