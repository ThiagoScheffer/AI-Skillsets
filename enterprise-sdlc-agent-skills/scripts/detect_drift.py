#!/usr/bin/env python3
from pathlib import Path
import sys, subprocess
from _common import project_root

root = project_root(sys.argv[1] if len(sys.argv) > 1 else '.')
try:
    out = subprocess.check_output(['git','-C',str(root),'status','--porcelain'], text=True)
except Exception:
    print('Git status unavailable; drift detector requires a git repository.')
    raise SystemExit(0)

changed=[line[3:] for line in out.splitlines() if len(line)>=4]
code=[p for p in changed if not p.startswith('.sdlc/') and not p.startswith('docs/')]
sdlc=[p for p in changed if p.startswith('.sdlc/')]

print('Changed code/config files:', len(code))
print('Changed SDLC files:', len(sdlc))
if code and not sdlc:
    print('WARN: implementation changed with no .sdlc updates. Review for design/contract/traceability drift.')
else:
    print('No coarse drift warning.')
